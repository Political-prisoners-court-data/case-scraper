from dataclasses import dataclass
from datetime import date
from typing import Optional, ClassVar


@dataclass
class RfmPersonItem:
    table: ClassVar[str] = "rfm_person"
    full_name: str
    aliases: Optional[list[str]]
    is_terr: bool
    birth_date: Optional[date]
    address: Optional[str]


@dataclass
class RfmPersonUnparsedItem:
    text: str
