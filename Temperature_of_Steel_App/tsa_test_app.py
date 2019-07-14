# -*- coding: utf-8 -*-
import sys
import os
import time
import xlrd
import xlwt
import Temperature_of_Steel_App.tsa_class as tsa_class
import tkinter as tk
from tkinter import ttk


def write_slogan():
    print("Tkinter is easy to use!")


def button1_clicked():
    print('v1 = %s' % v1.get())
    quit()


def rb_clicked():
    print('v1 = %s' % v1.get())

    if v1.get() == 'A':
        frame4.pack_forget()
        frame3.pack(side='left')
    elif v1.get() == 'B':
        frame3.pack_forget()
        frame4.pack(side='left')


def rb_clicked1():
    print('v2 = %s' % v2.get())

    if v2.get() == 'A':
        e01.configure(foreground="black",state='normal')
        e02.configure(foreground="gray",state='readonly')
    elif v2.get() == 'B':
        e01.configure(foreground="gray",state='readonly')
        e02.configure(foreground="black",state='normal')


master = tk.Tk()
master.title("tsa_GUI")
master.geometry("330x400")

style0 = ttk.Style()
style0.configure(
    'TLabel', font=('meiryo', 8),
    foreground='black')
style0.configure(
    'TLabelframe.Label', font=('meiryo', 10),
    foreground='black')
style0.configure(
    'TRadiobutton', font=('meiryo', 10),
    foreground='black')
style0.configure(
    'TEntry', font=('meiryo', 10),
    foreground='red')

frame0 = ttk.LabelFrame(master, text="部材種", padding=5, width=500)
frame1 = ttk.Label(frame0, padding=5, width=400)
frame10 = ttk.Label(frame1, padding=0, width=400)
frame2 = ttk.Label(frame0, padding=5)
frame3 = ttk.Label(frame2, padding=5)

row_type_steel_material_guide = 3
ttk.Label(frame3, text="高さ(h)").grid(row=row_type_steel_material_guide, column=1)
ttk.Label(frame3, text="幅(w)").grid(row=row_type_steel_material_guide, column=3)
ttk.Label(frame3, text="厚さ(r)").grid(row=row_type_steel_material_guide, column=5)

row_type_steel_material = 4
entry_width_type_steel = 5
ttk.Label(frame3, text="鋼材種").grid(row=row_type_steel_material)
ttk.Entry(frame3, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=1)
ttk.Label(frame3, text="×").grid(row=row_type_steel_material, column=2)
ttk.Entry(frame3, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=3)
ttk.Label(frame3, text="×").grid(row=row_type_steel_material, column=4)
ttk.Entry(frame3, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=5)
ttk.Label(frame3, text="[mm]").grid(row=row_type_steel_material, column=6)

frame4 = ttk.Label(frame2, padding=5)

row_type_steel_material_guide = 3
ttk.Label(frame4, text="高さ(h)").grid(row=row_type_steel_material_guide, column=1)
ttk.Label(frame4, text="幅(w)").grid(row=row_type_steel_material_guide, column=3)
ttk.Label(frame4, text="ｳｪﾌﾞ(r1)").grid(row=row_type_steel_material_guide, column=5)
ttk.Label(frame4, text="ﾌﾗﾝｼﾞ(r2)").grid(row=row_type_steel_material_guide, column=7)

row_type_steel_material = 4
entry_width_type_steel = 5
ttk.Label(frame4, text="鋼材種").grid(row=row_type_steel_material)
ttk.Entry(frame4, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=1)
ttk.Label(frame4, text="×").grid(row=row_type_steel_material, column=2)
ttk.Entry(frame4, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=3)
ttk.Label(frame4, text="×").grid(row=row_type_steel_material, column=4)
ttk.Entry(frame4, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=5)
ttk.Label(frame4, text="×").grid(row=row_type_steel_material, column=6)
ttk.Entry(frame4, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=7)
ttk.Label(frame4, text="[mm]").grid(row=row_type_steel_material, column=8)

frame5 = ttk.LabelFrame(master, text="耐火被覆", padding=5)
frame5_0 = ttk.Frame(frame5)
combo01 = ttk.Combobox(frame5_0, state='readonly')
combo01["values"] = ("ロックウール","セラミックファイバー")
combo01.current(0)
combo01.pack(side='left')
frame50 = ttk.Frame(frame5)
ttk.Label(frame50, text="厚さ").grid(row=0)
ttk.Entry(frame50, width=entry_width_type_steel, justify="right").grid(row=0, column=1)
ttk.Label(frame50, text="[mm]").grid(row=0, column=2)

frame51 = ttk.Frame(frame5)
frame511 = ttk.Frame(frame51)
e01 = ttk.Entry(frame511, width=entry_width_type_steel, justify="right")
frame512 = ttk.Frame(frame51)
e02 = ttk.Entry(frame512, width=entry_width_type_steel, justify="right", state="readonly")

v1 = tk.StringVar()
v1.set('A')
rb1 = ttk.Radiobutton(
    frame10,
    text='角形鋼管   ',
    value='A',
    variable=v1,
    command=rb_clicked)
rb1.pack(side='left')

rb2 = ttk.Radiobutton(
    frame10,
    text='H形鋼',
    value='B',
    variable=v1,
    command=rb_clicked)
rb2.pack()

v2 = tk.StringVar()

v2.set('A')
rb3 = ttk.Radiobutton(
    frame511,
    text='計算層数',
    width=10,
    value='A',
    variable=v2,
    command=rb_clicked1)
rb3.grid()
e01.grid(row=0, column=1)
ttk.Label(frame511, text="層     ").grid(row=0, column=3)

rb4 = ttk.Radiobutton(
    frame512,
    text='1層の厚さ',
    width=10,
    value='B',
    variable=v2,
    command=rb_clicked1)
rb4.grid()
e02.grid(row=0, column=1)
ttk.Label(frame512, text="[mm]").grid(row=0, column=3)

frame0.pack(fill='x')
# frame0.pack_propagate(0)

frame10.pack(side='left')
frame1.pack(fill='x')
# frame1.pack_propagate(0)
frame2.pack(fill='x')
# frame2.pack_propagate(0)
frame3.pack(side='left')


frame5.pack(fil="x")
frame5_0.pack(fill='x')
frame50.pack(side='left')
frame51.pack(side='left')
frame511.pack()
frame512.pack()

master.mainloop()
