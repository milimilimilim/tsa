# -*- coding: utf-8 -*-
import sys
import os
import time
import xlrd
import xlwt
import tsa_class
from decimal import *
import configparser
from datetime import datetime
#from tkinter import messagebox
import tkinter
import tkinter.messagebox
num = 1
num2 =1
#for i in range(10):
#    print(num)
#    num =num +num2
#    print (num2)
#    num2 = num + num2

#bar_template = "\r[{0}] {1}/{2} {3}% 読み込み"
#for i in range(50):
#    time.sleep(0.1)
#    j = int ( (i*30/50) + 1)
#    # []内の"#"と空白を調整する。iが1で#1つに空白29、iが30で#30個に空白0
#    bar = "#" * j + " " * (30-j)
#    pers = int (j *100/30)
#    print(bar_template.format(bar, j, 30,pers), end="")
#print()
#root = tkinter.Tk()


#root.withdraw()

#ret = tkinter.messagebox.askyesno('確認', 'ウィンドウを閉じますか？')
inifile = configparser.ConfigParser()
inifile.read('./tsa_config.ini', 'UTF-8')

excel_sheet = xlwt.Workbook()
sheet0 = excel_sheet.add_sheet('sheet2')
char_detafile_date =datetime.now().strftime("%m%d_%Y_%H%M%S")
char_detafile_name = 'TSA_DATA'+ char_detafile_date + '.xls'
pathpath = inifile.get('settings', 'data_save_path')
char_detafile_path = os.path.join(pathpath,char_detafile_name)
print(char_detafile_path)

print(inifile.get('settings', 'data_save_path'))

excel_sheet.save(char_detafile_path)

tsa1 = tsa_class.Surface_Fireporoofing()
tsa2 = tsa_class.Fp_to_Fp()
tsa3 = tsa_class.Fp_terminal()
tsa1.temperature_furnace(99/60)




#print(tsa1.temp_F)
#print(tsa1.surface_FP(644.681936028725,601.029996677171))
dn = 8
A = 477.626522227032
B = 385.962420395018
C = 383.812793590009
print(tsa2.fp_to_fp(dn,A,B,C))
#print((B*0.11/400)-0.02)
#print(tsa1.pf_ther_conductivity(819.761724839044))
#Q = 293.000000041662+0.0044114109489909*0.705*0.09*(293.000048670292-293.000000041662)/1.25
#print(Q)
D = 293.000048670292
F = 293.000000041662
#print(tsa3.fp_terminal(D,F))
#print(tsa1.temp_surf)

temp_Tn = [20+273] * 9
#print(temp_Tn)
#print(temp_Tn[3])
j=[0]*10
print(1/0.1)
print(Decimal(1/0.1))
for i in range(10):
    print(j)
    for J,_ in enumerate(j) : j[J]=j[J]+J
classesA = []
classesA.append(tsa_class.Test_tsa(1, 'テスト１'))
classesA.append(tsa_class.Test_tsa(2, 'テスト２'))

for test_cls in classesA:
    print('===== Class =====')
    print('code --> ' + str(test_cls.code))
    print('name --> ' + test_cls.name)
  
