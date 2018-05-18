# -*- coding: utf-8 -*-
import scrapy
import xlsxwriter

global_authors_list = []
global_affliation_list = []


class Top1000researchSpider(scrapy.Spider):
    name = 'top1000research'
    # allowed_domains = ['http://www.guide2research.com/scientists/']

    def start_requests(self):
        urls = [
            'http://www.guide2research.com/scientists/page-1',
            'http://www.guide2research.com/scientists/page-2',
            'http://www.guide2research.com/scientists/page-3',
            'http://www.guide2research.com/scientists/page-4',
            'http://www.guide2research.com/scientists/page-5',
            'http://www.guide2research.com/scientists/page-6',
            'http://www.guide2research.com/scientists/page-7',
            'http://www.guide2research.com/scientists/page-8',
            'http://www.guide2research.com/scientists/page-9',
            'http://www.guide2research.com/scientists/page-10'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]

        filename = 'body-%s.html' % page

        authors_list = response.xpath('//table')[3:103].re(r'<h3 style="margin-bottom:1px;"><a href=".*>(.*)</a></h3>\n\t\t\t\t')
        affliation_list = response.xpath('//table')[3:103].re(r'"http://www.guide2research.com/scientists/uni-[0-9]*">([a-zA-Z| ]*)')

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        global_authors_list.extend(authors_list)
        global_affliation_list.extend(affliation_list)

        workbook = xlsxwriter.Workbook('guide2reserach.xlsx')
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'Name', bold)
        worksheet.write('B1', 'Affliation', bold)

        row = 1
        for i in range(len(global_authors_list)):
            worksheet.write_string  (row, 0, global_authors_list[i])
            worksheet.write_string  (row, 1, global_affliation_list[i])
            row += 1
        workbook.close()
