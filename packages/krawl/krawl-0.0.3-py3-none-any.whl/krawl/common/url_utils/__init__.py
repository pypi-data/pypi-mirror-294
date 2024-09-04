
from urllib import parse


def fullhref(base: str, url: str) -> str:
    # url = (
    #     src.lstrip("/") if src.startswith("///") else
    #     parse.urljoin(base_url, src)
    # )
    return parse.urljoin(base, url)
