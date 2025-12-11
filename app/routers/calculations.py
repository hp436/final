# app/routers/calculations.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.calculation import (
    CalculationCreate,
    CalculationRead,
    CalculationUpdate
)
from app.models.calculation import Calculation
from app.operations import add, subtract, multiply, divide, power

router = APIRouter(prefix="/calculations", tags=["Calculations"])

# NEW: Added "power"
OPERATION_MAP = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "power": power,
}

# ---------------------------
# Browse ALL calculations (public)
# ---------------------------
@router.get("/", response_model=list[CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    return db.query(Calculation).all()


# ---------------------------
# Read calculation by ID (public)
# ---------------------------
@router.get("/{calc_id}", response_model=CalculationRead)
def read_calculation(calc_id: str, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    return calc


# ---------------------------
# Create calculation (public)
# ---------------------------
@router.post("/", response_model=CalculationRead)
def create_calculation(payload: CalculationCreate, db: Session = Depends(get_db)):

    if payload.operation not in OPERATION_MAP:
        raise HTTPException(status_code=400, detail="Invalid operation")

    operation_fn = OPERATION_MAP[payload.operation]
    result = operation_fn(payload.a, payload.b)

    calc = Calculation(
        operation=payload.operation,
        a=payload.a,
        b=payload.b,
        result=result,
        user_id=None,      # tests expect no user for this assignment
    )

    db.add(calc)
    db.commit()
    db.refresh(calc)

    return calc


# ---------------------------
# Update calculation (public)
# ---------------------------
@router.put("/{calc_id}", response_model=CalculationRead)
@router.patch("/{calc_id}", response_model=CalculationRead)
def update_calculation(
    calc_id: str,
    payload: CalculationUpdate,
    db: Session = Depends(get_db),
):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    # Update operation
    if payload.operation:
        if payload.operation not in OPERATION_MAP:
            raise HTTPException(status_code=400, detail="Invalid operation")
        calc.operation = payload.operation

    # Update numbers
    if payload.a is not None:
        calc.a = payload.a

    if payload.b is not None:
        calc.b = payload.b

    # Recalculate result
    operation_fn = OPERATION_MAP[calc.operation]
    calc.result = operation_fn(calc.a, calc.b)

    db.commit()
    db.refresh(calc)

    return calc


# ---------------------------
# Delete calculation (public)
# ---------------------------
@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: str, db: Session = Depends(get_db)):

    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    db.delete(calc)
    db.commit()

    return
