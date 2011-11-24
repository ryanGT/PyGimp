#!/usr/bin/python

import os, glob, re
import time
import math
from gimpfu import *
import rwkos
import pdb as Pdb
import txt_mixin
#import pygimp_lecture_utils
#reload(pygimp_lecture_utils)

Linux = rwkos.amiLinux()


import tkFileDialog
txttypes = [('txt files', '*.txt'), ('all files', '.*')]

import tk_simple_dialog
import tk_msg_dialog

dpi = 300
width = 4*dpi
height = 6*dpi

def scale_to_300_dpi(img, drawable):
    w = img.width
    h = img.height
    dialog = tk_simple_dialog.width_and_dpi_dialog()
    if dialog.result is not None:
        des_width_in, dpi = dialog.result
        des_width_px = float(des_width_in)*dpi
        des_height_px = des_width_px*float(h)/float(w)
        des_height_in = float(des_height_px)/float(dpi)
        new_w = int(des_width_px)
        new_h = int(des_height_px)
        pdb.gimp_image_scale(img, new_w, new_h)

        pathin = img.filename
        folder, filename = os.path.split(pathin)
        fno, ext = os.path.splitext(filename)
        name_out = fno + '_cropped_%0.2f_by_%0.2f' % \
                   (des_width_in, des_height_in)
        name_out = name_out.replace('.','_')
        name_out += '.jpg'
        cropped_folder = os.path.join(folder, 'cropped')
        if not os.path.exists(cropped_folder):
            os.mkdir(cropped_folder)
        cropped_path = os.path.join(cropped_folder, name_out)
        print('cropped_path = ' + str(cropped_path))
        pdb.gimp_file_save(img, drawable, cropped_path, cropped_path)
        pdb.gimp_selection_all(img)
        pdb.gimp_edit_copy_visible(img)
        pdb.gimp_image_clean_all(img)

        return img


register("scale_to_300_dpi",
         "Scale image to 300 dpi size",
         "Scale image to 300 dpi size",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/scrapbooking/Scale Image to 300 dpi Size",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         scale_to_300_dpi)


def new_4_by_6(landscape=False):
    if landscape:
        mywidth = height
        myheight = width
    else:
        mywidth = width
        myheight = height
        
    img = gimp.Image(mywidth, myheight, RGB)

    white_layer = gimp.Layer(img, "White Layer", mywidth, myheight, \
                             RGB_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(white_layer, WHITE_FILL)
    img.add_layer(white_layer)

    out1 = gimp.Display(img)
    gimp.displays_flush()
    pdb.gimp_image_clean_all(img)
    ## title_in = img.filename
    ## log_msg('title_in=%s' % title_in)
    return img


register("new_4_by_6",
         "A new image for scrapbooking",
         "A new image for scrapbooking",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Ryan/scrapbooking/New _4 by 6",
         "",#RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         new_4_by_6)


def new_6_by_4():
    img = new_4_by_6(landscape=True)
    return img


register("new_6_by_4",
         "A new image for scrapbooking",
         "A new image for scrapbooking",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Ryan/scrapbooking/New _6 by 4",
         "",#RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         new_6_by_4)


def _my_select(img, x, y, width, height, dpi=300.0, convert=True):
    feather = 0
    feather_radius = 0
    Replace = 2
    if convert:
        scale = dpi
    else:
        scale = 1.0

    x_px = x*scale
    y_px = y*scale
    width_px = width*scale
    height_px = height*scale
    
    pdb.gimp_rect_select(img, x_px, y_px, width_px, height_px, \
                         Replace, feather, feather_radius)
    

def _my_fg_bucket_fill(drawable):
    pdb.gimp_bucket_fill(drawable, 0, 0, 100, 0, 0, 0, 0)
    

def new_design_2_photos_first_layout(img, drawable):
    gap = 0.2
    
    #img 0 25 100 50 REPLACE 0 0
    x1 = 3.9
    y1 = 1.0
    w1 = 3.0
    h1 = 3.0
    b1 = y1 + h1
    _my_select(img, x1, y1, w1, h1)
    _my_fg_bucket_fill(drawable)

    w2 = 2.0
    h2 = 2.75
    x2 = x1
    y2 = y1 + h1 + gap
    _my_select(img, x2, y2, w2, h2)
    _my_fg_bucket_fill(drawable)

    h3 = 4.0
    w3 = 3.0
    x3 = x2
    y3 = y2 + h2 + gap
    _my_select(img, x3, y3, w3, h3)
    _my_fg_bucket_fill(drawable)

    h4 = h2
    w4 = 5.25
    y4 = y2
    x4 = x2 + w2 + gap
    _my_select(img, x4, y4, w4, h4)
    _my_fg_bucket_fill(drawable)

    h5 = 2.0
    w5 = 3.0
    y5 = b1 - h5
    x5 = x1 + w1 + gap
    _my_select(img, x5, y5, w5, h5)
    _my_fg_bucket_fill(drawable)

    h6 = 2.0
    w6 = 2.75
    y6 = 2.9
    r6 = x1 - gap
    x6 = r6 - w6
    _my_select(img, x6, y6, w6, h6)
    _my_fg_bucket_fill(drawable)
    
    h7 = 3.0
    w7 = 3.0
    r7 = r6
    x7 = r7 - w7
    y7 = y6 + h6 + gap
    _my_select(img, x7, y7, w7, h7)
    _my_fg_bucket_fill(drawable)
    
    
    #drawable, fill mode (fg), paint mode (normal), opacity,
    #threshold, sample-merged, x, y - Note that x and y are only used
    #if there is not selection
    
    print('yeah, I filled it')
    return img
    
    
register("new_design_2_photos_first_layout",
         "Create digital scrapbooking layout #2",
         "Create digital scrapbooking layout #2",
         "Ryan Krauss",
         "Ryan Krauss",
         "2011",
         "<Image>/Filters/Ryan/scrapbooking/Digital/Create New Layout #2",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         new_design_2_photos_first_layout)

    
main()
