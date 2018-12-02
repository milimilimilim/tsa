
# -*- coding: utf-8 -*-
import xlrd
import xlwt
import pprint
wb2 = xlwt.Workbook('D:\Documents\python\sample.xlsx')
print("hello,world")




sheet2 = wb2.add_sheet('sheet2')
for x in range(10):
 for y in range(10):
     char = str(x)+str(y)
     sheet2.write(x, y,char )




wb2.save('D:\Documents\python\sample2.xls')

