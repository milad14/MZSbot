import scrapy
from scrapy.loader import ItemLoader
from MZSbot.items import ReutersItem


class ReutersSpider(scrapy.Spider):
    name = "reuters"

    def start_requests(self):

        url = 'https://www.reuters.com/news/archive?view=page&page=2&pageSize=10'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for story in response.selector.xpath("//article[@class='story ']"):
            loader = ItemLoader(item=ReutersItem() , selector=story , response=response)
            loader.add_xpath('title',".//div[@class='story-content']/a/h3/text()")
            loader.add_xpath('summary',".//div[@class='story-content']/p/text()")
            loader.add_xpath('date', ".//div[@class='story-content']/time/span/text()")
            loader.add_xpath('link',".//div[@class='story-content']/a/@href")
            yield loader.load_item()


            
        new_page = response.selector.xpath("//a[@class='control-nav-next']/@href").extract_first()
        if new_page is not None :
            new_page_link = response.urljoin(new_page)
            yield scrapy.Request(url = new_page_link , callback= self.parse)

