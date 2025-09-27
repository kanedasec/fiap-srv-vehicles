from fastapi import APIRouter, Depends
from sqlalchemy import text
from src.adapters.db.base import SessionLocal, engine
from src.adapters.db.repository import SqlAlchemyVehicleRepository
from src.application.usecases.create_vehicle import create_vehicle
from src.domain.models import VehicleStatus
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

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
    status_enum = VehicleStatus(status.lower())
    rows = repo.list_by_status_ordered(status_enum)
    return jsonable_encoder(rows)

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
