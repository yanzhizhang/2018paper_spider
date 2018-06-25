#paper-author-venue-topic-organization(if applicable-OAG has it)；注意*仅限人工智能领域*的论文。额外可补充的是link，abstract, citations

import os
import re
import xlsxwriter
import json

# file = os.listdir(os.getcwd())

files = ["s2-corpus-00"]

workbook = xlsxwriter.Workbook('sc2.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': 1})
worksheet.write('A1', 'title', bold)
worksheet.write('B1', 'authors', bold)
worksheet.write('C1', 'venue', bold)
worksheet.write('D1', 'paperAbstract', bold)
worksheet.write('E1', 'entities', bold)
worksheet.write('F1', 'pdfUrls', bold)
worksheet.write('G1', 'inCitations', bold)
worksheet.write('H1', 'outCitations', bold)
row = 1

for file in files:
    with open(file) as f:
        readbylines = f.readlines()
        json_dict = []
        for line in readbylines:
            json_dict = json.loads(line)
            topic = json_dict["entities"]
            if "Artificial intelligence" in topic:
                title = json_dict["title"]
                authors_list = json_dict["authors"]
                authors = []
                for i in authors_list:
                    authors.append(i['name'])
                authors = ";".join(authors)
                venue = json_dict["venue"]
                entities = json_dict["entities"]
                entities = ";".join(entities)
                pdfUrls = json_dict["pdfUrls"]
                if len(pdfUrls) != 0:
                    pdfUrls = ";".join(pdfUrls)
                else:
                    pdfUrls = ""
                paperAbstract = json_dict["paperAbstract"]
                inCitations = json_dict["inCitations"]
                inCitations =";".join(inCitations)
                outCitations = json_dict["outCitations"]
                outCitations =" ".join(outCitations)
                worksheet.write_string  (row, 0, title)
                worksheet.write_string  (row, 1, authors)
                worksheet.write_string  (row, 2, venue)
                worksheet.write_string  (row, 3, paperAbstract)
                worksheet.write_string  (row, 4, entities)
                worksheet.write_string  (row, 5, pdfUrls)
                worksheet.write_string  (row, 6, inCitations)
                worksheet.write_string  (row, 7, outCitations)
                row += 1

workbook.close()
