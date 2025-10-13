from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

# ============= Usermodel ================
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(index=True, unique=True)
    full_name: str 
    email: EmailStr = Field(unique=True)
    batch: Optional[str] = Field(default="2080")
    program: Optional[str] = Field(default="CSIT")

    attendance_records: List["Attendance"] = Relationship(back_populates="user")
    fees_records: List["Fees"] = Relationship(back_populates="user")
    marks_records: List["Marks"] = Relationship(back_populates="user")
 
# ============= Attendance Information Table =============
class Attendance(SQLModel, table=True):
    """
    Attendance model for 2080 Batch Ashoj Month CSIT 4th semester
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")

    month: str = Field(default="Ashoj")
    semester: str = Field(default="4th")
    
    total: int
    attendee_status: str

    # add relationship 
    user: Optional[User] = Relationship(back_populates="attendance_records")

# ============== Fee Payment table ====================
class Fees(SQLModel, table=True):
    """
    Fee Payment tracking model for 2080 Batch CSIT students
    Maps username to semester-wise fee payment records
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    
    # 8 semesters fee payment
    semester: int = Field(default=0)
    
    # Financial summary
    total_paid: int = Field(default=0)
    amount_due: int = Field(default=0)
    payment_status: str = Field(default="Pending")
    
    # Metadata
    last_payment_date: datetime = Field(default=None)
    
    user: Optional[User] = Relationship(back_populates="fees_records")

    def __init__(self, **data):
        super().__init__(**data)
        self.amount_due = 84000 - self.total_paid

        if self.amount_due == 0:
            self.payment_status = "Paid"
        else:
            self.payment_status = "Pending"

# =================== Results table =================
class Marks(SQLModel, table=True):
    """
    Student Marks model for 4th Semester CSIT 2080 Batch
    Tracks theory, practical, and total marks for 5 subjects
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    semester: str = Field(default="4th")

    # details 
    subject: str
    
    # Summary
    total_marks: int = Field(default=0)
    grade: Optional[str] = None
    status: str = Field(default="Pass")
    exam_date: datetime

    user: Optional[User] = Relationship(back_populates="marks_records")

    def __init__(self, **data):
        super().__init__(**data)

        if self.total_marks >= 24:
            self.status = "Pass"
        else:
            self.status = "Fail"

# ============= Notices Table =================
class Notice(SQLModel, table=True):
    """
    Notice and Announcement model for Tribhuvan University
    Stores all official notices and announcements from the college
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    notice_type: str  # e.g., "Exam", "Academic", "Event", "Holiday", "General"
    category: str  # e.g., "CSIT", "BBS", "BA", "All"
    batch: str
    semester: str

    # Dates
    issued_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Status
    is_active: bool = Field(default=True)
    is_urgent: bool = Field(default=True)
    
    # Additional info
    issued_by: str = Field(default="MBMC Admin")
    attachments_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
