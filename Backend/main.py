import operator
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models, schemas
from database import engine, get_db

# Initialize database schema
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Calculator API with History Tracking")

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPERATIONS = {
    schemas.OperationEnum.ADD: operator.add,
    schemas.OperationEnum.SUBTRACT: operator.sub,
    schemas.OperationEnum.MULTIPLY: operator.mul,
    schemas.OperationEnum.DIVIDE: operator.truediv,
    schemas.OperationEnum.POWER: operator.pow,
}

@app.post("/calculate", response_model=schemas.CalculationResponse, status_code=status.HTTP_201_CREATED)
def calculate_and_save(payload: schemas.CalculationRequest, db: Session = Depends(get_db)):
    if payload.operation == schemas.OperationEnum.DIVIDE and payload.num2 == 0:
        raise HTTPException(status_code=400, detail="Division by zero is undefined.")

    calc_func = OPERATIONS[payload.operation]
    calculated_result = calc_func(payload.num1, payload.num2)

    record = models.CalculationRecord(
        num1=payload.num1,
        num2=payload.num2,
        operation=payload.operation.value,
        result=calculated_result
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@app.get("/history", response_model=List[schemas.CalculationResponse])
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.CalculationRecord).order_by(models.CalculationRecord.timestamp.desc()).limit(limit).all()

@app.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
def clear_history(db: Session = Depends(get_db)):
    db.query(models.CalculationRecord).delete()
    db.commit()
    return None