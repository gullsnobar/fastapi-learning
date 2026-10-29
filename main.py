from fastapi import FastAPI, HTTPException, Query
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

@app.get("/")
async def root():
    return {"message": "Patient Management System API"}

@app.get("/about")
async def about():
    return {"message": "A fully functional API to manage your patient records"}

# UPDATED ENDPOINT: View with sorting and filtering
@app.get("/view")
async def view_all_patients(
    city: Optional[str] = Query(None, description="Filter patients by city (e.g., New York)"),
    sort_by: Optional[str] = Query(None, description="Sort by 'age', 'weight', or 'bmi'"),
    order: str = Query("asc", description="Sort order: 'asc' or 'desc'")
):
    data = load_data()

    # 1. Filtering logic (if the user provided a city)
    if city:
        # We use a list comprehension to keep only patients matching the city (case-insensitive)
        data = [p for p in data if p["city"].lower() == city.lower()]

    # 2. Sorting logic (if the user provided a sort_by field)
    if sort_by:
        # Check if the sort_by field is one of the allowed fields to avoid errors
        if sort_by in ["age", "weight", "bmi"]:
            # We use a reverse flag if order is 'desc'
            reverse_flag = True if order.lower() == "desc" else False
            # Sort the list of dictionaries by the given key
            data = sorted(data, key=lambda x: x[sort_by], reverse=reverse_flag)
        else:
            raise HTTPException(
                status_code=400, 
                detail="Invalid sort_by field. Choose from 'age', 'weight', or 'bmi'."
            )

    return data

@app.get("/patient/{patient_id}")
async def view_patient(patient_id: str):
    data = load_data()
    for patient in data:
        if patient["id"] == patient_id:
            return patient
            
    raise HTTPException(status_code=404, detail=f"Patient with ID '{patient_id}' not found")