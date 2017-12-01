import tkinter as tk
from tkinter import *

class object_handler:
    """
    Handles object behaviour in canvas
    """
    def __init__(self, canvas=None):
        self.objects = []
        self.area = []

    def add_obj(self, object):
        """
        When adding object to frame
        :param object: canvas object
        :return:
        """
        self.objects.append(object)
        self.update_area(object)

    def update_area(self, object):
        """
        Updates the area that highlights when mouse is hovering over object
        :param object: some object on canvas
        :return:
        """
        if object.obj == "circle":
            pass
        elif object.obj == "line":
            pass
        elif object.obj == "point":
            pass