#!/usr/bin/python

## How to use my GIMP LaTeX stuff:

## 1. select an area where the text will be pasted
## 2. F8 (Filters/Ryan/Latex/Initialize Latex Paste) brings up the wx window 

##     - this is the top Ryan in the Filters menu

## 3. type in the wx box
## 4. press either alt-\ for normal text or ctrl-\ to first wrap in $ $
## 5. the KeyPressed method of wx frame should pass F7 to GIMP through xdotool, but if not, F7 pastes the png into the selected area

##     - F7 is tied to Filters/Ryan/Latex/paste egn
##     - it may use only the top left corner of the selection rectangle

import os, glob, re
import pdb as Pdb
import time
import math
from gimpfu import *
import rwkos

from gimp_copy_utils import *

from xdotool import windows_with_str_in_title, activate_window, \
     get_active_window_id, save_active_window_id

import latex_dvi_png
cache_dir = latex_dvi_png.find_cache_dir()
offset_name = 'offsets.txt'
offset_path = os.path.join(cache_dir, offset_name)
temp_name = 'Latex TEMP'

#from new_grid_image import _save_and_close

import pygimp_lecture_utils
from pygimp_lecture_utils import folder_from_pickle, \
     save_all_slides, \
     close_all, _save_and_close, \
     my_save_2010, rst_is_blank, \
     rst_to_png_all_three, rst_to_png_one_path, \
     folder_and_pngpath_from_rstpath

     

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


    
## def copy_png_to_img(png_path, img, x_offset=None, y_offset=None, \
##                     autocrop=True):
##     img2 = pdb.gimp_file_load(png_path, png_path)
##     if autocrop:
##         pdb.plug_in_autocrop(img2, img2.layers[0])
##     w = img.width
##     max_w = w-50
##     h = img.height
##     max_h = h-50
##     if x_offset is not None:
##         max_w -= x_offset
##     if y_offset is not None:
##         max_h -= y_offset
##     scale_image(img2, max_w, max_h)
##     #print('max_w=%s' % max_w)
## ##     if (img2.width > max_w) or (img2.height > max_h):
## ##         s1 = img2.width/max_w
## ##         s2 = img2.height/max_h
## ##         ar = float(img2.height)/float(img2.width)
## ##         new_h = max_w*ar
## ##         pdb.gimp_image_scale(img2, max_w, new_h)
##     pdb.gimp_edit_copy_visible(img2)
##     #gimp.Display(img2)
##     width = img.width
##     height = img.height
##     #print('width = %s' % width)
##     #print('height = %s' % height)
##     if top_layer_is_TEMP(img):
##         trans_layer = img.layers[0]
##     else:
##         trans_layer = gimp.Layer(img, 'Latex', width, height, \
##                                  RGBA_IMAGE, 100, NORMAL_MODE)
##         img.add_layer(trans_layer)
##     float_layer = pdb.gimp_edit_paste(trans_layer, 1)
##     if (x_offset is not None) or (y_offset is not None):
##         if x_offset is None:#if either is not None, the other defaults
##                             #to 0
##             x_offset = 0
##         if y_offset is None:
##             y_offset = 0
##         pdb.gimp_layer_set_offsets(float_layer, x_offset, y_offset)
##     else:
##         mcmd = "xdotool key M"
##         time.sleep(0.1)
##         os.system(mcmd)
##     return float_layer


def load_outline_png(folder=None, save=True, close=True):
    if save or close:
        success = _save_and_close(save=save, close=close)
        if not success:
            return    
    myname = 'outline1.png'
    if folder is None:
        folder = folder_from_pickle()
    path1 = os.path.join(folder, myname)
    path2 = os.path.join(folder, 'exclude')
    path2 = os.path.join(path2, myname)
    mypath = None
    if os.path.exists(path1):
        mypath = path1
    else:
        if os.path.exists(path2):
            mypath = path2
    if mypath is not None:
        img = pdb.python_fu_new_grid_image_2010()
        floating_sel = copy_png_to_img(mypath, img, x_offset=25, \
                                       y_offset=25)
        if top_layer_is_TEMP(img, 1) or top_layer_is_Latex(img, 1):
            pdb.gimp_floating_sel_anchor(floating_sel)
    else:
        print('outline1.png not found in curdir or curdir/exlude.')


register(
        "load_outline_png",
        "Load outline into file",
        "Load outline into file",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Load/Load Outline",
        "",#"RGB*, GRAY*",
        [],
        [],
        load_outline_png)


register(
        "rst_to_png_all_three",
        "Call rst_outline_gen.py for OAR",
        "Call rst_outline_gen.py for outline, announcements, and reminders",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Load/RST2PNG OAR (all 3)",
        "",#"RGB*, GRAY*",
        [],
        [],
        rst_to_png_all_three)


import tkFileDialog
pngtypes = [('png files', '*.png')]
pdftypes = [('pdf files', '*.pdf')]
jpgtypes = [('jpg files', '*.jpg')]
rsttypes = [('rst files', '*.rst')]

import tk_simple_dialog

def one_png_to_slide(rstpath):
    folder, pngpath = folder_and_pngpath_from_rstpath(rstpath) 
    if os.path.exists(rstpath):
        if not rst_is_blank(rstpath):
            if os.path.exists(pngpath):
                img = pdb.python_fu_new_grid_image_2010()
                floating_sel = copy_png_to_img(pngpath, img, x_offset=25, \
                                               y_offset=25)
                if top_layer_is_TEMP(img, 1) or top_layer_is_Latex(img, 1):
                    pdb.gimp_floating_sel_anchor(floating_sel)
                my_save_2010(img)


def OAR_pngs_to_slides():
    filenames = ['outline','announcements','reminders']
    folder = folder_from_pickle()
    exclude_dir = os.path.join(folder, 'exclude')
    for filename in filenames:
        rstname = filename + '.rst'
        rstpath = os.path.join(exclude_dir, rstname)
        one_png_to_slide(rstpath)



register(
        "OAR_pngs_to_slides",
        "load OAR pngs onto slides",
        "load OAR pngs onto slides",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Load/make OAR slides (all 3)",
        "",#"RGB*, GRAY*",
        [],
        [],
        OAR_pngs_to_slides)



def rst_to_slide(save=True, close=True):
    if save or close:
        success = _save_and_close(save=save, close=close)
        if not success:
            return    
    rstpath = open_rst()
    print('rstpath = ' + rstpath)
    rst_to_png_one_path(rstpath)
    one_png_to_slide(rstpath)
    

register(
        "rst_to_slide",
        "load one RST file onto a slide",
        "load one RST file onto a slide",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Load/_RST to slide (one)",    
        "",#"RGB*, GRAY*",
        [],
        [],
        rst_to_slide)

    
def open_png(initialdir=None, initialfile=None):
    filename = tkFileDialog.askopenfilename(initialfile=initialfile,
                                            initialdir=initialdir,
                                            filetypes=pngtypes)
    return filename

def open_pdf(initialdir=None, initialfile=None):
    filename = tkFileDialog.askopenfilename(initialfile=initialfile,
                                            initialdir=initialdir,
                                            filetypes=pdftypes)
    return filename

def open_jpg(initialdir=None, initialfile=None):
    filename = tkFileDialog.askopenfilename(initialfile=initialfile,
                                            initialdir=initialdir,
                                            filetypes=jpgtypes)
    return filename


def open_rst(initialdir=None, initialfile=None):
    if initialdir is None:
        initialdir = folder_from_pickle()
        tempdir = os.path.join(initialdir, 'exclude')
        if os.path.exists(tempdir):
            initialdir = tempdir
    filename = tkFileDialog.askopenfilename(initialfile=initialfile,
                                            initialdir=initialdir,
                                            filetypes=rsttypes)
    return filename



def load_any_png(save=True, close=True):
    if save or close:
        success = _save_and_close(save=save, close=close)
        if not success:
            return    
    img = pdb.python_fu_new_grid_image_2010()
    initialdir = folder_from_pickle()
    tempdir = os.path.join(initialdir, 'exclude')
    if os.path.exists(tempdir):
        initialdir = tempdir
    pngpath = open_png(initialdir=initialdir)
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
        "<Toolbox>/Lecture/Load/Load PNG",
        "",#"RGB*, GRAY*",
        [],
        [],
        load_any_png)


def load_any_pdf(save=True, close=True):
    if save or close:
        success = _save_and_close(save=save, close=close)
        if not success:
            return        
    img = pdb.python_fu_new_grid_image_2010()
    initialdir = folder_from_pickle()
    pdfpath = open_pdf(initialdir=initialdir)
    floating_sel = copy_pdf_to_img(pdfpath, img, x_offset=25, \
                                   y_offset=25)
##     if top_layer_is_TEMP(img, 1) or top_layer_is_Latex(img, 1):
##         pdb.gimp_floating_sel_anchor(floating_sel)


register(
        "load_any_pdf",
        "Load any pdf into file",
        "Load pdf from pyp into file",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Load/Load PDF",
        "",#"RGB*, GRAY*",
        [],
        [],
        load_any_pdf)
    

def load_any_jpg(save=True, close=True):
    if save or close:
        success = _save_and_close(save=save, close=close)
        if not success:
            return    
    img = pdb.python_fu_new_grid_image_2010()
    initialdir = folder_from_pickle()
    jpgpath = open_jpg(initialdir=initialdir)
    floating_sel = copy_jpg_to_img(jpgpath, img, x_offset=25, \
                                   y_offset=25)
##     if top_layer_is_TEMP(img, 1) or top_layer_is_Latex(img, 1):
##         pdb.gimp_floating_sel_anchor(floating_sel)


register(
        "load_any_jpg",
        "Load any jpg into file",
        "Load jpg into file",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Load/Load JPG",
        "",#"RGB*, GRAY*",
        [],
        [],
        load_any_jpg)
    

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
