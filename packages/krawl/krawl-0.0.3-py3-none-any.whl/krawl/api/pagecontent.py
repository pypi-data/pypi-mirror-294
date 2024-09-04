"""
Public API for directly getting page content.
"""
from typing import List

from krawl.common.schema.dtypes import CrawlResponse, StructuredResponseGroup
from krawl.expert_crawler import GenericCrawler


def get_main_text(
    urls: List[str],
    max_char_len: int = 2000,
    min_paragraph_len: int = 3,
    max_paragraph_len: int = 2000
) -> CrawlResponse:
    crawler = GenericCrawler()
    texts = [
        crawler.check_content(url)
        for url in urls
    ]
    return CrawlResponse(
        first=texts[0],
        items=texts
    )


def get_main_content_structured(
    urls: List[str],
    max_char_len: int = 2000,
    min_paragraph_len: int = 3,
    max_paragraph_len: int = 2000
) -> StructuredResponseGroup:
    crawler = GenericCrawler()
    resp = [
        crawler.check_content_structured(url=url)
        for url in urls
    ]
    return StructuredResponseGroup(
        first=resp[0],
        items=resp
    )
