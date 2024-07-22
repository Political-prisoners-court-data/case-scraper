import re
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
    re_number = re.compile(r'^\d+\.')

    def parse(self, response: Response, **kwargs: Any) -> Iterable[RfmPersonItem]:
        for person in response.css('#russianFL .terrorist-list li::text'):
            record = person.get()
            remainder = record.rstrip('; ')
            full_name, _, remainder = remainder.partition(',')
            full_name = full_name.strip()
            is_terr = full_name.endswith('*')
            if is_terr:
                full_name = full_name[:-1]
            full_name = self.re_number.sub('', full_name).strip()
            val, _, remainder = remainder.partition(',')
            val = val.strip()
            if val.startswith('(') and val.endswith(')'):
                aliases = [alias.strip() for alias in val[1:-1].split(',')]
                val, _, remainder = remainder.partition(',')
            else:
                aliases = None
            val = val.strip()
            if val == '':
                birth_date = datetime.min
            else:
                try:
                    birth_date = datetime.strptime(val, '%d.%m.%Y г.р.').date()
                except ValueError:
                    yield RfmPersonUnparsedItem(record)
                    continue
            address = remainder.strip(', ')
            if address == '':
                address = None
            yield RfmPersonItem(full_name, aliases, is_terr, birth_date, address)
