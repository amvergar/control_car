# /src/core/services.py
from dataclasses import dataclass
from datetime import date
from typing import Dict, Tuple
from .contracts import Repository
from .entities import FuelLoad, OilChange, MaintenanceRecord
from .validators import ValidationError, require_positive, require_non_negative


@dataclass
class MonthlySummary:
    month: int
    year: int
    fuel_cost_usd: float
    maintenance_cost_usd: float
    total_cost_usd: float


class ControlCarService:
    """Servicio CORE (SRP): orquesta reglas de negocio sin depender de I/O ni BD real."""
    def __init__(self, repo: Repository):
        self.repo = repo

    # --- Operaciones de registro ---
    def register_fuel_load(self, fuel: FuelLoad) -> None:
        self._validate_odometer_sequence(fuel.vehicle_id, fuel.odometer_km)
        self.repo.add_fuel_load(fuel)

    def register_oil_change(self, oc: OilChange) -> None:
        self._validate_odometer_sequence(oc.vehicle_id, oc.odometer_km)
        self.repo.add_oil_change(oc)

    def register_maintenance(self, m: MaintenanceRecord) -> None:
        self.repo.add_maintenance(m)

    # --- Reglas de negocio principales ---
    def calculate_efficiency_km_per_l(self, vehicle_id: str) -> float:
        """Calcula rendimiento (km/l) usando últimas dos cargas con odómetro."""
        loads = sorted(self.repo.list_fuel_loads(vehicle_id), key=lambda x: x.date_)
        if len(loads) < 2:
            raise ValidationError("Se requieren al menos dos cargas de gasolina para calcular rendimiento.")
        last, prev = loads[-1], loads[-2]
        distance = last.odometer_km - prev.odometer_km
        require_positive("distancia recorrida (km)", distance)
        liters_used = last.liters  # Asume tanque repostado; ajustar si se desea método promedio.
        require_positive("litros consumidos", liters_used)
        return round(distance / liters_used, 2)

    def next_oil_change_at_km(self, vehicle_id: str) -> float:
        """Devuelve el odómetro objetivo para el próximo cambio de aceite."""
        changes = self.repo.list_oil_changes(vehicle_id)
        if not changes:
            raise ValidationError("No hay registros de cambio de aceite.")
        last = max(changes, key=lambda x: x.date_)
        return round(last.odometer_km + last.interval_km, 0)

    def generate_alerts(self, vehicle_id: str, current_odometer_km: float) -> Dict[str, str]:
        """Genera alertas: próximo cambio de aceite y variación de rendimiento."""
        require_non_negative("odómetro actual (km)", current_odometer_km)
        alerts: Dict[str, str] = {}

        # Alerta de aceite
        try:
            due_km = self.next_oil_change_at_km(vehicle_id)
            if current_odometer_km >= due_km:
                alerts["oil_change"] = f"Cambio de aceite vencido. Realizar inmediatamente (≥ {due_km} km)."
            elif (due_km - current_odometer_km) <= 200:
                alerts["oil_change"] = f"Cambio de aceite próximamente: faltan ~{int(due_km - current_odometer_km)} km."
        except ValidationError:
            alerts["oil_change"] = "Sin registros de cambio de aceite."

        # Alerta de rendimiento (si hay suficientes datos)
        try:
            efficiency = self.calculate_efficiency_km_per_l(vehicle_id)
            if efficiency < 8.0:
                alerts["efficiency"] = f"Rendimiento bajo: {efficiency} km/l. Revisar presión de llantas o estilo de conducción."
        except ValidationError:
            alerts["efficiency"] = "Insuficientes datos para calcular rendimiento."

        return alerts

    def monthly_summary(self, vehicle_id: str, month: int, year: int) -> MonthlySummary:
        """Resumen mensual de costos de combustible y mantenimiento."""
        require_positive("mes", month)
        require_positive("año", year)
        fuel_cost = sum(f.cost_usd for f in self.repo.list_fuel_loads(vehicle_id)
                        if f.date_.month == month and f.date_.year == year)
        mnt_cost = sum(m.cost_usd for m in self.repo.list_maintenances(vehicle_id)
                       if m.date_.month == month and m.date_.year == year)
        total = round(fuel_cost + mnt_cost, 2)
        return MonthlySummary(month=month, year=year,
                              fuel_cost_usd=round(fuel_cost, 2),
                              maintenance_cost_usd=round(mnt_cost, 2),
                              total_cost_usd=total)

    # --- Reglas de consistencia ---
    def _validate_odometer_sequence(self, vehicle_id: str, new_odo_km: float) -> None:
        """Validación: el odómetro no debe retroceder respecto al último registro."""
        require_non_negative("odómetro (km)", new_odo_km)
        last_values = [
            *(r.odometer_km for r in self.repo.list_fuel_loads(vehicle_id)),
            *(r.odometer_km for r in self.repo.list_oil_changes(vehicle_id))
        ]
        if last_values and new_odo_km < max(last_values):
            raise ValidationError("El odómetro no puede ser menor al último registro.")
