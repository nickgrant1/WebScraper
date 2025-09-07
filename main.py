from crawl import *
import sys
import asyncio
from asynchcrawler import crawl_site_async
from csv_report import write_csv_report

async def main():
    print("Hello from webscraper!")
    length = len(sys.argv)
    if length<2:
        print('no website provided')
        sys.exit(1)
    if length>4:
        print('too many arguments provided')
        sys.exit(1)
    max_concurrency, max_pages = 3, 35
    if length>=3:
        max_concurrency=sys.argv[2]
        if length==4:
            max_pages=sys.argv[3]
    url = sys.argv[1]
    print(f'Starting crawl of: {url}')
    page_data = await crawl_site_async(url, int(max_concurrency), int(max_pages))
    write_csv_report(page_data)    

if __name__ == "__main__":
    asyncio.run(main())
