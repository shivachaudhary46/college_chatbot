from enum import Enum
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class QueryType(str, Enum):
    ATTENDANCE = "attendance"
    MARKS = "marks"
    FEES = "fees"
    COLLEGE_INFO = "college_info"
    GENERAL = "general"

class ChatMessage(BaseModel):
    username: str
    query: str

class ChatResponse(BaseModel):
    response: str
    query_type: QueryType

def classify_query(query: str) -> QueryType: 
    """classify the user query into appropriate categories"""
    query_lower = query.lower()

    attendance_keywords = ["attendance", "present", "absent", "class", "lectures", "session"]
    marks_keywords = ["marks", "score", "result", "grade", "exam", "test", "performance"]
    fees_keywords = ["fees", "payment", "tuition", "dues", "billing", "amount due"]
    college_keywords = ["college", "course", "program", "announcement", "admission", "faculty", "campus"]

    if any(keyword in query_lower for keyword in attendance_keywords):
        return QueryType.ATTENDANCE
    elif any(keyword in query_lower for keyword in marks_keywords):
        return QueryType.MARKS
    elif any(keyword in query_lower for keyword in fees_keywords):
        return QueryType.FEES
    elif any(keyword in query_lower for keyword in college_keywords):
        return QueryType.COLLEGE_INFO
    else: 
        return QueryType.GENERAL
    
# ============ Data Formatters ==================
def format_attendance_data(attendance_records: list) -> str:

    if not attendance_records: 
        return "No attendance records found."
    
    formatted = "Your Attendance Records: \n"
    for record in attendance_records: 
        formatted += f"- {record.month}: {record.total}%  - ({record.semester}) - {record.attendee_status}"
    return formatted

def format_fees_data(fees_record: list) -> str:

    if not fees_record:
        return "No fee records found"
    
    formatted = "Your Fee Payment Records: \n"
    for record in fees_record:
        formatted += f"- Semester {record.semester}: Rs. {record.total_paid} paid, Rs. {record.amount} due - {record.payment_status}\n"
    return formatted

def format_marks_data(marks_records: list) -> str:
    """Format marks records into readable text"""
    if not marks_records:
        return "No marks records found."
    
    formatted = "Your Marks:\n"
    for record in marks_records:
        formatted += f"- {record.subject} ({record.semester}): {record.total_marks}/100 - Grade: {record.grade} ({record.status})\n"
    return formatted

