from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..schemas import CourseCreate, CourseResponse
from ..models import User
from ..crud import (
    get_all_courses,
    get_course_by_id,
    update_course,
    delete_course,
    create_course,
    enroll_student_to_course,
    unenroll_student_from_course,
    get_courses_for_student,
    get_students_from_course,
)
from ..OAuth import role_required
from ..database import SessionDep

router = APIRouter(
    prefix="/api/v1",
    tags=["courses"]
)

@router.post("/courses/", response_model=CourseResponse)
def create_course_endpoints(
    course_data: CourseCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Create a new course (teacher/admin only)"""
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials token")

    return create_course(session, user, course_data)

@router.get("/users/courses/", response_model=List[CourseResponse])
def get_all_course_endpoints(session: SessionDep):
    """Get all course in course database"""
    return get_all_courses(session)

@router.get("/courses/{course_id}", response_model=List[CourseResponse])
def get_course_by_id_endpoints(session: SessionDep, course_id: int):
    """Get course by course_id"""
    return get_course_by_id(session, course_id)

@router.get("/students/{students_id}/courses", response_model=List[CourseResponse])
def get_course_by_user_id_endpoints(session: SessionDep, user_id: int):
    """Get courses by user id"""
    return get_courses_for_student(session, user_id)

@router.get("/courses/{course_id}/students", response_model=List[CourseResponse])
def get_course_by_course_id_endpoints(session: SessionDep, course_id: int):
    """Get students by course_id"""
    return get_students_from_course(session, course_id)

@router.post("/students/enroll/", response_model=dict[str, str])
def enroll_student(
    session: SessionDep, 
    course_id: int, 
    student_id: int, 
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Enroll student to course"""
    return enroll_student_to_course(session, course_id, student_id, user)

@router.delete("/students/unenroll/", response_model=dict[str, str])
def unenroll_student(
    session: SessionDep, 
    course_id: int, 
    student_id: int, 
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Unenroll student from course"""
    return unenroll_student_from_course(session, course_id, student_id, user)

@router.put("/update_course/", response_model=CourseResponse)
def update_course_endpoints(
    course_data: CourseCreate,
    session: SessionDep,
    course_id: int, 
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Update a course (teacher/admin only)"""
    courses = update_course(session, course_id, user, course_data)

    if not courses:
        raise HTTPException(status_code=404, detail="courses not found")
    return courses

@router.delete("/delete_course/")
def delete_course_by_course_id_endpoints(
    session: SessionDep,
    course_id: int, 
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Delete a course by id (teacher/admin only)"""
    if not delete_course(session, course_id, user):
        raise HTTPException(status_code=404, detail="course not found")
    return {"message": "course deleted successfully"}