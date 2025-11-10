from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def load_college_vectorstore(index_name="mbmc-college-website"):
    """Load the existing Pinecone index for college website"""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    print(f"Loading vectorstore from index: {index_name}")
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )
    print("✓ Vectorstore loaded successfully!")
    return vectorstore


def ask_question(vectorstore, question, k=3):
    """Ask a question and get an answer from the college website data"""
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': k})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)
    
    result = chain.invoke(question)
    return result['result']


def main():
    """Interactive Q&A with college website data"""
    print("=" * 70)
    print("🎓 MBMC College Website Q&A System")
    print("=" * 70)
    
    # Load the vectorstore
    vectorstore = load_college_vectorstore()
    
    print("\n💬 Ask questions about MBMC College (type 'exit' to quit)")
    print("-" * 70)
    
    while True:
        question = input("\n🤔 Your question: ").strip()
        
        if question.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not question:
            continue
        
        print("\n🤖 Thinking...")
        answer = ask_question(vectorstore, question, k=3)
        print(f"\n💡 Answer:\n{answer}")
        print("-" * 70)


if __name__ == "__main__":
    main()