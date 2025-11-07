# from fastapi import FastAPI, HTTPException
# from schemas import ChatMessage, ChatResponse, QueryType
# from crud import get_user_by_username, get_user_attendance, get_user_fees, get_user_marks
# from chatbot import classify_query, format_attendance_data, get_conversational_response, format_marks_data, format_fees_data, get_college_info_response, get_general_search_response
# from database import SessionDep
# # app = FastAPI() 

# # @app.post("/api/v1/chat", response_model=ChatResponse)
# async def chat(message: ChatMessage, session: SessionDep):
#     """Main chat handler - process user query"""
    
#     username = message.username
#     query = message.query
    
#     # Verify user exists
#     user = get_user_by_username(session, username)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Classify the query
#     query_type = classify_query(query)
    
#     # Route to appropriate handler
#     if query_type == QueryType.ATTENDANCE:
#         attendance_records = get_user_attendance(session, username)
#         formatted_data = format_attendance_data(attendance_records)
#         response = get_conversational_response(formatted_data, query)
        
#     elif query_type == QueryType.MARKS:
#         marks_records = get_user_marks(session, username)
#         formatted_data = format_marks_data(marks_records)
#         response = get_conversational_response(formatted_data, query)
        
#     elif query_type == QueryType.FEES:
#         fees_records = get_user_fees(session, username)
#         formatted_data = format_fees_data(fees_records)
#         response = get_conversational_response(formatted_data, query)
        
#     elif query_type == QueryType.COLLEGE_INFO:
#         response = get_college_info_response(query)
        
#     else:  # GENERAL
#         response = get_general_search_response(query)
    
#     return ChatResponse(response=response, query_type=query_type)

# if __name__ == "__main__":
#     import asyncio
#     from database import engine
#     from sqlmodel import Session
    
#     with Session(engine) as session:
#         request = ChatMessage(username="shivachaudhary", query="what is 3*4 ^ 2 ?")
#         response = asyncio.run(chat(request, session))
#         print(response)

from fastapi import HTTPException
from sqlmodel import select, Session

from app.models import Course, UserCourseLink, User
from app.schemas import CourseCreate, CourseResponse


# =============================#
# COURSE SERVICE FUNCTIONS by ( TEACHER / ADMIN)
# =============================#

def create_course(session: Session, user: User, course_data: CourseCreate):
    """Teacher/Admin create course"""
    teacher_id = user.id if user.role == "teacher" else course_data.teacher_id

    course = Course(
        name=course_data.name,
        code=course_data.code,
        teacher_id=teacher_id,
    )
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def update_course(session: Session, course_id: int, user: User, course_data: CourseCreate):
    """Teacher/Admin update course"""

    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(404, "Course not found")

    if user.role == "teacher" and course.teacher_id != user.id:
        raise HTTPException(403, "You are not authorized to modify this course")

    course.name = course_data.name
    course.code = course_data.code

    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def delete_course(session: Session, course_id: int, user: User):
    """Teacher/Admin delete course"""

    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(404, "Course not found")

    if user.role == "teacher" and course.teacher_id != user.id:
        raise HTTPException(403, "You are not authorized to delete this course")

    session.delete(course)
    session.commit()
    return {"message": "Course deleted successfully"}


def get_all_courses(session: Session):
    return session.exec(select(Course)).all()


def get_course_by_id(session: Session, course_id: int):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(404, "Course not found")
    return course


# =============================#
# STUDENT VIEW COURSES
# =============================#

def get_courses_for_student(session: Session, user_id: int):
    enrollments = session.exec(
        select(Course).join(UserCourseLink).where(UserCourseLink.user_id == user_id)
    ).all()
    return enrollments


# =============================#
# ENROLLMENT SERVICE
# =============================#

def enroll_student_to_course(session: Session, course_id: int, student_id: int, user: User):
    """Teacher/Admin enroll student to course"""

    student = session.get(User, student_id)
    if not student or student.role != "student":
        raise HTTPException(404, "Student not found")

    existing = session.get(UserCourseLink, (student_id, course_id))
    if existing:
        raise HTTPException(400, "Student already enrolled")

    link = UserCourseLink(user_id=student_id, course_id=course_id)
    session.add(link)
    session.commit()
    return {"message": "Student enrolled successfully"}


def unenroll_student_from_course(session: Session, course_id: int, student_id: int, user: User):
    """Remove student from course"""

    existing = session.get(UserCourseLink, (student_id, course_id))
    if not existing:
        raise HTTPException(404, "Student not enrolled in this course")

    session.delete(existing)
    session.commit()
    return {"message": "Student unenrolled successfully"}


def get_students_in_course(session: Session, course_id: int):
    """Return list of students enrolled into course"""

    students = session.exec(
        select(User).join(UserCourseLink).where(UserCourseLink.course_id == course_id)
    ).all()

    return students
