from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(url: str) -> str:
    split_result = urlsplit(url)
    return f"{split_result.netloc}{split_result.path}".rstrip("/")

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find("h1")
    if result:
        return result.get_text(strip=True)

    result = soup.find("h2")
    if result:
        return result.get_text(strip=True)

    return ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    if not soup.find("main"):
        if not soup.find("p"):
            return ""

        return soup.find("p").get_text(strip=True)

    main_para = soup.find("main").find("p")
    return main_para.get_text(strip=True) if isinstance(main_para, Tag) else ""

def get_urls_from_html(html: str, base_url: str) -> list[str] | str:
    try:
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        links = soup.find_all('a')
        for link in links:
            url = link.get('href') if link.get('href').startswith(base_url) else urljoin(base_url, link.get('href'))
            urls.append(url)
        return urls
    except Exception as e:
        return str(e)

def get_images_from_html(html: str, base_url: str) -> list[str] | str:
    try:
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        imgs = soup.find_all('img')
        for img in imgs:
            url = img.get('src') if img.get('src').startswith(base_url) else urljoin(base_url, img.get('src'))
            urls.append(url)
        return urls
    except Exception as e:
        return str(e)

def extract_page_data(html: str, page_url: str) -> PageData:
    data = {}
    data["url"] = page_url
    data['heading'] = get_heading_from_html(html)
    data['first_paragraph'] = get_first_paragraph_from_html(html)
    data['outgoing_links'] = get_urls_from_html(html, page_url)
    data['image_urls'] = get_images_from_html(html, page_url)
    return data
