# ============ Import necessary libraries ==============
from sqlmodel import Session, select
from typing import Optional, List

from .models import User, Attendance, Fees, Marks

# =============== User Operations ==================
def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Fetch user by username"""
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    """Fetch user by ID"""
    return session.get(User, user_id)

def get_all_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Fetch all users"""
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()

def create_user(session: Session, user: User) -> User:
    """Create new user"""
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int) -> bool:
    """Delete user by ID"""
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

# =============== Attendance Operations ==================
def get_user_attendance(session: Session, user_id: int) -> List[Attendance]:
    """Get all attendance records for a user"""
    statement = select(Attendance).where(Attendance.user_id == user_id)
    return session.exec(statement).all()

def create_attendance(session: Session, attendance: Attendance) -> Attendance:
    """Create attendance record"""
    session.add(attendance)
    session.commit()
    session.refresh(attendance)
    return attendance

def get_attendance_by_id(session: Session, attendance_id: int) -> Optional[Attendance]:
    """Get attendance record by ID"""
    return session.get(Attendance, attendance_id)

# =============== Fees Operations ==================
def get_user_fees(session: Session, user_id: int) -> List[Fees]:
    """Get all fee records for a user"""
    statement = select(Fees).where(Fees.user_id == user_id)
    return session.exec(statement).all()

def create_fees(session: Session, fees: Fees) -> Fees:
    """Create fee record"""
    session.add(fees)
    session.commit()
    session.refresh(fees)
    return fees

def update_fees(session: Session, fees_id: int, total_paid: int) -> Optional[Fees]:
    """Update fee payment"""
    fees = session.get(Fees, fees_id)
    if fees:
        fees.total_paid = total_paid
        fees.amount_due = 84000 - total_paid
        fees.payment_status = "Paid" if fees.amount_due == 0 else "Pending"
        session.add(fees)
        session.commit()
        session.refresh(fees)
    return fees

def get_fees_by_id(session: Session, fees_id: int) -> Optional[Fees]:
    """Get fee record by ID"""
    return session.get(Fees, fees_id)

# =============== Marks Operations ==================
def get_user_marks(session: Session, user_id: int) -> List[Marks]:
    """Get all marks records for a user"""
    statement = select(Marks).where(Marks.user_id == user_id)
    return session.exec(statement).all()

def create_marks(session: Session, marks: Marks) -> Marks:
    """Create marks record"""
    session.add(marks)
    session.commit()
    session.refresh(marks)
    return marks

def get_marks_by_id(session: Session, marks_id: int) -> Optional[Marks]:
    """Get marks record by ID"""
    return session.get(Marks, marks_id)

# =============== Combined Data ==================
def get_user_with_all_data(session: Session, user_id: int) -> Optional[dict]:
    """Get user with all related data"""
    user = session.get(User, user_id)
    if not user:
        return None
    
    return {
        "user": user,
        "attendance": user.attendance_records,
        "fees": user.fees_records,
        "marks": user.marks_records
    }

def get_all_users_with_data(session: Session, skip: int = 0, limit: int = 100) -> List[dict]:
    """Get all users with their related data"""
    users = get_all_users(session, skip, limit)
    
    return [
        {
            "user": user,
            "attendance": user.attendance_records,
            "fees": user.fees_records,
            "marks": user.marks_records
        }
        for user in users
    ]