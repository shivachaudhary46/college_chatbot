# chatbot.py
"""
A chatbot module that integrates with main FastAPI app
"""
import os
from enum import Enum
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from typing import Annotated
from dotenv import load_dotenv, find_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun

from database import SessionDep
from crud import get_user_by_username, get_user_attendance, get_user_fees, get_user_marks

load_dotenv(find_dotenv(), override=True)

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

# =============== Query Classification ==================
def classify_query(query: str) -> QueryType:
    """Classify the user query into appropriate categories"""
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

# =============== Data Formatters ==================
def format_attendance_data(attendance_records: list) -> str:
    """Format attendance records into readable text"""
    if not attendance_records:
        return "No attendance records found."
    
    formatted = "Your Attendance Records:\n"
    for record in attendance_records:
        formatted += f"- {record.month} ({record.semester}): {record.total}% - {record.attendee_status}\n"
    return formatted

def format_fees_data(fees_records: list) -> str:
    """Format fees records into readable text"""
    if not fees_records:
        return "No fee records found."
    
    formatted = "Your Fee Payment Records:\n"
    for record in fees_records:
        formatted += f"- Semester {record.semester}: Rs. {record.total_paid} paid, Rs. {record.amount_due} due - {record.payment_status}\n"
    return formatted

def format_marks_data(marks_records: list) -> str:
    """Format marks records into readable text"""
    if not marks_records:
        return "No marks records found."
    
    formatted = "Your Marks:\n"
    for record in marks_records:
        formatted += f"- {record.subject} ({record.semester}): {record.total_marks}/100 - Grade: {record.grade} ({record.status})\n"
    return formatted

# =============== LLM Response Generators ==================
def get_conversational_response(user_data: str, query: str) -> str:
    """Generate a natural, friendly response using LLM"""
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    
    template = """You are a friendly and helpful college student assistant chatbot.
Your tone should be warm, professional, and encouraging - like a helpful friend.
Keep responses concise and natural.

User Query: {query}

Student Information:
{user_data}

Please provide a helpful response based on the student's information. 
Be warm, supportive, and conversational."""

    prompt = PromptTemplate(
        input_variables=["query", "user_data"],
        template=template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"query": query, "user_data": user_data})
    
    return response.strip()

def get_college_info_response(query: str) -> str:
    """Get college information using web search"""
    
    try:
        search = DuckDuckGoSearchRun()
        search_results = search.run(f"MBMC college {query}")
    except Exception as e:
        search_results = f"Unable to fetch results: {str(e)}"
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
    
    template = """You are a helpful college assistant providing information.
You are friendly, professional, and always helpful.

Query: {query}

Search Results: {search_results}

Please provide a helpful and warm response. If specific information isn't available,
offer to help in other ways."""

    prompt = PromptTemplate(
        input_variables=["query", "search_results"],
        template=template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"query": query, "search_results": search_results})
    
    return response.strip()

def get_general_search_response(query: str) -> str:
    """Handle general queries with web search"""
    
    try:
        search = DuckDuckGoSearchRun()
        search_results = search.run(query)
    except Exception as e:
        search_results = "Unable to search at the moment."
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    
    template = """You are a friendly and helpful assistant.
Help answer questions with a warm, conversational tone.

User Question: {query}

Search Results: {search_results}

Please provide a helpful and friendly response."""

    prompt = PromptTemplate(
        input_variables=["query", "search_results"],
        template=template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"query": query, "search_results": search_results})
    
    return response.strip()

# =============== Main Chat Handler ==================
async def handle_chat_query(message: ChatMessage, session: SessionDep) -> ChatResponse:
    """Main chat handler - process user query"""
    
    username = message.username
    query = message.query
    
    # Verify user exists
    user = get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Classify the query
    query_type = classify_query(query)
    
    # Route to appropriate handler
    if query_type == QueryType.ATTENDANCE:
        attendance_records = get_user_attendance(session, user.id)
        formatted_data = format_attendance_data(attendance_records)
        response = get_conversational_response(formatted_data, query)
        
    elif query_type == QueryType.MARKS:
        marks_records = get_user_marks(session, user.id)
        formatted_data = format_marks_data(marks_records)
        response = get_conversational_response(formatted_data, query)
        
    elif query_type == QueryType.FEES:
        fees_records = get_user_fees(session, user.id)
        formatted_data = format_fees_data(fees_records)
        response = get_conversational_response(formatted_data, query)
        
    elif query_type == QueryType.COLLEGE_INFO:
        response = get_college_info_response(query)
        
    else:  # GENERAL
        response = get_general_search_response(query)
    
    return ChatResponse(response=response, query_type=query_type)

# =============== Setup Function ==================
def setup_chatbot_routes(app):
    """Add chatbot routes to the main FastAPI app"""
    
    @app.post("/api/v1/chat", response_model=ChatResponse)
    async def chat(message: ChatMessage, session: SessionDep):
        """Main chat endpoint"""
        return await handle_chat_query(message, session)
    
    @app.get("/api/v1/chat/info")
    async def chat_info():
        """Get chatbot info"""
        return {
            "name": "Student Assistant Chatbot",
            "version": "1.0",
            "capabilities": [
                "Answer questions about your attendance",
                "Check your marks and grades",
                "Query fee payment status",
                "Get college information",
                "Answer general questions"
            ],
            "example_queries": [
                "Can you tell me my attendance?",
                "What are my marks?",
                "What's my fee status?",
                "Tell me about the college",
                "How to prepare for exams?"
            ]
        }