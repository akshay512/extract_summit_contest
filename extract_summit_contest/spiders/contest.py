import scrapy
import json
import re


class ContestSpider(scrapy.Spider):
    name = 'contest'
    allowed_domains = ['extract-summit-kokb7ng7-5umjfyjn4a-ew.a.run.app']
    start_urls = ['https://extract-summit-kokb7ng7-5umjfyjn4a-ew.a.run.app/clickhere?sort_by=alphabetically']

    def parse(self, response):
        item_links = response.css(".gtco-practice-area-item .gtco-copy a")
        yield from response.follow_all(item_links, self.parse_item)

        page_links = response.xpath("//a[contains(text(), 'Next Page')]")
        yield from response.follow_all(page_links)

    def parse_item(self, response):
        recommended_links = response.css(".team-item a")
        # print('recommended')
        # print(len(recommended_links)>0)
        yield from response.follow_all(recommended_links, self.parse_item)

        # il = TestItemLoader(response=response)
        # il.add_css("item_id", "#uuid::text")
        # il.add_css("name", "h2.heading-colored::text")
        telephone_number = response.css("#gtco-about > .container > div:nth-child(3) > script").get().split('"')[1]
        # print('telephone: '+telephone_number)

        cyphered_phone = [*telephone_number]
        telephone = ''
        for x in cyphered_phone:
            number = chr(ord(x) - 16)
            telephone += number

        item = {'item_id': response.css('#uuid::text').get(),
                'name': response.css('h2.heading-colored::text').get(),
                'phone': telephone}

        image_id_css = ".img-shadow ::attr(src)"
        image_id_pattern = r"/([\da-f-]+)\.jpg"
        image_id = response.css(image_id_css).re_first(image_id_pattern)
        if not image_id:
            script_xpath = "//script[contains(text(), 'mainimage')]"
            image_id = response.xpath(script_xpath).re_first(image_id_pattern)
        if image_id:
            item['image_id'] = image_id
        else:
            item['image_id'] = None

        rating = response.css('p:contains("Rating") span::text').get()
        if rating is None or "NO RATING" in rating:
            yield from response.follow_all(
                response.css("::attr(data-price-url)"),
                callback=self.parse_rating,
                cb_kwargs={"item": item},
            )
            return
        item['rating'] = rating

        yield item

    def parse_rating(self, response, item):
        item_res = item
        data = json.loads(response.text)
        item_res['rating'] = data.get("value")
        yield item_res
