from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from enum import Enum


# ------------------------------
# ENUM FOR CALCULATION TYPES
# ------------------------------
class CalculationType(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"


# ------------------------------
# USER SCHEMAS
# ------------------------------
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(BaseModel):
    email: str
    username: str   # add this
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------------
# CALCULATION SCHEMAS
# ------------------------------
class CalculationBase(BaseModel):
    a: float
    b: float
    type: str  # Accept string from frontend (case-insensitive)

    @validator("type")
    def validate_type(cls, v):
        v_upper = v.upper()
        if v_upper not in {"ADD", "SUBTRACT", "MULTIPLY", "DIVIDE"}:
            raise ValueError("Unsupported operation")
        return v_upper


class CalculationCreate(CalculationBase):
    """Frontend provides only a, b, type. User_id comes from JWT."""
    pass


class CalculationUpdate(BaseModel):
    """All fields optional for PUT update."""
    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[str] = None

    @validator("type")
    def validate_type(cls, v):
        if v is None:
            return v
        v_upper = v.upper()
        if v_upper not in {"ADD", "SUBTRACT", "MULTIPLY", "DIVIDE"}:
            raise ValueError("Unsupported operation")
        return v_upper


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: str
    result: float

    class Config:
        orm_mode = True


# ------------------------------
# AUTH SCHEMAS
# ------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordChange(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)