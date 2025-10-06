from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt 
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel

from sqlmodel import SQLModel, Field, Session, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def get_session():
    with Session(engine) as session:
        yield session

def create_all_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_all_db_and_tables()

SessionDep = Annotated[Session, Depends(get_session)]

secret_key = "b84805d2ac3814b0a375bedf53df3531d3437176f858a4fd770aa1d327ea2b2a"
ALGO = "HS256"
ACCESS_TOKEN_EXPIRE = 30

oauth_scheme2 = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token : str
    token_type : str 

class Token_Data(BaseModel):
    username: str | None = None

class User(SQLModel, table=True):
    id: int | None = None
    fullname: str 
    username: str 
    email: str | None = None 
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

db = {
    "shivachaudhary": {
        "id": 1, 
        "fullname": "shiva chaudhary",
        "username": "shivachaudhary",
        "email": "yuukiassuna100@gmail.com",
        "hashed_password": '$argon2id$v=19$m=65536,t=3,p=4$BQaQNa7V82rzR0g61+1tqQ$l+2P0ugmJGAbygnqaVz172BVehqjvJ1nq2yEjnXwye0',
        "disabled": False, 
    },
    "umangaghimire": {
        "id": 2, 
        "fullname": "umanga ghimire", 
        "username": "umangaghimire",
        "email": "umagaghimire416@gmail.com",
        "hashed_password": '$argon2id$v=19$m=65536,t=3,p=4$V4MiWYmwoRxbkYKYr/xxog$qyRiaLSCeOXH/weY3+jjYmYgnVDKlNSYFPOORkUkTbQ',
        "disabled": False,
    }
}

def get_user(db, username: str):
    if username in db:
        user = db[username]
        return UserInDB(**user)
    
def verify_password(password, hashed_password):
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hashed_password) # if match return True, If not then False
    
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expire_time: timedelta | None):
    form_data = data.copy()
    if expire_time:
        access_time = datetime.now(timezone.utc) + expire_time
    else:
        access_time = datetime.now(timezone.utc) + timedelta(minutes=15)
    form_data.update({"exp": access_time})
    token = jwt.encode(form_data, secret_key, algorithm=ALGO)
    return token 

async def get_current_user(token: Annotated[str, Depends(oauth_scheme2)]):
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
        token_data = Token_Data(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(db, data.username, data.password)
    if not user: 
        raise HTTPException(status_code=400, detail="invalid Username or password")
    
    access_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    token = create_access_token(
        data = {"sub": user.username}, expire_time = access_time
    )

    if token is None :
        raise HTTPException(status_code=400, detail="invalid username or password")

    return Token(access_token=token, token_type="bearer")


'''
It t
'''
@app.get("/token")
async def get_current_username(current_user: Annotated[User, Depends(get_current_user)]):
    return {"user": current_user.username}

    