import asyncio
import aiohttp
from urllib.parse import urlparse
from crawl import normalize_url, extract_page_data, get_urls_from_html

class AsynchCrawler:
    def __init__(self, base_url, base_domain, max_concurrency, max_pages):
        (self.base_url,
        self.base_domain,
        self.page_data,
        self.lock,
        self.max_concurrency,
        self.semaphore,
        self.session,
        self.max_pages,
        self.should_stop,
        self.all_tasks,
        self.page_count
         ) = (base_url,
         base_domain,
         {},
         asyncio.Lock(),
         max_concurrency,
         asyncio.Semaphore(max_concurrency),
         None,
         max_pages,
         False,
         set(),
         0)
    
    async def __aenter__(self):
	    self.session = aiohttp.ClientSession()
	    return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        if self.should_stop:
            return False
        
        async with self.lock:
            if normalized_url in self.page_data:
                return False

            self.page_count += 1
            self.page_data[normalized_url] = None
            if self.page_count >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
            return True

    async def get_html(self, url):
        headers={"User-Agent": "BootCrawler/1.0"}
        try:
            async with self.session.request('GET', url=url, headers=headers) as r:
                if r.status>=400:
                    return
                if r.content_type != 'text/html':
                    print(f'Content type is not text/html... Skipping: {url}')
                    return
                return await r.text()
        except Exception as e:
            print('REQ ERROR', url, e)
            return
    
    async def crawl_page(self, base_url, current_url=None):
        if not await self.domain_check(current_url):
            return
        normalized_current_url = normalize_url(current_url)

        async with self.semaphore:
            current_html = await self.get_html(current_url)
            if current_html is None:
                return
            current_page_data = extract_page_data(current_html, current_url)
            async with self.lock:
                self.page_data[normalized_current_url] = current_page_data
            if self.should_stop:
                return
            urls = get_urls_from_html(current_html, current_url)
            for url in urls:
                normalized_child_url = normalize_url(url)
                if not await self.domain_check(url):
                    continue
                if not await self.add_page_visit(normalized_child_url):
                    continue
                print(f'Crawling: {url}')
                task = self.make_tracked(base_url, url)


    def make_tracked(self, base_url, url):
        async def run():
            try:
                await self.crawl_page(base_url, url)
            finally:
                self.all_tasks.discard(asyncio.current_task())  

        task = asyncio.create_task(run())
        self.all_tasks.add(task)           
        return task
    
    async def crawl(self):
        if await self.add_page_visit(normalize_url(self.base_url)):
            self.make_tracked(self.base_url, self.base_url)

        while self.all_tasks:
            await asyncio.gather(*self.all_tasks, return_exceptions=True)
        return {k: v for k, v in self.page_data.items() if v}
        
    async def domain_check(self, url):
        return urlparse(url).netloc == self.base_domain

async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsynchCrawler(base_url, urlparse(base_url).netloc, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()


        