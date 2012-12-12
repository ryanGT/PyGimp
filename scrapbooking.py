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


def open_and_scale_img(filename, w, h):
    img = pdb.gimp_file_load(filename, filename)
    CUBIC = 2
    #pdb.gimp_image_scale_full(img, w, h, CUBIC)
    pdb.gimp_image_scale(img, w, h)
    return img


def Christmas_card_2011_layout(img, drawable):
    total_w = 300.0*8
    total_h = 300.0*4
    
    #gap = 0.025*300
    gap = 0
    
    #margin = 0.25*300
    top_margin = 215#0.5*300
    
    w = 740
    h = w

    margin = int((total_w - 3*w - 2*gap)/2)

    #create new layer
    new_layer = gimp.Layer(img, "New Image Layer", total_w, total_h, \
                           RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(new_layer, TRANSPARENT_FILL)
    img.add_layer(new_layer)

    #image #1
    x1 = margin
    y1 = top_margin
    _my_select(img, x1, y1, w, h, convert=False)
    #_my_fg_bucket_fill(drawable)

    path1 = '/home/ryan/Desktop/christmas_card_2011/DSC_0840.JPG'
    img1 = open_and_scale_img(path1, w, h)
    pdb.gimp_edit_copy_visible(img1)
    float_layer = pdb.gimp_edit_paste(new_layer, 1)
    pdb.gimp_floating_sel_anchor(float_layer)


    x2 = margin + w + gap
    y2 = y1
    _my_select(img, x2, y2, w, h, convert=False)
    #_my_fg_bucket_fill(drawable)

    path2 = '/home/ryan/Desktop/christmas_card_2011/portrait_3_krausses.jpg'
    img2 = open_and_scale_img(path2, w, h)
    pdb.gimp_edit_copy_visible(img2)
    float_layer = pdb.gimp_edit_paste(new_layer, 1)
    pdb.gimp_floating_sel_anchor(float_layer)


    x3 = margin + w*2 + gap*2
    y3 = y1
    _my_select(img, x3, y3, w, h, convert=False)
    #_my_fg_bucket_fill(drawable)

    path3 = '/home/ryan/Desktop/christmas_card_2011/joshua_hole_DSC_0247_w_775.jpg'
    img3 = open_and_scale_img(path3, w, h)
    pdb.gimp_edit_copy_visible(img3)
    float_layer = pdb.gimp_edit_paste(new_layer, 1)
    pdb.gimp_floating_sel_anchor(float_layer)

    pdb.gimp_selection_none(img)

    print('done')
    return img


register("Christmas_card_2011_layout",
         "Create Christmas card layout",
         "Create Christmas card layout",
         "Ryan Krauss",
         "Ryan Krauss",
         "2011",
         "<Image>/Filters/Ryan/scrapbooking/Christmas card layout 2011", 
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         Christmas_card_2011_layout)



def scale_and_paste_img_onto_selected_area(path, w, h, dest_layer, \
                                           dpi=300, scale=True):
    """open the image located at path, scale it to w by h and paste in
    into dest_layer"""
    if scale:
        w = w*dpi
        h = h*dpi
    img1 = open_and_scale_img(path, w, h)
    pdb.gimp_edit_copy_visible(img1)
    float_layer = pdb.gimp_edit_paste(dest_layer, 1)
    pdb.gimp_floating_sel_anchor(float_layer)
    return float_layer

    
def missy_christmas_gift_1_add_pics(img, drawable):
    gap = 0.2

    Christmas_dir = '/home/ryan/ryan_personal/top_secret/Christmas_2011/'

    #create new layer
    total_w = 3600
    total_h = total_w
    new_layer = gimp.Layer(img, "New Image Layer", total_w, total_h, \
                           RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(new_layer, TRANSPARENT_FILL)
    img.add_layer(new_layer)

    #img 0 25 100 50 REPLACE 0 0
    x1 = 3.5
    y1 = 0.75
    w1 = 3.0
    h1 = 3.0
    b1 = y1 + h1
    _my_select(img, x1, y1, w1, h1)
    name1 = 'christmas_card_shot_0001_re_cropped_scaled.jpg'
    path1 = os.path.join(Christmas_dir, name1)
    scale_and_paste_img_onto_selected_area(path1, w1, h1, new_layer)
    #_my_fg_bucket_fill(drawable)

    w2 = 2.0
    h2 = 3.0
    x2 = x1
    y2 = y1 + h1 + gap
    _my_select(img, x2, y2, w2, h2)
    name2 = 'DSC_8992_joshua_dragging_backpack_bw_scaled.jpg'
    path2 = os.path.join(Christmas_dir, name2)
    scale_and_paste_img_onto_selected_area(path2, w2, h2, new_layer)
    ## _my_fg_bucket_fill(drawable)

    h3 = 4.0
    w3 = 3.0
    x3 = x2
    y3 = y2 + h2 + gap
    _my_select(img, x3, y3, w3, h3)
    name3 = 'DSC_8903_cropped_missy_and_joshua_first_day_of_school_bw_cropped.jpg'
    path3 = os.path.join(Christmas_dir, name3)
    scale_and_paste_img_onto_selected_area(path3, w3, h3, new_layer)
    
    ## _my_fg_bucket_fill(drawable)

    h4 = h2
    w4 = 5.25
    y4 = y2
    x4 = x2 + w2 + gap
    _my_select(img, x4, y4, w4, h4)
    name4 = 'DSC_8991_Joshua_looking_up_w_backpack_5_25_by_3_0_bw_scaled.jpg'
    path4 = os.path.join(Christmas_dir, name4)
    scale_and_paste_img_onto_selected_area(path4, w4, h4, new_layer)
    ## _my_fg_bucket_fill(drawable)

    h5 = 2.0
    w5 = 3.0
    y5 = b1 - h5
    x5 = x1 + w1 + gap
    _my_select(img, x5, y5, w5, h5)
    name5 = 'DSC_0247_cropped_4_by_6_bw_Joshua_hole.jpg'
    path5 = os.path.join(Christmas_dir, name5)
    scale_and_paste_img_onto_selected_area(path5, w5, h5, new_layer)
    
    ## _my_fg_bucket_fill(drawable)

    h6 = 2.0
    w6 = 2.75
    y6 = 2.9
    r6 = x1 - gap
    x6 = r6 - w6
    _my_select(img, x6, y6, w6, h6)
    name6 = 'portfolio_bw_cropped.jpg'
    path6 = os.path.join(Christmas_dir, name6)
    scale_and_paste_img_onto_selected_area(path6, w6, h6, new_layer)
    
    ## _my_fg_bucket_fill(drawable)

    h7 = 3.0
    w7 = 3.0
    r7 = r6
    x7 = r7 - w7
    y7 = y6 + h6 + gap
    _my_select(img, x7, y7, w7, h7)
    name7 = 'daisy_square.JPG'
    path7 = os.path.join(Christmas_dir, name7)
    scale_and_paste_img_onto_selected_area(path7, w7, h7, new_layer)

    ## _my_fg_bucket_fill(drawable)


    ## #drawable, fill mode (fg), paint mode (normal), opacity,
    ## #threshold, sample-merged, x, y - Note that x and y are only used
    ## #if there is not selection

    ## print('yeah, I filled it')
    return img


register("missy_christmas_gift_1_add_pics",
         "Missy Christmas gift 1 add pics",
         "Missy Christmas gift 1 add pics",
         "Ryan Krauss",
         "Ryan Krauss",
         "2011",
         "<Image>/Filters/Ryan/scrapbooking/Digital/Missy Christmas Gift 1 Add Pics",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         missy_christmas_gift_1_add_pics)


def summer_vacation_2011_add_pics(img, drawable):
    gap = 0.2

    summer_vaca_dir = '/home/ryan/ryan_personal/top_secret/Christmas_2011/summer_vacation/'

    #create new layer
    total_w = 3600
    total_h = total_w
    new_layer = gimp.Layer(img, "New Image Layer", total_w, total_h, \
                           RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(new_layer, TRANSPARENT_FILL)
    img.add_layer(new_layer)

    top_margin = (12.0 - (4.0+3.0+3.0+2*gap))/2.0
    left_margin = (12.0 - (4.0+2.0+3.0+2*gap))/2.0

    x_vert_1 = left_margin + 4.0 + 2.0 + gap#right vertical edge for
                                            #top 3x4 and center 2x3
                                            
    
    #img 0 25 100 50 REPLACE 0 0
    w1 = 3.0
    h1 = 4.0
    x1 = x_vert_1 - w1
    y1 = top_margin
    b1 = y1 + h1
    _my_select(img, x1, y1, w1, h1)
    name1 = 'joshie_bench.jpg'
    path1 = os.path.join(summer_vaca_dir, name1)
    scale_and_paste_img_onto_selected_area(path1, w1, h1, new_layer)
    #_my_fg_bucket_fill(drawable)


    h3 = 3.0
    w3 = 4.0
    x3 = left_margin
    y3 = y1 + h1 + gap
    _my_select(img, x3, y3, w3, h3)
    name3 = 'excavator_3_krausses.jpg'
    path3 = os.path.join(summer_vaca_dir, name3)
    scale_and_paste_img_onto_selected_area(path3, w3, h3, new_layer)

    ## ## _my_fg_bucket_fill(drawable)

    h4 = 3.0
    w4 = 2.0
    y4 = y3
    x4 = x3 + w3 + gap
    _my_select(img, x4, y4, w4, h4)
    name4 = 'grafton_3_krausses.jpg'
    path4 = os.path.join(summer_vaca_dir, name4)
    scale_and_paste_img_onto_selected_area(path4, w4, h4, new_layer)
    ## _my_fg_bucket_fill(drawable)

    h5 = 4.0
    w5 = 3.0
    y5 = y4 - 1.0
    x5 = x4 + w4 + gap
    _my_select(img, x5, y5, w5, h5)
    name5 = 'joshua_tractor_tire.jpg'
    path5 = os.path.join(summer_vaca_dir, name5)
    scale_and_paste_img_onto_selected_area(path5, w5, h5, new_layer)

    ## ## _my_fg_bucket_fill(drawable)

    w2 = 2.0
    h2 = 2.0
    x2 = x5
    y2 = y5 - h2 - gap
    _my_select(img, x2, y2, w2, h2)
    name2 = 'kissing.jpg'
    path2 = os.path.join(summer_vaca_dir, name2)
    scale_and_paste_img_onto_selected_area(path2, w2, h2, new_layer)
    ## _my_fg_bucket_fill(drawable)

    h7 = 3.0
    w7 = 6.0*3.0/4.0
    x7 = x_vert_1 - w7
    y7 = y3 + h3 + gap
    _my_select(img, x7, y7, w7, h7)
    name7 = 'grafton_0004.jpg'
    path7 = os.path.join(summer_vaca_dir, name7)
    scale_and_paste_img_onto_selected_area(path7, w7, h7, new_layer)

    ## _my_fg_bucket_fill(drawable)

    h6 = 2.0
    w6 = 2.0
    y6 = y7
    x6 = x7 - gap - w6
    _my_select(img, x6, y6, w6, h6)
    name6 = 'little_joshie_big_tractor.jpg'
    path6 = os.path.join(summer_vaca_dir, name6)
    scale_and_paste_img_onto_selected_area(path6, w6, h6, new_layer)

    ## ## _my_fg_bucket_fill(drawable)


    ## #drawable, fill mode (fg), paint mode (normal), opacity,
    ## #threshold, sample-merged, x, y - Note that x and y are only used
    ## #if there is not selection

    ## print('yeah, I filled it')
    return img


register("summer_vacation_2011_add_pics",
         "Summer Vacation 2011 add pics",
         "Summer Vacation 2011 add pics",
         "Ryan Krauss",
         "Ryan Krauss",
         "2011",
         "<Image>/Filters/Ryan/scrapbooking/Digital/Summer Vacation 2011 Add Pics",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         summer_vacation_2011_add_pics)


def dawn_christmas_2011(img, drawable):
    gap = 0.2

    summer_vaca_dir = '/home/ryan/ryan_personal/top_secret/Christmas_2011/Dawn/'

    #create new layer
    total_w = 3600
    total_h = total_w
    new_layer = gimp.Layer(img, "New Image Layer", total_w, total_h, \
                           RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(new_layer, TRANSPARENT_FILL)
    img.add_layer(new_layer)

    top_margin = (12.0 - (4.0+3.0+3.0+2*gap))/2.0
    left_margin = (12.0 - (4.0+2.0+3.0+2*gap))/2.0

    x_vert_1 = left_margin + 4.0 + 2.0 + gap#right vertical edge for
        #top 3x4 and center 2x3


    #img 0 25 100 50 REPLACE 0 0
    w1 = 3.0
    h1 = 4.0
    x1 = x_vert_1 - w1
    y1 = top_margin
    b1 = y1 + h1
    _my_select(img, x1, y1, w1, h1)
    #name1 = 'Jan_2009_dsc_8712_3_by_4.jpg'
    name1 = 'Jan_2009_dsc_8715_3_by_4.jpg'
    path1 = os.path.join(summer_vaca_dir, name1)
    scale_and_paste_img_onto_selected_area(path1, w1, h1, new_layer)
    #_my_fg_bucket_fill(drawable)


    h3 = 3.0
    w3 = 4.0
    x3 = left_margin
    y3 = y1 + h1 + gap
    _my_select(img, x3, y3, w3, h3)
    name3 = 'at_picture_park_dsc_1947_4_by_3.jpg'
    path3 = os.path.join(summer_vaca_dir, name3)
    scale_and_paste_img_onto_selected_area(path3, w3, h3, new_layer)

    ## ## _my_fg_bucket_fill(drawable)

    h4 = 3.0
    w4 = 2.0
    y4 = y3
    x4 = x3 + w3 + gap
    _my_select(img, x4, y4, w4, h4)
    name4 = 'sitting_w_Gramma_at_Grant_St_July_2010_csc_9487_2_by_3.jpg'
    path4 = os.path.join(summer_vaca_dir, name4)
    scale_and_paste_img_onto_selected_area(path4, w4, h4, new_layer)
    ## _my_fg_bucket_fill(drawable)

    h5 = 4.0
    w5 = 3.0
    y5 = y4 - 1.0
    x5 = x4 + w4 + gap
    _my_select(img, x5, y5, w5, h5)
    name5 = 'Christmas_2008_DSC_6854_3_by_4.JPG'
    path5 = os.path.join(summer_vaca_dir, name5)
    scale_and_paste_img_onto_selected_area(path5, w5, h5, new_layer)

    ## ## _my_fg_bucket_fill(drawable)

    w2 = 2.75
    h2 = 2.75
    x2 = x5
    y2 = y5 - h2 - gap
    _my_select(img, x2, y2, w2, h2)
    name2 = 'reading_Jan_2010_dsc_1586_square.jpg'
    path2 = os.path.join(summer_vaca_dir, name2)
    scale_and_paste_img_onto_selected_area(path2, w2, h2, new_layer)
    ## _my_fg_bucket_fill(drawable)

    h7 = 3.0
    w7 = 4.0
    x7 = x_vert_1 - w7 + 1.125
    y7 = y3 + h3 + gap
    _my_select(img, x7, y7, w7, h7)
    name7 = 'Joshua_meets_Gramma_and_Grampa_Krauss_img_0840_4_by_3.jpg'
    path7 = os.path.join(summer_vaca_dir, name7)
    scale_and_paste_img_onto_selected_area(path7, w7, h7, new_layer)

    ## _my_fg_bucket_fill(drawable)

    h6 = 2.75
    w6 = 2.75
    y6 = y7
    x6 = x7 - gap - w6
    _my_select(img, x6, y6, w6, h6)
    name6 = 'Jan_2009_w_Grampa_on_couch_dsc_8741_square.jpg'
    path6 = os.path.join(summer_vaca_dir, name6)
    scale_and_paste_img_onto_selected_area(path6, w6, h6, new_layer)

    ## ## _my_fg_bucket_fill(drawable)


    ## #drawable, fill mode (fg), paint mode (normal), opacity,
    ## #threshold, sample-merged, x, y - Note that x and y are only used
    ## #if there is not selection

    ## print('yeah, I filled it')
    return img


register("dawn_christmas_2011",
         "Dawn Christmas 2011 add pics",
         "Dawn Christmas 2011 add pics",
         "Ryan Krauss",
         "Ryan Krauss",
         "2011",
         "<Image>/Filters/Ryan/scrapbooking/Digital/Dawn Christmas 2011 Add Pics",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         dawn_christmas_2011)



def missy_bday_2012(img, drawable):
    gap = 0.2

    mydir = '/home/ryan/ryan_personal/Missy_birthday_2012/cropped'

    #create new layer
    total_w = 3600
    total_h = total_w
    new_layer = gimp.Layer(img, "New Image Layer", total_w, total_h, \
                           RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(new_layer, TRANSPARENT_FILL)
    img.add_layer(new_layer)

    top_margin = (12.0 - (4.0+3.0+3.0+2*gap))/2.0
    left_margin = (12.0 - (4.0+2.0+3.0+2*gap))/2.0

    x_vert_1 = left_margin + 4.0 + 2.0 + gap#right vertical edge for
        #top 3x4 and center 2x3


    #img 0 25 100 50 REPLACE 0 0
    w1 = 3.0
    h1 = 4.0
    x1 = x_vert_1 - w1
    y1 = top_margin
    b1 = y1 + h1
    _my_select(img, x1, y1, w1, h1)
    #name1 = 'Jan_2009_dsc_8712_3_by_4.jpg'
    name1 = 'D7K_005430_cropped_swing_backyard_3_by_4.JPG'
    path1 = os.path.join(mydir, name1)
    scale_and_paste_img_onto_selected_area(path1, w1, h1, new_layer)
    #_my_fg_bucket_fill(drawable)


    h3 = 3.0
    w3 = 4.0
    x3 = left_margin
    y3 = y1 + h1 + gap
    _my_select(img, x3, y3, w3, h3)
    name3 = 'D7K_004981_cropped_brighened_level_adjust_castlewood_model_pose_4_by_3.jpg'
    path3 = os.path.join(mydir, name3)
    scale_and_paste_img_onto_selected_area(path3, w3, h3, new_layer)

    ## ## ## _my_fg_bucket_fill(drawable)

    h4 = 3.0
    w4 = 2.0
    y4 = y3
    x4 = x3 + w3 + gap
    _my_select(img, x4, y4, w4, h4)
    name4 = 'D7K_005089_cropped_castlewood_w_Joshie_2_by_3.jpg'
    path4 = os.path.join(mydir, name4)
    scale_and_paste_img_onto_selected_area(path4, w4, h4, new_layer)
    ## ## _my_fg_bucket_fill(drawable)

    h5 = 4.0
    w5 = 3.0
    y5 = y4 - 1.0
    x5 = x4 + w4 + gap
    _my_select(img, x5, y5, w5, h5)
    name5 = 'D7K_004940_castlewood_big_smile_3_by_4.JPG'
    path5 = os.path.join(mydir, name5)
    scale_and_paste_img_onto_selected_area(path5, w5, h5, new_layer)

    ## ## ## _my_fg_bucket_fill(drawable)

    w2 = 2.0
    h2 = 2.0
    x2 = x5
    y2 = y5 - h2 - gap
    _my_select(img, x2, y2, w2, h2)
    name2 = 'D7K_003629_surgery_bw_2_by_2.JPG'
    path2 = os.path.join(mydir, name2)
    scale_and_paste_img_onto_selected_area(path2, w2, h2, new_layer)
    ## ## _my_fg_bucket_fill(drawable)

    h7 = 3.0
    w7 = 4.0
    x7 = x_vert_1 - w7 + 1.125
    y7 = y3 + h3 + gap
    _my_select(img, x7, y7, w7, h7)
    name7 = 'D7K_003409_bw_hc_sling_by_window_4_by_3.JPG'
    path7 = os.path.join(mydir, name7)
    scale_and_paste_img_onto_selected_area(path7, w7, h7, new_layer)

    ## ## _my_fg_bucket_fill(drawable)

    h6 = 2.75
    w6 = 2.75
    y6 = y7
    x6 = x7 - gap - w6
    _my_select(img, x6, y6, w6, h6)
    name6 = 'D7K_004844_stroller_w_cookie_square.JPG'
    path6 = os.path.join(mydir, name6)
    scale_and_paste_img_onto_selected_area(path6, w6, h6, new_layer)

    ## ## _my_fg_bucket_fill(drawable)


    ## #drawable, fill mode (fg), paint mode (normal), opacity,
    ## #threshold, sample-merged, x, y - Note that x and y are only used
    ## #if there is not selection

    ## print('yeah, I filled it')
    return img


register("missy_bday_2012",
         "Missy BDay 2012 add pics",
         "Missy BDay 2012 add pics",
         "Ryan Krauss",
         "Ryan Krauss",
         "2011",
         "<Image>/Filters/Ryan/scrapbooking/Digital/Missy BDay 2012",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         missy_bday_2012)


def find_height_given_width(filename, des_width):
    img2 = pdb.gimp_file_load(filename, filename)
    width = img2.width
    height = img2.height
    scale = des_width/width
    des_height = scale*height
    return des_height


def Christmas2012A(img, drawable):
    gap = 0.2

    #mydir = '/home/ryan/ryan_personal/top_secret/Christmas_2012/'
    mydir = '/home/ryan/ryan_personal/top_secret/Christmas_2012/black_and_whites'
    #create new layer
    total_w = 3600
    total_h = total_w
    new_layer = gimp.Layer(img, "New Image Layer", total_w, total_h, \
                           RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(new_layer, TRANSPARENT_FILL)
    img.add_layer(new_layer)

    small_pics = ['bw_0001.jpg', \
                  'bw_0003.jpg', \
                  'bw_0004.jpg', \
                  'bw_0005.jpg', \
                  'bw_0006.jpg', \
                  'bw_0007.jpg', \
                  ]


    top_margin = 0.5
    left_margin = (12.0 - (4.0+2.0+3.0+2*gap))/2.0

    #gap = 0.25
    N_small = len(small_pics)
    #H1*N_small + gap*(N_small-1) = 12 - 2*top_margin
    #solve for H1
    h1 = ((12 - 2*top_margin) - gap*(N_small-1))/N_small
    w1 = h1*1.5#assuming 6x4
    
    x1 = 0.75
    y1 = top_margin
    prevy = y1

    redo_small = 0

    if redo_small:
        for i, name in enumerate(small_pics):
            curpath = os.path.join(mydir, name)
            if i > 0:
                cury = prevy + h1 + gap
            else:
                cury = prevy

            _my_select(img, x1, cury, w1, h1)
            scale_and_paste_img_onto_selected_area(curpath, w1, h1, new_layer)
            prevy = cury


    #four bigger pics
    #head kisses: DSC_3205bw_cropped.JPG
    #Siah sleeping: D7K_000804_bw.JPG
    #Grandpa Krauss: bw_0008_cropped.jpg
    #Grandpa Dickson: bw_0009.jpg

    #sleeping Siah
    x5 = x1 + w1 + gap
    w5 = 3.8
    y5 = 1.7
    fn5 = 'D7K_000804_bw.JPG'
    path5 = os.path.join(mydir, fn5)
    h5 = find_height_given_width(path5, w5)
    _my_select(img, x5, y5, w5, h5)    
    scale_and_paste_img_onto_selected_area(path5, w5, h5, new_layer)

    #head kisses
    x4 = x5
    w4 = w5
    fn4 = 'DSC_3205bw_cropped.JPG'
    path4 = os.path.join(mydir, fn4)
    h4 = find_height_given_width(path4, w4)    
    y4 = y5 + h5 + gap
    _my_select(img, x4, y4, w4, h4)    
    scale_and_paste_img_onto_selected_area(path4, w4, h4, new_layer)

    #Grandpa Dickson
    x2 = x4 + w4 + gap
    w2 = w4
    path2 = os.path.join(mydir, 'bw_0009.jpg')
    h2 = find_height_given_width(path2, w2)
    y2 = y4 - (h2 - h4)
    _my_select(img, x2, y2, w2, h2)    
    scale_and_paste_img_onto_selected_area(path2, w2, h2, new_layer)                 

    #Grandpa Krauss
    x3 = x5
    y3 = y4 + h4 + gap
    w3 = 4.5
    path3 = os.path.join(mydir, 'bw_0008_cropped.jpg')
    h3 = find_height_given_width(path3, w3)
    _my_select(img, x3, y3, w3, h3)    
    scale_and_paste_img_onto_selected_area(path3, w3, h3, new_layer)



    
    return img


register("Christmas2012A",
         "Christmas 2012 A add pics",
         "Christmas 2012 A add pics",
         "Ryan Krauss",
         "Ryan Krauss",
         "2012",
         "<Image>/Filters/Ryan/scrapbooking/Digital/Christmas 2012 A",
         "RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         Christmas2012A)



main()
