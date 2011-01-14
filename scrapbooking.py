#!/usr/bin/python

import os, glob, re
import time
import math
from gimpfu import *
import rwkos
import pdb as Pdb
import txt_mixin
import pygimp_lecture_utils
reload(pygimp_lecture_utils)

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

    white_layer = gimp.Layer(img, "White Layer", width, height, \
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

main()
