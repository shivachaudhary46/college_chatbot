from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..schemas import MarksCreate, MarksResponse
from ..models import User, Marks
from ..crud import (
    get_user_by_username,
    create_marks,
    get_marks_by_user_id,
    get_all_marks,
    get_marks_by_id,
    update_marks,
    delete_marks_by_user_id,
)
from ..OAuth import role_required
from ..database import SessionDep
from ..logger import logger

router = APIRouter(
    prefix="/api/v1",
    tags=["marks"]
)

@router.post("/users/{student_username}/marks/", response_model=MarksResponse)
def add_marks_record(
    student_username: str,
    marks_data: MarksCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Add marks record for a student (teacher/admin access only)"""
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials token")

        student = get_user_by_username(session, student_username)
        if not student:
            logger.warning(f"Student not found with username {student_username}")
            raise HTTPException(status_code=404, detail="Student not found")

        marks = Marks(
            user_id=student.id,
            semester=marks_data.semester,
            subject=marks_data.subject,
            total_marks=marks_data.total_marks,
            grade=marks_data.grade,
            exam_date=marks_data.exam_date
        )

        created_marks = create_marks(session, marks)
        logger.info(f"marks created for {marks.user_id}")
        return created_marks

    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while creating marks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/users/marks/", response_model=List[MarksResponse])
def get_marks_endpoints(session: SessionDep):
    """Get all marks from users"""
    try:
        return get_all_marks(session)
    except Exception as e:
        logger.error(f"Unexpected error while fetching marks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/marks/{marks_id}", response_model=List[MarksResponse])
def get_marks_by_id_endpoints(session: SessionDep, marks_id: int):
    """Get marks by marks_id"""
    try:
        return get_marks_by_id(session, marks_id)
    except Exception as e:
        logger.error(f"Unexpected error while fetching marks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/users/marks/{user_id}", response_model=List[MarksResponse])
def get_marks_by_user_id_endpoints(session: SessionDep, user_id: int):
    """Get marks by user id"""
    try:
        return get_marks_by_user_id(session, user_id)
    except Exception as e:
        logger.error(f"Unexpected error while fetching marks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/marks/{student_id}", response_model=MarksResponse)
def update_marks_endpoints(
    student_id: int,
    marks_data: MarksCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Update marks (teacher/admin only)"""
    try:
        marks = update_marks(session, int(student_id), marks_data)
        if not marks:
            raise HTTPException(status_code=404, detail="marks not found")
        return marks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while updating marks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/marks/{student_id}")
def delete_mark_by_user_id_endpoints(
    student_id: int,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Delete mark by id (teacher/admin only)"""
    try:
        if not delete_marks_by_user_id(session, student_id):
            raise HTTPException(status_code=404, detail="marks not found")
        return {"message": "marks deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while deleting marks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")