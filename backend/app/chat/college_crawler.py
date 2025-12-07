import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from dotenv import load_dotenv
import os
from datetime import datetime

from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

async def crawl_college_website():
    """Crawl MBMC college website and return documents"""
    urls = [
        "https://www.mbmc.edu.np/about-us",
        "https://www.mbmc.edu.np/publications",
        "https://www.mbmc.edu.np/course",
        "https://www.mbmc.edu.np/events",
        "https://www.mbmc.edu.np/gallery"
    ]
    
    run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=True)
    documents = []

    print("Starting to crawl college website...")
    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun_many(urls, config=run_conf):
            if result.success:
                print(f"✓ Successfully crawled: {result.url}")
                
                # Create a LangChain Document with metadata
                doc = Document(
                    page_content=result.markdown.raw_markdown,
                    metadata={
                        "source": result.url,
                        "page": result.url.split('/')[-1],
                        "last_updated": datetime.now().isoformat()
                    }
                )
                documents.append(doc)
            else:
                print(f"✗ Error crawling {result.url}: {result.error_message}")
    
    print(f"\n✓ Total pages crawled: {len(documents)}")
    return documents

def chunk_documents(documents, chunk_size=512, chunk_overlap=50):
    """Split documents into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    return chunks 

def get_or_create_index(index_name):
    """Get existing index or create new one"""
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        print(f"Creating new index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=384,  # text-embedding-004 dimension
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        print(f"✓ Index '{index_name}' created")
    else:
        print(f"✓ Using existing index: {index_name}")
    
    return pc.Index(index_name)

def delete_pinecone_index(index_name="all"):
    from pinecone import Pinecone, ServerlessSpec

    pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

    if index_name == "all":
        indexes = pc.list_indexes()
        print("Deleting all indexes...")
        for index in indexes:
            pc.delete_index(index.name)
            print(f"completed deleting index {index.name}")
    else:
        print(f"Deleting index {index_name}")
        pc.delete_index(index_name)
        print("Done...")

def add_to_pinecone(index_name, chunks):
    """Add or update chunks in Pinecone vector store"""
    embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=index_name
    )
    # Document added succesfully 

    # Return vectorstore without namespace for querying all content
    return PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )

def test_query(vectorstore, query="What is recent notices you can find on MBMC"):
    """Test the vectorstore with a sample query"""
    from langchain.chains import RetrievalQA
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    print(f"\n🔍 Testing query: '{query}'")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)
    
    answer = chain.invoke(query)
    print(f"\n💡 Answer: {answer['result']}\n")


async def main():
    index_name = "mbmc-college-website"
    # MBM college website crawler index 
    
    # Step 1: Crawl the website # need to add logging 
    documents = await crawl_college_website()
    
    if not documents:
        print("❌ No documents crawled. Exiting.")
        return
    
    # Step 2: Chunk the documents
    chunks = chunk_documents(documents, chunk_size=512, chunk_overlap=50)
    
    # step 3: Delete pinecone index 
    delete_pinecone_index()

    # Step 4: Setting or create Pinecone index
    index = get_or_create_index(index_name)
    
    # Step 5: Add to pinecone
    vectorstore = add_to_pinecone(index_name, chunks)

    test_query(vectorstore, "What is recent notices you can find on MBMC college website ?")
    test_query(vectorstore, "Tell me about MBMC college")
    
    return vectorstore, index_name

if __name__ == "__main__":
    # # Run the crawler
    vectorstore, index_name = asyncio.run(main())
    
    # print(f"\n✓ You can now use the index '{index_name}' in your QA application!")
    # print(f"✓ Run this script again to update the index with fresh content.")
