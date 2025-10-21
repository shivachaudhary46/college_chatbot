# routes.py
"""
Student management routes - Import into main.py
"""
from fastapi import HTTPException, Depends, Query, FastAPI 
from typing import Annotated, List
from datetime import timedelta
import os
from dotenv import load_dotenv

from database import SessionDep
from models import User, Attendance, Fees, Marks
from schemas import (
    UserCreate, UserResponse, AttendanceCreate, AttendanceResponse,
    FeesCreate, FeesResponse, MarksCreate, MarksResponse,
    Token, UserDataResponse
)
from crud import (
    get_user_by_username, get_user_by_id, get_all_users, create_user, delete_user,
    get_user_attendance, create_attendance,
    get_user_fees, create_fees, update_fees,
    get_user_marks, create_marks,
    get_user_with_all_data
)
from utilities import authenticate_user, create_access_token, get_current_user
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm

from chatbot import setup_chatbot_routes

load_dotenv()
ACCESS_TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE", 60))

hasher = PasswordHash.recommended()

# =============== USER ENDPOINTS ==================
def setup_user_routes(app):
    """Setup user management routes"""

    app = FastAPI()
        
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

# =============== ATTENDANCE ENDPOINTS ==================
def setup_attendance_routes(app):
    """Setup attendance routes"""
    @app.post("/api/v1/users/{user_id}/attendance/", response_model=AttendanceResponse)
    def add_attendance(
        user_id: int,
        attendance_data: AttendanceCreate,
        session: SessionDep
    ):
        """Add attendance record for a user"""
        user = get_user_by_id(session, user_id)
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

    @app.get("/api/v1/users/{user_id}/attendance/", response_model=List[AttendanceResponse])
    def get_attendance(user_id: int, session: SessionDep):
        """Get all attendance records for a user"""
        user = get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return get_user_attendance(session, user_id)  
    

# =============== FEES ENDPOINTS ==================
def setup_fees_routes(app):
    """Setup fees routes"""
    @app.post("/api/v1/users/{user_id}/fees/", response_model=FeesResponse)
    def add_fee(
        user_id: int,
        fees_data: FeesCreate,
        session: SessionDep
    ):
        """Add fee record for a user"""
        user = get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        fees = Fees(
            user_id=user_id,
            semester=fees_data.semester,
            total_paid=fees_data.total_paid,
            last_payment_date=fees_data.last_payment_date
        )
        return create_fees(session, fees)

    @app.get("/api/v1/users/{user_id}/fees/", response_model=List[FeesResponse])
    def get_fees(user_id: int, session: SessionDep):
        """Get all fee records for a user"""
        user = get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return get_user_fees(session, user_id)

    @app.put("/api/v1/fees/{fees_id}", response_model=FeesResponse)
    def update_fee_payment(
        fees_id: int,
        fees_data: FeesCreate,
        session: SessionDep
    ):
        """Update fee payment amount"""
        updated = update_fees(session, fees_id, fees_data.total_paid)
        if not updated:
            raise HTTPException(status_code=404, detail="Fee record not found")
        return updated   

# =============== MARKS ENDPOINTS ==================
def setup_marks_routes(app):
    """Setup marks routes"""
    
    @app.post("/api/v1/users/{user_id}/marks/", response_model=MarksResponse)
    def add_marks_record(
        user_id: int,
        marks_data: MarksCreate,
        session: SessionDep
    ):
        """Add marks record for a user"""
        user = get_user_by_id(session, user_id)
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

    @app.get("/api/v1/users/{user_id}/marks/", response_model=List[MarksResponse])
    def get_marks(user_id: int, session: SessionDep):
        """Get all marks records for a user"""
        user = get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return get_user_marks(session, user_id)

# =============== COMBINED DATA ENDPOINTS ==================
def setup_dashboard_routes(app):
    """Setup dashboard and combined data routes"""
    
    @app.get("/api/v1/users/{user_id}/all-data/", response_model=UserDataResponse)
    def get_all_user_data(user_id: int, session: SessionDep):
        """Get all user data including attendance, fees, and marks"""
        data = get_user_with_all_data(session, user_id)
        if not data:
            raise HTTPException(status_code=404, detail="User not found")
            
        return {
                "id": data["user"].id,
                "username": data["user"].username,
                "full_name": data["user"].full_name,
                "email": data["user"].email,
                "batch": data["user"].batch,
                "program": data["user"].program,
                "attendance": data["attendance"],
                "fees": data["fees"],
                "marks": data["marks"]
            }

    @app.get("/api/v1/dashboard/", response_model=UserDataResponse)
    def get_dashboard(
        current_user: Annotated[User, Depends(get_current_user)],
        session: SessionDep
    ):
        """Get dashboard data for current logged-in user"""
        data = get_user_with_all_data(session, current_user.id)
        if not data:
            raise HTTPException(status_code=404, detail="User data not found")
            
        return {
                "id": data["user"].id,
                "username": data["user"].username,
                "full_name": data["user"].full_name,
                "email": data["user"].email,
                "batch": data["user"].batch,
                "program": data["user"].program,
                "attendance": data["attendance"],
                "fees": data["fees"],
                "marks": data["marks"]
        }

# =============== AUTH ENDPOINTS ==================
def setup_auth_routes(app):
    """Setup authentication routes"""
    
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

# # =============== Main Setup Function ==================
def setup_all_routes(app):
    """Setup all routes at once"""
    setup_user_routes(app)
    setup_attendance_routes(app)
    setup_fees_routes(app)
    setup_marks_routes(app)
    setup_dashboard_routes(app)
    setup_auth_routes(app)