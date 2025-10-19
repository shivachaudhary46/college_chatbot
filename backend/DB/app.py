# main.py or your FastAPI startup file
"""
Integration example - combining chatbot with existing routes
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_all_db_tables
from routes import app as routes_app
from chatbot import app as chatbot_app

# Create main app
app = FastAPI(title="Student Management System with AI Chatbot")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes_app.router, prefix="/api", tags=["students"])
app.include_router(chatbot_app.router, prefix="/api/chat", tags=["chatbot"])

@app.on_event("startup")
def startup():
    create_all_db_tables()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Student Management System",
        "docs": "/docs",
        "chat_endpoint": "/api/chat/chat"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True, host="0.0.0.0", port=8000)


# =============== Example Usage ==================

# Example 1: User asking for attendance
# POST /api/chat/chat
# {
#   "username": "shivachaudhary",
#   "query": "Can you tell me my attendance status?"
# }
# Response:
# {
#   "response": "Hey there! 👋 Let me check your attendance for you...
#                Looking at your records, you've been doing great! 
#                Your attendance is solid and consistent...",
#   "query_type": "attendance"
# }

# Example 2: User asking for college info
# POST /api/chat/chat
# {
#   "username": "shivachaudhary",
#   "query": "What courses does the college offer?"
# }
# Response:
# {
#   "response": "Great question! Our college offers comprehensive programs in...
#                Here are some popular choices...",
#   "query_type": "college_info"
# }

# Example 3: General query
# POST /api/chat/chat
# {
#   "username": "shivachaudhary",
#   "query": "How to prepare for coding interviews?"
# }
# Response:
# {
#   "response": "That's a fantastic question! Here are some great strategies...",
#   "query_type": "general"
# }