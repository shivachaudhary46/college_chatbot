# schemas.py
"""
Pydantic request/response schemas with proper datetime handling
"""
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List

# =============== User Schemas ==================
class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str
    batch: str
    program: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    batch: str
    program: str
    created_at: datetime

    class Config:
        from_attributes = True

# =============== Attendance Schemas ==================
class AttendanceCreate(BaseModel):
    month: str
    semester: str
    total: int
    attendee_status: str
    
    @field_validator('total')
    @classmethod
    def validate_total(cls, v):
        if not 0 <= v <= 24: # why 24 ? because our class only runs 24 days in one month. 
            raise ValueError('Total attendance must be between 0 and 24')
        return v

class AttendanceResponse(BaseModel):
    id: int
    user_id: int
    month: str
    semester: str
    total: int
    attendee_status: str
    created_at: datetime

    class Config:
        from_attributes = True

# =============== Fees Schemas ==================
class FeesCreate(BaseModel):
    semester: int
    total_paid: int = 0
    last_payment_date: Optional[datetime] = None
    
    @field_validator('semester')
    @classmethod
    def validate_semester(cls, v):
        if not 1 <= v <= 8:
            raise ValueError('Semester must be between 1 and 8')
        return v
    
    @field_validator('total_paid')
    @classmethod
    def validate_total_paid(cls, v):
        if v < 0:
            raise ValueError('Total paid cannot be negative')
        return v

class FeesResponse(BaseModel):
    id: int
    user_id: int
    semester: int
    total_paid: int
    amount_due: int
    payment_status: str
    last_payment_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# =============== Marks Schemas ==================
class MarksCreate(BaseModel):
    semester: str
    subject: str
    total_marks: int
    grade: Optional[str] = None
    exam_date: datetime
    
    @field_validator('total_marks')
    @classmethod
    def validate_marks(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Marks must be between 0 and 100')
        return v
    
    @field_validator('exam_date')
    @classmethod
    def validate_exam_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Invalid datetime format. Use ISO format: 2025-10-19T08:09:49Z')
        return v

class MarksResponse(BaseModel):
    id: int
    user_id: int
    semester: str
    subject: str
    total_marks: int
    grade: Optional[str] = None
    status: str
    exam_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# =============== Auth Schemas ==================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

# =============== Combined Response Schemas ==================
class UserDataResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    batch: str
    program: str
    attendance: List[AttendanceResponse] = []
    fees: List[FeesResponse] = []
    marks: List[MarksResponse] = []

    class Config:
        from_attributes = True