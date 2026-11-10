import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


class PatientApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "patients.json"
        self.database_path.write_text(
            json.dumps(
                [
                    {
                        "id": "P001",
                        "name": "Legacy Patient",
                        "city": "Lahore",
                        "age": 30,
                        "weight": 70,
                        "bmi": 22.1,
                    }
                ]
            ),
            encoding="utf-8",
        )
        self.client_context = TestClient(create_app(self.database_path))
        self.client = self.client_context.__enter__()

    def tearDown(self) -> None:
        self.client_context.__exit__(None, None, None)
        self.temp_directory.cleanup()

    def test_root(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Patient Management System API")

    def test_city_filter_supports_legacy_data(self) -> None:
        response = self.client.get("/view", params={"city": "lahore"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([patient["id"] for patient in response.json()], ["P001"])

    def test_create_uses_next_available_id(self) -> None:
        response = self.client.post(
            "/create",
            json={
                "name": "Alex Morgan",
                "email": "alex@example.com",
                "age": 32,
                "gender": "Male",
                "weight": 72.5,
                "height": 1.78,
                "address": {
                    "city": "Karachi",
                    "state": "Sindh",
                    "pin_code": "74000",
                },
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["patient"]["id"], "P002")

    def test_invalid_sort_field_is_rejected(self) -> None:
        response = self.client.get("/view", params={"sort_by": "name"})

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
