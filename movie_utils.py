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

base = '/home/ryan/ryan_personal/top_secret/'

def open_txt(initialdir=base, initialfile=None):
    filename = tkFileDialog.askopenfilename(initialfile=initialfile,
                                            initialdir=initialdir,
                                            filetypes=txttypes)
    return filename

#720p settings
vwidth = 1280
vheight = 720
var = float(vwidth)/float(vheight)

outpath = '/home/ryan/ryan_personal/top_secret/1280_by_720/Jan'

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


pwidth = 1200
pheight = 1800
var = float(vwidth)/float(vheight)

def adjust_img_size_4_by_6(img, drawable):
    w = img.width
    h = img.height
    x_offset = 0#int((pwidth-w)/2)
    y_offest = 0#int((pheight-h)/2)
    pdb.gimp_image_resize(img, pwidth, pheight, x_offset, y_offest)
    return img

register("adjust_img_size_4_by_6",
         "Add to image size for 4 by 6 printing",
         "Add to image size for 4 by 6 printing",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/Adjust Image Size 4 by 6",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         adjust_img_size_4_by_6)


car = 1
cheight = 1050
cwidth = 1050

def scale_to_cube(img, drawable):
    w = img.width
    h = img.height
    iar = float(w)/float(h)
    if iar  < car:
        #I think this means the height will be the issue
        ratio = float(h)/cheight
        new_h = cheight
        new_w = int(w/ratio)
    else:
        ratio = float(w)/cwidth
        new_w = cwidth
        new_h = int(h/ratio)
    pdb.gimp_image_scale(img, new_w, new_h)
    return img


register("scale_to_cube",
         "Scale image to cube size",
         "Scale image to cube size",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/Scale Image to Cube Size",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         scale_to_cube)


def add_black_layer(img, drawable):
    pdb.gimp_context_set_foreground((0,0,0))
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



def add_white_layer(img, drawable):
    pdb.gimp_context_set_foreground((255,255,255))
    white_layer = gimp.Layer(img, "White Layer", pwidth, pheight, \
                             RGB_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(white_layer, 0)
    img.add_layer(white_layer)
    pdb.gimp_image_lower_layer_to_bottom(img, white_layer)
    pdb.gimp_image_merge_down(img, drawable, 1)
    return img


register("add_white_layer",
         "Add white background layer",
         "Add white background layer",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/Add _White Background Layer",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         add_white_layer)


def save(img, drawable):
    pathin = img.filename
    folder, filename = os.path.split(pathin)
    print('filename = ' + str(filename))
    #Pdb.set_trace()
    root, month = os.path.split(folder)
    #outbase = '/home/ryan/ryan_personal/top_secret/1280_by_720/'
    outbase = '/media/FA_ext3/ryan_personal/top_secret/1280_by_720/'
    outmonth = os.path.join(outbase, month)
    if not os.path.exists(outmonth):
        os.mkdir(outmonth)
    #outdir = os.path.join(outmonth, 'frames')
    #if not os.path.exists(outdir):
    #    os.mkdir(outdir)
    outdir = outmonth
    filepath = os.path.join(outdir, filename)
    print('filepath = ' + str(filepath))
    pdb.gimp_file_save(img, drawable, filepath, filepath)
    pdb.gimp_image_clean_all(img)



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


def scale_add_black_and_save(img, drawable):
    scaled_img = scale_to_video(img, img.layers[0])
    sized_img = adjust_img_size(scaled_img, scaled_img.layers[0])
    blackened_img = add_black_layer(sized_img, sized_img.layers[0])
    save(blackened_img, blackened_img.layers[0])
    return blackened_img


register("scale_add_black_and_save",
         "Scale an img to move size, add black background, and then save",
         "Scale an img to move size, add black background, and then save",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/Scale, Add _Black, and Save",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         scale_add_black_and_save)


    
def process_one_movie_path(pathin):
    folder, filename = os.path.split(pathin)
    scaled_folder = os.path.join(folder, 'scaled')
    mypath = pathin
    if os.path.exists(scaled_folder):
        scaled_path = os.path.join(scaled_folder, filename)
        if os.path.exists(scaled_path):
            mypath = scaled_path
    img = pdb.gimp_file_load(mypath, mypath)
    scaled_img = scale_to_video(img, img.layers[0])
    sized_img = adjust_img_size(scaled_img, scaled_img.layers[0])
    blackened_img = add_black_layer(sized_img, sized_img.layers[0])
    save(blackened_img, blackened_img.layers[0])


def process_many_movie_paths(pathin=None):
    mylist = open_txt_list(pathin)
    for path in mylist:
        process_one_movie_path(path)
    

register("process_many_movie_paths",
         "Process movie frames",
         "Process movie frames",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Ryan/movie/_Process Movie Frames",
         "",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         process_many_movie_paths)


def open_txt_list(pathin=None):
    if pathin is None:
        pathin = open_txt()
    print('pathin = %s' % pathin)
    myfile = txt_mixin.txt_file_with_list(pathin)
    mylist = filter(None, myfile.list)
    mylist = txt_mixin.txt_list(mylist)
    return mylist
    

register("open_txt_list",
         "Open txt list of paths",
         "Open txt list of paths",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Ryan/movie/_Open txt list",
         "",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         open_txt_list)



def open_all_for_editting(pathin=None):
    mylist = open_txt_list(pathin)
    for path in mylist:
        img = pdb.gimp_file_load(path, path)
        gimp.Display(img)


register("open_all_for_editting",
         "Open all imaged in txt list of paths",
         "Open all imaged in txt list of paths",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Ryan/movie/_Open all in txt list",
         "",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         open_all_for_editting)


def set_opacity_and_save_copy(img, drawable, opacity, savepath):
    pdb.gimp_layer_set_opacity(drawable, opacity)
    pygimp_lecture_utils.save_flattened_copy(img, savepath)


def save_copy(img, savepath):
    pygimp_lecture_utils.save_flattened_copy(img, savepath)


def build_title_filename(ind):
    outfolder = '/home/ryan/ryan_personal/top_secret/1280_by_720/intro'
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    pat = 'title_fadein_frame%0.4i.jpg'
    curname = pat % (ind)
    savepath = os.path.join(outfolder, curname)
    return savepath

    
def fade_in_layer(img, drawable):
    startfi = 181
    N = 30
    for i in range(N):
        savepath = build_title_filename(i+startfi)
        opacity = float(i)*100.0/(N-1)
        set_opacity_and_save_copy(img, drawable, opacity, savepath)
        
    return img

register("fade_in_layer",
         "Fade in a layer for annimation",
         "Fade in a layer for annimation",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/_Fade In Layer",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         fade_in_layer)


def fade_out_layer(img, drawable):
    startfi = 271
    N = 30
    for i in range(N):
        savepath = build_title_filename(i+startfi)
        opacity = 100.0-float(i)*100.0/(N-1)
        set_opacity_and_save_copy(img, drawable, opacity, savepath)

    return img


register("fade_out_layer",
         "Fade out a layer for annimation",
         "Fade out a layer for annimation",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/_Fade Out Layer",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         fade_out_layer)


def save_many_copies(img, drawable):
    """Save many copies of an image for movie making"""
    startfi = 211 
    N = 60
    for i in range(N):
        savepath = build_title_filename(i+startfi)
        save_copy(img, savepath)

    return img


register("save_many_copies",
         "Save many copies of an image for movie making",
         "Save many copies of an image for movie making",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Image>/Filters/Ryan/movie/_Save Many Copies",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         save_many_copies)

main()
