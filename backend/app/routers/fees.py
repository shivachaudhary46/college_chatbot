from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.db.database import SessionDep
from app.models.schemas import FeesCreate, FeesResponse
from app.models.models import Fees, User
from app.auth.OAuth import role_required
from app.logger.logger import logger 
from app.utilities.crud import (
    get_user_by_username,
    create_fees,
    get_fees_by_user_id,
    get_all_fees,
    get_fees_by_id,
    delete_fees_by_user_id,
    delete_fees_by_id,
    update_fees,
)

router = APIRouter(
    prefix="/api/v1/fees",
    tags=["fees"]
)


# ADD FEES FOR A STUDENT
@router.post("/users/{student_username}/", response_model=FeesResponse)
def add_user_fee(
    student_username: str,
    fee_data: FeesCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Add fees record for a student"""
    try:
        student = get_user_by_username(session, student_username)
        if not student:
            logger.warning(f"Student: {student_username} not found")
            raise HTTPException(status_code=404, detail="student not found")

        fees = Fees(
            user_id=student.id,
            semester=fee_data.semester,
            total_paid=fee_data.total_paid
        )

        created_fees = create_fees(session, fees)
        logger.info(f"fees created successfully for {student_username}")
        return create_fees(session, fees)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while creating fees: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# GET ALL FEES
@router.get("/", response_model=List[FeesResponse])
def get_fees_endpoints(session: SessionDep):
    try:
        all_fees = get_all_fees(session)
        logger.info(f"Successfully fetched all fees")
        return all_fees
    except Exception as e:
        logger.error(f"Unexpected error while fetching fees: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# GET FEES BY FEES ID
@router.get("/{fees_id}", response_model=FeesResponse)
def get_fees_by_id_endpoints(session: SessionDep, fees_id: int):
    try:
        fees = get_fees_by_id(session, fees_id)
        if not fees:
            logger.warning(f"fees not found for {fees_id}")
            raise HTTPException(status_code=404, detail="fees not found")
        return fees
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching fees: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# GET FEES BY USER ID
@router.get("/users/{user_id}", response_model=List[FeesResponse])
def get_fees_by_user_id_endpoints(session: SessionDep, user_id: int):
    try:
        fees = get_fees_by_user_id(session, user_id)
        logger.info(f"Successfully fetched the fees by user_id {user_id}")
        return fees
    except Exception as e:
        logger.error(f"Unexpected error while fetching fees: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# UPDATE FEES
@router.put("/{fees_id}", response_model=FeesResponse)
def update_fees_endpoints(
    fees_id: int,
    fees_data: FeesCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    try:
        fees = update_fees(session, fees_id, fees_data)
        if not fees:
            logger.warning(f"Successfully updated fees for {fees_id}")
            raise HTTPException(status_code=404, detail="fees not found")
        return fees
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while updating fees: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# DELETE FEES
@router.delete("/{fees_id}")
def delete_fee_by_user_id_endpoints(
    fees_id: int,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    try:
        if not delete_fees_by_id(session, fees_id):
            logger.warning(f"Fees could not found for {fees_id}")
            raise HTTPException(status_code=404, detail="fees not found")
        return {"message": "fees deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while deleting fees: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")