import json
from pathlib import Path
from typing import Any

from app.models import Patient


class PatientDB:
    """Small JSON-backed patient repository used by the API."""

    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)
        self.data: list[dict[str, Any]] = []
        self.load()

    def load(self) -> None:
        try:
            with self.filepath.open(encoding="utf-8") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []

    def save(self) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with self.filepath.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)
            file.write("\n")

    def get_all(self) -> list[dict[str, Any]]:
        return self.data

    def get_by_id(self, patient_id: str) -> dict[str, Any] | None:
        return next(
            (patient for patient in self.data if patient["id"] == patient_id),
            None,
        )

    def email_exists(self, email: str) -> bool:
        return any(patient.get("email") == email for patient in self.data)

    def create(self, patient: Patient) -> dict[str, Any]:
        record = patient.model_dump(mode="json")
        record["id"] = self._next_id()
        self.data.append(record)
        self.save()
        return record

    def delete(self, patient_id: str) -> dict[str, Any] | None:
        for index, patient in enumerate(self.data):
            if patient["id"] == patient_id:
                deleted = self.data.pop(index)
                self.save()
                return deleted
        return None

    def _next_id(self) -> str:
        numeric_ids = (
            int(patient["id"][1:])
            for patient in self.data
            if patient.get("id", "").startswith("P")
            and patient["id"][1:].isdigit()
        )
        return f"P{max(numeric_ids, default=0) + 1:03d}"
