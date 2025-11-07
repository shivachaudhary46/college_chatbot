from .schemas import UserCreate, UserResponse, AttendanceCreate, AttendanceResponse, FeesCreate, FeesResponse, MarksResponse, MarksCreate, Token, ChatMessage, ChatResponse, QueryType, CourseResponse, CourseCreate, AssignmentCreate, AssignmentResponse, NoticeResponse, NoticeCreate
from .database import SessionDep, create_all_db_tables
from .models import User, Attendance, Fees, Marks, Course, Notice, Assignment
from .crud import get_user_by_username, create_user, create_attendance, create_fees, create_marks, get_all_users, delete_user_by_id, create_course_records, create_assignment_records, create_notice_records, get_all_notices, get_notice_by_id, update_notice, delete_notice, get_attendance_by_user_id, update_assignment, delete_assignment_by_id, get_assignment_by_course_id, get_assignment_by_id, get_recent_assignment_per_course, get_marks_by_user_id, get_fees_by_user_id, get_attendance_by_id, update_attendance, delete_attendance_by_user_id, get_all_fees, get_fees_by_id, delete_fees_by_user_id, update_fees, get_all_marks, get_marks_by_id, get_marks_by_user_id, update_marks, delete_marks_by_user_id, get_all_courses, get_course_by_id, update_course, get_course_by_user_id, delete_course
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
    delete_user_by_id(session, user.id)
    return {"ok": True}

# ===== Give access to insert datas to teacher only ====
# ===== But don't give accesss to insert fees for teacher ====

# ===== ATTENDANCE ENDPOINTS ===== # teacher, admin 
@app.post("/api/v1/users/attendance/", response_model=AttendanceResponse)
def add_attendance(
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

# get all student attendance
@app.get("/api/v1/users/attendance/", response_model=List[AttendanceResponse])
def get_attendance_by_userid(session: SessionDep, user_id: int):
    """Get all users"""
    return get_attendance_by_user_id(session, user_id)

# ===== Update Attendance endpoints ======
@app.put("/api/v1/attendance/{attendance_id}", response_model=AttendanceResponse)
def update_attendance_endpoints(
    attendance_id: int,
    attendance_data: AttendanceCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Update an assignment (teacher/admin only)"""

    attendance = update_attendance(session, int(attendance_id), attendance_data)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

# ===== delete attendance endpoints =====
@app.delete("/api/v1/attendance/{attendance_id}")
def delete_attendance_by_user_id_endpoints(
    student_id: int, 
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Delete an attendance by id (teacher/admin only)"""

    if not delete_attendance_by_user_id(session, student_id):
        raise HTTPException(status_code=404, detail="Attendance not found")
    return {"message": "Attendance deleted successfully"}


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

# Get all fees records
@app.get("/api/v1/users/fees/", response_model=List[FeesResponse])
def get_fees_endpoints(session: SessionDep):
    """Get all users"""
    return get_all_fees(session)

# get fees by id 
@app.get("/api/v1/fees/", response_model=List[FeesResponse])
def get_fees_by_id_endpoints(session: SessionDep, fees_id: int):
    """Get fees by fees id"""
    return get_fees_by_id(session, fees_id)

# get fees by user id 
@app.get("/api/v1/users/fees/", response_model=List[FeesResponse])
def get_fees_by_user_id_endpoints(session: SessionDep, user_id: int):
    """Get fees by user id"""
    return get_fees_by_user_id(session, user_id)

# ===== Update Fees endpoints ======
@app.put("/api/v1/fees/{student_id}", response_model=FeesResponse)
def update_fees_endpoints(
    student_id: int,
    fees_data: FeesCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Update an fees (teacher/admin only)"""

    fees = update_fees(session, int(student_id), fees_data)
    if not fees:
        raise HTTPException(status_code=404, detail="fees not found")
    return fees

# ===== delete fees endpoints =====
@app.delete("/api/v1/fees/{student_id}")
def delete_fee_by_user_id_endpoints(
    student_id: int,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Delete an attendance by id (teacher/admin only)"""

    if not delete_fees_by_user_id(session, student_id):
        raise HTTPException(status_code=404, detail="fees not found")
    return {"message": "fees deleted successfully"}

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

# Get all marks records
@app.get("/api/v1/users/marks/", response_model=List[MarksResponse])
def get_marks_endpoints(session: SessionDep):
    """Get all marks from users"""
    return get_all_marks(session)

# get marks by id 
@app.get("/api/v1/users/marks/", response_model=List[MarksResponse])
def get_marks_by_id_endpoints(session: SessionDep, marks_id: int):
    """Get marks by marks_id"""
    return get_marks_by_id(session, marks_id)

# get marks by user id 
@app.get("/api/v1/users/marks/", response_model=List[MarksResponse])
def get_marks_by_user_id_endpoints(session: SessionDep, user_id: int):
    """Get marks by user id"""
    return get_marks_by_user_id(session, user_id)

# ===== Update marks endpoints ======
@app.put("/api/v1/marks/{student_id}", response_model=MarksResponse)
def update_marks_endpoints(
    student_id: int,
    marks_data: MarksCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Update an marks (teacher/admin only)"""

    marks = update_marks(session, int(student_id), marks_data)
    if not marks:
        raise HTTPException(status_code=404, detail="marks not found")
    return marks

# ===== delete marks endpoints =====
@app.delete("/api/v1/marks/{student_id}")
def delete_mark_by_user_id_endpoints(
    student_id: int,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Delete an mark by id (teacher/admin only)"""

    if not delete_marks_by_user_id(session, student_id):
        raise HTTPException(status_code=404, detail="marks not found")
    return {"message": "marks deleted successfully"}

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

# Get all course records
@app.get("/api/v1/users/courses/", response_model=List[CourseResponse])
def get_course_endpoints(session: SessionDep):
    """Get all marks from users"""
    return get_all_courses(session)

# get courses by id 
@app.get("/api/v1/users/courses/", response_model=List[CourseResponse])
def get_course_by_id_endpoints(session: SessionDep, course_id: int):
    """Get course by course_id"""
    return get_course_by_id(session, course_id)

# get courses by user id 
@app.get("/api/v1/users/courses/", response_model=List[CourseResponse])
def get_course_by_user_id_endpoints(session: SessionDep, user_id: int):
    """Get courses by user id"""
    return get_course_by_user_id(session, user_id)

# ===== Update course endpoints ======
@app.put("/api/v1/courses/", response_model=CourseResponse)
def update_course_endpoints(
    course_data: CourseCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Update an course (teacher/admin only)"""

    courses = update_course(session, int(user.id), course_data)
    if not courses:
        raise HTTPException(status_code=404, detail="courses not found")
    return courses

# ===== delete course endpoints =====
@app.delete("/api/v1/courses/")
def delete_course_by_user_id_endpoints(
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Delete an course by id (teacher/admin only)"""

    if not delete_course(session, user.id):
        raise HTTPException(status_code=404, detail="course not found")
    return {"message": "course deleted successfully"}


# ===== ASSIGNMENT ENDPOINTS ====== # teacher, admin
@app.post("/api/v1/courses/{course_id}/assignments/", response_model=AssignmentResponse)
def add_assignment_endpoints(
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
        teacher_id=user.id,
    )
    return create_assignment_records(session, assignment)

# ===== Update Assignment endpoints ======
@app.put("/api/v1/assignments/{assignment_id}", response_model=AssignmentResponse)
def update_assignment_endpoints(
    assignment_id: int,
    assignment_data: AssignmentCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Update an assignment (teacher/admin only)"""

    assignment = update_assignment(session, int(assignment_id), assignment_data)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

# ===== delete assignment endpoints =====
@app.delete("/api/v1/assignments/{assignment_id}")
def delete_assignment_by_id_endpoints(
    assignment_id: int,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"])),
):
    """Delete an assignment by id (teacher/admin only)"""

    if not delete_assignment_by_id(session, assignment_id):
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {"message": "Assignment deleted successfully"}

# get all courses recent assignment =====================
@app.get("/api/v1/assignments/recent-per-course", response_model=List[AssignmentResponse])
def get_recent_assignment_per_course_endpoint(
    session: SessionDep,
    user: User = Depends(role_required(["student", "teacher", "admin"])),
):
    """Get the most recent assignment from each course."""
    assignments = get_recent_assignment_per_course(session)
    if not assignments:
        raise HTTPException(status_code=404, detail="No recent assignments found for any course")
    return assignments

# ===== get assignment by id ======
@app.get("/api/v1/assignment/{assignment_id}", response_model=AssignmentResponse)
def get_assignment_by_id_endpoint(assignment_id: int, session: SessionDep):
    assignment = get_assignment_by_id(session, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="assignment not found")
    return assignment

# ===== get assignment by id ======
@app.get("/api/v1/assignment/{assignment_id}", response_model=AssignmentResponse)
def get_assignment_by_course_id_endpoint(course_id: int, session: SessionDep):
    assignment = get_assignment_by_course_id(session, course_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Course Assignment not found")
    return assignment

# ==== Auth Endpoints ==== # teacher, admin, students
# ========================  
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

# ************************************************
# ************************************************
# ===== NOTICE ENDPOINTS ===== # for teacher admin
@app.post("/api/v1/notices/", response_model=NoticeResponse)
def post_notice(
    notice_data: NoticeCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Teachers or admins can post notices"""
    notice = Notice(
        title=notice_data.title,
        content=notice_data.content,
        created_by=user.id,
        target_batch=notice_data.target_batch,
        target_program=notice_data.target_program,
        course_id=notice_data.course_id
    )
    return create_notice_records(session, notice)

# ===== all users can view the notices =======
# ======================================================
@app.get("/api/v1/notices/", response_model=List[NoticeResponse])
def get_notices_endpoint(session: SessionDep):
    """All users can view all notices"""
    return get_all_notices(session)

@app.get("/api/v1/notices/{notice_id}", response_model=NoticeResponse)
def get_notice_by_id_endpoint(notice_id: int, session: SessionDep):
    """Get a specific notice"""
    notice = get_notice_by_id(session, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@app.put("/api/v1/notices/{notice_id}", response_model=NoticeResponse)
def update_notice_endpoint(
    notice_id: int,
    notice_data: NoticeCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Update a notice (only by teacher/admin)"""
    notice = update_notice(session, notice_id, notice_data)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@app.delete("/api/v1/notices/{notice_id}")
def delete_notice_endpoint(
    notice_id: int,
    session: SessionDep,
    user: User = Depends(role_required(["admin"]))
):
    """Delete a notice (admin only)"""
    if not delete_notice(session, notice_id):
        raise HTTPException(status_code=404, detail="Notice not found")
    return {"message": "Notice deleted successfully"}

# ===== chatbot ===== Endpoints ======
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat( 
    message: ChatMessage, session: SessionDep,
    user: User = Depends(role_required(["student", "teacher", "admin"])),
):
    """Main chat handler - process user query"""

    # Validate authenticated user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials token")
    
    user_id = user.user_id
    query = message.query
    
    # Classify the query
    query_type = classify_query(query)
    
    # Route to appropriate handler
    if query_type == QueryType.ATTENDANCE:
        attendance_records = get_attendance_by_user_id(session, user_id)
        formatted_data = format_attendance_data(attendance_records)
        response = get_conversational_response(formatted_data, query)
        
    elif query_type == QueryType.MARKS:
        marks_records = get_marks_by_user_id(session, user_id)
        formatted_data = format_marks_data(marks_records)
        response = get_conversational_response(formatted_data, query)
        
    elif query_type == QueryType.FEES:
        fees_records = get_fees_by_user_id(session, user_id)
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