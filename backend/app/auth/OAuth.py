from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlmodel import select
import jwt
from jwt.exceptions import InvalidTokenError
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv()

from app.db.database import SessionDep
from app.models.models import User
from app.models.schemas import TokenData
from typing import Annotated
from app.logger.logger import logger

'''
get important environment variables from .env file, using load_dotenv()
'''
secret_key = os.getenv("secret_key")
ALGO = os.getenv("ALGO")

'''
This will create sleek looking authorize and authentication which will 
take the username, password with the password bearer token, 
Header -> must be added with bearer + application/json, and we can access 
with OAuth2PasswordRequestForm
'''
oauth_scheme2 = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

'''
to get username from the database, it is necessary function to extract
username and dump in to the UserInDB class. 
'''
def get_user(username: str, session: SessionDep) -> User:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    account = results.first()

    if not account:
        return None

    return account

'''
first, we will try to read the username from the database
second, verify the password. remember we have done hashing of the password, to store
so we need to verify by using the PasswordHash.recommended(),we need to pass plain_password, 
and hashed password as argument. 
'''
def authenticate_user(session: SessionDep, username: str, password: str) :
    user = get_user(username, session)

    from pwdlib import PasswordHash
    hasher = PasswordHash.recommended()

    if not user:
        logger.info("Username not found in database")
        return False
    if not hasher.verify(password, user.hashed_password):
        logger.info(f"Password not matched of username {username}")
        return False
    return user

'''
we can create a token with the jwt, the dict data will look like this which 
will later converted into the json web tokens, 
data = {
    "sub": "user.username",
    "exp": timedelta(minutes=??),  ## this will determine the token expirity
}
Create access token 
'''
def create_access_token(data: dict, expire_time: timedelta | None):
    form_data = data.copy()
    if expire_time:
        access_time = datetime.now(timezone.utc) + expire_time
    else:
        access_time = datetime.now(timezone.utc) + timedelta(minutes=15)
    form_data.update({"exp": access_time})
    token = jwt.encode(form_data, secret_key, algorithm=ALGO)
    return token 

'''
We can look if the user has token expirity remaining or not, we can do by using, 
jwt.decode() with secret key and algorithm, and we can access the username, and 
extract that user from the database.  
'''
async def get_current_user(token: Annotated[str, Depends(oauth_scheme2)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGO])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user

def role_required(allowed_roles: list):
    def wrapper(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return current_user
    return wrapper