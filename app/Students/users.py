from .schemas import UserCreate, UserResponse, AttendanceCreate, AttendanceResponse, FeesCreate, FeesResponse, MarksResponse, MarksCreate, Token
from .database import SessionDep, create_all_db_tables
from .models import User, Attendance, Fees, Marks
from .crud import get_user_by_username, create_user, create_attendance, create_fees, create_marks, get_all_users, delete_user
from .utilities import hasher 
from .OAuth import authenticate_user, create_access_token, get_current_user

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

# ===== USER ENDPOINTS =====
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
        batch=user_data.batch,
        program=user_data.program,
        hashed_password=hasher.hash(user_data.password)
    )
    return create_user(session, user)

@app.get("/api/v1/users/", response_model=List[UserResponse])
def read_all_users(
    session: SessionDep,
    skip: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    """Get all users"""
    return get_all_users(session, skip, limit)

@app.get("/api/v1/users/{username}", response_model=UserResponse)
def read_user(username: str, session: SessionDep):
    """Get a specific user by username"""
    user = get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/api/v1/users/{username}")
def delete_user_by_username(username: str, session: SessionDep):
    """Delete a user"""
    user = get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(session, user.id)
    return {"ok": True}

# ===== ATTENDANCE ENDPOINTS =====
@app.post("/api/v1/users/{user_id}/attendance/", response_model=AttendanceResponse)
def add_user_attendance(
    user_id: str,
    attendance_data: AttendanceCreate,
    session: SessionDep
):
    """Add attendance record for a user"""
    user = get_user_by_username(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    attendance = Attendance(
        user_id=user_id,
        month=attendance_data.month,
        semester=attendance_data.semester,
        total=attendance_data.total,
        attendee_status=attendance_data.attendee_status
    )
    return create_attendance(session, attendance)

# ===== FEES ENDPOINTS =======
@app.post("/api/v1/users/{user_id}/fee/", response_model=FeesResponse)
def add_user_fee(
    user_id: str, 
    fee_data: FeesCreate,
    session: SessionDep
):
    """Add fees record for a user"""
    user = get_user_by_username(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    fees = Fees(
        user_id=user_id, 
        semester=fee_data.semester,
        total_paid=fee_data.total_paid,
        last_payment_date=fee_data.last_payment_date
    )

    return create_fees(session, fees)

# ===== MARKS ENDPOINTS ======
@app.post("/api/v1/users/{user_id}/marks/", response_model=MarksResponse)
def add_marks_record(
    user_id: str,
    marks_data: MarksCreate,
    session: SessionDep
):
    """Add marks record for a user"""
    user = get_user_by_username(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    marks = Marks(
            user_id=user_id,
            semester=marks_data.semester,
            subject=marks_data.subject,
            total_marks=marks_data.total_marks,
            grade=marks_data.grade,
            exam_date=marks_data.exam_date
    )
    return create_marks(session, marks)

# ==== Auth Endpoints ====
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