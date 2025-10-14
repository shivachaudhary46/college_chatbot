from variables import user_data, attendance_data, fees_data, marks_data
from functions import add_user, add_attendance, add_fees, add_marks, get_user_with_all_data

# ========= insert all data to database ==========
def insert_data():

    for i in range(len(user_data)):

        # creating user
        user = add_user(
            user_data[i]["username"], 
            user_data[i]["full_name"], 
            user_data[i]["email"]
        )
        print(f"created user: {user.username}")
        
        attendance = add_attendance(
            user.id, 
            attendance_data[i]["month"], 
            attendance_data[i]["semester"], 
            attendance_data[i]["total"], 
            attendance_data[i]["attendee_status"],# Good Attendance, Regular, Not Consistent
        )

        fee = add_fees(
            user.id, 
            fees_data[i]["semester"],
            fees_data[i]["total_paid"],
            fees_data[i]["last_payment_date"],
        )

        marks = add_marks(
            user.id, 
            marks_data[i]["semester"],
            marks_data[i]["subject"],
            marks_data[i]["total_marks"],
            marks_data[i]["grade"],
            marks_data[i]["exam_date"],
        )

        get_user_with_all_data(user.id)

# ======= utilities for login backend ===========
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
oauth_scheme2 = OAuth2PasswordBearer(tokenUrl="token")

'''
to get username from the database, it is necessary function to extract
username and dump in to the UserInDB class. 
'''
def get_user(username: str, session: SessionDep) -> User:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    account = results.one()

    return Info(**account.model_dump())

'''
first, we will try to read the username from the database
second, verify the password. remember we have done hashing of the password, to store
so we need to verify by using the PasswordHash.recommended(),we need to pass plain_password, 
and hashed password as argument. 
'''
def authenticate_user(username: str, password: str, session: SessionDep) :
    user = get_user(username, session)
    if not user:
        return False
    if not user.verify_password(password, user.hashed_password):
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
        token_data = Token_Data(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user
