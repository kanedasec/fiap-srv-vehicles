from src.adapters.db.repository import SqlAlchemyVehicleRepository

def sell_vehicle(repo: SqlAlchemyVehicleRepository, vehicle_id: str) -> dict:
    return repo.mark_sold(vehicle_id)
