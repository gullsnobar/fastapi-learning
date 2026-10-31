from fastapi import FastAPI, HTTPException, Query, Path
from typing import Optional, List
import json
from models import Patient, PatientUpdate   # ← NEW: import our models

app = FastAPI(
    title="Patient Management System API",
    description="A fully functional API to manage your patient records.",
    version="0.1.0"
)

# --- Load data ---
def load_data() -> List[dict]:
    with open("patients.json", "r") as f:
        return json.load(f)

def save_data(data: List[dict]) -> None:
    # Helper we'll need for POST/PUT/DELETE later
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

# --- Endpoints ---
@app.get("/", tags=["General"])
async def root():
    return {"message": "Patient Management System API"}

@app.get("/about", tags=["General"])
async def about():
    return {"message": "A fully functional API to manage your patient records"}

@app.get(
    "/view",
    summary="View all patients (with optional filtering & sorting)",
    tags=["Patient Management"]
)
async def view_all_patients(
    city: Optional[str] = Query(None, description="Filter by city"),
    sort_by: Optional[str] = Query(None, description="Sort by 'age', 'weight', 'bmi'"),
    order: str = Query("asc", description="Sort order: 'asc' or 'desc'")
):
    data = load_data()

    if city:
        data = [p for p in data if p["address"]["city"].lower() == city.lower()]

    if sort_by:
        if sort_by in ["age", "weight", "bmi"]:
            reverse_flag = order.lower() == "desc"
            data = sorted(data, key=lambda x: x[sort_by], reverse=reverse_flag)
        else:
            raise HTTPException(400, "Invalid sort_by. Choose age / weight / bmi.")

    return data

@app.get(
    "/patient/{patient_id}",
    summary="Get a specific patient by ID",
    tags=["Patient Management"]
)
async def view_patient(
    patient_id: str = Path(..., description="Patient ID e.g., P001", example="P001")
):
    data = load_data()
    for patient in data:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(404, f"Patient with ID '{patient_id}' not found")

# --- NEW ENDPOINT: Create a patient using Pydantic ---
@app.post(
    "/create",
    summary="Create a new patient record",
    tags=["Patient Management"],
    status_code=201
)
async def create_patient(patient: Patient):     # ← Pydantic handles validation here
    data = load_data()

    # Auto-generate a new ID
    new_id = f"P{len(data) + 1:03d}"

    # Convert Pydantic object → plain dict, then attach the ID
    new_patient_dict = patient.model_dump(mode="json")
    new_patient_dict["id"] = new_id

    data.append(new_patient_dict)
    save_data(data)

    return {"message": "Patient created successfully", "patient": new_patient_dict}