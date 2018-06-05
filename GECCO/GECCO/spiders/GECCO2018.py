# -*- coding: utf-8 -*-
import scrapy
import re
import xlsxwriter

class Gecco2018Spider(scrapy.Spider):
    name = 'GECCO2018'
    allowed_domains = ['gecco-2018.sigevo.org/']

    def start_requests(self):
        urls = ['http://gecco-2018.sigevo.org/index.html/tiki-index.php?page=Accepted%20Papers',
                ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'body-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        author_list = []
        affliation_list = []
        print("LETS GET STARTED")
        for index, i in enumerate(response.xpath('//tr/td')):
            if ((index+1) % 3 )== 0:
                authors = i.re('>(.*)<')[0].split("), ")
                for j in authors:
                    author_list.append(j.split(" (")[0])
                    affliation_list.append(j.split(" (")[1])
                    print(j.split(" (")[0])

        workbook = xlsxwriter.Workbook('gecco2018.xlsx')
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'Name', bold)
        worksheet.write('B1', 'Affliation', bold)
        row = 1
        for i in range(len(author_list)):
            worksheet.write_string(row, 0, author_list[i])
            worksheet.write_string(row, 1, affliation_list[i])
            row += 1
        workbook.close()
