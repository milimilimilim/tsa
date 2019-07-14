# -*- coding: utf-8 -*-
import os
import math
import time
# import ntpath
# import xlrd
import xlwt
# import pprint
import Temperature_of_Steel_App.tsa_class as tsa_class
from datetime import datetime
import tkinter.messagebox
from statistics import mean

excel_sheet = xlwt.Workbook()
sheet0 = excel_sheet.add_sheet('DATA_sheet')

input_value = tsa_class.LoadingInputValue()
tsa_cal = tsa_class.TemperatureCalculation(input_value)

delta_time = float(tsa_cal.delta_time)
testing_time = int(tsa_cal.testing_time)
per_unit_time = float(1 / delta_time)
unit_row = int(60 * per_unit_time)
loop_range = int(round(testing_time * 60 / delta_time, 0))  # loop回数

array_temperature = tsa_cal.array_temperature
array_temperature[len(tsa_cal.list_name_layer) - 1] = "none"
array_temperature_prevent = tsa_cal.array_temperature_prevent

is_display_with_kelvin = input_value.is_display_with_kelvin
# loop_range = 50000

bar_message = "\r[{0}] {1}/{2} {3}% 完了"

# 温度をケルビンで保存
if is_display_with_kelvin:
    difference_K = int(0)
else:
    difference_K = int(273)

tsa_cal.display_input_column()
minutes_10_prev = "none"
array_cal_time = []
cal_time_0 = time.time()
cal_time_1 = 0
array_temperature_save = []

for loop_count in range(loop_range + 1):
    current_time_seconds = delta_time * loop_count
    current_time_minutes = current_time_seconds / 60
    # print("------now ", current_time_seconds, "s")
    minutes_10_now = int(math.floor(current_time_minutes))
    # print("\n値は",current_time_minutes, minutes_10_prev,minutes_10_now,"\n")

    array_temperature = tsa_cal.cal_new_temperature_array(current_time_seconds)

    if loop_count % 100 == 0:
        cal_time_1 = cal_time_0
        cal_time_0 = time.time()
        array_cal_time.append(cal_time_0 - cal_time_1)

    if minutes_10_now != minutes_10_prev:
        array_temperature_save_temp = []
        for i in range(len(tsa_cal.list_name_layer)):
            array_temperature_save_temp.append(array_temperature[i])
        array_temperature_save.append(array_temperature_save_temp)

        array_temperature_save[minutes_10_now][len(tsa_cal.list_name_layer) - 1] = current_time_seconds

    tsa_cal.array_temperature_prevent = array_temperature
    minutes_10_prev = minutes_10_now

    # ======各tempを記録========

    # 進捗状況を表示
    r_message = int((loop_count * 30 / loop_range) + 1)  # パーセント表示
    bar = "#" * r_message + " " * (30 - r_message)  # []内の"#"と空白を調整する。iが1で#1つに空白29、iが30で#30個に空白0
    pers = int(round((loop_count / loop_range) * 100, 1))
    print(bar_message.format(bar, loop_count, loop_range - 1, pers), end="")

# Excel への保存処理
cel_row = 1
terminal_layer_number = tsa_cal.list_name_layer.index('terminal')

for i, element in enumerate(tsa_cal.list_name_layer):
    if element == 'inside_steel':
        pass
    else:
        sheet0.write(0, i + 1, element)

for i in range(minutes_10_prev + 1):
    cel_row += 1
    # print("\n save",array_temperature_save[i])
    sheet0.write(cel_row, 0, array_temperature_save[i][terminal_layer_number + 2] / 60)  # 時刻(秒)を保存
    # sheet0.write(cel_row, 1, array_temperature_save[i][0] - difference_K)
    # sheet0.write(cel_row, 2, array_temperature_save[i][1] - difference_K)

    # for excel_column in range(2, terminal_layer_number + 2):
    #     sheet0.write(cel_row, excel_column + 1, array_temperature_save[i][excel_column] - difference_K)

    for excel_column in range (terminal_layer_number+2):
        sheet0.write(cel_row, excel_column + 1, array_temperature_save[i][excel_column] - difference_K)

# 保存
print('\n=====実行完了=====')
average_cal_time = mean(array_cal_time)
print("100ループの平均計算時間",average_cal_time)
print(average_cal_time / 100 * loop_range)
root = tkinter.Tk()
root.withdraw()
ret = tkinter.messagebox.askyesno('確認', 'データを保存しますか？')
if ret:
    char_datafile_date = datetime.now().strftime("%m%d_%Y_%H%M%S")
    char_datafile_name = 'TSA_DATA_' + char_datafile_date + '.xls'
    setting_path = input_value.data_save_path
    char_datafile_path = os.path.join(setting_path, char_datafile_name)
    print(char_datafile_path)
    excel_sheet.save(char_datafile_path)
