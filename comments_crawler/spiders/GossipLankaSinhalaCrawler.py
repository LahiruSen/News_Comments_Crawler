import scrapy
import json
from pathlib import Path
from random import randrange
from scrapy.shell import inspect_response
from scrapy import Request

class GossipLankaSinhalaCrawler(scrapy.Spider):
    name = "GossipLankaSinhalaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.gossiplankanews.com/'
    ]

    def writeToJson(self, header, time, content, url,comments):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content,
            'Comments': comments
        }
        # self.data['news'].append({  
        #     'Header': header,
        #     'Time': time,
        #     'Content': content
        # })

        Path("./data/gossiplanka/sinhala").mkdir(parents=True, exist_ok=True)

        name = str(randrange(1000000))

        with open("./data/gossiplanka/sinhala/" + name + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css("div.title h1 a ::attr(href)").getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        yield scrapy.Request(response.css("span.next-entries a ::attr(href)").get(), self.parse)

    def parseNews(self, response):
        inspect_response(response, self)
        # header = response.css("div.title h1 a ::text").get()
        # content = response.css("div.entry ::text").getall()
        # time = response.url.split("/")[3] + "/" + response.url.split("/")[4]
        # url = response.url
        # comments = response.css("div.idc ::text").getall()
        # self.writeToJson(header, time, content, url,comments)



