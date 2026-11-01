from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from typing import Optional, List
from models import Patient
from database import PatientDB

# 1. Lifespan: Initialize DB on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create the DB instance and attach it to the app state
    app.state.db = PatientDB("patients.json")
    yield
    # Shutdown: Anything here happens when server stops (optional)

app = FastAPI(
    title="Patient Management System API",
    lifespan=lifespan
)

# 2. Dependency: A function that returns the DB instance
def get_db() -> PatientDB:
    return app.state.db

@app.get("/", tags=["General"])
async def root():
    return {"message": "Patient Management System API"}

@app.get("/view", tags=["Patient Management"])
async def view_all_patients(
    db: PatientDB = Depends(get_db),  # <--- INJECTED HERE
    city: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    order: str = Query("asc")
):
    data = db.get_all()

    if city:
        data = [p for p in data if p["address"]["city"].lower() == city.lower()]
    if sort_by and sort_by in ["age", "weight", "bmi"]:
        reverse_flag = order.lower() == "desc"
        data = sorted(data, key=lambda x: x[sort_by], reverse=reverse_flag)

    return data

@app.get("/patient/{patient_id}", tags=["Patient Management"])
async def view_patient(patient_id: str, db: PatientDB = Depends(get_db)):
    patient = db.get_by_id(patient_id)
    if not patient:
        raise HTTPException(404, f"Patient '{patient_id}' not found")
    return patient

@app.post("/create", status_code=201, tags=["Patient Management"])
async def create_patient(patient: Patient, db: PatientDB = Depends(get_db)):
    # Pydantic already validated the data
    new_record = db.create(patient)
    return {"message": "Patient created successfully", "patient": new_record}