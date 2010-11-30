#!/usr/bin/python

import os, glob, re
import time
import math
from gimpfu import *
import rwkos
import pdb as Pdb

Linux = rwkos.amiLinux()


#720p settings
vwidth = 1280
vheight = 720
var = float(vwidth)/float(vheight)

outpath = '/home/ryan/ryan_personal/top_secret/1280_by_720/'

def adjust_img_size(img, drawable):
    w = img.width
    h = img.height
    x_offset = int((vwidth-w)/2)
    y_offest = int((vheight-h)/2)
    pdb.gimp_image_resize(img, vwidth, vheight, x_offset, y_offest)
    return img


register("adjust_img_size",
         "Add to image size for vertical pictures",
         "Add to image size for vertical pictures",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/_Adjust Image Size",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         adjust_img_size)


def scale_to_video(img, drawable):
    w = img.width
    h = img.height
    iar = float(w)/float(h)
    if iar  < var:
        #I think this means the height will be the issue
        ratio = float(h)/vheight
        new_h = vheight
        new_w = int(w/ratio)
    else:
        ratio = float(w)/vwidth
        new_w = vwidth
        new_h = int(h/ratio)
    pdb.gimp_image_scale(img, new_w, new_h)
    return img


register("scale_to_video",
         "Scale image to video size",
         "Scale image to video size",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/_Scale Image to Video Size",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         scale_to_video)


def add_black_layer(img, drawable):
    black_layer = gimp.Layer(img, "Black Layer", vwidth, vheight, \
                             RGB_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(black_layer, 0)
    img.add_layer(black_layer)
    pdb.gimp_image_lower_layer_to_bottom(img, black_layer)
    pdb.gimp_image_merge_down(img, drawable, 1)
    return img


register("add_black_layer",
         "Add black background layer",
         "Add black background layer",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/_Add Black Background Layer",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         add_black_layer)


def save(img, drawable):
    pathin = img.filename
    folder, filename = os.path.split(pathin)
    print('filename = ' + str(filename))
    filepath = os.path.join(outpath, filename)
    print('filepath = ' + str(filepath))
    pdb.gimp_file_save(img, drawable, filepath, filepath)


register("save",
         "Save movie frame",
         "Save movie frame",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/_Save Movie Image as Frame",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         save)

main()
