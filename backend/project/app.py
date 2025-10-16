
import asyncio
from crawl4ai import AsyncWebCrawler, AdaptiveCrawler, AdaptiveConfig
import os

# Splitting the paragraphs into smaller chunks. so we can easily store in the vector db 
def chunk_data(docs):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # chunk size (characters)
        chunk_overlap=200, # chunk overlap (characters)
        add_start_index=True # track index in original document
    )
    
    all_splits = text_splitter.split_documents(docs)


async def get_contents_from_website(query: str):

    # Note : this does not works when offline 

    async with AsyncWebCrawler() as crawler:
        # and config options 
        config = AdaptiveConfig(
            confidence_threshold=0.8, 
            max_pages=30,
            top_k_links=5, 
            min_gain_threshold=0.05
        )

        # intitalize adaptive
        adaptive = AdaptiveCrawler(crawler, config)
        
        # Start crawling with a query
        result = await adaptive.digest(
            start_url="https://www.mbmc.edu.np/",
            query="give me details about of pyshco social session "
        )
        
        # View statistics
        # adaptive.print_stats()  # if you want to view un comment 
        
        # Get the most relevant content
        relevant_pages = adaptive.get_relevant_content(top_k=5)
        for page in relevant_pages:
            print(f"- {page['url']} (score: {page['score']:.2f})")
            print(f"page content: {page['content']}")


if __name__ == "__main__":
    asyncio.run(get_contents_from_website("announcement of ev course"))