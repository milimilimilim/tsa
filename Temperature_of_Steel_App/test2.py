# -*- coding: utf-8 -*-
import sys
import os
import time
import xlrd
import xlwt
import Temperature_of_Steel_App.tsa_class as tsa_class
from decimal import *
import configparser
from datetime import datetime
# from tkinter import messagebox
import tkinter
import tkinter.messagebox

loading_val = tsa_class.LoadingInputValue()
a = tsa_class.TemperatureCalculation(loading_val)
print("インスタンス生成完了")
# fp_thick = [1, 0 for i in range(3), 1]

# print(a.total_width_test_specimen, a.total_height_test_specimen)
# print(a.array_thickness_fireproof)

# for i in range(8):
#     print(a.array_thickness_fireproof[i], a.list_name_layer[i])
# for i in range(8):
#     print(a.array_len_width_height[i][0], " ", a.array_len_width_height[i][1], a.list_name_layer[i])
# for i in range(8):
#     print(a.array_len_around[i], a.list_name_layer[i])
# area_test = (a.array_len_around[1]+a.array_len_around[6])/2*10
# print("area=", area_test)
#

# list_a = a.list_name_layer
# list_b = []
# for i, name in enumerate(list_a):
#     len_list = 15 - len(str(name))
#     input_name = str(name) + " " * len_list + ":"
#     list_b.append(input_name)
# for i in list_b:
#     print(i)

a.display_input_column()
print("s_time",a.cal_stability_time())

# d_time = a.delta_time
# test_time = a.testing_time
# loop = int(round(test_time * 60 / d_time, 0))
# # loop = 1000
# array_temperature = a.array_temperature
# array_temperature[len(a.list_name_layer) - 1] = "none"
# array_temperature_prevent = a.array_temperature_prevent
#
# for loop_count in range(loop):
#     current_time_seconds = d_time * loop_count
#     print("------now ", current_time_seconds, "s")
#     array_temperature = a.cal_new_temperature_array(current_time_seconds)
#     for i in range(len(a.list_name_layer) - 1):
#         print(array_temperature[i] - 273)
#     print(array_temperature[len(a.list_name_layer) - 1])
#     a.array_temperature_prevent = array_temperature
#
# def list_2 (i):
#     return [i, i * 2, i * 3]
# # print(a.cal_stability_time())
# list_f = []
# list_g =list_2(i)
# for i in range(10):
#     list_f.append(list_2(i))
# for i in range(10):
#     print(list_f[i])


