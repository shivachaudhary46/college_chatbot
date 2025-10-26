# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv


from database import create_all_db_tables
from chatbot import setup_chatbot_routes  

load_dotenv(find_dotenv(), override=True)

# Create main app
app = FastAPI(
    title="Student Management System with AI Chatbot",
    description="Integrated student management and AI chatbot system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    """Initialize database on startup"""
    create_all_db_tables()
    print("✅ Database initialized")

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Student Management System with AI Chatbot",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "endpoints": {
            "students": "/api/v1/users",
            "attendance": "/api/v1/users/{user_id}/attendance",
            "marks": "/api/v1/users/{user_id}/marks",
            "fees": "/api/v1/users/{user_id}/fees",
            "chatbot": "/api/v1/chat"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Include student management routes
print("Loading student management routes...")
# Note: Import and include student routes here after all dependencies are set

# Include chatbot routes
print("Loading chatbot routes...")
setup_chatbot_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        reload=True,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )