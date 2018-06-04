# -*- coding: utf-8 -*-
import scrapy
import re
import xlsxwriter


class SigmodSpider(scrapy.Spider):
    name = 'SIGMOD'
    allowed_domains = ['sigmod2018.org']

    def start_requests(self):
        urls = ['https://sigmod2018.org/sigmod_research_list.shtml']
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
        for i in response.xpath('//div[@id="maincontent"]/div/ul/li'):
            authors = i.re('</strong>(.*)</li>')[0].split("); ")
            for j in authors:
                author_list.append(re.search('(.*)\s\(', j).group(1))
                temp = re.search('\s\((.*)', j).group(1)
                affliation_list.append(re.sub('(\))', '', temp))

        workbook = xlsxwriter.Workbook('SIGMOD2018.xlsx')
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
