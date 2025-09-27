from typing import Any, Iterable, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.adapters.db.models import VehicleORM
from src.domain.models import Vehicle, VehicleStatus

class SqlAlchemyVehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def _to_payload(self, data: Any) -> dict:
        # Aceita dict ou objeto de domínio Vehicle
        if isinstance(data, dict):
            payload = dict(data)
        elif isinstance(data, Vehicle):
            payload = {
                "brand": data.brand,
                "model": data.model,
                "year": data.year,
                "color": data.color,
                "price": data.price,
                "status": data.status,
            }
        else:
            # fallback defensivo
            payload = {
                "brand": getattr(data, "brand", None),
                "model": getattr(data, "model", None),
                "year": getattr(data, "year", None),
                "color": getattr(data, "color", None),
                "price": getattr(data, "price", None),
                "status": getattr(data, "status", None),
            }

        # Normaliza status
        st = payload.get("status")
        if st is None:
            payload["status"] = VehicleStatus.AVAILABLE
        elif not isinstance(st, VehicleStatus):
            payload["status"] = VehicleStatus(getattr(st, "value", st).lower())

        # Remove None
        return {k: v for k, v in payload.items() if v is not None}

    # --------- Métodos públicos ---------
    def add(self, data: Any) -> VehicleORM:
        payload = self._to_payload(data)
        row = VehicleORM(**payload)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def list_by_status_ordered(self, status: VehicleStatus) -> list[VehicleORM]:
        return (
            self.db.query(VehicleORM)
            .filter(VehicleORM.status == status)
            .order_by(
                VehicleORM.price.asc(),
                VehicleORM.brand.asc(),
                VehicleORM.model.asc(),
            )
            .all()
        )

    # Exemplos de assinaturas para futuro uso
    def get(self, vehicle_id: UUID) -> Optional[VehicleORM]:
        return self.db.query(VehicleORM).get(str(vehicle_id))

    def update(self, row: VehicleORM) -> VehicleORM:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row
