# ===== Import necessary libraries =====
from sqlmodel import Session, select
from typing import Optional, List

from .models import User, Attendance, Fees, Marks

# ====== User Operations =====
def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Fetch user by username"""
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def create_user(session: Session, user: User) -> User:
    """Create new user"""
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_all_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Fetch all users"""
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()

def delete_user(session: Session, user_id: int) -> bool:
    """Delete user by ID"""
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

# ===== Attendance Operations =====
def create_attendance(session: Session, attendance: Attendance) -> Attendance:
    """Create new attendance"""
    session.add(attendance)
    session.commit() 
    session.refresh(attendance)
    return attendance

# ===== Fees Operations =====
def create_fees(session: Session, fees: Fees) -> Fees:
    """Create fee record"""
    session.add(fees)
    session.commit()
    session.refresh(fees)
    return fees

# ==== Marks Operations =====
def create_marks(session: Session, marks: Marks) -> Marks: 
    """Create marks record"""
    session.add(marks)
    session.commit()
    session.refresh(marks)
    return marks 