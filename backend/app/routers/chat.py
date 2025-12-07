import logging
from fastapi import APIRouter, HTTPException, Depends

from models.schemas import ChatQuery, ChatResponse, QueryType
from models.models import User
from utilities.crud import (
    get_attendance_by_user_id,
    get_marks_by_user_id,
    get_fees_by_user_id,
    get_courses_for_student,
    get_recent_assignment_per_course,
    get_user_by_user_id,
    get_recent_notices,
)
from chat.chatbot import (
    classify_query,
    format_attendance_data,
    format_fees_data,
    format_marks_data,
    get_conversational_response,
    get_college_info_response,
    get_general_search_response,
    format_course_data,
    format_assignment_data,
    format_user_data,
    format_notice_data,
)
from auth.OAuth import role_required
from db.database import SessionDep
from logger.logger import logger

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chatbot"]
)

@router.post("/", response_model=ChatResponse)
async def chat(
    message: ChatQuery,
    session: SessionDep,
    user: User = Depends(role_required(["student", "teacher", "admin"])),
):
    """Main chat handler - process user query"""

    if not user:
        logger.warning("Unauthorized chat access attempt detected.")
        raise HTTPException(status_code=401, detail="Invalid credentials token")

    user_id = user.id
    query = message.query

    logger.info(f"Chat query received from user_id={user_id}: {query}")

    query_type = classify_query(query)
    logger.info(f"Query classified as: {query_type}")

    try:
        if query_type == QueryType.ATTENDANCE:
            attendance_records = get_attendance_by_user_id(session, user_id)
            formatted_data = format_attendance_data(attendance_records)
            response = get_conversational_response(formatted_data, query)
            logger.info(f"Response created using attendance records of user {user.username} by chatbot")

        elif query_type == QueryType.MARKS:
            marks_records = get_marks_by_user_id(session, user_id)
            formatted_data = format_marks_data(marks_records)
            response = get_conversational_response(formatted_data, query)
            logger.info(f"Response created using marks records of user {user.username} by chatbot")

        elif query_type == QueryType.FEES:
            fees_records = get_fees_by_user_id(session, user_id)
            formatted_data = format_fees_data(fees_records)
            response = get_conversational_response(formatted_data, query)
            logger.info(f"Response created using fees records of user {user.username} by chatbot")

        elif query_type == QueryType.COLLEGE_INFO:
            response = get_college_info_response(query)["answer"]
            logger.info(f"Fetched result from pinecone and given to LLM")

        elif query_type == QueryType.COURSE:
            user_course_records = get_courses_for_student(session, user_id)
            formatted_data = format_course_data(user_course_records)
            response = get_conversational_response(formatted_data, query)
            logger.info(f"Response created using course records of user {user.username} by chatbot")

        elif query_type == QueryType.ASSIGNMENT:
            assignment_records = get_recent_assignment_per_course(session)
            formatted_data = format_assignment_data(assignment_records)
            response = get_conversational_response(formatted_data, query)
            logger.info(f"Response created by fetching records of user {user.username} by chatbot")

        elif query_type == QueryType.USER_INFO:
            user_records = get_user_by_user_id(session, user_id)
            formatted_data = format_user_data(user_records)
            response = get_conversational_response(formatted_data, query)
            logger.info(f"Response created by fetching user record of user {user.username} by chatbot")

        elif query_type == QueryType.NOTICES:
            notice_records = get_recent_notices(session)
            formatted_data = format_notice_data(notice_records)
            response = get_conversational_response(formatted_data, query)
            logger.info(f"Response created by using notice records of user {user.username} by chatbot")

        else:  # GENERAL
            response = get_general_search_response(query)
            logger.info("General query response created")

    except Exception as e:
        logger.error(f"Error processing query for user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    logger.info(f"Response generated for user_id={user_id}: type={query_type}")

    return ChatResponse(response=response, query_type=query_type)


@router.get("/info")
async def chat_info():
    """Get chatbot info"""
    logger.info("Chatbot info endpoint accessed.")
    
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
