#!/usr/bin/python

import os, glob, re
import time
import math
from gimpfu import *
import rwkos

import latex_dvi_png
cache_dir = latex_dvi_png.find_cache_dir()

def openemacs(pathin=None):
    if pathin is None:
        filename = 'temp.tex'
        pathin = os.path.join(cache_dir, filename)
    if os.path.exists(pathin):
        if rwkos.amiLinux():
            cmd='emacs '+pathin+' &'
            os.system(cmd)
        else:
            cmd='emacsclientw '+pathin
            subprocess.Popen(cmd)
        print cmd

register("openemacs", \
        "Open Emacs for Gimp Latex", \
        "Open Emacs for Gimp Latex", \
        "Ryan Krauss", \
        "Ryan Krauss", \
        "2009", \
        "<Toolbox>/Xtns/Languages/Ryan/Emacs", \
        "",#RGB*, GRAY*",
        [], \
        [], \
        openemacs)


def copy_png_to_img(png_path, img):
    img2 = pdb.gimp_file_load(png_path, png_path)
    if img2.width > 1950:
        ar = float(img2.height)/float(img2.width)
        new_h = 1950*ar
        pdb.gimp_image_scale(img2, 1950, new_h)
    pdb.gimp_edit_copy_visible(img2)
    #gimp.Display(img2)
    width = img.width
    height = img.height
    print('width = %s' % width)
    print('height = %s' % height)
    trans_layer = gimp.Layer(img, 'Latex', width, height, \
                             RGBA_IMAGE, 100, NORMAL_MODE)
    img.add_layer(trans_layer)
    pdb.gimp_edit_paste(trans_layer, 1)
    mcmd = "xdotool key M"
    time.sleep(0.3)
    os.system(mcmd)
    
def tex_file_to_png(img, drawable):
    png_path = latex_dvi_png.read_from_file_dvi_png()
    copy_png_to_img(png_path, img)

register(
        "tex_file_to_png",
        "Run Latex -> png on tex file",
        "Run Latex -> png on tex file",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Latex -> PNG File",
        "RGB*, GRAY*",
        [],
        [],
        tex_file_to_png)

def load_png_from_preview(img, drawable):
    png_path = latex_dvi_png.find_png_name()
    copy_png_to_img(png_path, img)

register(
        "load_png_from_preview",
        "Load LaTeX PNG file",
        "Load LaTeX PNG file",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Load PNG File",
        "RGB*, GRAY*",
        [],
        [],
        load_png_from_preview)

main()
