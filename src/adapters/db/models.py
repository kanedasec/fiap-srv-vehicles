from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Enum as SAEnum
from src.adapters.db.base import Base
from src.domain.models import VehicleStatus  # <-- importa do domínio
import uuid

class VehicleORM(Base):
    __tablename__ = "vehicles"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[VehicleStatus] = mapped_column(
        SAEnum(VehicleStatus, name="vehicle_status"),
        default=VehicleStatus.AVAILABLE,
        nullable=False,
    )
