# =============  Models for login backend ===========================================================
# ============= *************************  ============================================================
'''
This is the production level backend
'''

# ============== Login backend imports =============
from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, Optional, List
from pydantic import EmailStr, BaseModel

from pwdlib import PasswordHash

from datetime import datetime

hasher = PasswordHash.recommended()

# =============== Usermodel table ==================
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(index=True, unique=True)
    full_name: str 
    email: str 

    batch: str
    program: str 

    hashed_password: str 
    disabled: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now())

    attendance_records: List["Attendance"] = Relationship(back_populates="user")
    fees_records: List["Fees"] = Relationship(back_populates="user")
    marks_records: List["Marks"] = Relationship(back_populates="user")
    
# ================ User Info =======================
class Info(SQLModel):
    username: str | None = Field(index=True, unique=True)

    full_name: str 
    email: str 
    batch: str
    program: str 

    hashed_password: str 
    disabled: bool = Field(default=False)

    def set_password(self, plain_password: str):
        self.hashed_password = hasher.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return hasher.verify(plain_password, hashed_password) 

# ======= JWT token info ================== 
class Token(BaseModel):
    access_token: str
    token_type: str

# ====== Token Data ======================
class Token_Data(BaseModel):
    username: str

# ====== for storing Hashed Password ===================
class UserInDB(User):
    hashed_password: str

# ====== username from database ===================
def get_user(db, username: str):
    if username in db:
        user = db[username]
        return UserInDB(**user)
    
# =========== verifying hashed password ===================
def verify_password(password, hashed_password):
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hashed_password) # if match return True, If not then False
    
# =========== Authenticate username =====================
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

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
    created_at: datetime = Field(default=datetime.now())

    # add relationship 
    user: Optional[User] = Relationship(back_populates="attendance_records")

# # ============== Fee Payment table ====================
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
    created_at: datetime = Field(default=datetime.now())
    
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

# # =================== Results table =================
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

# ======== Pydantic models for API ========
class UserCreate(BaseModel):
    # schema for creating a user
    username: str
    full_name: str
    email: str
    batch: str
    program: str
    password: str

class UserResponse(BaseModel):
    # schema for user response with relationships
    id: int
    username: str
    full_name: str
    email: str
    batch: str
    program: str

    created_at: datetime
    attendance_records: List["Attendance"] = []
    fees_records: List["Fees"] = []
    marks_records: List["Marks"] = []

class UserWithAllData(BaseModel):
    """Complete user data with all relationships"""
    user: UserResponse
    attendance: List["Attendance"]
    fees: List["Fees"]
    marks: List["Marks"]

from sqlmodel import select 
from database import SessionDep

def get_user_by_username(session: SessionDep, username: str) -> Optional[UserResponse]:
    statement = select(UserResponse).where(UserResponse.username == username)
    return session.exec(statement).first()

def get_all_users_with_data (session: SessionDep, skip: int = 0, limit: int = 100) -> List[dict]:
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all() 

    result = [
        {
            "user": user, 
            "attendance": user.attendance_records,
            "fees": user.fees_records,
            "marks": user.marks_records
        }
        for user in users
    ]

def get_user_attendance(session: SessionDep, user_id: int) -> List[Attendance]:
    statement = select(Attendance).where(Attendance.user_id == user_id)
    return statement.exec(statement).all() 

def get_user_fees(session: SessionDep, user_id: int) -> List[Fees]:
    statement = select(Fees).where(Fees.user_id == user_id)
    return session.exec(statement).all()

def get_user_marks(session: SessionDep, user_id: int) -> List[Marks]:
    statement = select(Marks).where(Marks.user_id == user_id)
    return session.exec(statement).all() 
