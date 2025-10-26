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
    hashed_password:   str 
    disabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    attendance_records: List["Attendance"] = Relationship(back_populates="user")

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
