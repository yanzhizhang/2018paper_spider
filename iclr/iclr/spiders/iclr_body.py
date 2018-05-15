import scrapy
import re
import numpy as np
import csv
from urllib.parse import urlparse
from scrapy.http import Request
from subprocess import call
import os

COUNTER = 0

class IclrSpider(scrapy.Spider):
    name = "iclr_body"

    def start_requests(self):
        urls = [
            'https://www.iclr.cc/Conferences/2018/Schedule?type=Poster'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        yield scrapy.Request(url="https://openreview.net/forum?id=H1T2hmZAb", callback=self.parse_pdf)

    def parse_pdf(self, response):
        href_pdf = response.selector.xpath('//meta').re(r'"citation_pdf_url" content="(.*)"')[0]
        return Request(url=response.urljoin(href_pdf), callback=self.save_pdf)

    def save_pdf(self, response):
        global COUNTER
        path = str(COUNTER) +".pdf"
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
        str(COUNTER)+".txt"
        call(["python", "pdf2txt.py", path, "-o", str(COUNTER)+".txt", "-p", "1"])

        with open(str(COUNTER)+".txt", 'r') as f:
            lines = f.readlines()


        pattern  = '(.*@.*)'
        new_files = ""
        for line in lines:
            match = re.search(pattern, line)
            if match:
                # print(match.group())
                new_files += match.group() + " "
        #new_files就是所有email在一个string

        while "{" in new_files:
            match_author = re.search('{(.*)}', new_files).group(1)
            match_affliation = re.search('}([a-zA-Z|\.]*)', new_files).group(1)

            temp = match_author.split(',')
            new_string = ""
            for i in range(len(temp)):
                temp[i] = temp[i] + match_affliation+" "
                new_string += temp[i]


            new_files = re.sub('({.*}[a-zA-Z|\.]*)',new_string ,new_files)

        # new_line = ""
        # for i in new_files.split(" "):
        #     if re.search("(@.*)",i):
        #         new_line += re.search("(@.*)",i).group(1)+ " "

        text_file = open(str(COUNTER)+"affliation.txt", "w")
        text_file.write("%s" % new_files)
        text_file.close()


        COUNTER += 1


    def parse(self, response):
        page = response.url.split("/")[-2]

        filename = 'body-%s.html' % page

        authors_list = response.css("div.maincardFooter").re(r">(.*)<")
        titles_list = response.css("div.maincardBody").re(r'Body">(.*)</div>')
        hrefs_list = response.selector.xpath('//a[contains(@href,"open")]').re('(https://openreview.net/forum\?id=.*)" class="btn b')

        for counter, href in enumerate(hrefs_list):
            yield Request(url=response.urljoin(href),callback=self.parse_pdf)

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        for i in range(COUNTER):
            os.remove(str(i)+".pdf")


        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['authors', 'titles', 'hrefs'])
            writer.writeheader()

            for i in range(len(authors_list)):
                writer.writerow({"authors": authors_list[i],"titles": titles_list[i],"hrefs": hrefs_list[i]})
