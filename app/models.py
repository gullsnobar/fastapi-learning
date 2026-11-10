from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, computed_field


class Address(BaseModel):
    city: str
    state: str
    pin_code: str


class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title="Name of the patient")]
    email: EmailStr
    age: Annotated[int, Field(gt=0, lt=120)]
    gender: str
    weight: Annotated[float, Field(gt=0, strict=True)]
    height: Annotated[float, Field(gt=0, strict=True)]
    married: bool = False
    allergies: list[str] | None = None
    address: Address

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / self.height**2, 2)
