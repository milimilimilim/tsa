# -*- coding: utf-8 -*-
import os
import ntpath
import xlrd
import xlwt
import pprint
import Temperature_of_Steel_App.tsa_class as tsa_class
from datetime import datetime
import tkinter.messagebox

excel_sheet = xlwt.Workbook()
sheet0 = excel_sheet.add_sheet('DATA_sheet')
# ip_tsa_class = tsa_class.TemperatureCalculation(tsa_class.LoadingInputValue())
input_value = tsa_class.LoadingInputValue()
tsa_classTC = tsa_class.TemperatureCalculation(input_value)
tsa_class_surFP = tsa_class.SurfaceFireProofing(tsa_classTC)
tsa_class_fp = tsa_class.FpToFp(tsa_classTC)
tsa_class_Term = tsa_class.FpTerminal(tsa_classTC)

delta_T = float(tsa_classTC.delta_time)
per_UT = float(1/delta_T)
n_layer = input_value.total_layer
temp_f = float(tsa_classTC.temperature_furnace)
temp_surf = float(tsa_classTC.temperature_fireproof_default)
temp_Tn = [float(tsa_classTC.temperature_fireproof_default)] * n_layer
temp_Tn_new = [0] * n_layer
temp_Term = float(tsa_classTC.temperature_fireproof_default)
unit_row = int(60*per_UT)
testing_time = int(tsa_classTC.testing_time)
loop_range = int((testing_time * 60 * int(per_UT)) + 1)
is_display_with_kelvin = input_value.is_display_with_kelvin
# loop_range = 50000
micro_test = False
macro_test = False
rowSrt = 0
bar_message = "\r[{0}] {1}/{2} {3}% 完了"

# 温度をケルビンで保存
if is_display_with_kelvin:
    difference_K = int(0)
else:
    difference_K = int(273)

for row in range(loop_range):
    # print ('======='+str(row)+'=======')
    time_minutes = (row/per_UT) / 60

    temp_f_new = tsa_classTC.cal_temperature_furnace(time_minutes)
    temp_surf_new = tsa_class_surFP.surface_fp(temp_f, temp_surf, temp_Tn[0])  # temp_surf_newに代入
    temp_Tn_new[0] = tsa_class_fp.fp_to_fp(0, temp_surf, temp_Tn[0], temp_Tn[1])  # レイヤー0をtemp_Tn_newに代入

    # レイヤー1から7までをtemp_Tn_newに代入ループ
    for layer, _ in enumerate(temp_Tn):
        if layer == 0:
            pass  # レイヤー0を除外
        elif layer == (n_layer - 1):
            pass  # レイヤー8を除外
        else:
            # レイヤー1から7までをtemp_Tn_newに代入
            temp_Tn_new[layer] = tsa_class_fp.fp_to_fp(layer, temp_Tn[layer-1], temp_Tn[layer], temp_Tn[layer+1])
            # レイヤー8をtemp_Tn_newに代入
            temp_Tn_new[n_layer-1] = tsa_class_fp.fp_to_fp(n_layer-1, temp_Tn[n_layer-2], temp_Tn[n_layer-1], temp_Term)
            temp_Term_new = tsa_class_Term.fp_terminal(temp_Tn[n_layer - 1], temp_Term)

    # 各tempを更新
    temp_f = temp_f_new
    temp_surf = temp_surf_new
    for layer, _ in enumerate(temp_Tn):
        temp_Tn[layer] = temp_Tn_new[layer]
    temp_Term = temp_Term_new

# ======各tempを記録========

    # 保存間隔のためrowSrtを処理
    if micro_test:
        rowSrt = row  # デバック用 macro_testがTrueですべての時間保存する
    elif macro_test and rowSrt > 67:
        pass
    else:
        rowSrt = int((row // unit_row)+1)  # 保存の時間の間隔を代入

    # 一定（unit_row）の間隔で保存
    # 代入した時間間隔のとき保存 またはmacro_testがTrueですべての時間を保存
    if row % unit_row == 0 or micro_test or (row == loop_range - 1) or (macro_test and rowSrt) > 66:
        # 進捗状況を表示
        r_message = int((row * 30 / loop_range) + 1)  # パーセント表示
        bar = "#" * r_message + " " * (30-r_message)  # []内の"#"と空白を調整する。iが1で#1つに空白29、iが30で#30個に空白0
        pers = int(r_message * 100/30)
        print(bar_message.format(bar, row, loop_range - 1, pers), end="")
        # print ('======='+str(row)+'=======')

        if micro_test or (row == loop_range - 1)or (rowSrt > 66 and macro_test):
            rowSrt = rowSrt + 1
        # デバック用 macro_testがTrueの時 時間を秒で保存
        if micro_test or (rowSrt > 66 and macro_test):
            sheet0.write(rowSrt, 0, row/per_UT)
        elif row == 0:
            sheet0.write(rowSrt, 0, int(time_minutes))
        else:
            sheet0.write(rowSrt, 0, int(time_minutes+1))
          
        # Excel への保存処理
        sheet0.write(rowSrt, 1, temp_f-difference_K)
        sheet0.write(rowSrt, 2, temp_surf-difference_K)
        for excel_column, _ in enumerate(temp_Tn):
            sheet0.write(rowSrt, excel_column + 3, temp_Tn[excel_column] - difference_K)
        sheet0.write(rowSrt, n_layer+3, temp_Term-difference_K)
    pass

# 保存
print('\n=====実行完了=====')
root = tkinter.Tk()
root.withdraw()
ret = tkinter.messagebox.askyesno('確認', 'データを保存しますか？')
if ret:
    char_datafile_date = datetime.now().strftime("%m%d_%Y_%H%M%S")
    char_datafile_name = 'TSA_DATA' + char_datafile_date + '.xls'
    setting_path = input_value.data_save_path
    char_datafile_path = os.path.join(setting_path, char_datafile_name)
    print(char_datafile_path)
    excel_sheet.save(char_datafile_path)
