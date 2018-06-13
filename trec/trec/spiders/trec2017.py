# -*- coding: utf-8 -*-
import scrapy
import re
import xlsxwriter

class Trec2017Spider(scrapy.Spider):
    name = 'trec2017'
    # allowed_domains = ['https://trec.nist.gov/pubs/trec26/trec2017.html']

    def start_requests(self):
        urls = ['file:///Users/Jens/Google Drive/self_learning/2018paper_spider/trec/trec2017.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'body-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        overall_author_list = []
        overall_affliation_list = []

        authors_list = response.xpath('/html/body/center/table/tr[7]//li').re(r'<br>\n(.*)<br>\n<br>')
        for authors in authors_list:
            if " - " in authors:
                authors_temp = authors.split(" - ")[0]
                affliation = authors.split(" - ")[1]

                for i in authors_temp.split(" and "):
                    overall_author_list.append(i)
                    overall_affliation_list.append(affliation)

        workbook = xlsxwriter.Workbook('trec2017.xlsx')
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'Name', bold)
        worksheet.write('B1', 'Affliation', bold)
        row = 1
        for i in range(len(overall_author_list)):
            worksheet.write_string(row, 0, overall_author_list[i])
            worksheet.write_string(row, 1, overall_affliation_list[i])
            row += 1
        workbook.close()
