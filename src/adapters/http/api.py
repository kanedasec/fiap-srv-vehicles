# src/adapters/http/api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from src.adapters.db.base import SessionLocal, engine
from src.adapters.db.repository import SqlAlchemyVehicleRepository
from src.adapters.db.models import VehicleStatus
from src.application.usecases.create_vehicle import create_vehicle

router = APIRouter()

def get_repo():
    db = SessionLocal()
    try:
        yield SqlAlchemyVehicleRepository(db)
    finally:
        db.close()

class VehicleIn(BaseModel):
    brand: str
    model: str
    year: int
    color: str
    price: float

class ReserveIn(BaseModel):
    reserved_by: str

class HealthResponse(BaseModel):
    status: str

@router.post("/vehicles")
def add_vehicle(data: VehicleIn, repo: SqlAlchemyVehicleRepository = Depends(get_repo)):
    row = create_vehicle(repo, data.model_dump())
    return jsonable_encoder(row)

@router.get("/vehicles")
def list_vehicles(
    status: str = "available",
    repo: SqlAlchemyVehicleRepository = Depends(get_repo),
):
    try:
        status_enum = VehicleStatus(status.lower())
    except ValueError:
        raise HTTPException(status_code=422, detail="status deve ser: available | reserved | sold")
    rows = repo.list_by_status_ordered(status_enum)
    return jsonable_encoder(rows)

@router.post("/vehicles/{vehicle_id}/reserve")
def reserve_vehicle(
    vehicle_id: str,
    payload: ReserveIn,
    repo: SqlAlchemyVehicleRepository = Depends(get_repo),
):
    updated = repo.mark_reserved(vehicle_id, payload.reserved_by)
    if not updated:
        raise HTTPException(status_code=404, detail="Veículo não encontrado ou não disponível para reserva")
    return jsonable_encoder(updated)

@router.post("/vehicles/{vehicle_id}/unreserve")
def unreserve_vehicle(
    vehicle_id: str,
    repo: SqlAlchemyVehicleRepository = Depends(get_repo),
):
    updated = repo.unreserve(vehicle_id)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Veículo não encontrado ou não está reservado",
        )
    return jsonable_encoder(updated)

@router.post("/vehicles/{vehicle_id}/sell")
def sell_vehicle(
    vehicle_id: str,
    repo: SqlAlchemyVehicleRepository = Depends(get_repo),
):
    updated = repo.mark_sold(vehicle_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return jsonable_encoder(updated)

@router.get("/healthz", response_model=HealthResponse, tags=["health"])
def healthz():
    return {"status": "ok"}

@router.get("/readyz", response_model=HealthResponse, tags=["health"])
def readyz():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        return {"status": "degraded"}
