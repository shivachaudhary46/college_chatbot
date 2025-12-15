import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.schemas import CourseCreate, CourseResponse
from app.models.models import User
from app.utilities.crud import (
    get_all_courses,
    get_course_by_id,
    update_course,
    delete_course,
    create_course,
    enroll_student_to_course,
    unenroll_student_from_course,
    get_courses_for_student,
    get_students_from_course,
    get_courses_for_teacher
)
from app.auth.OAuth import role_required
from app.db.database import SessionDep
from app.logger.logger import logger

router = APIRouter(
    prefix="/api/v1",
    tags=["courses"]
)

# CREATE COURSE
@router.post("/courses/", response_model=CourseResponse)
def create_course_endpoints(
    course_data: CourseCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    try:
        logger.info("Create course request received")

        if not user:
            logger.warning("Unauthorized course creation attempt")
            raise HTTPException(status_code=401, detail="Invalid credentials token")

        result = create_course(session, user, course_data)
        logger.info(f"Course created successfully: {result.id}")

        return result

    except Exception as e:
        logger.error(f"Error creating course: {e}")
        raise HTTPException(status_code=500, detail="Failed to create course")



# GET ALL COURSES
@router.get("/users/courses/", response_model=List[CourseResponse])
def get_all_course_endpoints(session: SessionDep):
    try:
        logger.info("Fetching all courses")
        return get_all_courses(session)

    except Exception as e:
        logger.error(f"Error fetching all courses: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch courses")



# GET COURSE BY ID
@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course_by_id_endpoints(session: SessionDep, course_id: int):
    try:
        logger.info(f"Fetching course with ID: {course_id}")

        result = get_course_by_id(session, course_id)

        if not result:
            logger.warning(f"Course not found: {course_id}")
            raise HTTPException(status_code=404, detail="Course not found")

        return result

    except Exception as e:
        logger.error(f"Error fetching course {course_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch course")



# GET COURSES FOR STUDENT
@router.get("/students/{student_id}/courses", response_model=List[CourseResponse])
def get_course_by_user_id_endpoints(session: SessionDep, student_id: int):
    try:
        logger.info(f"Fetching courses for student_id: {student_id}")
        return get_courses_for_student(session, student_id)

    except Exception as e:
        logger.error(f"Error fetching courses for student {student_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch student courses")

# GET COURSES FOR TEACHER
@router.get("/teachers/{teacher_id}/courses", response_model=List[CourseResponse])
def get_course_by_teacher_id(session: SessionDep, teacher_id: int):
    try: 
        logger.info(f"Fetching courses for teacher_id: {teacher_id}")
        return get_courses_for_teacher(session, teacher_id)
    
    except Exception as e:
        logger.error(f"Error fetching courses for teacher {teacher_id} : {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch teacher courses")

# ENROLL STUDENT
@router.post("/students/enroll/", response_model=dict[str, str])
def enroll_student(
    session: SessionDep,
    course_id: int,
    student_id: int,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    try:
        logger.info(f"Enroll student {student_id} into course {course_id}")
        return enroll_student_to_course(session, course_id, student_id, user)

    except Exception as e:
        logger.error(f"Error enrolling student {student_id} in course {course_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to enroll student")


# UNENROLL STUDENT
@router.delete("/students/unenroll/", response_model=dict[str, str])
def unenroll_student(
    session: SessionDep,
    course_id: int,
    student_id: int,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    try:
        logger.info(f"Unenroll student {student_id} from course {course_id}")
        return unenroll_student_from_course(session, course_id, student_id, user)

    except Exception as e:
        logger.error(f"Error unenrolling student {student_id} from course {course_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to unenroll student")



# UPDATE COURSE
@router.put("/update_course/", response_model=CourseResponse)
def update_course_endpoints(
    course_data: CourseCreate,
    session: SessionDep,
    course_id: int,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    try:
        logger.info(f"Update course request for course_id: {course_id}")

        result = update_course(session, course_id, user, course_data)

        if not result:
            logger.warning(f"Course not found during update: {course_id}")
            raise HTTPException(status_code=404, detail="Course not found")

        logger.info(f"Course updated successfully: {course_id}")
        return result

    except Exception as e:
        logger.error(f"Error updating course {course_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update course")



# DELETE COURSE
@router.delete("/delete_course/")
def delete_course_by_id_endpoints(
    session: SessionDep,
    course_id: int,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    try:
        logger.info(f"Delete course request for course_id: {course_id}")

        if not delete_course(session, course_id, user):
            logger.warning(f"Course not found during delete: {course_id}")
            raise HTTPException(status_code=404, detail="Course not found")

        logger.info(f"Course deleted successfully: {course_id}")
        return {"message": "Course deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting course {course_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete course")
