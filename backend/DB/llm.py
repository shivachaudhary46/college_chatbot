# chatbot.py
"""
Intelligent student chatbot that routes queries intelligently
"""
import os
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from dotenv import load_dotenv, find_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from database import SessionDep
from crud import get_user_by_username, get_user_attendance, get_user_fees, get_user_marks
from models import User, Attendance, Fees, Marks

load_dotenv(find_dotenv(), override=True)

app = FastAPI()

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
    college_keywords = ["college", "course", "program", "announcement", "admission", "faculty", "campus", "facilities"]
    
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
        formatted += f"- {record.month} ({record.semester} semester): {record.total}% - {record.attendee_status}\n"
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
def get_conversational_response(user_data: str, query: str, context: str = "") -> str:
    """Generate a natural, friendly response using LLM"""
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    
    template = """You are a friendly and helpful college student assistant chatbot. 
Your tone should be warm, professional, and encouraging - like a helpful friend.

User Query: {query}

{context_section}

Please provide a helpful, concise, and warm response. Keep it conversational and friendly.
If providing information from records, present it in an easy-to-understand way.
Always be supportive and encouraging."""

    context_section = f"Student Information:\n{user_data}" if user_data else ""
    
    prompt = PromptTemplate(
        input_variables=["query", "context_section"],
        template=template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({
        "query": query,
        "context_section": context_section
    })
    
    return response.strip()

def get_college_info_response(query: str) -> str:
    """Get college information using web search and RAG"""
    
    search = DuckDuckGoSearchRun()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # Try to search for college info first
    try:
        search_results = search.run(f"MBMC college {query}")
    except:
        search_results = ""
    
    template = """You are a helpful college assistant providing information about the institution.
You are friendly, professional, and always helpful.

Query: {query}

Search Results: {search_results}

Please provide a helpful, warm response about the college. If you don't have specific information,
offer to help in other ways or suggest what they can do."""

    prompt = PromptTemplate(
        input_variables=["query", "search_results"],
        template=template
    )
    
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.run({
        "query": query,
        "search_results": search_results
    })
    
    return response.strip()

def get_general_search_response(query: str) -> str:
    """Handle general queries with web search"""
    
    search = DuckDuckGoSearchRun()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    
    try:
        search_results = search.run(query)
    except:
        search_results = "No search results available."
    
    template = """You are a friendly and helpful assistant. 
You help answer various questions with a warm, conversational tone.

User Question: {query}

Search Results: {search_results}

Please provide a helpful, warm response. Be conversational and friendly in your tone."""

    prompt = PromptTemplate(
        input_variables=["query", "search_results"],
        template=template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({
        "query": query,
        "search_results": search_results
    })
    
    return response.strip()

# =============== Main Chat Handler ==================
@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, session: SessionDep):
    """Main chat endpoint that routes queries intelligently"""
    
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
    
    return ChatResponse(
        response=response,
        query_type=query_type
    )

@app.get("/chat/test")
async def test_chat():
    """Test endpoint to check the chatbot"""
    return {
        "message": "Chatbot is running!",
        "example_queries": [
            "Can you get my attendance info?",
            "What are my marks?",
            "Tell me about my fees",
            "What courses does the college offer?",
            "Tell me about Python programming"
        ]
    }