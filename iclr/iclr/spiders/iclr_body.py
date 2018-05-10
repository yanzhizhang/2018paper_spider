import scrapy
import re
import numpy as np
import csv

class PapersFile(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
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

        authors_list = response.css("div.maincardFooter").re(r">(.*)<")
        titles_list = response.css("div.maincardBody").re(r'Body">(.*)</div>')
        hrefs_list = response.selector.xpath('//a[contains(@href,"open")]').re('(https://openreview.net/forum\?id=.*)" class="btn b')


        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['authors', 'titles', 'hrefs'])
            writer.writeheader()

            for i in range(len(authors_list)):
                writer.writerow({"authors": authors_list[i],"titles": titles_list[i],"hrefs": hrefs_list[i]})
