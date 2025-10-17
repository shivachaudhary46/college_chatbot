import os 

import asyncio
from crawl4ai import AsyncWebCrawler, AdaptiveCrawler, AdaptiveConfig
from pinecone import Pinecone

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

hf_key = os.environ["HUGGINGFACEHUB_API_TOKEN"]
api_key = os.environ["GOOGLE_API_KEY"]
INDEX_NAME = "mbmc-data"

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
    

# $if you have created new index and you are storing the document in to the vector then only use this function 
def embedding_and_storing(index_name, chunks):  # must have index name, and already chunked the store

    from langchain_pinecone import PineconeVectorStore
    from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

    embeddings = HuggingFaceEndpointEmbeddings(
        model= "mixedbread-ai/mxbai-embed-large-v1",
        task="feature-extraction",
        huggingfacehub_api_token=hf_key,
    )

    # print("only applicable if you have created a new Index....")
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=index_name
    )
    print("Documents successfully uploaded to pinecone!!")

    return vectorstore

# Splitting the paragraphs into smaller chunks. so we can easily store in the vector db 
def chunk_data(relevant_pages):
    from langchain_core.documents import Document
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    docs = []

    for page in relevant_pages:
        doc = Document(
            page_content=page.get('content', ''),  # or use 'markdown' if available
            metadata={
                "source": page.get('url', 'unknown'),
                "score": page.get('score', 0),
                "title": page.get('title', ''),
            }
        )
        docs.append(doc)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # chunk size (characters)
        chunk_overlap=200, # chunk overlap (characters)
        add_start_index=True # track index in original document
    )
    
    all_splits = text_splitter.split_documents(docs)
    return all_splits

# we can get the content from the websites
async def get_contents_from_website(query: str, start_url: str):

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
            start_url=start_url,
            query="give me details about of pyshco social session "
        )
        
        # View statistics
        # adaptive.print_stats()  # if you want to view un comment 
        
        # Get the most relevant content
        relevant_pages = adaptive.get_relevant_content(top_k=5)

        return relevant_pages
        # for page in relevant_pages:
        #     # print(f"- {page['url']} (score: {page['score']:.2f})")
        #     # print(f"page content: {page['content']}")

def ask_and_get_answer(vectorstore, q):
    from langchain.chains import RetrievalQA
    from langchain_google_genai import ChatGoogleGenerativeAI

    from langchain import PromptTemplate
    from langchain.chains.summarize import load_summarize_chain

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)
    answer = chain.invoke(q)
    return answer

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


async def main():
    print("Starting document crawling and store documents")

    relevant_pages = await get_contents_from_website(
        query="college information courses announcements",
        start_url="https://www.mbmc.edu.np"
    )

    chunks = chunk_data(relevant_pages)

    creating_new_index(INDEX_NAME)

    vector_store = embedding_and_storing(INDEX_NAME, chunks)

    print(f"Index '{INDEX_NAME}' is ready for querying")
            
if __name__ == "__main__":
    asyncio.run(main())
    # delete_pinecone_index()

