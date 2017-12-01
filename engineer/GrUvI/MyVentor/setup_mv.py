from engineer.SQLbeast.sql_class import sql_cmds as sqls
import tkinter as tk
from tkinter import*
import docopt
import os
import sys
from engineer.GrUvI.my_naut import nautilus

"""
<short>
DESCRIPTION: 

USAGE:
    setup_mv.py --option [--option2] [--varflag <var>] [--verbose] [--debug]
    setup_mv.py -h | --help
    setup_mv.py -v | --version

OPTIONS:
    -h, --help       Shows this help and exits
    -v, --version    Print tool version and exits
    --verbose        Run with lots of information
    --debug          Run in debug mode

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Author:		Arnar Evgeni Gunnarsson
Date:		2017-11-28
Version:	dev
Contact:	s171950@student.dtu.dk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Engineering Design & Applied Mechanics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Development of Engineering Tools
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""

CURDIR = os.path.dirname(__file__)

class setup_mv(Frame):
    """
    Setup myventor
    """
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.init_frames()
        self.choose_dir()


    def init_frames(self):
        """
        Initializes Frames
        :return:
        """
        self.naut = None
        self.choose_dirf = None

    def init_vars(self):
        """
        Initializes needed variables
        :return:
        """
        self.install_dir = ""
        self.def_save_dir = ""
        self.selFolder = None

    def choose_dir(self):
        """
        Choose default directories and stuff
        :return:
        """
        def go(self):
            self.install_dir = inst.get()
            self.def_save_dir = defs.get()

        def browsei(self):
            naut = self.nautilus_init()
            print(self.selFolder)
            if self.selFolder:
                inst.delete(END)
                inst.insert(END, self.selFolder)
                self.selFolder = None
                # naut.destroy()
        def browses(self):
            naut = self.nautilus_init()
            print(self.selFolder)
            if self.selFolder:
                defs.delete(END)
                defs.insert(END, self.selFolder)
                self.selFolder = None
                # naut.destroy()

        if not self.choose_dirf:
            self.choose_dirf = Frame(self.master)
            self.choose_dirf.pack(side="left")
        Label(self.choose_dirf, text="Default Save Directory").grid(row=1, column=0)
        Label(self.choose_dirf, text="Install Directory").grid(row=2, column=0)
        inst = Entry(self.choose_dirf, width=75)
        inst.insert(END, CURDIR)
        defs = Entry(self.choose_dirf, width=75)
        defs.insert(END, CURDIR)
        inst.grid(row=2, column=1)
        defs.grid(row=1, column=1)
        chooseB = Button(self.choose_dirf, text="Install", command=lambda: go(self))
        browseBs = Button(self.choose_dirf, text="Browse Files", command=lambda: browses(self))
        browseBi = Button(self.choose_dirf, text="Browse Files", command=lambda: browsei(self))
        chooseB.grid(row=3, column=3)
        browseBi.grid(row=2, column=4)
        browseBs.grid(row=1, column=4)



    def nautilus_init(self):
        """
        File browser for default settings and setup
        :return:
        """
        if self.naut:
            pass
        naut = tk.Tk()
        nautf = nautilus(naut)
        nautf.mainloop()
        self.selFolder = nautf.selFolder
        nautf.master.destroy()




if __name__ == '__main__':

    if len(sys.argv) == 1:
        print(__doc__)
        # exit(0)

    root_frame = tk.Tk()
    app = setup_mv(root_frame)
    app.mainloop()
    # perhaps execute system check
