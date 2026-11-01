import json
from typing import List, Dict, Any
from models import Patient

DB_FILE = "patients.json"

class PatientDB:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data: List[Dict[str, Any]] = []
        self.load()

    def load(self):
        """Load data from JSON file into memory."""
        try:
            with open(self.filepath, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save(self):
        """Write in-memory data back to JSON file."""
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_all(self) -> List[Dict[str, Any]]:
        return self.data

    def get_by_id(self, patient_id: str) -> Dict[str, Any] | None:
        for patient in self.data:
            if patient["id"] == patient_id:
                return patient
        return None

    def create(self, patient: Patient) -> Dict[str, Any]:
        new_id = f"P{len(self.data) + 1:03d}"
        record = patient.model_dump(mode="json")
        record["id"] = new_id
        self.data.append(record)
        self.save()  # Save immediately after change
        return record