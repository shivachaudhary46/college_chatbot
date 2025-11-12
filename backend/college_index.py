import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from dotenv import load_dotenv
import os
from datetime import datetime

from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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
    print(f"✓ Created {len(chunks)} chunks")
    return chunks


def get_or_create_index(index_name):
    """Get existing index or create new one"""
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        print(f"Creating new index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=768,  # text-embedding-004 dimension
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


def delete_old_vectors_for_page(index_name, page_name):
    """Delete old vectors for a specific page before adding new ones"""
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    index = pc.Index(index_name)
    
    try:
        # Query to find all vectors with this page metadata
        # Note: This requires metadata filtering support in Pinecone
        print(f"  Checking for existing vectors for page: {page_name}")
        
        # Delete by metadata filter (if supported by your Pinecone plan)
        index.delete(filter={"page": page_name})
        
        # Alternative: Delete all and re-add (simpler but less efficient)
        # We'll use namespaces to organize by page
        
    except Exception as e:
        print(f"  Note: Could not delete old vectors: {e}")


def add_to_pinecone(index_name, chunks, update_mode=True):
    """Add or update chunks in Pinecone vector store"""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    if update_mode:
        print(f"Updating index '{index_name}' with new data...")
        
        # Group chunks by page
        pages = {}
        for chunk in chunks:
            page = chunk.metadata.get('page', 'unknown')
            if page not in pages:
                pages[page] = []
            pages[page].append(chunk)
        
        # Process each page separately
        for page, page_chunks in pages.items():
            print(f"  Processing page: {page} ({len(page_chunks)} chunks)")
            
            # Use upsert mode - will overwrite existing vectors with same ID
            vectorstore = PineconeVectorStore.from_documents(
                documents=page_chunks,
                embedding=embeddings,
                index_name=index_name,
                namespace=page   # Use page as namespace for organization
            )
        
        print("✓ Index updated successfully!")
    else:
        print(f"Adding chunks to index '{index_name}'...")
        vectorstore = PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            index_name=index_name
        )
        print("✓ Documents added successfully!")
    
    # Return vectorstore without namespace for querying all content
    return PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )


def get_index_stats(index_name):
    """Get statistics about the index"""
    try:
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        
        print(f"\n📊 Index Statistics for '{index_name}':")
        print(f"  Total vectors: {stats.total_vector_count}")
        if hasattr(stats, 'namespaces'):
            print(f"  Namespaces: {len(stats.namespaces)}")
            for ns, count in stats.namespaces.items():
                print(f"    - {ns}: {count.vector_count} vectors")
    except Exception as e:
        print(f"Could not get index stats: {e}")


def test_query(vectorstore, query="What is recent notices you can find on MBMC"):
    """Test the vectorstore with a sample query"""
    from langchain.chains import RetrievalQA
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    print(f"\n🔍 Testing query: '{query}'")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)
    
    answer = chain.invoke(query)
    print(f"\n💡 Answer: {answer['result']}\n")


async def main():
    """Main function to crawl and update Pinecone index"""
    index_name = "mbmc-college-website"
    
    print("=" * 70)
    print("🎓 MBMC College Website Crawler & Indexer")
    print("=" * 70)
    
    # Step 1: Crawl the website
    print("\n[Step 1] Crawling college website...")
    documents = await crawl_college_website()
    
    if not documents:
        print("❌ No documents crawled. Exiting.")
        return
    
    # Step 2: Chunk the documents
    print("\n[Step 2] Chunking documents...")
    chunks = chunk_documents(documents, chunk_size=512, chunk_overlap=50)
    
    # Step 3: Get or create Pinecone index
    print("\n[Step 3] Setting up Pinecone index...")
    index = get_or_create_index(index_name)
    
    # Step 4: Add/Update in Pinecone (UPDATE MODE = True)
    print("\n[Step 4] Updating Pinecone index...")
    vectorstore = add_to_pinecone(index_name, chunks, update_mode=True)
    
    # Step 5: Show statistics
    get_index_stats(index_name)
    
    print("\n" + "=" * 70)
    print("✅ Process completed successfully!")
    print("=" * 70)
    
    # Optional: Test with a query
    print("\n" + "=" * 70)
    test_query(vectorstore, "What is recent notices you can find on MBMC college website ?")
    test_query(vectorstore, "Tell me about MBMC college")
    
    return vectorstore, index_name

if __name__ == "__main__":
    # Run the crawler
    vectorstore, index_name = asyncio.run(main())
    
    print(f"\n✓ You can now use the index '{index_name}' in your QA application!")
    print(f"✓ Run this script again to update the index with fresh content.")


# need to delete this 
#######################
######################
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
