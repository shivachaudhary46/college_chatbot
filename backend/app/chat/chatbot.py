"""
A chatbot module that integrates with main FastAPI app
"""
import os
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from dotenv import load_dotenv, find_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import GoogleGenerativeAIEmbeddings
 
from app.classify.classify_query import get_classifier
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from app.models.schemas import QueryType
load_dotenv(find_dotenv(), override=True)

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from typing import Dict

from app.logger.logger import logger
from langchain_community.embeddings import HuggingFaceEmbeddings

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
genai_key = os.environ.get("GOOGLE_API_KEY")

def normalize_label(label):
    """Convert any label format to a standard key"""
    return label.lower().replace(" ", "_").strip()

# =============== Query Classification ==================
def classify_query(query: str) -> QueryType:
    """
    Classify the user query using the trained model
    """
    try:
        # Get the trained classifier instance
        clf = get_classifier()
        
        # Predict query type
        prediction = clf.predict(query)
        logger.info(f"query classified into : {prediction}")
        
        # Check for errors
        if "error" in prediction:
            logger.warning(f"Classification error: {prediction['error']}, QueryType = {prediction}")
            # Fallback to GENERAL if classification fails
            return QueryType.GENERAL
        
        # Get predicted query type
        query_type = prediction["query_type"]
        confidence = prediction["confidence"]
        
        logger.info(f"Query: '{query[:50]}...' -> Type: {query_type} (confidence: {confidence:.2%})")
        
        query_type_mapping = {
            "attendance": QueryType.ATTENDANCE,
            "fees": QueryType.FEES,
            "marks": QueryType.MARKS,
            "course": QueryType.COURSE,
            "assignment": QueryType.ASSIGNMENT,
            "college_info": QueryType.COLLEGE_INFO,
            "user_info": QueryType.USER_INFO,
            "general": QueryType.GENERAL,
            "notices": QueryType.NOTICES,
        }

        query_type_normalized = normalize_label(query_type)
        result = query_type_mapping.get(query_type_normalized, QueryType.GENERAL)
      
        # If confidence is too low, fallback to GENERAL
        if confidence < 0.15:  # Adjust threshold as needed
            logger.info(f"Low confidence ({confidence:.2%}, using GENERAL)")
            return QueryType.GENERAL
        
        logger.info(f"returning mapped query: {result}")
        return result
        
    except Exception as e:
        logger.warning(f"Error in classify_query : {e} will return QueryType = GENERAL")
        return QueryType.GENERAL
    # chatbot.py


# =============== Loading pinecone index ==============
def load_existing_vectorstore(index_name):
    """Load existing Pinecone vectorstore without re-indexing"""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},  # or 'cuda' if available
        encode_kwargs={'normalize_embeddings': True}
    )
    
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
        pinecone_api_key=os.getenv("PINECONE_API_KEY")
    )

    return vectorstore
    
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
    
    chain = prompt | llm
    response = chain.invoke({"query": query, "user_data": user_data})
    
    return response.content.strip()


def get_college_info_response(query: str) -> Dict[str, str]:
    """
    Alternative implementation using LLMChain for more control.
    """
    index_name = "mbmc-college-website"
    try:
        vectorstore = load_existing_vectorstore(index_name)
        
        # Initialize LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Configure retriever
        retriever = vectorstore.as_retriever(
            search_type='similarity',
            search_kwargs={'k': 5}
        )
        
        # Retrieve relevant documents
        retrieved_docs = retriever.invoke(query)
        
        # Extract document information
        doc_info = []
        for i, doc in enumerate(retrieved_docs):
            doc_info.append({
                'index': i + 1,
                'content': doc.page_content,
                'metadata': doc.metadata
            })
        
        # Format context
        context = "\n\n".join([
            f"Document {i+1}:\n{doc.page_content}" 
            for i, doc in enumerate(retrieved_docs)
        ])
        
        # Create prompt
        template = """You are a knowledgeable and friendly college information assistant.

Context Information:
{context}

Student's Question: {query}

Instructions:
- Provide accurate information based on the context
- Be warm, professional, and encouraging
- If information is not in the context, acknowledge this honestly
- Use bullet points for lists when appropriate
- Keep responses concise but comprehensive

Response:"""

        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template=template
        )
        
        # Create and run chain
        chain = prompt | llm
        result = chain.invoke({"context": context, "query": query})
        
        # Extract content from AIMessage object
        response_text = result.content if hasattr(result, 'content') else str(result)
        
        return {
            'answer': response_text.strip(),
            'source_documents': doc_info,
            'query': query,
            'num_sources': len(retrieved_docs)
        }
        
    except Exception as e:
        return {
            'answer': f"I apologize, but I encountered an error: {str(e)}",
            'source_documents': [],
            'query': query,
            'num_sources': 0,
            'error': str(e)
        }

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
    
    chain = prompt | llm
    response = chain.invoke({"query": query, "search_results": search_results})
    
    return response.content.strip()