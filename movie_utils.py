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

#base = '/home/ryan/ryan_personal/top_secret/'
#outbase = '/mnt/personal/pictures/moms_movie_60th_bday/1280_by_720'
#base = '/home/ryan/ryan_personal/top_secret/Christmas_2012'
#outbase = os.path.join(base, '1280_by_720')
base = '/home/ryan/ryan_personal/'
outbase = base

if not os.path.exists(outbase):
    os.mkdir(outbase)
    

def open_txt(initialdir=base, initialfile=None):
    filename = tkFileDialog.askopenfilename(initialfile=initialfile,
                                            initialdir=initialdir,
                                            filetypes=txttypes)
    return filename

#ipad Mini settings (sort of 720p) - actual screensize is 1280 by 768
vwidth = 1280
vheight = 720
var = float(vwidth)/float(vheight)

#outpath = '/home/ryan/ryan_personal/top_secret/1280_by_720/Jan'

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
    root, dir = os.path.split(folder)
    #outbase = '/home/ryan/ryan_personal/top_secret/1280_by_720/'
    #outbase = '/media/FA_ext3/ryan_personal/top_secret/1280_by_720/'
    outbase = '/home/ryan/ryan_personal/top_secret/Christmas_2012/1280_by_720'
    
    outdir = os.path.join(outbase, dir)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    #outdir = os.path.join(outdir, 'frames')
    #if not os.path.exists(outdir):
    #    os.mkdir(outdir)
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


def process_all_paths_in_folder():
    myfolder = tkFileDialog.askdirectory(initialfile=None, \
                                         initialdir=base)
    print("myfolder = " + str(myfolder))
    pat = os.path.join(myfolder, "*.jpg")
    pat2 = os.path.join(myfolder, "*.JPG")
    files1 = glob.glob(pat)
    files2 = glob.glob(pat2)
    filt2 = [item for item in files2 if item not in files1]
    mypaths = files1 + filt2
    print('mypaths = ' + str(mypaths))
    mypaths.sort()
    for path in mypaths:
        process_one_movie_path(path)


register("process_all_paths_in_folder",
         "Process movie frames glob",
         "Process movie frames glob",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Ryan/movie/Process Movie Frames _Glob",
         "",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         process_all_paths_in_folder)


def proces_one_folder(pathin):
    print("pathin = " + str(pathin))
    pat = os.path.join(pathin, "*.jpg")
    pat2 = os.path.join(pathin, "*.JPG")
    files1 = glob.glob(pat)
    files2 = glob.glob(pat2)
    filt2 = [item for item in files2 if item not in files1]
    mypaths = files1 + filt2
    print('mypaths = ' + str(mypaths))
    mypaths.sort()
    for path in mypaths:
        process_one_movie_path(path)

    
def process_all_2012_paths():
    root = '/home/ryan/ryan_personal/top_secret/Christmas_2012/unsorted/2012/'
    folders = ['Apr_2012', \
               'Aug_2012', \
               'Feb_2012', \
               'Jan_2012', \
               'July_2012', \
               'June_2012', \
               'Mar_2012', \
               'May_2012', \
               'Nov_2012', \
               'Oct_2012', \
               'Sept_2012',\
               ]

    for folder in folders:
        curpath = os.path.join(root, folder)
        proces_one_folder(curpath)
        

register("process_all_2012_paths",
         "Process all 2012 paths",
         "Process all 2012 paths",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Ryan/movie/Process All 2012 Path",
         "",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         process_all_2012_paths)

## register("new_grid_image_2010",
##          "A new image for class lectures",
##          "A new image for class lectures",
##          "Ryan Krauss",
##          "Ryan Krauss",
##          "2010",
##          "<Toolbox>/Lecture/_New Grid Image",
##          "",#RGB*, GRAY*",
##          [],
##          [(PF_IMAGE, 'img', 'the new image')],
##          new_grid_image_2010)


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


def find_highest_existing_title_filename():
    outfolder = '/home/ryan/ryan_personal/top_secret/Christmas_2012/1280_by_720/intro/part2/'
    import glob
    pat = 'title_fadein_frame*.jpg'
    full_pat = os.path.join(outfolder, pat)
    all_frames = glob.glob(full_pat)
    all_frames.sort()
    if len(all_frames) == 0:
        return 0
    last_frame = all_frames[-1]
    pne, ext = os.path.splitext(last_frame)
    digit_str = pne[-4:]
    return int(digit_str)

def get_startfi():
    N = find_highest_existing_title_filename()
    return N+1

    
def build_title_filename(ind):
    outfolder = '/home/ryan/ryan_personal/top_secret/Christmas_2012/1280_by_720/intro/part2/'
    
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    pat = 'title_fadein_frame%0.4i.jpg'
    curname = pat % (ind)
    savepath = os.path.join(outfolder, curname)
    return savepath

    
def fade_in_layer(img, drawable):
    startfi = get_startfi()
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
    startfi = get_startfi()
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
    startfi = get_startfi()
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


def save_all_xcf_to_jpg():
    myfolder = tkFileDialog.askdirectory(initialfile=None, \
                                         initialdir=base)
    print("myfolder = " + str(myfolder))
    pat = os.path.join(myfolder, "*.xcf")
    pat2 = os.path.join(myfolder, "*.XCF")
    files1 = glob.glob(pat)
    files2 = glob.glob(pat2)
    filt2 = [item for item in files2 if item not in files1]
    mypaths = files1 + filt2
    print('mypaths = ' + str(mypaths))
    mypaths.sort()
    for path in mypaths:
        pne, ext = os.path.splitext(path)
        jpg_path = pne + '.jpg'
        img = pdb.gimp_file_load(path, path)
        pygimp_lecture_utils.save_flattened_copy(img, jpg_path)

    return img


register("save_all_xcf_to_jpg",
         "Save all xcf files in the chosen directory to jpg",
         "Save all xcf files in the chosen directory to jpg",
         "Ryan Krauss",
         "Ryan Krauss",
         "2011",
         "<Toolbox>/Ryan/movie/_XCF to jpg",
         "",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         save_all_xcf_to_jpg)


main()
