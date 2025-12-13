# /tests/test_core.py
from datetime import date
from src.core.contracts import InMemoryRepository
from src.core.entities import Vehicle, FuelLoad, OilChange, MaintenanceRecord
from src.core.services import ControlCarService

def test_efficiency_and_alerts():
    repo = InMemoryRepository()
    svc = ControlCarService(repo)

    v = Vehicle(id="v1", owner_id="u1", plate="ABC-1234", make="Chevrolet", model="Onix", year=2021)
    repo.add_vehicle(v)

    svc.register_fuel_load(FuelLoad(id="f1", vehicle_id="v1", date_=date(2025, 1, 10), liters=10.0, cost_usd=25.0, odometer_km=10000, fuel_type="Extra"))
    svc.register_fuel_load(FuelLoad(id="f2", vehicle_id="v1", date_=date(2025, 1, 20), liters=12.0, cost_usd=28.0, odometer_km=10100, fuel_type="Extra"))

    efficiency = svc.calculate_efficiency_km_per_l("v1")
    assert efficiency == round((10100 - 10000) / 12.0, 2)

    svc.register_oil_change(OilChange(id="o1", vehicle_id="v1", date_=date(2025, 1, 5), oil_type="5W-30", odometer_km=9800, interval_km=5000))
    alerts = svc.generate_alerts("v1", current_odometer_km=10100)
    assert "oil_change" in alerts
