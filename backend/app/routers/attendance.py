from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models.schemas import AttendanceCreate, AttendanceResponse
from db.database import SessionDep
from models.models import User, Attendance
from utilities.crud import (
    get_user_by_username,
    create_attendance, 
    get_attendance_by_user_id,
    update_attendance, 
    delete_attendance_by_id
)
from auth.OAuth import role_required
from logger.logger import logger

router = APIRouter(
    prefix="/api/v1/attendance",
    tags=["attendance"]
)


# ================= Add Attendance ================= #
@router.post("/", response_model=AttendanceResponse)
def add_attendance(
    students_username: str,
    attendance_data: AttendanceCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Add attendance record for a student (teacher/admin only)"""
    try:
        # Note: role_required already validates user, so this check is redundant
        # But keeping it for extra safety is fine
        if not user:
            logger.warning("Invalid credentials: teacher/admin authorization failed.")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        student = get_user_by_username(session, students_username)

        if not student:
            logger.warning(f"Student '{students_username}' not found.")
            raise HTTPException(status_code=404, detail="Student not found")

        attendance = Attendance(
            user_id=student.id,
            month=attendance_data.month,
            semester=attendance_data.semester,
            total=attendance_data.total,
            attendee_status=attendance_data.attendee_status,
            marked_by=user.id
        )

        created_attendance = create_attendance(session, attendance)
        logger.info(
            f"Attendance created successfully for student '{students_username}' "
            f"(ID: {student.id}) by {user.username} (ID: {user.id})"
        )

        return created_attendance

    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error while creating attendance for '{students_username}': {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while creating attendance"
        )


# ================= Get Attendance by User ID ================= #
@router.get("/{user_id}", response_model=List[AttendanceResponse])
def get_attendance_by_userid(session: SessionDep, user_id: int):
    """Get attendance records for a specific user"""
    try:
        attendance_records = get_attendance_by_user_id(session, user_id)
        
        # Log the count for better debugging
        logger.info(f"Fetched {len(attendance_records)} attendance record(s) for user_id {user_id}")
        
        return attendance_records  # Empty list is valid, no need to check

    except Exception as e:
        logger.error(f"Unexpected error while fetching attendance for user_id {user_id}: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while fetching attendance"
        )


# ================= Update Attendance ================= #
@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance_endpoints(
    attendance_id: int,
    attendance_data: AttendanceCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Update attendance record (teacher/admin only)"""
    try:
        attendance = update_attendance(session, attendance_id, attendance_data)

        if not attendance:
            logger.warning(f"Attendance {attendance_id} not found for update")
            raise HTTPException(status_code=404, detail="Attendance not found")

        logger.info(f"Attendance {attendance_id} updated successfully by {user.username}")
        return attendance

    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error while updating attendance {attendance_id}: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while updating attendance"
        )


# ================= Delete Attendance ================= 
@router.delete("/{attendance_id}")
def delete_attendance_by_id_endpoints(
    attendance_id: int,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Delete attendance record (teacher/admin only)"""
    try:
        deleted = delete_attendance_by_id(session, attendance_id)

        if not deleted:
            logger.warning(f"Attendance {attendance_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Attendance not found")

        logger.info(f"Attendance {attendance_id} deleted successfully by {user.username}")
        return {"ok": True, "message": "Attendance deleted successfully"}

    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error while deleting attendance {attendance_id}: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while deleting attendance"
        )