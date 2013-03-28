#!/usr/bin/python

import os
import time
import math
from gimpfu import *

def my_py_eraser(timg, tdrawable):
    print('hello from pygimp')
    pdb.gimp_brushes_set_brush("Circle (17)")
    ecmd = "xdotool key shift+E"
    time.sleep(0.4)
    os.system(ecmd)
    
register(
        "my_py_eraser",
        "Attempt to set the eraser from PyGimp", 
        "Attempt to set the eraser from PyGimp",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Brushes/_Eraser Python",
        "RGB*, GRAY*",
        [],
        [],
        my_py_eraser)


def my_py_pen(timg, tdrawable):
    pdb.gimp_brushes_set_brush("Circle (05)")
    pcmd = "xdotool key P"
    time.sleep(0.4)
    os.system(pcmd)
    
register(
        "my_py_pen",
        "Attempt to set the pen from PyGimp", 
        "Attempt to set the pen from PyGimp",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Brushes/_Pen Python",
        "RGB*, GRAY*",
        [],
        [],
        my_py_pen)


def my_dashed_pen(timg, tdrawable):
    pdb.gimp_brushes_set_brush("Dashed")
    pcmd = "xdotool key P"
    time.sleep(0.4)
    os.system(pcmd)

register(
        "my_dashed_pen",
        "Setting the pen to dashed from PyGimp", 
        "Setting the pen to dashed from PyGimp",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Brushes/_Dashed Python Pen",
        "RGB*, GRAY*",
        [],
        [],
        my_dashed_pen)

main()
