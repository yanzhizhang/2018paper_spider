# -*- coding: utf-8 -*-
import scrapy
import re
import xlsxwriter

temp_1 = []
temp_2 = []
temp_3 = []

class CvpapersSpider(scrapy.Spider):
    name = 'cv_papers'
    allowed_domains = ['cvpapers.com']
    start_urls = ['http://cvpapers.com/']

    def parse(self, response):
        for raw_link in response.xpath("//*[@id='content']/div[1]/div[1]//li/a").extract():
            link = re.search('<a href="(.*)">.*</a>', raw_link).group(1)
            next_page = response.urljoin(link)
            if "cvpapers.com" in next_page:
                yield scrapy.Request(next_page, callback=self.parse_page)



    def parse_page(self, response):
        paper_title = response.xpath('//*[@id="content"]/dl/dt').extract()
        authors_name = response.xpath('//*[@id="content"]/dl/dd').extract()
        venue = response.url.split("/")[-1].split(".")[0]
        for i in range(len(paper_title)):
            paper_title[i] = re.sub('\<.*?\>','',paper_title[i])
            authors_name[i] = re.sub('\<.*?\>','',authors_name[i])
            self.record(paper_title[i], authors_name[i], venue)

    def record(self, title, author, venue):
        temp_1.append(title)
        temp_2.append(author)
        temp_3.append(venue)
        if len(temp_1) == 10284:
            self.writeToXlsx()


    def writeToXlsx(self):
        workbook = xlsxwriter.Workbook('cvpr.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'title', bold)
        worksheet.write('B1', 'authors', bold)
        worksheet.write('C1', 'venue', bold)
        row = 1

        for i in range(len(temp_1)):
            worksheet.write_string  (row, 0, temp_1[-i])
            worksheet.write_string  (row, 1, temp_2[-i])
            worksheet.write_string  (row, 2, temp_3[-i])
            row += 1
        workbook.close()
