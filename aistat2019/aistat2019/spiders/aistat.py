# -*- coding: utf-8 -*-
import scrapy
import re
import xlsxwriter

class AistatSpider(scrapy.Spider):
    name = 'aistat'
    allowed_domains = ['www.aistats.org/']

    def start_requests(self):
        urls = ['https://www.aistats.org/accepted.html']
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
        for index, i in enumerate(response.xpath('//tr/td[@class="tg-jogk"]')):
            if index % 2 == 1:
                authors = i.re('>(.*)<')[0]
                for j in authors.split('; '):
                    author_list.append(j.split(',')[0])
                    print(j.split(',')[0])
                    if len(j.split(',')) == 2:
                        affliation_list.append(j.split(', ')[1])
                    else:
                        affliation_list[-1] = affliation_list[-1]+j

        workbook = xlsxwriter.Workbook('aistat2019.xlsx')
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
