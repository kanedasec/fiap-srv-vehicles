from src.domain.models import Vehicle

def create_vehicle(repo, data: dict):
    vehicle = Vehicle.create(
        brand=data["brand"],
        model=data["model"],
        year=data["year"],
        color=data["color"],
        price=data["price"],
    )
    return repo.add(vehicle)
