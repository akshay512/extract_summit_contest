import scrapy
from ..items import ContestTestItem


class ContestTestSpider(scrapy.Spider):
    name = 'contest_test'
    allowed_domains = ['web-5umjfyjn4a-ew.a.run.app']
    start_urls = ['http://web-5umjfyjn4a-ew.a.run.app/clickhere']

    def parse(self, response):
        item_links = response.css('.gtco-practice-area-item .gtco-copy a')

        yield from response.follow_all(item_links,self.parse_item)

        next_page = response.xpath("//a[contains(text(),'Next Page')]")

        yield from response.follow_all(next_page)

    def parse_item(self, response):
        id = response.css('#uuid::text').get()
        item_name = response.css('.heading-colored::text').get()
        rating = response.css('p:contains("Rating") span::text').get()
        if 'NO RATING' in rating:
            response.follow_all(response.css('::attr(data-price-url)'),
                                callback=self.parse_rating,
                                cb_kwargs={"item": ContestTestItem(item_id=id,name=item_name)}
                                )
            rating == response.css('.price::text').extract_first()

        yield ContestTestItem(item_id=id,name=item_name,rating=rating)

        # item = ContestTestItem ()
    # def parse_rating(self,response,item):

