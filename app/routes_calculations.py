# routes/calculations.py or endpoints/calculations.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal

from app import models, schemas
from app.database import get_db
from app.calculation_factory import perform_calculation

router = APIRouter(prefix="/calculations", tags=["calculations"])


import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.CalculationRead, status_code=201)
def create_calculation(
    calculation: schemas.CalculationCreate,
    db: Session = Depends(get_db)
):
    """Create a new calculation with detailed error logging"""
    
    logger.info(f"Received calculation request: {calculation}")
    
    try:
        logger.info(f"Step 1: Extracting values - a={calculation.a}, b={calculation.b}, type={calculation.type}")
        
        # Use the factory pattern to perform the calculation
        logger.info("Step 2: Calling perform_calculation")
        result = perform_calculation(
            calculation.a,
            calculation.b,
            calculation.type.value
        )
        logger.info(f"Step 3: Result computed: {result}")
        
        # Create database object
        logger.info("Step 4: Creating database object")
        db_calculation = models.Calculation(
            a=calculation.a,
            b=calculation.b,
            type=calculation.type,
            result=result,
            user_id=calculation.user_id
        )
        
        # Save to database
        logger.info("Step 5: Saving to database")
        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation)
        
        logger.info(f"Step 6: Successfully saved calculation with id={db_calculation.id}")
        return db_calculation
        
    except Exception as e:
        logger.error(f"ERROR OCCURRED: {str(e)}")
        logger.error(f"ERROR TYPE: {type(e).__name__}")
        logger.error(f"FULL TRACEBACK:\n{traceback.format_exc()}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/", response_model=List[schemas.CalculationRead])
def get_calculations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all calculations with pagination.
    """
    calculations = db.query(models.Calculation).offset(skip).limit(limit).all()
    return calculations


@router.get("/{calculation_id}", response_model=schemas.CalculationRead)
def get_calculation(
    calculation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific calculation by ID.
    """
    calculation = db.query(models.Calculation).filter(
        models.Calculation.id == calculation_id
    ).first()
    
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    return calculation


@router.get("/user/{user_id}", response_model=List[schemas.CalculationRead])
def get_user_calculations(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all calculations for a specific user.
    """
    # Verify user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    calculations = db.query(models.Calculation).filter(
        models.Calculation.user_id == user_id
    ).all()
    
    return calculations


@router.delete("/{calculation_id}", status_code=204)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a calculation by ID.
    """
    calculation = db.query(models.Calculation).filter(
        models.Calculation.id == calculation_id
    ).first()
    
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    db.delete(calculation)
    db.commit()
    
    return None