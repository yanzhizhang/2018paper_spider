from urllib.request import urlopen
from bs4 import BeautifulSoup
import xlsxwriter
import re


urls = ['http://www.wikicfp.com/cfp/call?conference=data%20mining&page=1',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=2',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=3',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=4',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=5',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=6',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=7',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=8',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=9',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=10',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=11',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=12',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=13',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=14',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=15',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=16',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=17',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=18',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=19',
        'http://www.wikicfp.com/cfp/call?conference=data%20mining&page=20',
        ]
workbook = xlsxwriter.Workbook('wikicfp_data_mining.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': 1})
worksheet.write('A1', 'Name', bold)
row = 1

conf_list = []
for index, url in enumerate(urls):
    # print(url)
    content = urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")

    # page = url.split("&")[-1]
    # filename = 'body-%s.html' % page
    # with open(filename, 'wb') as f:
    #     f.write(content)


    temp = soup.select('body > div.contsec > center > form tr td a')[5:-4]
    for i in temp:
        i = str(i)
        if i not in conf_list:
            conf_list.append(re.search('>\s?(.*)<',i).group(1)[:-5])
            worksheet.write_string(row, 0, conf_list[-1])
        row += 1
workbook.close()
