import tkinter as tk
from tkinter import *

class point:
    """
    point class
    """
    obj = "point"
    pointsize = 2
    highlighted = False
    selected = False
    lock = False
    def __init__(self, canvas=None, evt=None, points=None):
        self.canvas = canvas
        if evt:
            x1, y1 = (evt.x - self.pointsize), (evt.y - self.pointsize)
            x2, y2 = (evt.x + self.pointsize), (evt.y + self.pointsize)
            self.center = [evt.x, evt.y]
        else:
            x1, y1 = (points[0] - self.pointsize), (points[1] - self.pointsize)
            x2, y2 = (points[0] + self.pointsize), (points[1] + self.pointsize)
            self.center = [points[0], points[1]]

        self.point_obj = canvas.create_oval(x1, y1, x2, y2)
        self.points = [x1, y1, x2, y2]

    def delete_object(self):
        self.canvas.delete(self.point_obj)

    def over(self, evt):
        """
        Algorithms to check if mouse is over object, made for every type of object
        :param evt:
        :return:
        """

        if evt.x < self.points[2]+1 and evt.x > self.points[0]-1 and evt.y < self.points[3]+1 and evt.y > self.points[1]-1:
            self.canvas.itemconfig(self.point_obj, fill="red")
            self.highlighted = True
        else:
            if not self.selected and not self.lock:
                self.canvas.itemconfig(self.point_obj, fill="white")
            self.highlighted = False
        return self.highlighted

    def select_function(self):
        """
        What happens/changes when an object is selected
        :return:
        """
        print("trying to select point")
        self.selected = True
        self.canvas.itemconfig(self.point_obj, fill="yellow")
        return self

    def return_to_default(self):
        """
        Returns the object to its default state
        :return:
        """
        if not self.lock:
            self.canvas.itemconfig(self.point_obj, fill="white")
            self.highlighted = False
            self.selected = False


class line:
    """
    Line class
    """
    obj = "line"
    highlighted = False
    selected = False
    def __init__(self, canvas=None, points=None):
        self.points = points
        self.canvas = canvas
        self.line_obj = canvas.create_line(points[0], points[1], points[2], points[3])
        self.end_points = [point(canvas, evt=None, points=points[:2]), point(canvas, evt=None, points=points[2:])]

    def delete_object(self):
        self.canvas.delete(self.line_obj)

    def over(self, evt, lock=False):
        """
        Algorithms to check if mouse is over object, made for every type of object
        :param evt:
        :return:
        """
        points = self.points
        xp = [points[0], points[2]]
        yp = [points[1], points[3]]
        self.end_points[0].over(evt)
        self.end_points[1].over(evt)
        if min(xp) - 5 <= evt.x <= max(xp) + 5 and min(yp) - 5 <= evt.y <= max(yp) + 5:
            check = (points[3] - points[1]) / (points[2] - points[0]) * (evt.x-points[0]) + points[1]
            check2 = (points[2] - points[0]) / (points[3] - points[1]) * (evt.y-points[1]) + points[0]
            if check - 5 <= evt.y <= check + 5 or check2 - 5 <= evt.x <= check2 + 5:
                self.highlighted = True
                self.canvas.itemconfig(self.line_obj, fill="yellow")
            else:
                if not self.selected:
                    self.canvas.itemconfig(self.line_obj, fill="black")
                self.highlighted = False
        else:
            if not self.selected:
                self.canvas.itemconfig(self.line_obj, fill="black")
            self.highlighted = False
        return self.highlighted

    def select_function(self):
        """
        What happens/changes when an object is selected
        :return:
        """
        print("trying to select line")
        self.selected = True
        self.canvas.itemconfig(self.line_obj, fill="yellow")
        return self

    def return_to_default(self):
        """
        Returns the object to its default state
        :return:
        """
        self.canvas.itemconfig(self.line_obj, fill="black")
        self.highlighted = False
        self.selected = False

class circle:
    """
    Circle class
    """
    obj = "circle"
    highlighted = False
    selected = False
    def __init__(self, canvas=None, center=None, evt=None):
        self.canvas = canvas
        radius = ((center[0] - evt.x) ** 2 + (center[1] - evt.y) ** 2) ** 0.5
        self.circle_obj = canvas.create_oval(center[0] - radius, center[1] - radius,
                                             center[0] + radius, center[1] + radius)
        self.radius = radius
        self.center = center
        self.center_point = point(canvas, points=center)

    def delete_object(self):
        self.canvas.delete(self.center_point)
        self.canvas.delete(self.circle_obj)

    def over(self, evt):
        """
        Algorithms to check if mouse is over object, made for every type of object
        :param evt: mouse event
        :return:
        """
        overpoint = False
        overcirc = over_circ_alg(self.radius, self.center, evt)
        if not overcirc:
            overpoint = self.center_point.over(evt)
        if overcirc or overpoint:
            self.highlighted = True
            self.canvas.itemconfig(self.circle_obj, outline="yellow")
            self.center_point.highlighted = True
            self.canvas.itemconfig(self.center_point, fill="red")
        else:
            self.highlighted = False
            if not self.selected:
                self.canvas.itemconfig(self.circle_obj, outline="black")
        return self.highlighted

    def select_function(self):
        """
        What happens/changes when an object is selected
        :return:
        """
        print("trying to select circle")
        self.selected = True
        self.canvas.itemconfig(self.circle_obj, outline="yellow")
        self.center_point.selected = True
        self.canvas.itemconfig(self.center_point, fill="red")
        self.center_point.lock = True
        return self

    def return_to_default(self):
        """
        Returns the object to its default state
        :return:
        """
        self.canvas.itemconfig(self.circle_obj, outline="black")
        self.center_point.return_to_default()
        self.highlighted = False
        self.selected = False

def over_circ_alg(radius, center, evt):
    """
    Checks if mouse is over circle
    :param radius:
    :param center:
    :param evt:
    :return:
    """
    # r^2 = x^2 + y^2
    # rad^2 = (x-evt.x)^2 + (y-evt.y)^2
    rsq = (center[0]-evt.x)**2 + (center[1]-evt.y)**2
    if rsq < (radius+10)**2 and rsq > (radius-10)**2:
        return True
    return False