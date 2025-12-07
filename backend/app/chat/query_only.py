# query_only.py
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_pinecone import PineconeVectorStore
import os 
from dotenv import load_dotenv
from pinecone import Pinecone 
load_dotenv() 

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def load_existing_vectorstore(index_name):
    """Load existing Pinecone vectorstore without re-indexing"""
    embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
        pinecone_api_key=os.getenv("PINECONE_API_KEY")
    )

    return vectorstore

def query_vectorstore(vectorstore, query):
    """Query the vectorstore with a custom question"""
    print(f"\n🔍 Query: '{query}'")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)
    
    answer = chain.invoke(query)
    print(f"\n💡 Answer: {answer['result']}\n")
    return answer['result']

if __name__ == "__main__":
    index_name = "mbmc-college-website"
    
    # Load existing vectorstore
    vectorstore = load_existing_vectorstore(index_name)
    
    # Query examples
    queries = [
        "What is recent notices you can find on MBMC? can you provide links",
        "What courses does MBMC offer?",
        "How can I contact MBMC?"
    ]
    
    # Run queries
    for query in queries:
        query_vectorstore(vectorstore, query)
        print("-" * 70)
    
    # Interactive mode (optional)
    # print("\n💬 Interactive Query Mode (type 'exit' to quit)")
    # while True:
    #     user_query = input("\nYour question: ").strip()
    #     if user_query.lower() in ['exit', 'quit', 'q']:
    #         break
    #     if user_query:
    #         query_vectorstore(vectorstore, user_query)