from fastapi import FastAPI, HTTPException
import json

app = FastAPI(
    title="Patient Management System API",
    description="A fully functional API to manage your patient records.",
    version="0.1.0"
)

# 1. Helper Function to load data from JSON
def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

# 2. Endpoints
@app.get("/")
async def root():
    return {"message": "Patient Management System API"}

@app.get("/about")
async def about():
    return {"message": "A fully functional API to manage your patient records"}

# GET endpoint to retrieve all patients
@app.get("/view")
async def view_all_patients():
    data = load_data()
    return data

# NEW Endponit: Get a specific patient by ID

@app.get("/patient/{patient_id}")
async def view_patient(patient_id: str):

    # 1. load all the data
    data = load_data()
    # 2. loop through the data to find the matching ID
    for patient in data:
        if patient["id"] == patient_id:
            return patient   # Return the patient if found

    # 3. If the loop finishes and no patient was found, raise an error
    raise HTTPException(
        status_code=404,
        detail=f"Patient with ID '{patient_id}' not found"
    )         