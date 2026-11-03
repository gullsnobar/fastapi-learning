from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from typing import Optional
from models import Patient
from database import PatientDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = PatientDB("patients.json")
    yield

app = FastAPI(
    title="Patient Management System API",
    lifespan=lifespan
)

def get_db() -> PatientDB:
    return app.state.db

@app.get("/", tags=["General"])
async def root():
    return {"message": "Patient Management System API"}

@app.get("/about", tags=["General"])
async def about():
    return {"message": "A fully functional API to manage your patient records"}

@app.get("/view", tags=["Patient Management"])
async def view_all_patients(
    db: PatientDB = Depends(get_db),
    city: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    order: str = Query("asc")
):
    data = db.get_all()

    if city:
        data = [p for p in data if p["address"]["city"].lower() == city.lower()]

    if sort_by:
        if sort_by in ["age", "weight", "bmi"]:
            reverse_flag = order.lower() == "desc"
            data = sorted(data, key=lambda x: x[sort_by], reverse=reverse_flag)
        else:
            raise HTTPException(400, "Invalid sort_by. Choose age / weight / bmi.")

    return data

@app.get("/patient/{patient_id}", tags=["Patient Management"])
async def view_patient(
    patient_id: str = Path(..., description="Patient ID e.g., P001", examples=["P001"]),
    db: PatientDB = Depends(get_db)
):
    patient = db.get_by_id(patient_id)
    if not patient:
        raise HTTPException(404, f"Patient with ID '{patient_id}' not found")
    return patient

@app.post("/create", status_code=201, tags=["Patient Management"])
async def create_patient(
    patient: Patient,
    db: PatientDB = Depends(get_db)
):
    if db.email_exists(patient.email):
        raise HTTPException(409, f"A patient with email '{patient.email}' already exists")

    new_record = db.create(patient)
    return {"message": "Patient created successfully", "patient": new_record}
