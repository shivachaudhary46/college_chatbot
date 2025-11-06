# ===== Import necessary libraries =====
from sqlmodel import Session, select, desc
from typing import Optional, List
from datetime import datetime

from .schemas import NoticeCreate, FeesCreate, MarksCreate, CourseCreate, AssignmentCreate, AttendanceCreate
from .models import User, Attendance, Fees, Marks, Assignment, Course, Notice

# ====== User Operations =======
# ==============================
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

def delete_user_by_id(session: Session, user_id: int) -> bool:
    """Delete user by ID"""
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

# ===== Attendance Operations =====
# =================================
def create_attendance(session: Session, attendance: Attendance) -> Attendance:
    """Create new attendance"""
    session.add(attendance)
    session.commit() 
    session.refresh(attendance)
    return attendance

# ===== update attendance =====
def update_attendance(session: Session, attendance_id: int, data: AttendanceCreate) -> Optional[Attendance]:
    """Update a attendance"""
    attendance = session.get(attendance, attendance_id)
    if not attendance:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(attendance, field, value)
    attendance.updated_at = datetime.now()

    session.add(attendance)
    session.commit()
    session.refresh(attendance)
    return attendance

# ===== get all attendance ======
def get_all_attendances(session: Session) -> List[Attendance]:
    """Get all attendances"""
    statement = select(Attendance)
    return session.exec(statement).all()

# ===== get attendance by user id =====
def get_attendance_by_user_id(session: Session, user_id: int) -> Optional[Attendance]:
    """Fetch attendance by user id"""
    statement = select(Attendance).where(Attendance.user_id == user_id)
    return session.exec(statement).all()

# ===== get attendance by id =====
def get_attendance_by_id(session: Session, attendance_id: int) -> Optional[Attendance]:
    """Fetch a single attendance record by its ID."""
    return session.get(Attendance, attendance_id)

# ===== delete attendance by id =====
def delete_attendance_by_id(session: Session, attendance_id: int) -> bool:
    """Delete an attendance record by ID."""
    attendance_record = session.get(Attendance, attendance_id)
    if not attendance_record:
        return False
    session.delete(attendance_record)
    session.commit()
    return True

# ===== delete attendance by user_id ====
def delete_attendance_by_user_id(session: Session, user_id: int) -> int:
    """Delete all attendance records for a specific user and return number of deleted rows."""
    statement = select(Attendance).where(Attendance.user_id == user_id)
    records = session.exec(statement).all()

    if not records:
        return False

    for record in records:
        session.delete(record)
    session.commit()
    return True

# ===== Fees Operations =====
# ===========================
def create_fees(session: Session, fees: Fees) -> Fees:
    """Create fee record"""
    session.add(fees)
    session.commit()
    session.refresh(fees)
    return fees

def update_fees(session: Session, fees_id: int, data: FeesCreate) -> Optional[Fees]:
    """Update a fee record"""
    fees_record = session.get(Fees, fees_id)
    if not fees_record:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(fees_record, field, value)
    fees_record.updated_at = datetime.now()

    session.add(fees_record)
    session.commit()
    session.refresh(fees_record)
    return fees_record

def get_all_fees(session: Session) -> List[Fees]:
    """Get all fee records"""
    statement = select(Fees)
    return session.exec(statement).all()

def get_fees_by_id(session: Session, fees_id: int) -> Optional[Fees]:
    """Fetch fee record by ID"""
    return session.get(Fees, fees_id)

def get_fees_by_user_id(session: Session, user_id: int) -> Optional[Fees]:
    """Fetch attendance by user id"""
    statement = select(Fees).where(Fees.user_id == user_id)
    return session.exec(statement).first()

def delete_fees_by_id(session: Session, fees_id: int) -> bool:
    """Delete fee record by ID"""
    record = session.get(Fees, fees_id)
    if not record:
        return False
    session.delete(record)
    session.commit()
    return True


def delete_fees_by_user_id(session: Session, user_id: int) -> int:
    """Delete all fee records for a user"""
    statement = select(Fees).where(Fees.user_id == user_id)
    records = session.exec(statement).all()
    if not records:
        return False
    
    for r in records:
        session.delete(r)
    session.commit()
    return True


# ===== Marks Operations =====
def create_marks(session: Session, marks: Marks) -> Marks:
    """Create marks record"""
    session.add(marks)
    session.commit()
    session.refresh(marks)
    return marks

def update_marks(session: Session, marks_id: int, data: MarksCreate) -> Optional[Marks]:
    """Update marks record"""
    record = session.get(Marks, marks_id)
    if not record:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)
    record.updated_at = datetime.now()

    session.add(record)
    session.commit()
    session.refresh(record)
    return record

def get_all_marks(session: Session) -> List[Marks]:
    """Get all marks"""
    statement = select(Marks)
    return session.exec(statement).all()

def get_marks_by_id(session: Session, marks_id: int) -> Optional[Marks]:
    """Fetch marks by ID"""
    return session.get(Marks, marks_id)

def get_marks_by_user_id(session: Session, user_id: int) -> List[Marks]:
    """Fetch all marks for a user"""
    statement = select(Marks).where(Marks.user_id == user_id)
    return session.exec(statement).all()

def delete_marks_by_id(session: Session, marks_id: int) -> bool:
    """Delete marks record by ID"""
    record = session.get(Marks, marks_id)
    if not record:
        return False
    session.delete(record)
    session.commit()
    return True

def delete_marks_by_user_id(session: Session, user_id: int) -> int:
    """Delete all marks for a user"""
    statement = select(Marks).where(Marks.user_id == user_id)
    records = session.exec(statement).all()
    if not records:
        return 0
    for r in records:
        session.delete(r)
    session.commit()
    return len(records)

# ===== Course Operations =====
def create_course_records(session: Session, course: Course) -> Course:
    """Create a new course record"""
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

def update_course(session: Session, course_id: int, data: CourseCreate) -> Optional[Course]:
    """Update course record"""
    record = session.get(Course, course_id)
    if not record:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)
    record.updated_at = datetime.now()

    session.add(record)
    session.commit()
    session.refresh(record)
    return record

def get_all_courses(session: Session) -> List[Course]:
    """Get all courses"""
    statement = select(Course)
    return session.exec(statement).all()

def get_course_by_id(session: Session, course_id: int) -> Optional[Course]:
    """Fetch course by ID"""
    return session.get(Course, course_id)

def delete_course_by_id(session: Session, course_id: int) -> bool:
    """Delete course by ID"""
    record = session.get(Course, course_id)
    if not record:
        return False
    session.delete(record)
    session.commit()
    return True


# ==== create assignments records
# ===== Assignment Operations =====
def create_assignment_records(session: Session, assignment: Assignment) -> Assignment:
    """Create assignment record"""
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment


def update_assignment(session: Session, assignment_id: int, data: AssignmentCreate) -> Optional[Assignment]:
    """Update assignment"""
    record = session.get(Assignment, assignment_id)
    if not record:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)
    record.updated_at = datetime.now()

    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def get_all_assignments(session: Session) -> List[Assignment]:
    """Get all assignments"""
    statement = select(Assignment)
    return session.exec(statement).all()


def get_assignment_by_id(session: Session, assignment_id: int) -> Optional[Assignment]:
    """Fetch assignment by ID"""
    return session.get(Assignment, assignment_id)

def get_recent_assignment_per_course(session: Session) -> List[Assignment]:

    # step 1: Get all distinct course_ids
    course_ids = session.exec(select(Course.id)).all()
    recent_assignments = []

    # step 2: for each course, fetch its most recent assignment 
    for course_id in course_ids:
        statement = (
            select(Assignment)
            .where(Assignment.course_id == course_id)
            .order_by(desc(Assignment.created_at))
            .limit(1)
        )

    latest_assignment = session.exec(statement).first()
    if latest_assignment:
        recent_assignments.append(latest_assignment)

    # Step 3: Optionally sort the final list by created_at (newest first)
    recent_assignments.sort(key=lambda a: a.created_at, reverse=True)
    return recent_assignments


def get_assignment_by_course_id(session: Session, course_id: int) -> List[Assignment]:
    """Fetch assignments for a specific course"""
    statement = select(Assignment).where(Assignment.course_id == course_id)
    return session.exec(statement).all()


def delete_assignment_by_id(session: Session, assignment_id: int) -> bool:
    """Delete assignment by ID"""
    record = session.get(Assignment, assignment_id)
    if not record:
        return False
    session.delete(record)
    session.commit()
    return True

# ====== Notice Operations ======
# ===============================

def create_notice_records(session: Session, notices: Notice) -> Notice:
    """Create course record"""
    session.add(notices) 
    session.commit()
    session.refresh(notices)
    return notices

def get_all_notices(session: Session) -> List[Notice]:
    """Get all notices"""
    statement = select(Notice).order_by(Notice.created_at.desc())
    return session.exec(statement).all()

def get_notice_by_id(session: Session, notice_id: int) -> Optional[Notice]:
    """Get a specific notice"""
    statement = select(Notice).where(Notice.id == notice_id)
    return session.exec(statement).first()

def update_notice(session: Session, notice_id: int, data: NoticeCreate) -> Optional[Notice]:
    """Update a notice"""
    notice = session.get(Notice, notice_id)
    if not notice:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(notice, field, value)
    notice.updated_at = datetime.now()

    session.add(notice)
    session.commit()
    session.refresh(notice)
    return notice

def delete_notice(session: Session, notice_id: int) -> bool:
    """Delete a notice"""
    notice = session.get(Notice, notice_id)
    if not notice:
        return False

    session.delete(notice)
    session.commit()
    return True