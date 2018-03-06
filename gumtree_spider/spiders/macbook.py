# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from urllib.parse import urljoin
import json


class MacbookSpider(scrapy.Spider):
    name = 'macbook'
    allowed_domains = ['gumtree.com.au']
    start_urls = [
        'https://www.gumtree.com.au/s-laptops/sydney/macbook/k0c18553l3003435/']
    base_url = 'http://www.gumtree.com.au'
    price_max = 1000

    def parse(self, response):
        main = response.xpath("//main[@class]").extract_first()
        link_itmes = Selector(text=main).xpath(
            ".//a[contains(@class,'user-ad-row') and contains(@class, 'link')]")
        for link_item in link_itmes:
            url = urljoin(
                self.base_url, link_item.xpath("@href").extract_first())
            title = link_item.xpath(
                ".//p[@class='user-ad-row__title']/text()").extract_first()
            price = link_item.xpath(
                ".//span[@class='user-ad-price__price']/text()").extract_first()
            if price:
                price = str(price).replace('$', '').replace(',', '')
            else:
                price = "0"
            abstract = link_item.xpath(
                ".//p[@class='user-ad-row__description']/span/text()").extract_first()
            location = link_item.xpath(
                ".//div[@class='user-ad-row__location']/text()").extract_first()
            location_area = link_item.xpath(
                ".//span[@class='user-ad-row__location-area']/text()").extract_first()

            if int(price) > 0 and int(price) < self.price_max:
                item = dict(url=url,
                            title=title,
                            price=price,
                            abstract=abstract,
                            location=f"{location_area} - {location}")
                print(json.dumps(item, sort_keys=True, indent=4))
                yield item
