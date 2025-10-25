# ===== Import necessary libraries =====
from sqlmodel import Session, select
from typing import Optional, List

from .models import User

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
