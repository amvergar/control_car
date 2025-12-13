# /src/core/contracts.py
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from .entities import Vehicle, FuelLoad, OilChange, MaintenanceRecord


class Repository(ABC):
    """Interfaz de repositorio (DIP). Permite cambiar la persistencia sin tocar la lógica."""
    @abstractmethod
    def add_vehicle(self, vehicle: Vehicle) -> None: ...
    @abstractmethod
    def get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]: ...
    @abstractmethod
    def list_fuel_loads(self, vehicle_id: str) -> List[FuelLoad]: ...
    @abstractmethod
    def add_fuel_load(self, fuel: FuelLoad) -> None: ...
    @abstractmethod
    def list_oil_changes(self, vehicle_id: str) -> List[OilChange]: ...
    @abstractmethod
    def add_oil_change(self, oc: OilChange) -> None: ...
    @abstractmethod
    def list_maintenances(self, vehicle_id: str) -> List[MaintenanceRecord]: ...
    @abstractmethod
    def add_maintenance(self, m: MaintenanceRecord) -> None: ...


class InMemoryRepository(Repository):
    """Implementación en memoria para pruebas (sin BD real)."""
    def __init__(self):
        self._vehicles = {}
        self._fuel = {}
        self._oil = {}
        self._mnt = {}

    def add_vehicle(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.id] = vehicle

    def get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]:
        return self._vehicles.get(vehicle_id)

    def list_fuel_loads(self, vehicle_id: str) -> List[FuelLoad]:
        return self._fuel.get(vehicle_id, [])

    def add_fuel_load(self, fuel: FuelLoad) -> None:
        self._fuel.setdefault(fuel.vehicle_id, []).append(fuel)

    def list_oil_changes(self, vehicle_id: str) -> List[OilChange]:
        return self._oil.get(vehicle_id, [])

    def add_oil_change(self, oc: OilChange) -> None:
        self._oil.setdefault(oc.vehicle_id, []).append(oc)

    def list_maintenances(self, vehicle_id: str) -> List[MaintenanceRecord]:
        return self._mnt.get(vehicle_id, [])

    def add_maintenance(self, m: MaintenanceRecord) -> None:
        self._mnt.setdefault(m.vehicle_id, []).append(m)
