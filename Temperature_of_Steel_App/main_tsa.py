# -*- coding: utf-8 -*-
import os
import ntpath
import xlrd
import xlwt
import pprint
import tsa_class
from datetime import datetime
from decimal import *
import tkinter
import tkinter.messagebox

excel_sheet = xlwt.Workbook()
sheet0 = excel_sheet.add_sheet('DATA_sheet')


tsa_class_surFP = tsa_class.Surface_Fireporoofing()
tsa_class_fp = tsa_class.Fp_to_Fp()
tsa_class_Term = tsa_class.Fp_terminal()
delta_T = float(tsa_class_surFP.d_time)
per_UT =float  (1/delta_T)
temp_f = Decimal  (tsa_class_surFP.temp_F)
temp_surf = Decimal  (tsa_class_surFP.temp_FP)
temp_Tn = [Decimal(tsa_class_surFP.temp_FP)] * 9
temp_Tn_new = [0] * 9
temp_Term = Decimal  (tsa_class_surFP.temp_FP)
unit_row = int(60*per_UT)
testing_time = int( tsa_class_surFP.test_t )
roop_range = int  ((testing_time * 60 * int(per_UT) ) + 1)
disp_K = tsa_class_surFP.disp_K
micro_test = False
macro_test =False
rowSrt = 0
bar_message = "\r[{0}] {1}/{2} {3}% 読み込み"

        #温度をケルビンで保存
if disp_K : difference_K = int (0) 
else:difference_K = int(273)
print(disp_K)


for row in range(roop_range):
    #print ('======='+str(row)+'=======')
    time_minutes = (row/per_UT) / 60

    temp_f_new = tsa_class_surFP.temperature_furnace(time_minutes)
    temp_surf_new = tsa_class_surFP.surface_FP(temp_f,temp_surf,temp_Tn[0])#temp_surft_newに代入
    temp_Tn_new[0] = tsa_class_fp.fp_to_fp(0,temp_surf,temp_Tn[0],temp_Tn[1]) #レイヤー0をtemp_Tn_newに代入
    #レイヤー1から7までをtemp_Tn_newに代入ループ
    for layer,_ in enumerate(temp_Tn):
     if layer == 0 :  pass#レイヤー0を除外
     elif layer == 8 : pass  #レイヤー8を除外
     else : temp_Tn_new[layer] = tsa_class_fp.fp_to_fp(layer,temp_Tn[layer-1],temp_Tn[layer],temp_Tn[layer+1])#レイヤー1から7までをtemp_Tn_newに代入
    temp_Tn_new[8] = tsa_class_fp.fp_to_fp(8,temp_Tn[7],temp_Tn[8],temp_Term) #レイヤー8をtemp_Tn_newに代入
    temp_Term_new = tsa_class_Term.fp_terminal(temp_Tn[8],temp_Term)

    #各tempを更新
    temp_f = temp_f_new
    temp_surf = temp_surf_new
    for layer,_ in enumerate(temp_Tn): temp_Tn[layer] = temp_Tn_new[layer]
    temp_Term = temp_Term_new

#======各tempを記録========

      #保存間隔のためrowSrtを処理
    if micro_test :rowSrt = row#　デバック用　macro_testがTrueですべての時間保存する
    elif macro_test and rowSrt >67 : pass
    else : rowSrt = int ( (row // unit_row) + 1 )#　保存の時間の間隔を代入

    #一定（unit_row）の間隔で保存
    if row % unit_row == 0 or micro_test or (macro_test and rowSrt) >66 :#　代入した時間間隔のとき保存　または　macro_testがTrueですべての時間を保存

        #進捗状況を表示
      r_message = int ( (row*30/roop_range) + 1)#パーセント表示
      bar = "#" * r_message + " " * (30-r_message) # []内の"#"と空白を調整する。iが1で#1つに空白29、iが30で#30個に空白0
      pers = int (r_message *100/30)
      print(bar_message.format(bar, row, roop_range-1 ,pers), end="")
      #print ('======='+str(row)+'=======')

      if micro_test or (rowSrt >66 and macro_test):
          rowSrt = rowSrt + 1
          sheet0.write(rowSrt,0,row/per_UT)#　デバック用　macro_testがTrueの時 時間を秒で保存
      else : 
          sheet0.write(rowSrt,0,time_minutes)
        #Excel への保存処理
      sheet0.write(rowSrt,1,temp_f-difference_K)
      sheet0.write(rowSrt,2,temp_surf-difference_K)
      for colum,_ in enumerate(temp_Tn):sheet0.write(rowSrt,colum+3,temp_Tn[colum]-difference_K)
      sheet0.write(rowSrt,12,temp_Term-difference_K)
    pass
     
     
 
   
   
 



#保存
print('\n=====実行完了=====')
root = tkinter.Tk()
root.withdraw()
ret = tkinter.messagebox.askyesno('確認', 'データを保存しますか？')
if ret :
    char_detafile_date =datetime.now().strftime("%m%d_%Y_%H%M%S")
    char_detafile_name = 'TSA_DATA'+ char_detafile_date + '.xls'
    setting_path = tsa_class_surFP.data_save_path
    char_detafile_path = os.path.join(setting_path,char_detafile_name)
    print(char_detafile_path)
    excel_sheet.save(char_detafile_path)

