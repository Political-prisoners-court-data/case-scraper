from scrapy import Spider
from scrapy.http import Response

from demhack8.items import RfmPersonItem, RfmOrgItem


class RfmSpider(Spider):
    name = "rfm"
    allowed_domains = ["www.fedsfm.ru"]
    start_urls = ["https://www.fedsfm.ru/documents/terrorists-catalog-portal-act"]

    def parse(self, response: Response):
        for org in response.css("#russianUL .terrorist-list li::text"):
            yield RfmOrgItem(org.get())
        for person in response.css("#russianFL .terrorist-list li::text"):
            yield RfmPersonItem(person.get())
