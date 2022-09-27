# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional

from itemloaders.processors import Compose, Join, TakeFirst
from scrapy.loader import ItemLoader

class ExtractSummitContestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

@dataclass
class ContestTestItem:
    item_id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    image_id: Optional[str] = field(default=None)
    rating: str = field(default_factory=str)
