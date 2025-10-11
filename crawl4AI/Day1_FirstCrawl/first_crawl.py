'''
Basic Installation of crawl4ai
$ pip install crawlai

You can run diagnostics to confirm everything is functioning:
crawl4ai-doctor

`
you can go to this website for more information: 

https://docs.crawl4ai.com/core/quickstart/
`
'''

# import asyncio
# from crawl4ai import AsyncWebCrawler
# from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

# async def main():
#     browser_config = BrowserConfig()   # Default browser configuration
#     run_config = CrawlerRunConfig() # Default crawl run configuration

#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         result = await crawler.arun(
#             url="https://chatgpt.com",
#             config=run_config
#         )
#         print(result.markdown) # print clean markdown content

# def configCrawling():
#     browser_config = BrowserConfig()

#     config = CrawlRunConfig(
#         markdown_generator=DefaultMarkdownGenerator(
#             content_filter=PruningContentFilter(threshold=0.6),
#             options={"ignore_links": True}
#         )
#     )
    
#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         result = await crawler.arun(
#             url="https://chatgpt.com",
#             config=config
#         )

# if __name__ == "__main__":
#     # asyncio.run(main())
#     asyncio.run(configCrawling())

import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai import BrowserConfig, CrawlerRunConfig 
from crawl4ai import DefaultMarkdownGenerator, PruningContentFilter

config = CrawlerRunConfig(
    markdown_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.6),
        options={"ignore_links": True}  
    )
)

async def main():
    browser_config = BrowserConfig()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://github.com",
            run_config=config
        )

        # print(result.html)
        # print(result.cleaned_html)  # cleaned HTML 
        # print(result.markdown.raw_markdown) # raw markdown from cleaned HTML 
        # print(result.markdown.fit_markdown) # most relevant content in markdown

        print(result.success)
        print(result.status_code)

        if not result.success:
            print(f"crawl failed: {result.error_message}")
            print(f"status code: {result.status_code}")

        # print()
        # print(result.media)
        # print(result.links)

        
if __name__ == "__main__":
    asyncio.run(main())
 