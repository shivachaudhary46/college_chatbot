import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

async def crawl_college_website():
    """Crawl college website and return documents"""
    urls = [
        "https://www.mbmc.edu.np/about-us",
        "https://www.mbmc.edu.np/publications",
        "https://www.mbmc.edu.np/course",
        "https://www.mbmc.edu.np/events",
        "https://www.mbmc.edu.np/gallery"
    ]
    
    run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=True)
    documents = []

    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun_many(urls, config=run_conf):
            if result.success:
                print(f"Successfully crawled: {result.url}")
                print(f"Markdown length: {len(result.markdown.raw_markdown)}")
                
                # Create a LangChain Document object
                doc = Document(
                    page_content=result.markdown.raw_markdown,
                    metadata={
                        "source": result.url,
                        "title": result.url.split('/')[-1].replace('-', ' ').title()
                    }
                )
                documents.append(doc)
            else:
                print(f"Error crawling {result.url}: {result.error_message}")
    
    return documents


def chunk_website_data(documents, chunk_size=512, chunk_overlap=50):
    """Split crawled documents into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} pages")
    return chunks


def create_or_get_index(index_name):
    """Create Pinecone index if it doesn't exist"""
    from pinecone import ServerlessSpec
    
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        print(f"Creating new index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=768,  # Google's embedding model dimension
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        print(f"Index '{index_name}' created successfully!")
    else:
        print(f"Index '{index_name}' already exists")
    
    return pc.Index(index_name)


def add_to_pinecone(index_name, chunks):
    """Add chunks to Pinecone vector store"""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    print(f"Embedding and storing {len(chunks)} chunks...")
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=index_name
    )
    print("Documents successfully uploaded to Pinecone!")
    
    return vectorstore


async def main():
    """Main function to crawl website and add to Pinecone"""
    index_name = "mbmc-college-website"
    
    print("=" * 60)
    print("Starting college website crawl and indexing process...")
    print("=" * 60)
    
    # Step 1: Crawl the college website
    print("\n[Step 1] Crawling college website...")
    documents = await crawl_college_website()
    print(f"✓ Crawled {len(documents)} pages successfully\n")
    
    # Step 2: Chunk the documents
    print("[Step 2] Chunking documents...")
    chunks = chunk_website_data(documents, chunk_size=512, chunk_overlap=50)
    print(f"✓ Created {len(chunks)} chunks\n")
    
    # Step 3: Create or get Pinecone index
    print("[Step 3] Setting up Pinecone index...")
    index = create_or_get_index(index_name)
    print(f"✓ Index ready\n")
    
    # Step 4: Add to Pinecone
    print("[Step 4] Adding chunks to Pinecone...")
    vectorstore = add_to_pinecone(index_name, chunks)
    print(f"✓ All data indexed successfully!\n")
    
    print("=" * 60)
    print(f"✓ Process completed! Index name: '{index_name}'")
    print("=" * 60)
    
    return vectorstore, index_name


if __name__ == "__main__":
    # Run the async main function
    vectorstore, index_name = asyncio.run(main())
    
    # Optional: Test the vectorstore with a sample query
    print("\n[Testing] Running a sample query...")
    from langchain.chains import RetrievalQA
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)
    
    test_query = "What courses does MBMC college offer?"
    answer = chain.invoke(test_query)
    print(f"\nQuery: {test_query}")
    print(f"Answer: {answer['result']}") 