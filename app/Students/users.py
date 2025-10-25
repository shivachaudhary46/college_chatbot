from fastapi import FastAPI, HTTPException
from .schemas import UserCreate, UserResponse
from .database import SessionDep
from .models import User
from .crud import get_user_by_username, create_user
from .utilities import hasher 

app = FastAPI() 

@app.post("/api/v1/users/", response_model=UserResponse)
def create_new_user(user_data: UserCreate, session: SessionDep):
    """Create a new user"""
    existing = get_user_by_username(session, user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
        
    user = User(
        username=user_data.username,
        full_name=user_data.full_name,
        email=user_data.email,
        batch=user_data.batch,
        program=user_data.program,
        hashed_password=hasher.hash(user_data.password)
    )
    return create_user(session, user)