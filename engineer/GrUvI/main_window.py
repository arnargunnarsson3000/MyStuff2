# !/usr/bin/python3
import tkinter as tk
from tkinter import *
import os, sys
import tkinter
import sqlite3
import engineer.SQLbeast.sql_class as sql
from engineer.SQLbeast.DEFAULT_SQL_COMMANDS import *
import engineer.GrUvI.my_naut as naut
import engineer.GrUvI.text_to_frame as t2f
import engineer.GrUvI.db_to_frame as d2f
import engineer.FVM_temp.house2 as house
from engineer.FVM_temp.FVM2 import fvm
from engineer.FVM_temp.plotting import animation
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

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
        self.fil_win = None
        self.house_frame = None
        self.fvm_frame = None
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
        filemenu.add_command(label="Open", command=self.OpenFileBrowse)

        filemenu.add_separator()                                        # adds a separator between options in filemenu
        filemenu.add_command(label="Exit", command=self.master.quit)    # closes window

        menubar.add_cascade(label="File", menu=filemenu)                # Once all options/shit added to filemenu, run this

        toolsmenu = Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="List Tools", command=ListTools)
        toolsmenu.add_command(label="Create House", command=self.House)
        menubar.add_cascade(label="Tools", menu=toolsmenu)

        self.master.config(menu=menubar)                    # run this once entire menu bar is ready

    def OpenFileBrowse(self):
        """
        This is what happens when 'Open' is pressed
        :return:
        """
        nautilus = Tk()
        browse = naut.nautilus(nautilus)
        browse.mainloop()
        self.chosen_file = browse.chosen_file  # returns the file chosen
        browse.master.destroy()  # when quitting must be done both inside naut.nautilus AND here

        self.open_file()

    def House(self):
        """
        Opens up a frame where one can design and edit a house
        :return:
        """
        h = house.House
        self.curr = house.House(1, 1, 5, 5, 10)
        self.house_mesh = self.curr.rmesh()
        self.house = self.curr
        def update_stuff(a, self):
            if not self.curr:
                self.curr = house.House(float(x1.get()), float(x2.get()), float(h.get()), float(w.get()), float(acc.get()))
            self.house_mesh = self.curr.rmesh()
            self.house = self.curr
            self.d = 1 / self.curr.scale
            a.clear()
            point = self.curr.plot_points()
            for each in point:
                a.plot(each[0], each[1], '*')
            canvas.show()
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        def add_roof(a, self):
            if not self.curr:
                self.curr = house.House(int(x1.get()), int(x2.get()), int(h.get()), int(w.get()), int(acc.get()))
            self.curr.add_roof()
            self.house_mesh = self.curr.rmesh()
            self.d = 1/self.curr.scale
            a.clear()
            point = self.curr.plot_points()
            for each in point:
                a.plot(each[0], each[1], '*')
            canvas.show()
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        def add_floor(a, self):
            if not self.curr:
                self.curr = house.House(int(x1.get()), int(x2.get()), int(h.get()), int(w.get()), int(acc.get()))
            self.curr.add_floor()
            self.house_mesh = self.curr.rmesh()
            self.d = 1 / self.curr.scale
            a.clear()
            point = self.curr.plot_points()
            for each in point:
                a.plot(each[0], each[1], '*')
            canvas.show()
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        def add_chimney(a, self):
            if not self.curr:
                self.curr = house.House(int(x1.get()), int(x2.get()), int(h.get()), int(w.get()), int(acc.get()))
            self.curr.add_chimney()
            self.house_mesh = self.curr.rmesh()
            self.d = 1 / self.curr.scale
            a.clear()
            point = self.curr.plot_points()
            for each in point:
                a.plot(each[0], each[1], '*')
            canvas.show()
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        def clearmesh(a, self):
            self.curr = None
            update_stuff(a, self)


        if self.house_frame:
            self.house_frame.destroy()
        self.house_frame = Frame(self.master)
        self.house_frame.pack(side='left', fill=BOTH)
        initFrame = Frame(self.house_frame)
        initFrame.pack(side='top')
        buttonFrame = Frame(self.house_frame)
        buttonFrame.pack(side='left')
        figureFrame = Frame(self.house_frame)
        figureFrame.pack(side='right')
        addfloor = Button(buttonFrame, text="add floor", command=lambda : add_floor(a, self))
        addfloor.pack(side='top')
        addroof = Button(buttonFrame, text="add roof", command=lambda : add_roof(a, self))
        addroof.pack(side='top')
        addchimney = Button(buttonFrame, text="add chimney", command=lambda : add_chimney(a, self))
        addchimney.pack(side='top')
        updatebutt = Button(buttonFrame, text="update mesh", command=lambda : update_stuff(a, self))
        updatebutt.pack(side='top')
        clear_mesh = Button(buttonFrame, text="Clear mesh", command=lambda: clearmesh(a, self))
        clear_mesh.pack(side='top')
        export_mesh = Button(buttonFrame, text="Export mesh", command=self.exportmesh)
        export_mesh.pack(side='top')

        x1 = Entry(initFrame, text='wall thickness')
        x1.pack(side='left')
        x1.insert(END, 1)
        x2 = Entry(initFrame, text='roof thickness')
        x2.pack(side='left')
        x2.insert(END, 1)
        h = Entry(initFrame, text='height')
        h.pack(side='left')
        h.insert(END, 5)
        w = Entry(initFrame, text='width')
        w.pack(side='left')
        w.insert(END, 5)
        acc = Entry(initFrame, text='accuracy')
        acc.pack(side='left')
        acc.insert(END, 10)

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)


        canvas = FigureCanvasTkAgg(f, self.house_frame)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self.house_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        update_stuff(a, self)

    def exportmesh(self):
        """
        export mesh to perform FVM on it
        :return:
        """
        if self.fvm_frame:
            self.fvm_frame.destroy()
        mesh = self.house_mesh
        hous = self.house
        print("managed to export")
        self.fvm_frame = Frame(self.master)

        self.conv = False
        self.both = False
        self.fvm_frame.pack(side='right')
        Label(self.fvm_frame, text="T initial").grid(row=1, column=0)
        Label(self.fvm_frame, text="rho").grid(row=2, column=0)
        Label(self.fvm_frame, text="cp").grid(row=3, column=0)
        Label(self.fvm_frame, text="k").grid(row=4, column=0)
        Label(self.fvm_frame, text="outside").grid(row=0, column=1)
        Label(self.fvm_frame, text="material").grid(row=0, column=2)
        Label(self.fvm_frame, text="ground").grid(row=0, column=3)
        Label(self.fvm_frame, text="inside").grid(row=0, column=4)
        Label(self.fvm_frame, text="Time:").grid(row=5, column=3)
        T0 = [273.15, 283.15]
        Ti = 273.15
        To = 283.15
        Tg = 278.15
        k = [1.6, 2.624 * 10 ** -1]
        ki = 0.02624
        ko = 0.02624
        kg = 1.5
        cp = [900, 100]
        cpi = 1.0057
        cpo = 1.0057
        cpg = 800
        rho = [2300, 7.706]
        rhoi = 1.1774
        rhoo = 1.1774
        rhog = 2000
        # outside = 0, material =1, nomaterial, ground=last-1, last = air
        rho = [rhoo, rho[0], rhog, rhoi]
        k = [ko, k[0], kg, ki]
        cp = [cpo, cp[0], cpg, cpi]
        T = [To, T0[0], Tg, Ti]
        defaults = [T, rho, cp, k]
        values = [[Entry(self.fvm_frame) for j in range(4)] for i in range(4)]
        timeE = Entry(self.fvm_frame)
        timeE.grid(row=5, column=4)
        timeE.insert(END, "60*60*24*5")
        for i in range(4):
            for j in range(4):
                values[i][j].grid(row=i+1, column=j+1)
                values[i][j].insert(END, defaults[i][j])
        def do_fvm(self):
            data1 = []
            data2 = []
            arr = [[0 for j in range(4)] for i in range(4)]
            for i in range(4):
                for j in range(4):
                    arr[i][j] = values[i][j].get()
            scale = 1/self.d
            T = arr[0]
            rho = arr[1]
            cp = arr[2]
            k = arr[3]
            const = [1, 0, 1, 1]
            time = timeE.get()
            if '*' in time:
                tot = 1
                time = time.split('*')
                for each in time: tot *= float(each)
                time = tot
            if not self.conv or self.both:
                try:
                    f = fvm(mesh, [float(i) for i in T],
                            [float(i) for i in k],
                            [float(i) for i in cp],
                            [float(i) for i in rho], const, scale, "fvm_cond", house_class=hous)
                    f.T_E(t=time)
                except sqlite3.OperationalError:
                    os.remove(f.db)
                    CREATE_DB(f.db)
                    CREATE_TABLE(f.project, 'tables')
                    f = fvm(mesh, [float(i) for i in T],
                            [float(i) for i in k],
                            [float(i) for i in cp],
                            [float(i) for i in rho], const, scale, "fvm_cond", house_class=hous)
                    f.T_E(t=time)
                conn, curs = f.sql.cc()
                data1 = f.sql.read_table(curs, 'data')
                f.sql.ccc(conn)
            if self.conv or self.both:
                f = fvm(mesh, [float(i) for i in T],
                        [float(i) for i in k],
                        [float(i) for i in cp],
                        [float(i) for i in rho], const, scale, "fvm_conv", house_class=hous)
                f.k_air = float(self.convEntry[0].get())
                f.Pr = float(self.convEntry[1].get())
                f.nu_air = float(self.convEntry[2].get())
                try:
                    f.T_Ec(t=time)
                except sqlite3.OperationalError:
                    os.remove(f.db)
                    CREATE_DB(f.db)
                    CREATE_TABLE(f.project, 'tables')
                    f = fvm(mesh, [float(i) for i in T],
                            [float(i) for i in k],
                            [float(i) for i in cp],
                            [float(i) for i in rho], const, scale, "fvm_conv", house_class=hous)
                    f.T_Ec(t=time)
                conn, curs = f.sql.cc()
                data2 = f.sql.read_table(curs, 'data')
                f.sql.ccc(conn)
            if data1 and not data2:
                data = data1
                for i in range(len(data)):
                    data[i] = data[i][1]
            elif not data1 and data2:
                data = data2
                for i in range(len(data)):
                    data[i] = data[i][1]
            else:
                data = []
                f.project = "both"
                for k in range(len(data1)):
                    m1 = f.str2mat(data1[k][1]).A
                    m2 = f.str2mat(data2[k][1]).A
                    for i in range(len(m1)):
                        m1[i] += m2[i]
                    data.append(m1)


            writer, ani = animation(data, f, name='Implicit', interval=50)
            name = 'animation%s.mp4' % f.project
            if os.path.exists(name):
                count=1
                while os.path.exists(name):
                    name = 'animation%s%d.mp4' % (f.project, count)
                    count += 1
            ani.save(name, writer=writer)
            print("\nVideo can be found in path:\n\t%s\n"%os.path.realpath(name))


        def inc_conv(self):
            """Include convection"""
            self.convEntry = [Entry(self.fvm_frame), Entry(self.fvm_frame), Entry(self.fvm_frame)]
            label = ['k_air', 'Pr', 'kinematic visc']
            defva = [0.02624, 0.71, 15.69*10**-6]
            self.conv = True
            for i in range(len(self.convEntry)):
                self.convEntry[i].grid(row=7, column=i+1)
                Label(self.fvm_frame, text=label[i]).grid(row=6, column=i+1)
                self.convEntry[i].insert(END, defva[i])
        def doboth(self): self.both = True
        convec = Button(self.fvm_frame, text="Include convection", command=lambda: inc_conv(self))
        launch = Button(self.fvm_frame, text="Launch", command=lambda: do_fvm(self))
        compbo = Button(self.fvm_frame, text="Compare Both", command=lambda: doboth(self))
        launch.grid(row=5, column=0)
        convec.grid(row=5, column=1)
        compbo.grid(row=5, column=2)


    def open_file(self):
        """
        Opens the file in Read-mode if it is right format
        :return:
        """
        if self.fil_win:
            self.fil_win.destroy()
        self.fil_win = Frame(self.master)
        self.fil_win.pack(side='left', fill=BOTH, expand=True)
        if ".db" in self.chosen_file:
            textwin = d2f.db2frame(master=self.fil_win, db=self.chosen_file)
        else:
            textwin = t2f.tex2frm(master=self.fil_win, text=self.chosen_file)


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
    print("here")

