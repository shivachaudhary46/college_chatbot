# models.py
"""
SQLModel database models - NO IMPORTS FROM OTHER APP MODULES
Only external dependencies here
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pwdlib import PasswordHash
from datetime import datetime
from enum import Enum

hasher = PasswordHash.recommended()

# ===== Role Model =====
class Role(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

# ====== User Model ======
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: str 
    email: str 
    batch: str
    program: str
    role: Role = Field(default=Role.student)
    hashed_password: str 
    disabled: bool = Field(default=False) 
    created_at: datetime = Field(default_factory=datetime.now)

    # for users/students only 
    attendance_records: List["Attendance"] = Relationship(back_populates="user", sa_relationship_kwargs={"foreign_keys": "[Attendance.user_id]"})
    fees_records: List["Fees"] = Relationship(back_populates="user")
    marks_records: List["Marks"] = Relationship(back_populates="user")
    courses: List["UserCourseLink"] = Relationship(back_populates="user") 

    # for teachers/admins 
    created_notices: List["Notice"] = Relationship(back_populates="user")
    assignments: List["Assignment"] = Relationship(back_populates="user")
    taught_courses: List["Course"] = Relationship(back_populates="teacher")

class Notice(SQLModel, table=True):
    """Notice board model for students, teachers, and admins."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_by: int = Field(foreign_key="user.id", index=True)
    
    target_batch: Optional[str] = None      # e.g., "2080"
    target_program: Optional[str] = None    # e.g., "BSc CSIT"
    course_id: Optional[int] = Field(default=None, foreign_key="course.id")
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    user: Optional["User"] = Relationship(back_populates="created_notices")      
    course: Optional["Course"] = Relationship(back_populates="notices")     

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str 
    code: str
    teacher_id: Optional[int] = Field(default=None, foreign_key="user.id") 
    
    # relationship 
    students: List["UserCourseLink"] = Relationship(back_populates="course")
    assignments: List["Assignment"] = Relationship(back_populates="course")
    teacher: Optional["User"] = Relationship(back_populates="taught_courses")
    notices: List["Notice"] = Relationship(back_populates="course")

class Assignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str 
    due_date: datetime

    course_id: Optional[int] = Field(default=None, foreign_key="course.id")
    teacher_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)

    #relationships 
    user: Optional["User"] = Relationship(back_populates="assignments")
    course: Optional["Course"] = Relationship(back_populates="assignments")

class UserCourseLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    course_id: Optional[int] = Field(default=None, foreign_key="course.id", primary_key=True)

    course: Optional["Course"] = Relationship(back_populates="students")
    user: Optional["User"] = Relationship(back_populates="courses")
    
# ====== Attendance Model ======
class Attendance(SQLModel, table=True):
    """Attendance model for 2080 Batch CSIT students"""
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    
    month: str = Field(default="Ashoj")
    semester: str = Field(default="4th")
    total: int
    attendee_status: str
    marked_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    
    user: Optional["User"] = Relationship(
        back_populates="attendance_records",
        sa_relationship_kwargs={"foreign_keys": "[Attendance.user_id]"}
    )

# ====== Fees Model ========
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
        total_fees = 84000
        self.amount_due = max(total_fees - self.total_paid, 0)
        self.payment_status = "Paid" if self.amount_due == 0 else "Pending"
        # Auto-set last payment time when record is created
        self.last_payment_date = self.created_at

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


