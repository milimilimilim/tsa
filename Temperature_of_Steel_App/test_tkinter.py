import tkinter as tk
from tkinter import ttk


def button1_clicked():
    print('v1 = %s' % v1.get())
    quit()


def rb_clicked():
    print('v1 = %s' % v1.get())
    input_frame = ttk.LabelFrame(frame1, text="test")


    if v1.get() == 'A':
        input_frame.pack_forget()
        tk.Label(input_frame, text="no").grid(row=3)
        input_frame.pack()
    elif v1.get() == 'B':
        input_frame.pack_forget()
        tk.Label(input_frame, text="yes").grid(row=3)
        input_frame.pack()


def make_frame():
    pass

# master = tk.Tk()
# master.geometry("300x400")
#
# frame0 = ttk.Labelframe(master, text='部材種', padding=5).grid(row=0, column=0)
#
# # tk.Label(frame0, text="鋼材種").grid(row=1)
#
# frame1 = ttk.LabelFrame(frame0, text='Options').grid(row=1, column=0)
#
# tk.Label(frame1, text="鋼材種").grid(row=2)
#
# frame0.pack()
# frame1.pack()
#
# master.mainloop()
root = tk.Tk()
root.geometry("300x400")
frame1 = ttk.LabelFrame(root, text="部材種", padding=5)
frame3 = ttk.Label(frame1)
frame4 = ttk.LabelFrame(frame1, text="test")
# label1 = ttk.Label(frame1,text="text1").grid(row=0,column=0)

v1 = tk.StringVar()
v1.set('A')
rb1 = ttk.Radiobutton(
    frame3,
    text='Option 1',
    value='A',
    variable=v1,
    command=rb_clicked,
    width=10)
# rb1.grid(row=0, column=0, sticky="WE")
rb1.pack(side = 'left')

rb2 = ttk.Radiobutton(
    frame3,
    text='Option 2',
    value='B',
    variable=v1,
    command=rb_clicked,
    width=10)
# rb2.grid(row=0, column=1, sticky="WE")
rb2.pack(side = 'left')
frame2 = ttk.LabelFrame(frame1, text="鋼材種")

if v1.get() == 'A':
    entry1 = ttk.Entry(frame2).grid(row=2, column=0)
    button1 = ttk.Button(frame2, text="BUTTON1").grid(row=2, column=1)
else:
    label_0 = tk.Label(frame2, text="no").grid(row=3)

frame3.pack()
frame2.pack()  # frame2を配置(綴じる)
frame1.grid(row=0, column=0)  # frame1を配置(綴じる)
# frame4.pack()
rb_clicked


root.mainloop()
