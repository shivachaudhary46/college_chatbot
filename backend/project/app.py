input_text = input("enter the text: ")
print(input_text)

def decision_layer():
    pass 

from langchain_community.tools import DuckDuckGoSearchResults
def searchDuckDuckGo(query):
    search = DuckDuckGoSearchResults(output_format="list")
    results = search.invoke(query)
    return results 

results = searchDuckDuckGo(input_text)
urls = []
for result in results:
    urls += result['link']

import asyncio
from crawl4ai import adaptive

async def crawl_links(urls, query):
    tasks = [
        adaptive.digest(url, query)
        for url in urls 
    ]
    results = await asyncio.gather(*tasks)
    return results