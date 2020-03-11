import scrapy
from scrapy.loader import ItemLoader
from MZSbot.items import ReutersItem
import MZSbot.utils as ut
from datetime import timedelta, date


class ReutersSpider(scrapy.Spider):

    
    name = "euronews"

    def start_requests(self):

        base_url = 'https://www.euronews.com/'
        urls = ut.url_array_generator( base_url, date(2019,1,1), date(2020,1,1))

        for url in urls:
             yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for story in response.selector.xpath("//article"):
            loader = ItemLoader(item=ReutersItem() , selector=story , response=response)
            loader.add_xpath('title',".//h3/a/text()")
            loader.add_xpath('summary',".//p/text()")
            loader.add_xpath('date', ".//time/text()")
            loader.add_xpath('link',".//a/@href")
            #loader.add_xpath('country',".//span/text()")
            yield loader.load_item()


            
        new_page = response.selector.xpath("//a[@class='c-paginator__text c-next']/@href").extract_first()
        if new_page is not None :
            new_page_link = response.urljoin(new_page)
            yield scrapy.Request(url = new_page_link , callback= self.parse)

