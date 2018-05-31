# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import xlsxwriter
import re

AUTHOR_LIST = []
EMAIL_LIST = []
TOPIC_LIST = []

urls = ['https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&before_author=nHv4_0aIAQAJ&astart=0',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=8nMTAPhI_v8J&astart=10',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=MZ8DAHXU_v8J&astart=20',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=MZ8DAHXU_v8J&astart=30',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=MZ8DAHXU_v8J&astart=40',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=MZ8DAHXU_v8J&astart=50',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=MZ8DAHXU_v8J&astart=60',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=MZ8DAHXU_v8J&astart=70',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=MZ8DAHXU_v8J&astart=80',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=MZ8DAHXU_v8J&astart=90',
        'https://scholar.google.com/citations?view_op=search_authors&hl=en&authuser=1&mauthors=label:artificial_intelligence&after_author=MZ8DAHXU_v8J&astart=100',
        ]
for index, url in enumerate(urls):
    print(url)
    content = urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")

    for author in soup.find_all('h3'):
        AUTHOR_LIST.append(author.a.contents[0])
    for email in soup.find_all('div', class_='gsc_oai_eml'):
        if len(email.contents) == 1:
            EMAIL_LIST.append(re.search("Verified email at (.*)",str(email.contents[0])).group(1))
        else:
            EMAIL_LIST.append("N/A")
    for topic in soup.find_all('div', class_='gsc_oai'):
        temp = []
        for i in topic.find_all('a', class_='gsc_oai_one_int'):
            temp += i.contents
        TOPIC_LIST.append(temp)

workbook = xlsxwriter.Workbook('google_scholar.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': 1})
worksheet.write('A1', 'Name', bold)
worksheet.write('B1', 'Email', bold)
worksheet.write('C1', 'Area', bold)

row = 1
for i in range(len(AUTHOR_LIST)):
    worksheet.write_string  (row, 0, AUTHOR_LIST[i])
    worksheet.write_string  (row, 1, EMAIL_LIST[i])
    worksheet.write_string  (row, 2, ', '.join(TOPIC_LIST[i]))
    row += 1
workbook.close()

# print(AUTHOR_LIST)
# print(EMAIL_LIST)
# print(TOPIC_LIST)
