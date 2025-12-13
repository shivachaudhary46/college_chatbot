from contextlib import asynccontextmanager
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from app.logger.logger import logger
from app.db.database import create_all_db_tables
from app.routers import (
    users, auth, attendance, fees, marks, courses, assignments, notices, chat
)
from app.classify.classify_query import get_classifier

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_db_tables()
    logger.info("Created and intialize the database")
    # Load the ML model
    ml_models["query_classify"] = get_classifier()
    logger.info("Loading the model when server starts")
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()
    logger.info("Deleting Ml model when server shutdown")


app = FastAPI(
    title="College Management System API",
    description="Comprehensive API for college management",
    version="1.0.0", 
    lifespan=lifespan
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=["backend/logs/*"]
    )