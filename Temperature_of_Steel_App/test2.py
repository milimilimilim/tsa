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

for i in range(8):
    print(a.array_thickness_fireproof[i], a.list_name_layer[i])
for i in range(8):
    print(a.array_len_width_height[i][0], " ", a.array_len_width_height[i][1], a.list_name_layer[i])
for i in range(8):
    print(a.array_len_around[i], a.list_name_layer[i])
print("\n 面積")
for i in range(8):
    print(a.array_area[i], a.list_name_layer[i])
# print(a.array_len_width_height[3][1])
