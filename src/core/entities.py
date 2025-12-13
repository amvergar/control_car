# /src/core/entities.py
from dataclasses import dataclass
from datetime import date
from typing import Optional
from .validators import require_not_empty, require_positive, require_non_negative


@dataclass(frozen=True)
class Vehicle:
    """Entidad Vehículo."""
    id: str           # UUID o cadena única
    owner_id: str     # Usuario propietario
    plate: str        # Placa
    make: str         # Marca
    model: str        # Modelo
    year: int         # Año

    def __post_init__(self):
        require_not_empty("id", self.id)
        require_not_empty("owner_id", self.owner_id)
        require_not_empty("plate", self.plate)
        require_not_empty("make", self.make)
        require_not_empty("model", self.model)
        if self.year < 1900 or self.year > date.today().year + 1:
            raise ValueError(f"Año inválido: {self.year}")


@dataclass(frozen=True)
class FuelLoad:
    """Entidad Carga de Gasolina."""
    id: str
    vehicle_id: str
    date_: date
    liters: float
    cost_usd: float
    odometer_km: float
    fuel_type: str  # Extra, Súper, Diésel

    def __post_init__(self):
        require_not_empty("id", self.id)
        require_not_empty("vehicle_id", self.vehicle_id)
        require_positive("litros", self.liters)
        require_positive("costo (USD)", self.cost_usd)
        require_non_negative("odómetro (km)", self.odometer_km)
        require_not_empty("tipo de combustible", self.fuel_type)


@dataclass(frozen=True)
class OilChange:
    """Entidad Cambio de Aceite."""
    id: str
    vehicle_id: str
    date_: date
    oil_type: str
    odometer_km: float
    interval_km: float  # Intervalo recomendado para próximo cambio

    def __post_init__(self):
        require_not_empty("id", self.id)
        require_not_empty("vehicle_id", self.vehicle_id)
        require_not_empty("tipo de aceite", self.oil_type)
        require_non_negative("odómetro (km)", self.odometer_km)
        require_positive("intervalo (km)", self.interval_km)


@dataclass(frozen=True)
class MaintenanceRecord:
    """Entidad Mantenimiento (preventivo/correctivo)."""
    id: str
    vehicle_id: str
    date_: date
    maintenance_type: str  # Preventivo/Correctivo o descripción específica
    cost_usd: float
    note: Optional[str] = None

    def __post_init__(self):
        require_not_empty("id", self.id)
        require_not_empty("vehicle_id", self.vehicle_id)
        require_not_empty("tipo de mantenimiento", self.maintenance_type)
        require_non_negative("costo (USD)", self.cost_usd)
