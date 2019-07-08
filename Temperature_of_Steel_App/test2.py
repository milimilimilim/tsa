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
print("\n 面積")
area_sum = 0
for i in range(8):
    if i != 0 and i != 7 and i != 6:
        area_sum += a.array_area[i]
print("area", area_sum)


# list_a = a.list_name_layer
# list_b = []
# for i, name in enumerate(list_a):
#     len_list = 15 - len(str(name))
#     input_name = str(name) + " " * len_list + ":"
#     list_b.append(input_name)
# for i in list_b:
#     print(i)
message_a = "{0} {1} {2}"
message_s = ["     layer  ", "think_L    ", "think_FP    "]
print(message_a.format(message_s[0], message_s[1], message_s[2]))


print(a.is_under_floor)
a.display_input_column()

