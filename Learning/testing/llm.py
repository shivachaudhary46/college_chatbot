from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

api_key = os.environ["GOOGLE_API_KEY"]

def get_conversational_respone(user_data: str, query: str):

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    template = """You are a friendly and helpful college student assistant chatbot. 
    Your tone should be warm, professional, and encouraging - like a helpful friend.
    keep response concise and natural. 

    User Query: {query}

    student Information: 
    {user_data}

    please provide a helpful response based on the student's information. 
    Be warm, supportive, and conversational.
    """

    prompt = PromptTemplate(
        input_variables=["query", "search_results"],
        template=template
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"query": query, "user_data": user_data})
    
    return response.strip()

# user_data = """User attendance data: total = 28 days, months = Ashoj, percentage = 90%, status=excellent"""

# Query = "Can you give my attendance ?"

# answer = get_conversational_respone(user_data, Query)
# print(answer)

def get_general_search_response(query: str) -> str:
    """Handle general queries with web search"""
    
    try:
        search = DuckDuckGoSearchRun()
        search_results = search.run(query)
    except Exception as e:
        search_results = "Unable to search at the moment."
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    
    template = """You are a friendly and helpful assistant.
Help answer questions with a warm, conversational tone.

User Question: {query}

Search Results: {search_results}

Please provide a helpful and friendly response."""

    prompt = PromptTemplate(
        input_variables=["query", "search_results"],
        template=template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"query": query, "search_results": search_results})
    
    return response.strip()

query = "what is the announcement for student by Madan Bhandari memorial college"

answer = get_general_search_response(query)

print(answer)