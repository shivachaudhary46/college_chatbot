from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from .database import create_all_db_tables
from .routers import (
    users, auth, attendance, fees, marks, courses, assignments, notices, chat
)

app = FastAPI(
    title="College Management System API",
    description="Comprehensive API for college management",
    version="1.0.0"
)

# CORS Configuration 
app.add_middleware(
    CORSMiddleware, 
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    """Initialize database on startup"""
    create_all_db_tables

@app.get("/")
def root():
    return {"message": "College Management System API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(attendance.router)
app.include_router(fees.router)
app.include_router(marks.router)
app.include_router(courses.router)
app.include_router(assignments.router)
app.include_router(notices.router)
app.include_router(chat.router)