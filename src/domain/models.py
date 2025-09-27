from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

class VehicleStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"

@dataclass
class Vehicle:
    id: UUID
    brand: str
    model: str
    year: int
    color: str
    price: float
    status: VehicleStatus = VehicleStatus.AVAILABLE
    reserved_by: str | None = None
    reserved_at: datetime | None = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    @staticmethod
    def create(brand, model, year, color, price):
        return Vehicle(
            id=uuid4(),
            brand=brand,
            model=model,
            year=year,
            color=color,
            price=price
        )
