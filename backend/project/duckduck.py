import os

from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from dotenv import load_dotenv, find_dotenv

load_dotenv()
load_dotenv(find_dotenv(), override=True)

api_key = os.environ.get("GOOGLE_API_KEY")

#Get the React prompt
prompt = hub.pull("hwchase17/react")

# Tools
search = DuckDuckGoSearchRun()
tools = [search]

# LLM 
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# create agent 
agent = create_react_agent(llm, tools, prompt)

# create executor 
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,
    max_iterations=3
)

query = input("Enter your query: ")
response = agent_executor.invoke({"input": query})
print(response["output"])