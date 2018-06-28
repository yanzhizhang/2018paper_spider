# -*- coding: utf-8 -*-
import scrapy
import xlsxwriter
import re


class Sigar2018Spider(scrapy.Spider):
    name = 'sigar2018'
    # allowed_domains = ['http://sigir.org/sigir2018/']

    def start_requests(self):
        urls = ['http://sigir.org/sigir2018/accepted-papers//']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        page = response.url.split("/")[-]

        filename = 'body-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        workbook = xlsxwriter.Workbook('2018acmsigar.xlsx')
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'Name', bold)
        worksheet.write('B1', 'Affliation', bold)

        row = 1
        worksheet.write(row, 0, 'Full paper', bold)
        row+=1
        authors_list = response.xpath('//table')[0].re(r'<span class="s1">(.*)</span></p>')
        for authors in authors_list:
            for author in authors.split(');'):
                worksheet.write(row, 0, author.split('(')[0])
                worksheet.write(row, 1, author.split('(')[1])
                row+=1


        worksheet.write(row, 0, 'Short paper', bold)
        row+=1
        authors_list = response.xpath('//table')[1].re(r'<td style="width: 475px;">(.*)</td>')
        for authors in authors_list:
            for author in authors.split(');'):
                worksheet.write(row, 0, author.split('(')[0])
                worksheet.write(row, 1, author.split('(')[1])
                row+=1


        worksheet.write(row, 0, 'Demo paper', bold)
        row+=1
        authors_list = response.xpath('//table')[2].re(r'<td style="width: 475px;">(.*)</td>')
        for authors in authors_list:
            for author in authors.split(');'):
                worksheet.write(row, 0, author.split('(')[0])
                worksheet.write(row, 1, author.split('(')[1])
                row+=1


        worksheet.write(row, 0, 'SIRIP Industry Papers', bold)
        row+=1
        authors_list = response.xpath('//table')[3].re(r'<span class="s1">(.*)</span></p>')
        for authors in authors_list:
            for author in authors.split(');'):
                worksheet.write(row, 0, author.split('(')[0])
                worksheet.write(row, 1, author.split('(')[1])
                row+=1


        worksheet.write(row, 0, 'Doctoral Consortium Abstracts', bold)
        row+=1
        authors_list = response.xpath('//table')[4].re(r'<span class="s1">(.*)</span></p>')
        for authors in authors_list:
            for author in authors.split(');'):
                worksheet.write(row, 0, author.split('(')[0])
                worksheet.write(row, 1, author.split('(')[1])
                row+=1
