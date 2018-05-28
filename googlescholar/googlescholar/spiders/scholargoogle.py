# -*- coding: utf-8 -*-
import scrapy
from urllib.request import urlopen
from bs4 import BeautifulSoup

class ScholargoogleSpider(scrapy.Spider):
    name = 'scholargoogle'

    def start_requests(self):
        urls = ['https://scholar.google.com/citations?hl=en&authuser=1&view_op=search_authors&mauthors=label%3Aartificial_intelligence&btnG=']
        for url in urls:
            content = urlopen(url).read()
            soup = BeautifulSoup(content, "lxml")
            page = url.split("/")[-2]
            with open('1.html', 'w') as f:
                f.write(soup.prettify())
            yield scrapy.Request("file:///Users/Jens/Google Drive/self_learning/2018paper_spider/1.html", callback = self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'body-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        # general Information
        response.xpath('//div[@class = "gsc_1usr gs_scl"]')
