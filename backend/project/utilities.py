from crawl4ai import AsyncWebCrawler, AdaptiveCrawler, AdaptiveConfig
from pinecone import Pinecone
import os

def creating_new_index(index_name):
    from pinecone import ServerlessSpec

    pc = Pinecone(
        api=os.environ.get("PINECONE_API_KEY")
    )

    if index_name not in pc.list_indexes():
        # if we could not find the index-name in the pinecone we have to create a new one
        print(f"Creating an index name...........{index_name}")
        pc.create_index(
            index_name,
            dimension=1024,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        print("Done creating Index..")

    else:
        print(f"Index {index_name} already exists.....", ends='')


async def get_contents_from_website(query: str, start_url: str):

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
            start_url=start_url,
            query="give me details about of pyshco social session "
        )
        
        # Get the most relevant content
        relevant_pages = adaptive.get_relevant_content(top_k=5)

        return relevant_pages