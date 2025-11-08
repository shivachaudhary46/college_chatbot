# from fastapi import FastAPI, HTTPException
# from schemas import ChatMessage, ChatResponse, QueryType
# from crud import get_user_by_username, get_user_attendance, get_user_fees, get_user_marks
# from chatbot import classify_query, format_attendance_data, get_conversational_response, format_marks_data, format_fees_data, get_college_info_response, get_general_search_response
# from database import SessionDep
# # app = FastAPI() 

# # @app.post("/api/v1/chat", response_model=ChatResponse)
# async def chat(message: ChatMessage, session: SessionDep):
#     """Main chat handler - process user query"""
    
#     username = message.username
#     query = message.query
    
#     # Verify user exists
#     user = get_user_by_username(session, username)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Classify the query
#     query_type = classify_query(query)
    
#     # Route to appropriate handler
#     if query_type == QueryType.ATTENDANCE:
#         attendance_records = get_user_attendance(session, username)
#         formatted_data = format_attendance_data(attendance_records)
#         response = get_conversational_response(formatted_data, query)
        
#     elif query_type == QueryType.MARKS:
#         marks_records = get_user_marks(session, username)
#         formatted_data = format_marks_data(marks_records)
#         response = get_conversational_response(formatted_data, query)
        
#     elif query_type == QueryType.FEES:
#         fees_records = get_user_fees(session, username)
#         formatted_data = format_fees_data(fees_records)
#         response = get_conversational_response(formatted_data, query)
        
#     elif query_type == QueryType.COLLEGE_INFO:
#         response = get_college_info_response(query)
        
#     else:  # GENERAL
#         response = get_general_search_response(query)
    
#     return ChatResponse(response=response, query_type=query_type)

# if __name__ == "__main__":
#     import asyncio
#     from database import engine
#     from sqlmodel import Session
    
#     with Session(engine) as session:
#         request = ChatMessage(username="shivachaudhary", query="what is 3*4 ^ 2 ?")
#         response = asyncio.run(chat(request, session))
#         print(response)

from transformers import pipeline 

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

query = "I was present yesterday but i was absent today ? did i pass my attendance optimum 70 % ?"


def classify_text(query):
    candidate_labels = ["attendance", "fees", "marks", "course", "assignment", "college", "user_info", "general"]
    result = classifier(query, candidate_labels=candidate_labels)
    
    # Get the label with highest score (first item in the result)
    top_label = result["labels"][0]
    top_score = result["scores"][0]
    
    return top_label

print(classify_text(query))