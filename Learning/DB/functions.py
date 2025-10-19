# =========================================================
# =========================================================
# ============= Database ==================================
from sqlmodel import Session, select
from typing import TYPE_CHECKING
from datetime import datetime


from models import User, Attendance, Fees, Marks
from database import engine

# ========= function to add user to database ==========
def add_user(username: str, full_name: str, email: str, batch: str | None = None, program: str | None = None):
    with Session(engine) as session:
        user = User(
            username=username,
            full_name=full_name,
            email=email,
            batch=batch,
            program=program
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
# ========= function to add attendance to database =======
def add_attendance(user_id: int, month: str, semester: str, total: int, status: str):
    with Session(engine) as session:
        attendee = Attendance(
            user_id=user_id,
            month=month,
            semester=semester,
            total=total,
            attendee_status=status
        )

        session.add(attendee)
        session.commit()
        session.refresh(attendee)
        return attendee

# ========= function to add fees to database =======
def add_fees(user_id: int, semester: int, total_paid: int, last_payment_date: datetime):
    with Session(engine) as session: 
        fee = Fees(
            user_id=user_id,
            semester=semester,
            total_paid=total_paid,
            last_payment_date=last_payment_date
        )
        session.add(fee)
        session.commit()
        session.refresh(fee)
        return fee
    
# ========= function to add marks to database =======
def add_marks(user_id: int, semester: str, subject: str, total_marks: int, grade: str, exam_date: datetime):
    with Session(engine) as session: 
        subject_mark = Marks(
            user_id= user_id,
            semester= semester,
            subject= subject,
            total_marks= total_marks, 
            grade=grade,
            exam_date=exam_date
        )

        session.add(subject_mark)
        session.commit()
        session.refresh(subject_mark)
        return subject_mark
    
# ====== To check the all data is added ? =======
def get_user_with_all_data(user_id: int):
    """Get user with all related data"""
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        
        if user:
            # Access relationships
            print(f"User: {user.username}")
            print(f"Attendance Records: {user.attendance_records}")
            print(f"Fees Records: {user.fees_records}")
            print(f"Marks Records: {user.marks_records}")
            return user
        return None
    
