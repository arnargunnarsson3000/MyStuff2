# !/usr/bin/python3
from tkinter import *
import os, sys
import tkinter
import sqlite3
import engineer.SQLbeast.sql_class as sql
from engineer.SQLbeast.DEFAULT_SQL_COMMANDS import *

DEFDIR = os.path.dirname(sys.argv[0])
DEFDB = "/media/addi/AddiStuff/MyStuff/engineer/TestScripts/Test_DB.db"
DEFDBdb = "TEMP_MESH"


def list_all():
    conn = sqlite3.connect(DEFDB)
    curs = conn.cursor()
    return LIST_TABLES(curs=curs)


def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()

def list_dir_menu(mb):
    for fil in os.listdir(DEFDIR):
        if os.path.isdir(fil):
            var = None
        mb.menu.add_checkbutton(label=fil,
                                variable=1)

def CurSelet(evt):
    print(evt)
    value=str((mylistbox.get(mylistbox.curselection())))
    print(value)

def browse_tables():
    root = Tk()
    sizex = 600
    sizey = 400
    posx = 40
    posy = 20
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    itemsforlistbox = ['one', 'two', 'three', 'four', 'five', 'six', 'seven']

    mylistbox = Listbox(root, width=60, height=10, font=('times', 13))
    mylistbox.bind('<<ListboxSelect>>', CurSelet)
    mylistbox.place(x=32, y=90)

    for items in itemsforlistbox:
        mylistbox.insert(END, items)
    root.mainloop()

if __name__ == "__main__":

    root = Tk()
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=browse_tables)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_command(label="Save as...", command=donothing)
    filemenu.add_command(label="Close", command=donothing)

    filemenu.add_separator()

    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo", command=donothing)

    editmenu.add_separator()

    editmenu.add_command(label="Cut", command=donothing)
    editmenu.add_command(label="Copy", command=donothing)
    editmenu.add_command(label="Paste", command=donothing)
    editmenu.add_command(label="Delete", command=donothing)
    editmenu.add_command(label="Select All", command=donothing)

    menubar.add_cascade(label="Edit", menu=editmenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)
    root.mainloop()