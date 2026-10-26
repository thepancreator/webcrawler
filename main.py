import crawl
import sys
import requests
import asynccrawler
from copy import deepcopy
import asyncio
import time

async def crawl_site_async(base_url:str, max_concurrency: int, max_pages: int):
    page_data = {}
    async with asynccrawler.AsyncCrawler(base_url, base_url, page_data, max_concurrency, max_pages) as async_crawler:
        return await async_crawler.crawl()

def crawl_page(base_url: str, current_url: str = None, page_data: dict[str, crawl.PageData] = None):
    if not current_url.startswith(base_url):
        return

    normalized_url = crawl.normalize_url(current_url)
    if normalized_url in page_data:
        return

    cur_html = get_html(current_url)

    page_data[normalized_url] = crawl.extract_page_data(cur_html, current_url)
    links = deepcopy(page_data[normalized_url]["outgoing_links"])
    if links == []:
        return
    for link in page_data[normalized_url]["outgoing_links"]:
        crawl_page(base_url, link, page_data)

def get_html(url:str) -> str:
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    if response.headers["content-type"].find("text/html") == -1:
        raise Exception(f"Error: content-type is not text/html, is {response.headers["content-type"]}")

    return response.text

async def main():
    if len(sys.argv) < 4:
        print('insufficient arguments; expected "url" max_concurrency max_pages')
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    if not isinstance(sys.argv[1], str):
        print(f'expected string for url: "www.example.com"')
        sys.exit(1)
    if not isinstance(int(sys.argv[2]), int):
        print(f'expected int for max_concurrency, received {sys.argv[2]}')
        sys.exit(1)
    if not isinstance(int(sys.argv[3]), int):
        print(f'expected int for max_pages')
        sys.exit(1)

    base_url = sys.argv[1]
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    print(f"starting crawl of {base_url}")
    print(f"maximum {max_concurrency} concurrent processe(s)")
    print(f"maximum {max_pages} total page(s) will be crawled")

    start = time.time()
    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)
    print(time.time() - start)
    for item in page_data:
        print(item)

if __name__ == "__main__":
    asyncio.run(main())
