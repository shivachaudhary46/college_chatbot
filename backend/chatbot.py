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

from transformers import pipeline 

from .schemas import QueryType
load_dotenv(find_dotenv(), override=True)

genai_key = os.environ.get("GOOGLE_API_KEY")

# =============== Query Classification ==================
def classify_query(query: str) -> QueryType:
    """Classify the user query into appropriate categories"""
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    
    candidate_labels = ["attendance", "fees", "marks", "course", "assignment", "college_info", "user_info", "general", "notices"]

    result = classifier(query, candidate_labels)
    
    top_label = result["labels"][0]
    
    if top_label == "attendance":
        return QueryType.ATTENDANCE
    elif top_label == "marks":
        return QueryType.MARKS
    elif top_label == "fees":
        return QueryType.FEES
    elif top_label == "college_info":
        return QueryType.COLLEGE_INFO
    elif top_label == "course":
        return QueryType.COURSE
    elif top_label == "assignment":
        return QueryType.ASSIGNMENT
    elif top_label == "user_info":
        return QueryType.USER_INFO
    elif top_label == "notices":
        return QueryType.NOTICES
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

def format_course_data(course_records: list) -> str:
    """Format course records into readable text"""
    if not course_records:
        return "No course records found."
    
    formatted = "Your Enrolled Courses:\n"
    for record in course_records:
        formatted += f"- {record.name} (Code: {record.code})\n"
        if hasattr(record, 'teacher_id') and record.teacher_id:
            formatted += f"  Teacher ID: {record.teacher_id}\n"
    return formatted

def format_assignment_data(assignment_records: list) -> str:
    """Format assignment records into readable text"""
    if not assignment_records:
        return "No assignment records found."
    
    formatted = "Recent Assignments:\n"
    for record in assignment_records:
        formatted += f"- {record.title}\n"
        formatted += f"  Course ID: {record.course_id}\n"
        formatted += f"  Description: {record.description}\n"
        formatted += f"  Due Date: {record.due_date.strftime('%Y-%m-%d %H:%M')}\n"
        formatted += f"  Assigned by: User ID {record.teacher_id}\n\n"
    return formatted

def format_user_data(user_record) -> str:
    """Format user record into readable text"""
    if not user_record:
        return "No user information found."
    
    formatted = "Your Profile Information:\n"
    formatted += f"- Full Name: {user_record.full_name}\n"
    formatted += f"- Username: {user_record.username}\n"
    formatted += f"- Email: {user_record.email}\n"
    formatted += f"- Batch: {user_record.batch}\n"
    formatted += f"- Program: {user_record.program}\n"
    formatted += f"- Role: {user_record.role}\n"
    formatted += f"- Account Status: {'Disabled' if user_record.disabled else 'Active'}\n"
    formatted += f"- Member Since: {user_record.created_at.strftime('%Y-%m-%d')}\n"
    return formatted

def format_notice_data(notice_records: list) -> str:
    """Format notice records into readable text"""
    if not notice_records:
        return "No notices found."
    
    formatted = "Recent Notices:\n"
    for record in notice_records:
        formatted += f"\n📢 {record.title}\n"
        formatted += f"   {record.content}\n"
        if record.target_batch:
            formatted += f"   Target Batch: {record.target_batch}\n"
        if record.target_program:
            formatted += f"   Target Program: {record.target_program}\n"
        if record.course_id:
            formatted += f"   Course ID: {record.course_id}\n"
        if record.created_by:
            formatted += f"   Created By: {record.created_by}\n"
        formatted += f"   Posted: {record.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        formatted += "   " + "-"*50 + "\n"
    return formatted

# =============== LLM Response Generators ==================
def get_conversational_response(user_data: str, query: str) -> str:
    """Generate a natural, friendly response using LLM"""
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, google_api_key=genai_key)
    
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
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5, google_api_key=genai_key)
    
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
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, google_api_key=genai_key)
    
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
