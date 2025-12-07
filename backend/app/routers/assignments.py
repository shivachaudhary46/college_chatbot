from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models.schemas import AssignmentCreate, AssignmentResponse
from models.models import User, Assignment, Course
from utilities.crud import (
    create_assignment_records,
    delete_assignment_by_id,
    get_assignment_by_course_id,
    get_assignment_by_id,
    update_assignment,
    get_recent_assignment_per_course,
    get_assignment_by_teacher_id,
)
from auth.OAuth import role_required
from db.database import SessionDep
from logger.logger import logger

router = APIRouter(
    prefix="/api/v1",
    tags=["assignments"]
)


# Create Assignment
@router.post("/courses/{course_id}/assignments/", response_model=AssignmentResponse)
def add_assignment_endpoints(
    course_id: int,
    assignment_data: AssignmentCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Add an assignment to a course (teacher/admin only)"""

    try:
        if not user:
            logger.warning("user not found")
            raise HTTPException(status_code=401, detail="Invalid credentials token")

        course = session.get(Course, course_id)
        if not course:
            logger.warning(f"Course not found of id : {course_id}")
            raise HTTPException(status_code=404, detail="Course not found")

        # If teacher, ensure teacher owns the course
        if user.role == "teacher" and course.teacher_id != user.id:
            logger.warning("Teacher and Admin role are only authorized to add assignment")
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to modify this course"
            )

        assignment = Assignment(
            title=assignment_data.title,
            description=assignment_data.description,
            due_date=assignment_data.due_date,
            course_id=course_id,
            teacher_id=user.id,
        )

        created_assignment = create_assignment_records(session, assignment)
        logger.info(f"Assignment created successfully for course {course_id}")
        return created_assignment

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while creating assignment for course {course_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ===============================
# Update Assignment
# ===============================
@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
def update_assignment_by_id_endpoints(
    assignment_id: int,
    assignment_data: AssignmentCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Update an assignment (teacher/admin only)"""

    try:
        assignment = update_assignment(session, int(assignment_id), assignment_data)

        if not assignment:
            logger.warning("Assignment not found id: {assignment_id}.")
            raise HTTPException(status_code=404, detail="Assignment not found")

        logger.info(f"Assignment {assignment_id} updated successfully")
        return assignment

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while updating assignment {assignment_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ===============================
# Delete Assignment
# ===============================
@router.delete("/assignments/{assignment_id}")
def delete_assignment_by_id_endpoints(
    assignment_id: int,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Delete an assignment by ID (teacher/admin only)"""

    try:
        deleted = delete_assignment_by_id(session, assignment_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found"
            )

        logger.info(f"Assignment {assignment_id} deleted successfully")
        return {"message": "Assignment deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while deleting assignment {assignment_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ===============================
# Get Recent Assignment Per Course
# ===============================
@router.get("/assignments/recent-per-course", response_model=List[AssignmentResponse])
def get_recent_assignment_per_course_endpoint(
    session: SessionDep,
    user: User = Depends(role_required(["student", "teacher", "admin"]))
):
    """Get the most recent assignment from each course"""

    try:
        assignments = get_recent_assignment_per_course(session)

        if not assignments:
            logger.warning("No recent assignment found for any course")
            raise HTTPException(
                status_code=404,
                detail="No recent assignments found for any course"
            )

        logger.info("Recent assignments fetched successfully")
        return assignments

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching recent assignments: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get Assignment by ID

@router.get("/assignment/{assignment_id}", response_model=AssignmentResponse)
def get_assignment_by_id_endpoint(
    assignment_id: int,
    session: SessionDep
):
    """Get assignment by ID"""

    try:
        assignment = get_assignment_by_id(session, assignment_id)

        if not assignment:
            logger.warning("Assignment not found of assignment {assignment_id}")
            raise HTTPException(status_code=404, detail="Assignment not found")

        return assignment

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching assignment {assignment_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ===============================
# Get Assignment by Course ID
# ===============================
@router.get("/assignment/course/{course_id}", response_model=List[AssignmentResponse])
def get_assignment_by_course_id_endpoint(
    course_id: int,
    session: SessionDep
):
    """Get assignment by course ID"""

    try:
        assignment = get_assignment_by_course_id(session, course_id)

        if not assignment:
            logger.warning("Course assignment not found of course : {course_id}")
            raise HTTPException(status_code=404, detail="Course assignment not found")

        return assignment

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching assignments for course {course_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/assignment/teacher/{teacher_id}", response_model=List[AssignmentResponse])
def get_assignment_by_teacher_id_endpoint(
    teacher_id: int,
    session: SessionDep
):
    """Get assignment by course ID"""

    try:
        assignment = get_assignment_by_teacher_id(session, teacher_id)

        if not assignment:
            logger.warning("Teachergiven assignment not found of teacher : {teacher_id}")
            raise HTTPException(status_code=404, detail="Teacher's assignment not found")

        return assignment

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching assignments for teacher id {teacher_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
