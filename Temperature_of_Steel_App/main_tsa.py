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



delta_T = 0.1
time_second = 0
temp_f = 20 +273
temp_surf = 20 + 273
temp_Tn = [20+273] * 9
temp_Tn_new = [0] * 9

tsa_class_tf= tsa_class.Temperature_Furnace(delta_T)
tsa_class_sht = tsa_class.Surface_Heat_Transfer(delta_T)
tsa_class_surFP = tsa_class.Surface_Fireporoofing(delta_T)
tsa_class_fp = tsa_class.Fp_to_Fp(delta_T)


for row in range(11):
    if row == 0 : continue
    time_minutes = time_second / 60
    temp_f=  tsa_class_tf.t_furnace(time_minutes)

    sheet2.write(row,0,time_second)
    sheet2.write(row,1,temp_f)
    sheet2.write(row,2,temp_surf)

    for colum,_ in enumerate(temp_Tn):
     sheet2.write(row,colum+3,temp_Tn[colum])
 
    tsa_class_sht.surface_HT(temp_f,temp_surf)
    temp_surf_new = tsa_class_surFP.surface_FP(temp_surf,temp_Tn[0],tsa_class_sht.qc,tsa_class_sht.qr)

    temp_Tn_new[0] = tsa_class_fp.fp_to_fp(0,temp_surf,temp_Tn[0],temp_Tn[0])
    for sheaf,_ in enumerate(temp_Tn):
     if sheaf == 0 : continue 
     elif sheaf == 8 : break
     else :
      temp_Tn_new[sheaf] = tsa_class_fp.fp_to_fp(sheaf,temp_Tn[sheaf-1],temp_Tn[sheaf],temp_Tn[sheaf+1])
    temp_Tn_new[8] = tsa_class_fp.fp_to_fp(8,temp_Tn[7],temp_Tn[8],293)



    time_second = time_second + delta_T
    temp_surf = temp_surf_new
    for sheaf,_ in enumerate(temp_Tn):
     temp_Tn[sheaf] = temp_Tn_new[sheaf]



#保存

char_detafile_date =datetime.now().strftime("%m%d_%Y_%H%M%S")
char_detafile_name = 'sample'+ char_detafile_date + '.xls'
char_detafile_path = os.path.join('D:','Documents','python',char_detafile_name)
print(char_detafile_path)
wb2.save('D:\Documents\python\sample0.xls')
os.rename('D:\Documents\python\sample0.xls',char_detafile_path)

