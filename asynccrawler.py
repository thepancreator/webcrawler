import crawl
import asyncio
import aiohttp
from copy import deepcopy

class AsyncCrawler:
    def __init__(self,
        base_url: str,
        base_domain: str,
        page_data: dict[str, crawl.PageData],
        max_concurrency: int = 1,
        max_pages: int = 25
    ) -> None:
        self.base_url = base_url
        self.base_domain = base_domain
        self.page_data = page_data or {}
        self.visited = set(())
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set(())


    async def __aenter__(self):
        '''Opens aiohttp session'''
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        '''Closes aiohttpe session'''
        await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        '''Checks if normalized_url has already been visited, returns False if it has, adds it to set and returns True if not'''
        async with self.lock:
            if normalized_url in self.visited:
                return False
            else:
                self.visited.add(normalized_url)
                self.should_stop = len(self.visited) > self.max_pages
                if self.should_stop:
                    print(f"Reached maximum number of pages to crawl ({self.max_pages} pages)")
                    return False
                return True

    async def get_html(self, url:str) -> str:
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
            if response.status > 399:
                raise Exception(f"Error: server responded with error code {response.status}")
            if "text/html" not in response.headers.get("content-type", ""):
                raise Exception(f"Error: content-type is not text/html, is {response.headers["content-type"]}")

            return await response.text()

    async def crawl_page(self, current_url: str):
        try:
            if self.should_stop:
                return
            if not current_url.startswith(self.base_url):
                return

            normalized_url = crawl.normalize_url(current_url)
            visited = not await self.add_page_visit(normalized_url)
            if visited:
                return
            print(f"crawling {normalized_url}")

            async with self.semaphore:
                cur_html = await self.get_html(current_url)

            async with self.lock:
                self.page_data[normalized_url] = crawl.extract_page_data(cur_html, current_url)


            links = deepcopy(self.page_data[normalized_url]["outgoing_links"])
            if links == []:
                return

            for link in links:
                task = asyncio.create_task(self.crawl_page(link))
                self.all_tasks.add(task)

            if self.should_stop:
                return
        finally:
            self.all_tasks.discard(asyncio.current_task())


    async def crawl(self) -> crawl.PageData:
        await self.crawl_page(self.base_url)
        while self.all_tasks:
            await asyncio.gather(*self.all_tasks)
        return self.page_data
