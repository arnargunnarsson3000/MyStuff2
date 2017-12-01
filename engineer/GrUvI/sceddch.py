import tkinter as tk
from tkinter import *
from engineer.GrUvI.draw_objects import *
from engineer.GrUvI.highlight_object import *

class drawFrame(Frame):
    """
    A frame/canvas for drawing stuff :)
    """

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.define_frames()
        self.do_canvas()
        self.option_buttons()
        self.object_handler = object_handler()
        self.pack_stuff()

    def define_frames(self):
        """
        Initiates empty variables of included frames in this class
        :return:
        """
        self.opt_but_frame = None       # Option Button Frame
        self.canvas_frame = None        # canvas frame
        self.curr_obj = None            # current object being drawn
        self.lines = []                 # contains all line objects
        self.points = []                # contains all point objects
        self.circles = []
        self.lclick = False             # is button one currently being pressed
        self.selected_obj = None        # which object is currently being selected
        self.highlighted_obj = None

    def mousemove(self, evt):
        # print("move")
        curr_highlight = False          # any current items highlighted on this run
        for obj in self.points:
            if obj.over(evt):
                curr_highlight = True
                self.highlighted_obj = obj

        for obj in self.circles:
            obj.over(evt)
            if obj.over(evt):
                curr_highlight = True
                self.highlighted_obj = obj

        for obj in self.lines:
            obj.over(evt)
            if obj.over(evt):
                curr_highlight = True
                self.highlighted_obj = obj
        if not curr_highlight:
            self.highlighted_obj = None


    def mouse1click(self, evt):
        print("mouseclick")
        self.lclick = True
        if self.curr_obj:
            if not self.click and self.curr_obj != "point":
                self.point_start = [evt.x, evt.y]
                self.click = True
            elif self.curr_obj == "point":
                self.points.append(point(self.canvas_frame, evt))
                self.curr_obj = None
            else:
                if self.curr_obj == "line":
                    self.lines.append(line(self.canvas_frame, [self.point_start[0], self.point_start[1], evt.x, evt.y]))
                if self.curr_obj == "circle":
                    self.circles.append(circle(self.canvas_frame, self.point_start, evt))
                self.click = False
                self.curr_obj = None
        if self.highlighted_obj:
            print("highlighted object click success")
            self.highlighted_obj.select_function()
            self.selected_obj = self.highlighted_obj
        if self.selected_obj and not self.selected_obj.over(evt):
            self.selected_obj.return_to_default()
            self.selected_obj = None


    def mouse1release(self, evt):
        print("mouse1release")
        self.lclick = False
        pass  # do something when mouse 1 released

    def do_canvas(self):
        """
        Makes the canvas to draw on!
        :return:
        """

        if self.canvas_frame:
            # do something
            pass
        if not self.canvas_frame:
            self.click = False
            self.canvas_frame = Canvas(self.master)
            self.canvas_frame.config(bg="white",width=600, height=600)
            self.canvas_frame.bind("<Motion>", self.mousemove)
            self.canvas_frame.bind("<ButtonPress-1>", self.mouse1click)
            self.canvas_frame.bind("<ButtonRelease-1>", self.mouse1release)


    def init_line(self):
        """
        Creates and does stuff to line
        :return:
        """
        self.curr_obj = "line"
        pass # for now

    def init_circle(self):
        """
        Creates and does stuff to line
        :return:
        """
        self.curr_obj = "circle"
        pass # for now

    def init_point(self):
        """
        Creates and does stuff to line
        :return:
        """
        self.curr_obj = "point"
        pass # for now

    def delete_selected(self):
        """
        Deletes selected object
        :return:
        """
        if self.selected_obj:
            self.selected_obj.delete_object()

    def option_buttons(self):
        """
        Add option side buttons
        :return:
        """
        if self.opt_but_frame:
            # do whatever to this frame
            pass
        if not self.opt_but_frame:
            self.opt_but_frame = Frame(self.master)
            self.opt_stuff = {
                "scrollbar": Scrollbar(self.opt_but_frame),
                "line":      Button(self.opt_but_frame, text="line", command=self.init_line),
                "point":     Button(self.opt_but_frame, text="point", command=self.init_point),
                "circle":    Button(self.opt_but_frame, text="circle", command=self.init_circle),
                "delete":    Button(self.opt_but_frame, text="delete", command=self.delete_selected)
            }

    def pack_stuff(self):
        """
        Packs everything where it is supposed to go
        :return:
        """
        def pack_opt_frame(self):
            self.opt_but_frame.pack(side='left', fill=Y)

            scroll_pack = 'right'
            button_pack = 'bottom'

            self.opt_stuff["scrollbar"].pack(side=scroll_pack, fill='y')
            self.opt_stuff["line"].pack(side=button_pack)
            self.opt_stuff["point"].pack(side=button_pack)
            self.opt_stuff["circle"].pack(side=button_pack)
            self.opt_stuff["delete"].pack(side=button_pack)
        def pack_canvas(self):
            self.canvas_frame.pack(side="right")
        pack_opt_frame(self)
        pack_canvas(self)

if __name__ == "__main__":
    root = tk.Tk()
    draw = drawFrame(root)
    draw.mainloop()