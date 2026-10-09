from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class OperationEnum(str, Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    POWER = "^"

class CalculationRequest(BaseModel):
    num1: float = Field(..., description="First operand")
    num2: float = Field(..., description="Second operand")
    operation: OperationEnum = Field(..., description="Operator (+, -, *, /, ^)")

class CalculationResponse(BaseModel):
    id: int
    num1: float
    num2: float
    operation: str
    result: float
    timestamp: datetime

    class Config:
        from_attributes = True