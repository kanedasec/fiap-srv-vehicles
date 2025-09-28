# src/adapters/db/repository.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from src.adapters.db.models import VehicleORM, VehicleStatus
from src.domain.models import Vehicle  # entidade de domínio


def _row_to_dict(row: VehicleORM) -> dict:
    return {
        "id": row.id,
        "brand": row.brand,
        "model": row.model,
        "year": row.year,
        "color": row.color,
        "price": row.price,
        "status": row.status.value if isinstance(row.status, VehicleStatus) else row.status,
        "reserved_by": row.reserved_by,
        "reserved_at": row.reserved_at.isoformat() if row.reserved_at else None,
    }


class SqlAlchemyVehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    # CREATE a partir da entidade de domínio
    def add(self, vehicle: Vehicle) -> dict:
        row = VehicleORM(
            id=str(vehicle.id),
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year,
            color=vehicle.color,
            price=vehicle.price,
            status=VehicleStatus(vehicle.status.value),  # mapeia Enum domínio -> Enum DB
            reserved_by=vehicle.reserved_by,
            reserved_at=vehicle.reserved_at,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return _row_to_dict(row)

    # READ helpers
    def get_by_id(self, vehicle_id: str) -> Optional[VehicleORM]:
        stmt = select(VehicleORM).where(VehicleORM.id == vehicle_id)
        return self.db.scalar(stmt)

    def list_by_status_ordered(self, status: VehicleStatus) -> List[dict]:
        stmt = (
            select(VehicleORM)
            .where(VehicleORM.status == status)
            .order_by(VehicleORM.brand, VehicleORM.model, VehicleORM.year)
        )
        rows = self.db.scalars(stmt).all()
        return [_row_to_dict(r) for r in rows]

    # UPDATEs de estado
    def mark_reserved(self, vehicle_id: str, reserved_by: str) -> Optional[dict]:
        row = self.get_by_id(vehicle_id)
        if not row:
            return None
        if row.status != VehicleStatus.AVAILABLE:
            # já reservado ou vendido
            return None
        row.status = VehicleStatus.RESERVED
        row.reserved_by = reserved_by
        row.reserved_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(row)
        return _row_to_dict(row)

    def mark_sold(self, vehicle_id: str) -> Optional[dict]:
        row = self.get_by_id(vehicle_id)
        if not row:
            return None
        if row.status == VehicleStatus.SOLD:
            return _row_to_dict(row)  # idempotente
        row.status = VehicleStatus.SOLD
        # opcional: manter rastros de reserva; se quiser limpar, descomente:
        # row.reserved_by = None
        # row.reserved_at = None
        self.db.commit()
        self.db.refresh(row)
        return _row_to_dict(row)
