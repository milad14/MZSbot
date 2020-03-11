import scrapy
from scrapy.loader import ItemLoader
from MZSbot.items import ReutersItem
import json

# ***ATTENTION***
#This spider is not ready to invoke

class MyFirstSpider(scrapy.Spider):
    name = "nytimes"


    allowed_domains = ['https://www.nytimes.com/section/world']
    start_urls = ['https://samizdat-graphql.nytimes.com/graphql/v2']

   
    def request(self, url, callback):
        """
         wrapper for scrapy.request
        """

        headers = {"accept-ranges": "bytes", "access-control-allow-credentials": "true","access-control-allow-origin": "https://www.nytimes.com","access-control-expose-headers": "x-nyt-audience-target-flat, x-nyt-continent, x-nyt-country, x-nyt-region, x-nyt-meridiem, x-nyt-gmt-offset"}
        cookies = {"__gads":"ID=da7a64ce6a7b6884:T=1583078357:S=ALNI_MbFXw-_evMG-8sDD6E5_Z7m3O6MBA","_gcl_au":"1.1.1669986619.1583078355","b2b_cig_opt":"{\"isCorpUser\":false}","datadome":"Y1WUQqQdsIrHBtO3YtL8K2HH50BP_UjnYUe7jcMpBe2zZ6Yk0w8cs2eyco~ufphHXGBb8hR1UbBmpRfU7epOYOJ1I16H6cR4qcZE4vfgLr","edu_cig_opt":"{\"isEduUser\":false}","iter_id":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI1ZTViZGJkZGI4NDA5NTAwMDFmYmY0YzUiLCJjb21wYW55X2lkIjoiNWMwOThiM2QxNjU0YzEwMDAxMmM2OGY5IiwiaWF0IjoxNTgzMDc4MzY1fQ.4QAmwytrANIH2xuEXA6tecHr4q1dskoBx4c0w1NqP0s","nyt-a":"favRptQlNBv3dcH4X1B8Dw","nyt-gdpr":"0","nyt-geo":"IR","nyt-jkidd":"uid=0&lastRequest=1583937794131&activeDays=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1]&adv=5&a7dv=4&a14dv=5&a21dv=5&lastKnownType=anon","nyt-m":"7DDF7584AA3459EEBAC16CB86E410E2F&l=l.1.3820291994&ier=i.0&iub=i.0&igd=i.1&iga=i.0&n=i.2&g=i.1&ica=i.0&igf=i.0&iru=i.0&uuid=s.0c9f2ea7-b575-4ef9-9cdf-ea4f107178c0&e=i.1585699200&t=i.1&pr=l.4.0.0.0.0&ft=i.0&fv=i.0&cav=i.1&imu=i.1&igu=i.1&prt=i.0&er=i.1583921100&s=s.core&vr=l.4.0.0.0.0&ira=i.0&iir=i.0&v=i.1&rc=i.0&iue=i.0&ird=i.0&vp=i.0&ifv=i.0&imv=i.0","nyt-purr":"cfhhcfh","NYT-T":"ok","optimizelyEndUserId":"oeu1583078355513r0.04448238494852985","purr-cache":"<K0<r<C_<G_","walley":"GA1.2.256983725.1583078356","walley_gid":"GA1.2.43124782.1583847793"}
 

        request = scrapy.Request(url=url, callback=callback)
        request.cookies.update(cookies)
        request.headers.update(headers)
        return request


    def start_requests(self):

        for i, url in enumerate(self.start_urls):
            yield self.request(url, self.parse)





    def parse(self, response):
        data = json.loads(response.txt)
        for news in data["search"]["hists"]["edges"]:
            yield {
                "title": news["node"]["node"]["promotionalHeadline"],
                "summary" : news["node"]["node"]["promotionalSummary"],
                "date": news["node"]["node"]["firstPublished"],
                "link": news["node"]["node"]["url"]
            }

        """
        for story in response.selector.xpath("//li[@class='css-ye6x8s']"):
            loader = ItemLoader(item=ReutersItem() , selector=story , response=response)
            loader.add_xpath('title',".//h2/text()")
            loader.add_xpath('summary',".//p/text()")
            loader.add_xpath('link',".//a/@href")
            loader.add_xpath('date',".//time/text()")
            yield loader.load_item()
"""
        new_page = response.selector.xpath("//button[@data-testid='search-show-more-button']").extract_first()
        url : 'https://samizdat-graphql.nytimes.com/graphql/v2'
        if new_page is not None :
            yield self.request(url, self.parse)

