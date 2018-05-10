import scrapy
import re
import numpy as np
import csv

class PapersFile(scrapy.Item):
    author = scrapy.Field()
    href = scrapy.Field()


class CvprSpider(scrapy.Spider):
    name = "iclr_body"

    def start_requests(self):
        urls = [
            'https://www.iclr.cc/Conferences/2018/Schedule?type=Poster'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]

        filename = 'body-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
