from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    split_result = urlsplit(url)
    return f"{split_result.netloc}{split_result.path}".rstrip("/")
