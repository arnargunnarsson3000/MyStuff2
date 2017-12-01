# !/usr/bin/python3
import tkinter as tk
from tkinter import *
import os, sys
import tkinter
import sqlite3
import engineer.SQLbeast.sql_class as sql
from engineer.SQLbeast.DEFAULT_SQL_COMMANDS import *

DEFDIR = os.path.dirname(sys.argv[0])
DEFDB = "/media/addi/AddiStuff/MyStuff/engineer/TestScripts/Test_DB.db"
DEFDBdb = "TEMP_MESH"

def NewWindowOpt():
    """
    This is what happens when 'New' is pressed
    :return:
    """
    print("Went to new window")
    print(app)
    pass

def OpenFileBrowse():
    """
    This is what happens when 'Open' is pressed
    :return:
    """
    print(os.listdir())

def ListTools():
    """
    Lists available tools, when tools are pressed
    :return:
    """

class gui(tk.Frame):
    """
    gui class
    """
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)         # initializes frame with master
        # self.pack()                             # makes gui as small as possible
        self.createWidgets()

    def createWidgets(self):
        """
        Creates widgets for gui
        :return:
        """
        # Adding cascade automatically adds next to previous, done in chronological order
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)                             # Menu(mastermenu, options), creates option in menubar
        filemenu.add_command(label="New", command=NewWindowOpt)         # Creates menu option, label is new and runs command
        filemenu.add_command(label="Open", command=OpenFileBrowse)


        filemenu.add_separator()                                        # adds a separator between options in filemenu
        filemenu.add_command(label="Exit", command=self.master.quit)    # closes window
        menubar.add_cascade(label="File", menu=filemenu)                # Once all options/shit added to filemenu, run this

        toolsmenu = Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="List Tools", command=ListTools)
        menubar.add_cascade(label="Tools", menu=toolsmenu)

        self.master.config(menu=menubar)                    # run this once entire menu bar is ready


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
    app = gui(root)
    app.mainloop()
