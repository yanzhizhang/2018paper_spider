import subprocess
import xlsxwriter
cmd = ["kaggle", "datasets", "list", "-p"]
input = 'foo\nfoofoo\n'.encode('utf-8')
ref = []
title = []

for i in range(10):
    temp_cmd = cmd
    cmd.extend([str(i+1), "-v"])
    result = subprocess.run(cmd, stdout=subprocess.PIPE, input=input)
    result.stdout.decode('utf-8')
    temp = result.stdout.decode('utf-8').split('\r\n')[1:-1]
    cmd = ["kaggle", "datasets", "list", "-p"]

    for i in temp[1:-3]:
        i = i.split(",")
        ref.append("https://www.kaggle.com/" + i[0])
        title.append(i[1])

workbook = xlsxwriter.Workbook('kaggle_dataset.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
worksheet.write('A1', 'ref', bold)
worksheet.write('B1', 'title', bold)
row = 1

for i in range(len(ref)):
    worksheet.write_string  (row, 0, ref[i])
    worksheet.write_string  (row, 1, title[i])
    row += 1
workbook.close()
