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


master = tk.Tk()
master.title("tsa_GUI")
master.geometry("330x400")

frame0 = ttk.LabelFrame(master, text="部材種", padding=5, width=500)
frame1 = ttk.Label(frame0, padding=5, width=400)
frame2 = ttk.LabelFrame(frame0, text="鋼材種", padding=5)
frame3 = ttk.Label(frame2, padding=5)

row_type_steel_material_guide = 3
ttk.Label(frame3, text="高さ(h)", font=("meiryo", 10)).grid(row=row_type_steel_material_guide, column=1)
ttk.Label(frame3, text="幅(w)", font=("meiryo", 10)).grid(row=row_type_steel_material_guide, column=3)
ttk.Label(frame3, text="鋼材厚(r)", font=("meiryo", 10)).grid(row=row_type_steel_material_guide, column=5)

row_type_steel_material = 4
entry_width_type_steel = 5
ttk.Label(frame3, text="鋼材種").grid(row=row_type_steel_material)
ttk.Entry(frame3, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=1)
ttk.Label(frame3, text="×").grid(row=row_type_steel_material, column=2)
ttk.Entry(frame3, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=3)
ttk.Label(frame3, text="×").grid(row=row_type_steel_material, column=4)
ttk.Entry(frame3, width=entry_width_type_steel, justify="right").grid(row=row_type_steel_material, column=5)

frame4 = ttk.Label(frame2, padding=5)

row_type_steel_material_guide = 3
ttk.Label(frame4, text="高さ(h)", font=("", 11)).grid(row=row_type_steel_material_guide, column=1)
ttk.Label(frame4, text="幅(w)", font=("", 11)).grid(row=row_type_steel_material_guide, column=3)
ttk.Label(frame4, text="ウェブ(r1)", font=("", 9)).grid(row=row_type_steel_material_guide, column=5)
ttk.Label(frame4, text="フランジ(r2)", font=("", 9)).grid(row=row_type_steel_material_guide, column=7)

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

frame5 = ttk.LabelFrame(frame0, text="耐火被覆", padding=5)
ttk.Label(frame5, text="厚さ").grid(row=0)
ttk.Entry(frame5, width=entry_width_type_steel, justify="right").grid(row=0, column=1)

v1 = tk.StringVar()

v1.set('A')
rb1 = ttk.Radiobutton(
    frame1,
    text='角形鋼管',
    value='A',
    variable=v1,
    command=rb_clicked)
rb1.pack(fil="x", side='left')

rb2 = ttk.Radiobutton(
    frame1,
    text='H形鋼',
    value='B',
    variable=v1,
    command=rb_clicked)
rb2.pack(fil="x", side='left')


frame0.pack(fill='x')
# frame0.pack_propagate(0)

frame1.pack()
# frame1.pack_propagate(0)
frame2.pack(fill='x')
# frame2.pack_propagate(0)
frame3.pack(side='left')

frame5.pack()

master.mainloop()
