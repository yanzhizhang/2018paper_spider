import scrapy
import re
import numpy as np
import csv

class PapersFile(scrapy.Item):
    author = scrapy.Field()
    href = scrapy.Field()


class CvprSpider(scrapy.Spider):
    name = "CVPR2017"

    def start_requests(self):
        urls = [
            'http://openaccess.thecvf.com/CVPR2017.py'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]

        filename = 'body-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        filename = 'cspr-%s.html' % page


        # authors_list = response.css("div.bibref").extract()
        authors_list = response.css("div.bibref").re(r'author = {(.*)}')
        hrefs = response.xpath('//a[contains(@href, "papers")]').extract()
        hrefs_list = []
        for href in hrefs:
            hrefs_list.append(re.search(r'<a href="(.*)">pdf', href).group(1))

        cat_dict = {}
        for i in range(len(authors_list)):
            cat_dict["authors"] = authors_list[i]
            cat_dict["hrefs"] = hrefs_list[i]

        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['authors', 'hrefs'])
            writer.writeheader()
            # writer.writerow(cat_dict)
            # for i in cat_dict:
            #     print(i)
            #     writer.writerow(i)

            for i in range(len(authors_list)):
                writer.writerow({"authors": authors_list[i],"hrefs": hrefs_list[i]})
                # cat_dict["authors"] = authors_list[i]
                # cat_dict["hrefs"] = hrefs_list[i]


        # for item in zip(authors_list, hrefs_list):
        #     new_item = PapersFile()
        #     new_item['author'] = item[0]
        #     new_item['href'] = item[1]
        #
        # yield new_item
        # yield {
        #     "authors": authors_list,
        #     "hrefs": hrefs_list,
        # }
