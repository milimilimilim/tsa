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
import tkinter as tk
from tkinter import ttk


def write_slogan():
    print("Tkinter is easy to use!")


def button1_clicked():
    print('v1 = %s' % v1.get())
    quit()


def rb_clicked():
    print('v1 = %s' % v1.get())


# root = tk.Tk()
# root.title("tsa_ver:0.0")
# frame1 = tk.Frame(root)
# frame1.pack()
# label1 = tk.Label(root, text='Your name:')

master = tk.Tk()
master.title("tsa_GUI")
master.geometry("400x400")

frame0 = ttk.LabelFrame(master, text="部材種", padding=5)
frame1 = ttk.Label(frame0, padding=5,width=500)
v1 = tk.StringVar()

str_dis = "0"

v1.set('A')
rb1 = ttk.Radiobutton(
    frame1,
    text='角形鋼管',
    value='A',
    variable=v1,
    command=rb_clicked)
rb1.pack(fil="x",side='left')

rb2 = ttk.Radiobutton(
    frame1,
    text='H形鋼',
    value='B',
    variable=v1,
    command=rb_clicked)
rb2.pack(fil="x",side='left')

a = True
if a:
    frame2 = ttk.LabelFrame(frame0, text='鋼材寸法', padding=5)
    row_type_steel_material_guide = 3
    lab_g1 = tk.Label(frame2, text="高さ(h)").grid(row=row_type_steel_material_guide, column=1)
    lab_g2 = tk.Label(frame2, text="幅(w)").grid(row=row_type_steel_material_guide, column=3)
    lab_g3 = tk.Label(frame2, text="ウェブ(r1)").grid(row=row_type_steel_material_guide, column=5)
    lab_g4 = tk.Label(frame2, text="フランジ(r2)").grid(row=row_type_steel_material_guide, column=7)

    row_type_steel_material = 4
    entry_width_type_steel = 5
    lab1 = tk.Label(frame2, text="鋼材種").grid(row=row_type_steel_material)
    e11 = tk.Entry(frame2, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=1)
    lab2 = tk.Label(frame2, text="  ×  ").grid(row=row_type_steel_material, column=2)
    e12 = tk.Entry(frame2, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=3)
    lab3 = tk.Label(frame2, text="  ×  ").grid(row=row_type_steel_material, column=4)
    e13 = tk.Entry(frame2, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=5)
    lab4 = tk.Label(frame2, text="  ×  ").grid(row=row_type_steel_material, column=6)
    e14 = tk.Entry(frame2, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=7)

    lab5 = tk.Label(frame2, text=str_dis).grid(row=5)
    # e2 = tk.Entry(frame2, width=5, justify="right").grid(row=5, column=1)
    # e11.grid(row=2, column=2)
    # e12.grid(row=2, column=4)
    # e13.grid(row=2, column=6)
    # e14.grid(row=2, column=8)
else:
    pass
frame1.pack()
frame2.pack()
# frame2を配置(綴じる)
frame0.grid(row=0, column=0)  # frame1を配置(綴じる)

# logo = tk.PhotoImage(file="D:\Picture\win_Picture\makina_kurage.png")
# w1 = tk.Label(root, image=logo).pack(side="right")
# explanation = "hyoujidekitanokanaa"
# w2 = tk.Label(root, justify=tk.LEFT, padx=10, text=explanation).pack(side="left")

# button = tk.Button(frame1,text="QUIT",fg="red",command=quit)
# button.pack(side=tk.LEFT)
# slogan = tk.Button(frame1,text="Hello",command=write_slogan)
# slogan.pack(side=tk.LEFT)

# string_var_t = 0
# entry1 = tk.Entry(frame1, textvariable=string_var_t)
# button1 = tk.Button(frame1, text='OK', command=foo)
#
# label1.pack()

# frame1.grid(row=0,column=0,sticky=(N,E,S,W))
# label1.grid(row=1,column=1,sticky=E)
# entry1.grid(row=1,column=2,sticky=W)
# button1.grid(row=2,column=2,sticky=W)


master.mainloop()
