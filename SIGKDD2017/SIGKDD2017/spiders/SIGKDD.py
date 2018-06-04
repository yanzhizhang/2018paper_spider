# -*- coding: utf-8 -*-
import scrapy
import re
import xlsxwriter


class SigkddSpider(scrapy.Spider):
    name = 'SIGKDD'

    def start_requests(self):
        urls = ['http://www.kdd.org/kdd2017/accepted-papers']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        authors_affliations_list = ";".join(response.xpath('//small').re(r'Author\(s\): (.*)</small>'))
        author_list = []
        affliation_list = []
        for author_affliation in authors_affliations_list.split(");"):
            if (re.match(r'Leonardo F. R. Ribeiro', author_affliation)) == None:
                match = author_affliation.split("(")
                author_list.append(match[0])
                affliation_list.append("(".join(match[1:]))
            else:
                match = "Leonardo F. R. Ribeiro (Federal University of Rio de Janeiro), Pedro H. P. Saverese (Federal University of Rio de Janeiro), Daniel R. Figueiredo (Federal University of Rio de Janeiro)"
                for author_affliation in match.split('), '):
                    author_list.append(author_affliation.split(' (')[0])
                    affliation_list.append(author_affliation.split(' (')[1])

        workbook = xlsxwriter.Workbook('2017SIGKDD.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'Name', bold)
        worksheet.write('B1', 'Affliation', bold)

        for i in range(len(author_list)):
            worksheet.write(i+1, 0, author_list[i])
            worksheet.write(i+1, 1, affliation_list[i])
