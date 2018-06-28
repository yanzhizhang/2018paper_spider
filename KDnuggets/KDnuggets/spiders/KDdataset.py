# -*- coding: utf-8 -*-
import scrapy
import xlsxwriter
import re


class KddatasetSpider(scrapy.Spider):
    name = 'KDdataset'
    allowed_domains = ['kdnuggets.com/datasets/']
    start_urls = ['https://www.kdnuggets.com/datasets/index.html']

    def parse(self, response):
        # raw_links = response.xpath('//*[@id="post-1219"]/ul[2]//a').extract()
        raw_name  = []
        raw_links = []
        raw_description = []
        # for link in raw_links:
        #     # print(repr(link))
        #     # if "Lyst" not in link:
        #     raw_name.append(re.search('>[\r\n]?(.*)</a>', repr(link)).group(1))
        #     link = re.search('href="(.*)">', link).group(1)
        #     # else:
        #     #     raw_name.append("Lyst Fashion Data Trends")
        #     #     link = "https://www.lyst.com/news/lyst-data-request/"
        # raw_description = response.xpath('//*[@id="post-1219"]/ul[2]//li').extract()
        for description in response.xpath('//*[@id="post-1219"]/ul[2]//li').extract():
            print(repr(description))
            raw_name.append(re.search('<a href=.*>[\r\n]?(.*)</a>', repr(description)).group(1))
            raw_links.append(re.search('href="(.*)">', repr(description)).group(1))
            raw_description.append(re.search('</a>[,|:|\s]?(.*)[\r\n]?', repr(description)).group(1))

        self.writeToXlsx(raw_name, raw_description, raw_links)

    def writeToXlsx(self, name, description, link):
        workbook = xlsxwriter.Workbook('KDdataset.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'name', bold)
        worksheet.write('B1', 'description', bold)
        worksheet.write('C1', 'link', bold)
        row = 1

        for i in range(len(name)):
            worksheet.write_string  (row, 0, name[i])
            worksheet.write_string  (row, 1, description[i])
            worksheet.write_string  (row, 2, link[i])
            row += 1
        workbook.close()
