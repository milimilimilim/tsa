import tkinter as tk
from tkinter import ttk


def button1_clicked():
    print('v1 = %s' % v1.get())
    quit()


def rb_clicked():
    print('v1 = %s' % v1.get())
    #  input_frame = ttk.LabelFrame(frame1, text="test")

    if v1.get() == 'A':
        # tL0.destroy()
        v2.set("A")
        ent01.configure(state='normal')

    elif v1.get() == 'B':
        # tL0.place(x=100,y=100)
        print("active")
        ent01.configure(state='readonly')


root = tk.Tk()
root.geometry("300x400")
frame0 = ttk.LabelFrame(root, text="部材種", padding=5, width=500)

tL0=tk.Label(root, text="[mm]")
tL0.place(x=100,y=100)

v1 = tk.StringVar()
v2 = tk.StringVar()
v3 = tk.StringVar()
# v3.set(" ")

lab_0 = ttk.Label(frame0,textvariable=v2)
ent01= ttk.Entry(frame0)
lab_0.pack()
ent01.pack()
ent01.pack_forget()
# v3.set("readonly")

ent01.pack()
v1.set('A')
rb1 = ttk.Radiobutton(
    frame0,
    text='角形鋼管   ',
    value='A',
    variable=v1,
    command=rb_clicked)
rb1.pack(side='left')

rb2 = ttk.Radiobutton(
    frame0,
    text='H形鋼',
    value='B',
    variable=v1,
    command=rb_clicked)
rb2.pack()


frame0.pack()

root.mainloop()
