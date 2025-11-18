from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import Optional
import enum

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True  # or `from_attributes = True` if using Pydantic v2

class OperationType(str, enum.Enum):
    """Enum for calculation operation types"""
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"

class CalculationCreate(BaseModel):
    """Schema for creating a calculation"""
    a: Decimal
    b: Decimal
    type: OperationType
    user_id: Optional[int] = None
    
    @field_validator('b')
    @classmethod
    def validate_division_by_zero(cls, v, info):
        """Prevent division by zero"""
        if info.data.get('type') == OperationType.DIVIDE and v == 0:
            raise ValueError("Cannot divide by zero")
        return v
    
    @field_validator('type')
    @classmethod
    def validate_operation_type(cls, v):
        """Validate operation type is supported"""
        if v not in OperationType:
            raise ValueError(f"Operation type must be one of: {', '.join([op.value for op in OperationType])}")
        return v


class CalculationRead(BaseModel):
    """Schema for reading a calculation"""
    id: int
    a: Decimal
    b: Decimal
    type: OperationType
    result: Decimal
    created_at: datetime
    user_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


class CalculationUpdate(BaseModel):
    """Schema for updating a calculation (if needed)"""
    a: Optional[Decimal] = None
    b: Optional[Decimal] = None
    type: Optional[OperationType] = None