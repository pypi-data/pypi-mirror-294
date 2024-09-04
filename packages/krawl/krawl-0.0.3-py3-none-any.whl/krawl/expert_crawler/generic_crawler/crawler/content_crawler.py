"""
Example
-------
>>> python companyshot/mine_landingpage.py check https://www.glean.ai/
"""


from krawl.common.flow import CrawlerBase
from krawl.common.recognizers import MainTextRecognizer, SoupGrabber
from krawl.common.schema.dtypes import Href, StructuredResponse
from krawl.common.soup_utils import HtmlPageReader
from krawl.common.textware import TextFilter


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class GenericCrawler(CrawlerBase):

    def __init__(self):
        self.reader = HtmlPageReader()
        self.text_getter = MainTextRecognizer()

    def check_content(
        self,
        url: str
    ) -> str:
        soup = self.reader.get_soup(url=url)
        text = self.text_getter.check(node=soup, base_url=url)
        return text

    def check_content_structured(
        self,
        url: str,
        see: set = {"*"}
    ) -> StructuredResponse:

        try:
            soup = self.reader.get_soup(url=url)
            failed = False
        except Exception as err:
            print(f"SOUPERR: {err}")
            failed = True
        if (
            soup is None or
            failed
        ):
            return StructuredResponse(
                title="",
                h1=[],
                h2=[],
                text="",
                links=[],
                image_url_primary=""
            )

        # Check what to see
        see_all = "*" in see
        see_title = "title" in see or see_all
        see_h1 = "h1" in see or see_all
        see_h2 = "h2" in see or see_all
        see_text = "text" in see or see_all
        see_links = "links" in see or see_all
        see_image = "image" in see or see_all

        text = self.text_getter.check(soup, base_url=url) if see_text else ""
        links = SoupGrabber.links(soup=soup, base_url=url) if see_links else []
        img = SoupGrabber.image_primary(soup, url) if see_image else ""
        resp = StructuredResponse(
            title=SoupGrabber.title(soup=soup) if see_title else "",
            h1=SoupGrabber.h1_all(soup=soup) if see_h1 else [],
            h2=SoupGrabber.h2_all(soup=soup) if see_h2 else [],
            text=text,
            coretext=TextFilter.corepart(text),
            links=[Href(**item) for item in links],
            image_url_primary=img
        )
        return resp
