from urllib.parse import urlparse
import scrapy

from scrapy.http import Request

class PapersFile(scrapy.Item):
    author = scrapy.Field()
    href = scrapy.Field()


class CvprSpider(scrapy.Spider):
    name = "CVPR2017pdf"

    def start_requests(self):
        urls = [
            'http://openaccess.thecvf.com/CVPR2017.py'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        for href in hrefs[0:9]:
            if href.endswith('.pdf'):
                yield Request(
                    url=response.urljoin(href),
                    callback=self.save_pdf
                )

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
