import os, sys
from tkinter import *
import tkinter as tk

class nautilus(tk.Frame):
    """
    GUI for browsing and selecting file
    """

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)  # initializes frame with master
        self.pack()                          # makes gui as small as possible, also used to pack side='left', 'right' etc
        # use for frames within frames (?)
        self.curdir = os.path.dirname(__file__)
        self.scroll_bar()
        self.mylist = Listbox(self.master, yscrollcommand=self.scrollbar.set)
        self.listbox_curdir()
        self.create_dir_frame = None
        self.create_dir_option()

    def askEntry(self):
        """
        ask for entry
        :return:
        """
        def export_dir(self):
            print("here")
            self.selFolder = entry.get()
            self.quit()
        def mk_dir(self):
            if not os.path.exists(entry.get()):
                os.mkdir(entry.get())
            export_dir(self)

        entry = Entry(self.create_dir_frame)
        entry.insert(END, self.curdir)
        eButt = Button(self.create_dir_frame, text="go", command= lambda : mk_dir(self))
        eButt.pack(side="right")
        eSel = Button(self.create_dir_frame, text="Select Dir", command=lambda: export_dir(self))
        eSel.pack(side="right")
        entry.pack(side="right")


    def create_dir_option(self):
        """
        Option to create a directory
        :return:
        """
        if self.create_dir_frame:
            self.create_dir_frame = None
        if not self.create_dir_frame:
            self.selFolder = None
            self.create_dir_frame = Frame(self.master)
            self.create_dir_frame.pack(side="right", fill=BOTH)
            self.new_dir_butt = Button(self.create_dir_frame, text="New Folder", command=self.askEntry)
            self.new_dir_butt.pack(side=RIGHT)
            self.select_folder = Button(self.create_dir_frame, text="New Folder", command=self.askEntry)



    def scroll_bar(self):
        """
        Creates scrollbar for files browser
        :return:
        """
        scrollbar = Scrollbar(self.master)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar = scrollbar


    def selection(self):
        """
        select from listbox
        :return:
        """
        selected = self.mylist.selection_get()
        if os.path.isfile(os.path.join(self.curdir, selected)):
            self.chosen_file = os.path.join(self.curdir, selected)
            self.master.quit()     # when quitting must be done both outside where func is called AND here
            # not quitting can be used to yield values
        self.update_naut(selected)

    def update_naut(self, selected):
        """
        Updates the nautilus after selection
        :param selected:
        :return:
        """
        if selected == "...":
            self.curdir = os.path.abspath(os.path.join(self.curdir, os.pardir))
            self.mylist.delete(0, END)
            self.listbox_curdir()
        elif os.path.isdir(os.path.join(self.curdir, selected)):
            self.curdir = os.path.join(self.curdir, selected)
            self.mylist.delete(0, END)
            self.listbox_curdir()


    def listbox_curdir(self):
        """
        Makes the listbox of the current directory
        :return:
        """
        self.mylist.insert(END, "...")
        for fil in os.listdir(self.curdir):
            self.mylist.insert(END, fil)

        self.mylist.pack(side=LEFT, fill=Y)
        self.scrollbar.config(command=self.mylist.yview)

        self.mylist.bind('<Double-1>', lambda x: self.selection())

if __name__ == "__main__":
    root = tk.Tk()
    nautilus(root).mainloop()
