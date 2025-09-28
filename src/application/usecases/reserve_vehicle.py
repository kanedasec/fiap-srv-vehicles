from typing import Optional
from src.adapters.db.repository import SqlAlchemyVehicleRepository

def reserve_vehicle(repo: SqlAlchemyVehicleRepository, vehicle_id: str, reserved_by: Optional[str]) -> dict:
    return repo.mark_reserved(vehicle_id, reserved_by)
