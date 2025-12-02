from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from .logger import logger
from .database import create_all_db_tables
from .routers import (
    users, auth, attendance, fees, marks, courses, assignments, notices, chat
)
from .model.classify_query import get_classifier

app = FastAPI(
    title="College Management System API",
    description="Comprehensive API for college management",
    version="1.0.0"
)

# CORS Configuration 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],  # Add all your frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)
@app.on_event("startup")
def startup():
    """Initialize database on startup"""
    create_all_db_tables
    logger.info("Created and intialize the database")
    
    # load the model and save it into the memory, so does not have to rerun 
    get_classifier()
    logger.info("Loading the model when server starts")

@app.on_event("shutdown")
async def shutdown_event():
    print("shutting down events!")
    logger.info("Shutting down model when server shutdown")

@app.get("/")
def root():
    return {"message": "College Management System API", "status": "running"}

@app.get("/health")
def health_check():
    """Check if model is loaded and ready"""
    clf = get_classifier()
    if clf.model is None:
        return {"status": "unhealthy", "reason": "Model not loaded"}
    return {
        "status": "healthy",
        "device": str(clf.device),
        "labels": list(clf.id2label.values())
    }

@app.get("/stats")
async def get_stats():
    """Get model statistics"""
    clf = get_classifier()
    return {
        "cache_info": clf.predict_cached.cache_info()._asdict(),
        "device": str(clf.device),
        "num_labels": len(clf.id2label)
    }

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