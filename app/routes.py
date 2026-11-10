from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request

from app.database import PatientDB
from app.models import Patient

router = APIRouter()


def get_db(request: Request) -> PatientDB:
    return request.app.state.db


def get_city(patient: dict[str, Any]) -> str:
    """Read both the current nested address and legacy flat city fields."""
    address = patient.get("address")
    if isinstance(address, dict):
        return str(address.get("city", ""))
    return str(patient.get("city", ""))


@router.get("/", tags=["General"])
async def root() -> dict[str, str]:
    return {"message": "Patient Management System API"}


@router.get("/about", tags=["General"])
async def about() -> dict[str, str]:
    return {"message": "A fully functional API to manage your patient records"}


@router.get("/view", tags=["Patient Management"])
async def view_all_patients(
    db: PatientDB = Depends(get_db),
    city: str | None = Query(default=None),
    sort_by: str | None = Query(default=None),
    order: str = Query(default="asc"),
) -> list[dict[str, Any]]:
    data = db.get_all()

    if city:
        data = [patient for patient in data if get_city(patient).lower() == city.lower()]

    if sort_by:
        if sort_by not in {"age", "weight", "bmi"}:
            raise HTTPException(400, "Invalid sort_by. Choose age / weight / bmi.")
        data = sorted(
            data,
            key=lambda patient: patient[sort_by],
            reverse=order.lower() == "desc",
        )

    return data


@router.get("/patient/{patient_id}", tags=["Patient Management"])
async def view_patient(
    patient_id: str = Path(
        description="Patient ID e.g., P001",
        examples=["P001"],
    ),
    db: PatientDB = Depends(get_db),
) -> dict[str, Any]:
    patient = db.get_by_id(patient_id)
    if patient is None:
        raise HTTPException(404, f"Patient with ID '{patient_id}' not found")
    return patient


@router.post("/create", status_code=201, tags=["Patient Management"])
async def create_patient(
    patient: Patient,
    db: PatientDB = Depends(get_db),
) -> dict[str, Any]:
    if db.email_exists(patient.email):
        raise HTTPException(409, f"A patient with email '{patient.email}' already exists")

    new_record = db.create(patient)
    return {"message": "Patient created successfully", "patient": new_record}


@router.delete("/delete/{patient_id}", tags=["Patient Management"])
async def delete_patient(
    patient_id: str = Path(
        description="Patient ID e.g., P001",
        examples=["P001"],
    ),
    db: PatientDB = Depends(get_db),
) -> dict[str, Any]:
    deleted_patient = db.delete(patient_id)
    if deleted_patient is None:
        raise HTTPException(404, f"Patient with ID '{patient_id}' not found")

    return {
        "message": "Patient deleted successfully",
        "patient": deleted_patient,
    }
