from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import SQLModel, Session, select
from pydantic import BaseModel
from database import engine
from models import Attendance
from dotenv import load_dotenv, find_dotenv
import os 

load_dotenv(find_dotenv(), override=True)

api_key = os.environ.get("GOOGLE_API_KEY")


app = FastAPI()

class UserQuery(BaseModel):
    query: str

def select_heroes(username: str):
    with Session(engine) as session: 
        statement = select(Attendance).where(Attendance.username == username)
        results = session.exec(statement)
        user = results.one()
        print(user)
        return user 
    
def retrieve_answer(attendance):
    from langchain import PromptTemplate
    from langchain.chains import LLMChain
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.5)
    template = '''This is my attendance can you summarize it in a natural language. Here's is attendance: {attendance}'''

    prompt = PromptTemplate(
        input_variables=['attendance'],
        template=template
    )

    chain=LLMChain(llm=llm, prompt=prompt)

    output=chain.run({'attendance': attendance})
    return output

@app.post("/get_question")
async def get_question_answer(username: str, userQuery: UserQuery):
    attendance = select_heroes(username)
    # results = attendance["total"]
    # percentage = attendance["percentage"]

    answer = retrieve_answer(attendance)
    return answer



# if the query gets the attendance then, 
# query = attendance

# select the attendance from the database 

# feed to the llm chain 

# give response in the llm natural language