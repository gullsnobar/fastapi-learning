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
        try:
            with open(self.filepath, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_all(self) -> List[Dict[str, Any]]:
        return self.data

    def get_by_id(self, patient_id: str) -> Dict[str, Any] | None:
        for patient in self.data:
            if patient["id"] == patient_id:
                return patient
        return None

    def email_exists(self, email: str) -> bool:
        # Existing records may predate the email field. Treat those records as
        # non-matches instead of failing every create request with a KeyError.
        return any(p.get("email") == email for p in self.data)

    def create(self, patient: Patient) -> Dict[str, Any]:
        new_id = f"P{len(self.data) + 1:03d}"
        record = patient.model_dump(mode="json")
        record["id"] = new_id
        self.data.append(record)
        self.save()
        return record

    def delete(self, patient_id: str) -> Dict[str, Any] | None:
        for index, patient in enumerate(self.data):
            if patient["id"] == patient_id:
                deleted = self.data.pop(index)
                self.save()
                return deleted
        return None
