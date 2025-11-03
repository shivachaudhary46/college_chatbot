from .schemas import UserCreate, UserResponse, AttendanceCreate, AttendanceResponse, FeesCreate, FeesResponse, MarksResponse, MarksCreate, Token, ChatMessage, ChatResponse, QueryType, CourseResponse, CourseCreate, AssignmentCreate, AssignmentResponse
from .database import SessionDep, create_all_db_tables
from .models import User, Attendance, Fees, Marks, Course, Notice, Assignment
from .crud import get_user_by_username, create_user, create_attendance, create_fees, create_marks, get_all_users, delete_user,  get_user_attendance, get_user_fees, get_user_marks, create_course_records, create_assignment_records
from .utilities import hasher 
from .OAuth import authenticate_user, create_access_token, get_current_user, role_required
from .chatbot import classify_query, format_attendance_data, format_fees_data, format_marks_data, get_conversational_response, get_college_info_response, get_general_search_response

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Annotated
import os
from datetime import timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE", 60))
app = FastAPI() 

@app.on_event("startup")
def startup():
    """Initialize database on startup"""
    create_all_db_tables()

# ===== USER ENDPOINTS ===== # Admin, student, user
@app.post("/api/v1/users/", response_model=UserResponse)
def create_new_user(user_data: UserCreate, session: SessionDep):
    """Create a new user"""
    existing = get_user_by_username(session, user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
        
    user = User(
        username=user_data.username,
        full_name=user_data.full_name,
        email=user_data.email,
        role=user_data.role,
        batch=user_data.batch,
        program=user_data.program,
        hashed_password=hasher.hash(user_data.password)
    )
    return create_user(session, user)

# ==== Upload assignments for only Teachers =====
# ==== Teacher has access to attendance, marks of students

# ==== admin has access to every post endpoints ====
# teacher, admin
@app.get("/api/v1/users/", response_model=List[UserResponse])
def read_all_users(
    session: SessionDep,
    skip: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    """Get all users"""
    return get_all_users(session, skip, limit)

# admin
@app.get("/api/v1/users/{username}", response_model=UserResponse)
def read_user(username: str, session: SessionDep):
    """Get a specific user by username"""
    user = get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# admin
@app.delete("/api/v1/users/{username}")
def delete_user_by_username(username: str, session: SessionDep):
    """Delete a user"""
    user = get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(session, user.id)
    return {"ok": True}

# ===== Give access to insert datas to teacher only ====
# ===== But don't give accesss to insert fees for teacher ====

# ===== ATTENDANCE ENDPOINTS ===== # teacher, admin 
@app.post("/api/v1/users/attendance/", response_model=AttendanceResponse)
def mark_attendance(
    students_username: str, 
    attendance_data: AttendanceCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Add attendance record for a teacher"""
    if not user:
        raise HTTPException(status_code=404, detail="invalid credentials token")
        
    student = get_user_by_username(session, students_username)

    if not student:
        raise HTTPException(status_code=404, detail="student not found")
    
    attendance = Attendance(
        user_id=student.id,
        month=attendance_data.month,
        semester=attendance_data.semester,
        total=attendance_data.total,
        attendee_status=attendance_data.attendee_status,
        marked_by=user.id
    )
    return create_attendance(session, attendance)

# ===== FEES ENDPOINTS ======= # admin 
@app.post("/api/v1/users/{user_id}/fee/", response_model=FeesResponse)
def add_user_fee(
    student_username: str, 
    fee_data: FeesCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Add fees record for a student (teacher/admin access only)"""

    # check token validity 
    if not user:
        raise HTTPException(status_code=404, detail="invalid credentials token")
    
    student = get_user_by_username(session, student_username)

    if not student:
        raise HTTPException(status_code=404, detail="student not found")

    fees = Fees(
        user_id=student.id, 
        semester=fee_data.semester,
        total_paid=fee_data.total_paid
    )

    return create_fees(session, fees)

# ===== MARKS ENDPOINTS ====== # teacher, admin
@app.post("/api/v1/users/{student_username}/marks/", response_model=MarksResponse)
def add_marks_record(
    student_username: str,
    marks_data: MarksCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Add marks record for a student (teacher/admin access only)"""

    # Validate authenticated user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials token")

    # Fetch the student by username
    student = get_user_by_username(session, student_username)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Create marks record
    marks = Marks(
        user_id=student.id,
        semester=marks_data.semester,
        subject=marks_data.subject,
        total_marks=marks_data.total_marks,
        grade=marks_data.grade,
        exam_date=marks_data.exam_date
    )

    return create_marks(session, marks)

# ===== COURSE ENDPOINTS ====== # teacher, admin
@app.post("/api/v1/courses/", response_model=CourseResponse)
def create_course(
    course_data: CourseCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Create a new course (teacher/admin only)"""

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials token")

    # Teachers can only create their own courses
    teacher_id = user.id if user.role == "teacher" else course_data.teacher_id

    course = Course(
        name=course_data.name,
        code=course_data.code,
        teacher_id=teacher_id,
    )
    return create_course_records(session, course)

# ===== ASSIGNMENT ENDPOINTS ====== # teacher, admin
@app.post("/api/v1/courses/{course_id}/assignments/", response_model=AssignmentResponse)
def add_assignment(
    course_id: int,
    assignment_data: AssignmentCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Add an assignment to a course (teacher/admin only)"""

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials token")

    # Verify course exists
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Teacher can only add to their own courses
    if user.role == "teacher" and course.teacher_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this course")

    assignment = Assignment(
        title=assignment_data.title,
        description=assignment_data.description,
        due_date=assignment_data.due_date,
        course_id=course_id,
        user_id=user.id,
    )
    return create_assignment_records(session, assignment)


# ==== Auth Endpoints ==== # teacher, admin, students
@app.post("/api/v1/token", response_model=Token)
async def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    """Login and get access token"""
    user = authenticate_user(credentials.username, credentials.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
    access_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    token = create_access_token(data={"sub": user.username}, expire_time=access_time)
    return Token(access_token=token, token_type="bearer")

@app.get("/api/v1/me", response_model=UserResponse)
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Get current logged-in user info"""
    return current_user

# ===== chatbot =====
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat( 
    message: ChatMessage, session: SessionDep,
    user: User = Depends(role_required(["student", "teacher", "admin"])),
):
    """Main chat handler - process user query"""

    # Validate authenticated user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials token")
    
    username = user.username
    query = message.query
    
    # Classify the query
    query_type = classify_query(query)
    
    # Route to appropriate handler
    if query_type == QueryType.ATTENDANCE:
        attendance_records = get_user_attendance(session, username)
        formatted_data = format_attendance_data(attendance_records)
        response = get_conversational_response(formatted_data, query)
        
    elif query_type == QueryType.MARKS:
        marks_records = get_user_marks(session, username)
        formatted_data = format_marks_data(marks_records)
        response = get_conversational_response(formatted_data, query)
        
    elif query_type == QueryType.FEES:
        fees_records = get_user_fees(session, username)
        formatted_data = format_fees_data(fees_records)
        response = get_conversational_response(formatted_data, query)
        
    elif query_type == QueryType.COLLEGE_INFO:
        response = get_college_info_response(query)
        
    else:  # GENERAL
        response = get_general_search_response(query)
    
    return ChatResponse(response=response, query_type=query_type)

@app.get("/api/v1/chat/info")
async def chat_info():
    """Get chatbot info"""
    return {
            "name": "Student Assistant Chatbot",
            "version": "1.0",
            "capabilities": [
                "Answer questions about your attendance",
                "Check your marks and grades",
                "Query fee payment status",
                "Get college information",
                "Answer general questions"
            ],
            "example_queries": [
                "Can you tell me my attendance?",
                "What are my marks?",
                "What's my fee status?",
                "Tell me about the college",
                "How to prepare for exams?"
            ]
        }