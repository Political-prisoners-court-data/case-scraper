from collections.abc import Iterable
from datetime import datetime
from typing import Any

from scrapy import Spider
from scrapy.http import Response

from demhack8.items import RfmPersonItem, RfmPersonUnparsedItem


class RfmSpider(Spider):
    name = 'rfm'
    allowed_domains = ['www.fedsfm.ru']
    start_urls = ['https://www.fedsfm.ru/documents/terrorists-catalog-portal-act']

    def parse(self, response: Response, **kwargs: Any) -> Iterable[RfmPersonItem]:
        for person in response.css('#russianFL .terrorist-list li::text'):
            record = person.get()
            remainder = record.rstrip('; ')
            name, _, remainder = remainder.partition(',')
            is_terr = name.strip().endswith('*')
            name = name.strip().rstrip('*').strip()
            val, _, remainder = remainder.partition(',')
            if val.strip().startswith('(') and val.strip().endswith(')'):
                aliases = [alias.strip() for alias in val[1:-1].split(',')]
                val, _, remainder = remainder.partition(',')
            else:
                aliases = None
            if val.strip() == '':
                birth_date = None
            else:
                try:
                    birth_date = datetime.strptime(val.strip(), '%d.%m.%Y г.р.').date()
                except ValueError:
                    yield RfmPersonUnparsedItem(record)
                    continue
            address = remainder.strip(', ')
            if address == '':
                address = None
            yield RfmPersonItem(name, aliases, is_terr, birth_date, address)
