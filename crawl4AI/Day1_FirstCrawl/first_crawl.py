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
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_config = BrowserConfig(verbose=True)
    run_config = CrawlerRunConfig(
        # Content filtering
        word_count_threshold=10,
        excluded_tags=['form', 'header'],
        exclude_external_links=True,

        # Content processing
        process_iframes=True,
        remove_overlay_elements=True,

        # Cache control
        cache_mode=CacheMode.ENABLED  # Use cache if available
    )

    async with AsyncWebCrawler(browser_configconfig=browser_config) as crawler:
        result = await crawler.arun(
            url="https://example.com",
            run_config=run_config
        )

        if result.success:
            # Print clean content
            print("Content:", result.markdown[:500])  # First 500 chars

            # Process images
            for image in result.media["images"]:
                print(f"Found image: {image['src']}")

            # Process links
            for link in result.links["internal"]:
                print(f"Internal link: {link['href']}")

        else:
            print(f"Crawl failed: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())


