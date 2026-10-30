from fastapi import FastAPI, HTTPException, Query, Path
from typing import Optional
import json

app = FastAPI(
    title="Patient Management System API",
    description="A fully functional API to manage your patient records.",
    version="0.1.0"
)

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/", tags=["General"])
async def root():
    return {"message": "Patient Management System API"}

@app.get("/about", tags=["General"])
async def about():
    return {"message": "A fully functional API to manage your patient records"}

# UPDATED ENDPOINT: View with sorting and filtering
@app.get(
    "/view", 
    summary="View all patients (with optional filtering & sorting)",
    tags=["Patient Management"]
)
async def view_all_patients(
    city: Optional[str] = Query(None, description="Filter patients by city (e.g., New York)"),
    sort_by: Optional[str] = Query(None, description="Sort by 'age', 'weight', or 'bmi'"),
    order: str = Query("asc", description="Sort order: 'asc' or 'desc'")
):
    data = load_data()

    if city:
        data = [p for p in data if p["city"].lower() == city.lower()]

    if sort_by:
        if sort_by in ["age", "weight", "bmi"]:
            reverse_flag = True if order.lower() == "desc" else False
            data = sorted(data, key=lambda x: x[sort_by], reverse=reverse_flag)
        else:
            raise HTTPException(
                status_code=400, 
                detail="Invalid sort_by field. Choose from 'age', 'weight', or 'bmi'."
            )

    return data

# UPDATED ENDPOINT: View single patient using Path parameter properly
@app.get(
    "/patient/{patient_id}", 
    summary="Get a specific patient's details by ID",
    tags=["Patient Management"]
)
async def view_patient(
    patient_id: str = Path(
        ..., 
        description="The unique ID of the patient (e.g., P001)", 
        example="P001"
    )
):
    """
    Retrieve the full profile of a single patient.
    
    - **patient_id**: Required path parameter. Must be an exact match (e.g., P001).
    - Returns **404 Not Found** if the patient does not exist.
    """
    data = load_data()
    for patient in data:
        if patient["id"] == patient_id:
            return patient
            
    raise HTTPException(status_code=404, detail=f"Patient with ID '{patient_id}' not found")