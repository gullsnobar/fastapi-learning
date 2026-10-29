from fastapi import FastAPI
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