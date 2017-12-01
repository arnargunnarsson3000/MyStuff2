# !/usr/bin/python3
import tkinter as tk
from tkinter import *
import os, sys
import tkinter
import sqlite3
import engineer.SQLbeast.sql_class as sql
from engineer.SQLbeast.DEFAULT_SQL_COMMANDS import *
import engineer.GrUvI.my_naut as naut

class tex2frm(tk.Frame):
    """
    displays text file in own frame
    """

    def __init__(self, master=None, text=None):
        tk.Frame.__init__(self, master=master)
        self.text = text

        self.text_file = "..."
        self.scroll_barY()
        self.scroll_barX()
        textbox = Text(self.master, wrap=NONE,
                       yscrollcommand=self.scrollbarY.set,
                       xscrollcommand=self.scrollbarX.set)

        self.scrollbarY.config(command=textbox.yview)
        self.scrollbarX.config(command=textbox.xview)
        textbox.pack(side="left", fill="both", expand=True)
        text_str = [i for i in open(text, 'r')]
        for each in text_str:
            textbox.insert(END, each)

    def scroll_barY(self):
        """
        Vertical scrollbar
        :return:
        """
        scrollbar = Scrollbar(self.master)
        scrollbar.pack(side="right", fill="y")
        self.scrollbarY = scrollbar

    def scroll_barX(self):
        """
        Horizontal scrollbar
        :return:
        """
        scrollbar = Scrollbar(self.master, orient=HORIZONTAL)
        scrollbar.pack(side="bottom", fill="x")
        self.scrollbarX = scrollbar
