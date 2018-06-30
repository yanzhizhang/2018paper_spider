# -*- coding: utf-8 -*-
import scrapy
import re
import xlsxwriter
all_titles = []
all_authors = []
all_href = []

class AclAnthologySpider(scrapy.Spider):
    name = 'acl_anthology'
    # allowed_domains = ['aclweb.org/']
    start_urls = ['http://aclweb.org/anthology/']



    def parse(self, response):
        acl_event = response.xpath('//*[@id="content"]/table[1]/*')
        other_event = response.xpath('//*[@id="content"]/table[2]/*')

        acl_href = response.xpath('//*[@id="content"]/table[1]//td/a').extract()[3:]
        for href in acl_href:
            if re.search('<a href="(.*)">',href).group(1)[0].isupper():
                next_page = response.urljoin(re.search('<a href="(.*)">',href).group(1))
                yield scrapy.Request(next_page, callback=self.parse_page)


    def parse_page(self, response):
        raw_data = response.xpath('//*[@id="content"]/p')
        paper_title = []
        authors_name = []
        paper_href = []
        for i in raw_data.extract():
            # print(i)
            paper_href.append(response.url + re.search('<a href="(.*)">', i).group(1))
            if "<b>" in i:
                authors_name.append(re.search('<b>(.*)</b>', i).group(1))
            else:
                authors_name.append("")
            if "<i>" in i:
                paper_title.append(re.search('<i>(.*)</i>', i).group(1))
            else:
                paper_title.append("")

        all_titles.extend(paper_title)
        all_authors.extend(authors_name)
        all_href.extend(paper_href)

        self.writeToXlsx()

    def writeToXlsx(self):
        workbook = xlsxwriter.Workbook('acl_anthology.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'title', bold)
        worksheet.write('B1', 'authors', bold)
        worksheet.write('C1', 'href', bold)
        row = 1

        for i in range(len(all_titles)):
            worksheet.write_string(row, 0, all_titles[i])
            worksheet.write_string(row, 1, all_authors[i])
            worksheet.write_string(row, 2, all_href[i])
            row += 1
        workbook.close()
        return 0
