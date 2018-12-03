# -*- coding: utf-8 -*-
import os
import ntpath
import xlrd
import xlwt
import pprint
import tsa_class
from datetime import datetime


wb2 = xlwt.Workbook('D:\Documents\python\sample.xlsx')
sheet2 = wb2.add_sheet('sheet2')


tsa_class0= tsa_class.Temperature_Furnace(0)
tsa_class0.t_furnace(3000)
print(tsa_class0.temp_F)
delta_T = 0.1
time_second = 0
temp_surf = 20 + 273
tsa_class= tsa_class.Temperature_Furnace(delta_T)

for colums in range(10):
    time_minutes = time_second / 60
    
    tsa_class.t_furnace(time_minutes)
    sheet2.write(colums,1,tsa_class.temp_F)
    tsa_class.Surface_Heat_Transfer.surface_HT(tsa_class.temp_F,temp_surf)
   
    time_second = time_second + delta_T


#保存

char_detafile_date =datetime.now().strftime("%m%d_%Y_%H%M%S")
char_detafile_name = 'sample'+ char_detafile_date + '.xls'
char_detafile_path = os.path.join('D:','Documents','python',char_detafile_name)
print(char_detafile_path)
wb2.save('D:\Documents\python\sample0.xls')
#os.rename('D:\Documents\python\sample0.xls','D:\Documents\python\sample012.xls')
os.rename('D:\Documents\python\sample0.xls',char_detafile_path)

