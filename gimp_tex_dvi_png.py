#!/usr/bin/python

import os, glob, re
import pdb as Pdb
import time
import math
from gimpfu import *
import rwkos

from xdotool import windows_with_str_in_title, activate_window, \
     get_active_window_id, save_active_window_id

import latex_dvi_png
cache_dir = latex_dvi_png.find_cache_dir()
offset_name = 'offsets.txt'
offset_path = os.path.join(cache_dir, offset_name)
temp_name = 'Latex TEMP'

def get_upper_left_selection(img, drawable):
    bounds = pdb.gimp_selection_bounds(img)
    ints = [int(item) for item in bounds]
    my_bool, x1, y1, x2, y2 = ints
    #print('bounds=' + str(ints))
    if my_bool:
        save_offsets_to_file(x1, y1)
        return x1, y1
    else:
        save_offsets_to_file(-1, -1)
        return None, None

register(
        "get_upper_left_selection",
        "Get selection bounds",
        "Get selection bounds",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Latex/Get selection bounds.", \
        "RGB*, GRAY*",
        [],
        [],
        get_upper_left_selection)

def initialize_Latex_paste_temp(img, drawable):
    save_active_window_id()
    x, y = get_upper_left_selection(img, drawable)
    if (x is not None) and top_layer_is_TEMP(img):
        pdb.gimp_image_merge_down(img, img.layers[0], 0)
    create_Latex_TEMP_layer(img, drawable)
    launch_wxPython_app()


register(
        "initialize_Latex_paste_temp",
        "Initialize Latex Paste into temp",
        "Initialize Latex Paste into temp",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Latex/Initialize Latex Paste", \
        "RGB*, GRAY*",
        [],
        [],
        initialize_Latex_paste_temp)


def initialize_Latex_paste_temp_w_vert_offset(img, drawable, dy=250):
    save_active_window_id()
    x, y = load_offsets_from_file()
    if x is None or y is None:
        print('failed to load old coordinates')
        return
    y += dy
    save_offsets_to_file(x, y)
    if (x is not None) and top_layer_is_TEMP(img):
        pdb.gimp_image_merge_down(img, img.layers[0], 0)
    create_Latex_TEMP_layer(img, drawable)
    launch_wxPython_app()


register(
        "initialize_Latex_paste_temp_w_vert_offset",
        "Initialize Latex Paste w vert offset",
        "Initialize Latex Paste w vert offset",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Latex/Initialize w vert. offset", \
        "RGB*, GRAY*",
        [],
        [],
        initialize_Latex_paste_temp_w_vert_offset)

    
def save_offsets_to_file(x_offset, y_offset):
    #print('saving %s %s to %s' % (x_offset, y_offset, offset_path))
    f = open(offset_path, 'wb')
    f.write('%s %s\n' % (x_offset, y_offset))
    f.close()

def load_offsets_from_file():
    if os.path.exists(offset_path):
        f = open(offset_path, 'rb')
        mylist = f.readlines()
        f.close()
        row0 = mylist[0]
        x, y = row0.split(' ',1)
        x = x.strip()
        y = y.strip()
        x = int(x)
        y = int(y)
        return x, y
    else:
        return -1, -1

def create_Latex_TEMP_layer(img, drawable):
    width = img.width
    height = img.height
    trans_layer = gimp.Layer(img, temp_name, width, height, \
                             RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(trans_layer, TRANSPARENT_FILL)
    img.add_layer(trans_layer)
    #print('layer[0].name=%s' % img.layers[0].name)

register(
        "create_Latex_TEMP_layer",
        "Create TEMP layer for Latex",
        "Create TEMP layer for Latex",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Latex/Create Latex TEMP layer", \
        "RGB*, GRAY*",
        [],
        [],
        create_Latex_TEMP_layer)

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

def launch_wxPython_app():
    """Launch or activate latex_eqn_preview_wx.py"""
    id_list = windows_with_str_in_title("'Latex Equation Preview'")
    #print('id_list=%s' % id_list)
    if id_list[0]:
        #print('found window and activating')
        activate_window(id_list[0])
    else:
        cmd = 'latex_eqn_preview_wx.py 1'#the 1 is for headless
                                         #operation
        os.system(cmd)
    

register("latex_eqn_preview_wx", \
        "Open My wxPython app for Gimp Latex", \
        "Open My wxPython app for Gimp Latex", \
        "Ryan Krauss", \
        "Ryan Krauss", \
        "2009", \
        "<Toolbox>/Xtns/Languages/Ryan/wxPython Latex Preview", \
        "",#RGB*, GRAY*",
        [], \
        [], \
        launch_wxPython_app)

def top_layer_is_TEMP(img, ind=0):
    return bool(img.layers[ind].name.find(temp_name) == 0)

def top_layer_is_Latex(img, ind=0, name='Latex'):
    return bool(img.layers[ind].name.find(name) == 0)

def copy_png_to_img(png_path, img, x_offset=None, y_offset=None):
    img2 = pdb.gimp_file_load(png_path, png_path)
    w = img.width
    max_w = w-50
    if x_offset is not None:
        max_w -= x_offset
    #print('max_w=%s' % max_w)
    if img2.width > max_w:
        ar = float(img2.height)/float(img2.width)
        new_h = max_w*ar
        pdb.gimp_image_scale(img2, max_w, new_h)
    pdb.gimp_edit_copy_visible(img2)
    #gimp.Display(img2)
    width = img.width
    height = img.height
    #print('width = %s' % width)
    #print('height = %s' % height)
    if top_layer_is_TEMP(img):
        trans_layer = img.layers[0]
    else:
        trans_layer = gimp.Layer(img, 'Latex', width, height, \
                                 RGBA_IMAGE, 100, NORMAL_MODE)
        img.add_layer(trans_layer)
    float_layer = pdb.gimp_edit_paste(trans_layer, 1)
    if (x_offset is not None) or (y_offset is not None):
        if x_offset is None:#if either is not None, the other defaults
                            #to 0
            x_offset = 0
        if y_offset is None:
            y_offset = 0
        pdb.gimp_layer_set_offsets(float_layer, x_offset, y_offset)
    else:
        mcmd = "xdotool key M"
        time.sleep(0.1)
        os.system(mcmd)
    return float_layer


def load_outline_png():
    img = pdb.python_fu_new_grid_image()
    floating_sel = copy_png_to_img('outline1.png', img, x_offset=25, \
                                   y_offset=25)
    if top_layer_is_TEMP(img, 1) or top_layer_is_Latex(img, 1):
        pdb.gimp_floating_sel_anchor(floating_sel)


register(
        "load_outline_png",
        "Load outline into file",
        "Load outline into file",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Xtns/Languages/Ryan/Latex/Load Outline",
        "",#"RGB*, GRAY*",
        [],
        [],
        load_outline_png)

import tkFileDialog
pngtypes = [('png files', '*.png')]
import tk_simple_dialog

def open_png(initialdir=None, initialfile=None):
    filename = tkFileDialog.askopenfilename(initialfile=initialfile,
                                            initialdir=initialdir,
                                            filetypes=pngtypes)
    return filename

def load_any_png():
    img = pdb.python_fu_new_grid_image()
    pngpath = open_png()
    floating_sel = copy_png_to_img(pngpath, img, x_offset=25, \
                                   y_offset=25)
    if top_layer_is_TEMP(img, 1) or top_layer_is_Latex(img, 1):
        pdb.gimp_floating_sel_anchor(floating_sel)


register(
        "load_any_png",
        "Load any png into file",
        "Load png from pyp into file",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Xtns/Languages/Ryan/Latex/Load PNG",
        "",#"RGB*, GRAY*",
        [],
        [],
        load_any_png)
    

def paste_eqn_with_offests_and_clear(img, drawable):
    #t1 = time.time()
    x, y = load_offsets_from_file()
    if x == -1:
        x = None
    if y == -1:
        y = None
    #t2 = time.time()
    if top_layer_is_TEMP(img):
        pdb.gimp_edit_clear(img.layers[0])
    #t3 = time.time()
    png_path = latex_dvi_png.find_png_name()
    #t4 = time.time()
    pdb.gimp_selection_clear(img)
    #t5 = time.time()
    floating_sel = copy_png_to_img(png_path, img, x_offset=x, y_offset=y)
    #t6 = time.time()
    if top_layer_is_TEMP(img, 1) and (x is not None) and (y is not None):
        pdb.gimp_floating_sel_anchor(floating_sel)
    #t7 = time.time()
##     for i in range(1, 7):
##         cur_diff = 't%s-t%s' % (i+1, i)
##         exec('cur_t = '+cur_diff)
##         print(cur_diff + '=%s' % cur_t)
    #print('In GIMP, t7-t1=%s' %(t7-t1))

register(
        "paste_eqn_with_offests_and_clear",
        "Paste Eqn into file",
        "Paste Eqn into file",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/Latex/paste eqn",
        "RGB*, GRAY*",
        [],
        [],
        paste_eqn_with_offests_and_clear)

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
        "<Image>/Filters/Ryan/Latex/Latex -> PNG File",
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
        "<Image>/Filters/Ryan/Latex/Load PNG File",
        "RGB*, GRAY*",
        [],
        [],
        load_png_from_preview)

main()
