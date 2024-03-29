import scrapy


class RfmSpider(scrapy.Spider):
    name = "rfm"
    allowed_domains = ["www.fedsfm.ru"]
    start_urls = ["https://www.fedsfm.ru/documents/terrorists-catalog-portal-act"]

    def parse(self, response):
        pass
