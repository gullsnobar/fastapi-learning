from pydantic import BaseModel, EmailStr, Field, computed_field
from typing import Annotated, Optional, List


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
    allergies: Optional[List[str]] = None
    address: Address

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, gt=0, lt=120)
    gender: Optional[str] = None
    weight: Optional[float] = Field(default=None, gt=0)
    height: Optional[float] = Field(default=None, gt=0)
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    address: Optional[Address] = None