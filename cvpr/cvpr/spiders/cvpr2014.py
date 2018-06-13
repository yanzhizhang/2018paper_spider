# -*- coding: utf-8 -*-
import scrapy
import re
import xlsxwriter


class Cvpr2014Spider(scrapy.Spider):
    name = 'cvpr2014'
    # allowed_domains = ['http://www.cvpapers.com/']
    def start_requests(self):
        urls = ['http://www.cvpapers.com/cvpr2014.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'body-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


        authors_list = []
        affliation_list = []
        for i in response.xpath('//*[@id="content"]/dl[1]/dd').extract() + response.xpath('//*[@id="content"]/dl[2]/dd').extract():
            i = re.sub('<.*?>','', i)
            print("NEW IIIIIIIII is ")
            print(i)

            while (len(i)) > 0:
                comma_index = i.find(",")
                column_index = i.find("(")

                if (comma_index < column_index and comma_index != -1 and column_index != -1) or (column_index == -1 and comma_index != -1) or (column_index == -1 and comma_index == -1) :
                    authors_list.append(i[:comma_index])
                    affliation_list.append("")
                    i = i[comma_index+1:]
                    print("authors_list -1 is %s"%authors_list[-1])
                    print("affliation_list -1 is empty %s"%affliation_list[-1])
                elif (comma_index > column_index and comma_index != -1 and column_index != -1) or ( column_index != 0 and comma_index == -1 ):
                    authors_list.append(i[:comma_index])
                    affliation_list.append(i[column_index+1:i.find(")")])
                    print("authors_list -1 is %s"%authors_list[-1])
                    print("affliation_list -1 is %s"%affliation_list[-1])
                    i = i[i.find(")")+1:]
                    print
                    if len(i) == 0:
                        break
                    if i[0] ==",":
                        i=i[1:]


                print(i)
                if comma_index == -1:
                    break




        workbook = xlsxwriter.Workbook('cvpr2014.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'Name', bold)
        worksheet.write('B1', 'Affliation', bold)
        row = 1
        for i in range(len(affliation_list)):
            worksheet.write_string(row, 0, authors_list[i])
            worksheet.write_string(row, 1, affliation_list[i])
            row += 1
        workbook.close()
