# -*- coding: utf-8 -*-
# 本程序的作用是将xlsx中的数据导入到txt文件中
import xlrd

data = xlrd.open_workbook('papers.xlsx')  # 打开Excel文件读取数据
table = data.sheet_by_name(u'Sheet1')  # 通过名称获取
nrows = table.nrows  # 获取行数

# 读取每一篇paper的ID和title，并保存到txt
with open('papers.txt', 'w') as f:
    for i in range(nrows):
        f.write("%s,%s\n" % (table.row_values(i)[0]+' '+table.row_values(i)[1][:3]+'_'+table.row_values(i)[1][4:], table.row_values(i)[2]))


