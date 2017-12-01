# !/usr/bin/python3
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import os, sys
import tkinter
import sqlite3
import engineer.SQLbeast.sql_class as sql
from engineer.SQLbeast.DEFAULT_SQL_COMMANDS import *
import engineer.GrUvI.my_naut as naut
import engineer.GrUvI.text_to_frame as t2f

class db2frame(tk.Frame):
    """
    Browse through database tables
    """
    def __init__(self, master=None, db=None):
        tk.Frame.__init__(self, master)
        self.db = db
        self.table_browse = Frame(master)
        self.mylist = Listbox(self.table_browse)
        self.scrollbar = Scrollbar(self.table_browse)
        self.table_browse.pack(side='left', fill='y')
        self.scrollbar.pack(side="right", fill=Y)
        self.mylist.pack(side="left", fill=Y)
        self.mylist.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.mylist.yview)
        self.db_frame = Frame(master)
        self.Tree = None
        self.list_boxdb()

    def read_table(self, table):
        """
        Reads all data from a table in a database
        :param table:
        :return:
        """
        return READ_TABLE(table, db=self.db)

    def list_tables(self):
        """
        List all tables in db
        :return:
        """
        return LIST_TABLES(db=self.db)

    def select_table(self):
        """
        Selects and displays table
        :return:
        """

        selected = self.mylist.selection_get()
        data = self.read_table(selected)
        db_frame = self.db_frame

        db_frame.pack(side="left", fill="both")
        col_names = tuple(("heading%d" % i for i in range(len(data[0]))))
        if not self.Tree:
            self.Tree = Treeview(db_frame, columns=col_names)
        else:
            self.Tree.destroy()
            self.scrollbarY.destroy()
            self.scrollbarX.destroy()
            self.Tree = Treeview(db_frame, columns=col_names)
        self.scrollbarY = Scrollbar(db_frame)
        self.scrollbarX = Scrollbar(db_frame, orient=HORIZONTAL)
        self.Tree.config(yscrollcommand=self.scrollbarY.set,
                         xscrollcommand=self.scrollbarX.set)

        for x in data:
            self.Tree.insert('', 'end', values=x)
        for col in col_names:
            self.Tree.heading(col, text=col)
        self.scrollbarY.config(command=self.Tree.yview)
        self.scrollbarY.pack(side='right', fill=Y)
        self.scrollbarX.config(command=self.Tree.xview)
        self.scrollbarX.pack(side='bottom', fill=X)
        self.Tree.pack(side='left', fill='both')


    def list_boxdb(self):
        """
        Makes the listbox of the current directory
        :return:
        """
        self.tables = self.list_tables()
        for table in self.tables:
            self.mylist.insert(END, table[0])
        self.mylist.bind('<Double-1>', lambda x: self.select_table())



if __name__ == "__main__":
    root = tk.Tk()
    db = "/media/addi/AddiStuff/MyStuff/engineer/TestScripts/Test_DB.db"
    d2f = db2frame(root, db)
    d2f.mainloop()


