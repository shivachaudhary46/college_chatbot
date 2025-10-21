# models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pwdlib import PasswordHash
from datetime import datetime

hasher = PasswordHash.recommended()

# =============== User Model ==================
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: str 
    email: str 
    batch: str
    program: str 
    hashed_password: str 
    disabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    attendance_records: List["Attendance"] = Relationship(back_populates="user")
    fees_records: List["Fees"] = Relationship(back_populates="user")
    marks_records: List["Marks"] = Relationship(back_populates="user")

# =============== Attendance Model ==================
class Attendance(SQLModel, table=True):
    """Attendance model for 2080 Batch CSIT students"""
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    
    month: str = Field(default="Ashoj")
    semester: str = Field(default="4th")
    total: int
    attendee_status: str
    created_at: datetime = Field(default=datetime.now())
    
    user: Optional[User] = Relationship(back_populates="attendance_records")

# =============== Fees Model ==================
class Fees(SQLModel, table=True):
    """Fee Payment tracking model for CSIT students"""
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    
    semester: int = Field(default=0)
    total_paid: int = Field(default=0)
    amount_due: int = Field(default=0)
    payment_status: str = Field(default="Pending")
    last_payment_date: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    user: Optional[User] = Relationship(back_populates="fees_records")

    def __init__(self, **data):
        super().__init__(**data)
        self.amount_due = 84000 - self.total_paid
        self.payment_status = "Paid" if self.amount_due == 0 else "Pending"

# =============== Marks Model ==================
class Marks(SQLModel, table=True):
    """Student Marks model for CSIT 2080 Batch"""
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    
    semester: str = Field(default="4th")
    subject: str
    total_marks: int = Field(default=0)
    grade: Optional[str] = None
    status: str = Field(default="Pass")
    exam_date: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    
    user: Optional[User] = Relationship(back_populates="marks_records")

    def __init__(self, **data):
        super().__init__(**data)
        self.status = "Pass" if self.total_marks >= 24 else "Fail"

# =============== Pydantic Schemas ==================
from pydantic import BaseModel

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
    attendance_records: List[Attendance] = []
    fees_records: List[Fees] = []
    marks_records: List[Marks] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str