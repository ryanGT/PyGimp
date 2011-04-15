#!/usr/bin/python

import os, glob, re
import time
import math
from gimpfu import *
import rwkos
import pdb as Pdb

from gimp_copy_utils import *

Linux = rwkos.amiLinux()

##graph_path = '/home/ryan/siue/classes/graph_paper.png'
## classes_base = '/home/ryan/siue/classes'
## keys = ['452','mechatronics','482','484','356','mobile_robotics']
## nums = ['452','458','482','484','356','492']
## course_num_dict = dict(zip(keys, nums))

## bases = ['452/lectures', 'mechatronics/2009/lectures', '482/2009/lectures', \
##          '484/lectures', '356/Fall_2009/lectures', \
##          'mobile_robotics/2009/lectures']
## base_dict = dict(zip(keys, bases))

## curdir = os.getcwd()
## log_msg('curdir = %s' % curdir)

import pygimp_lecture_utils
from pygimp_lecture_utils import set_lecture_path, get_course_number, \
     get_path_from_pkl, graph_path, get_date_for_slide, \
     save_as, save_as_jpg, \
     find_graph_ind, find_notes_layer, get_notes_layer_slide_num, \
     get_slide_num_filename, \
     log_msg, open_pickle, save_pickle, \
     folder_from_pickle, \
     save_all_slides, \
     close_all, _save_and_close, \
     my_save_2010, _really_save, \
     slide_num_from_path

import pygimp_lecture_utils as PGLU

## def get_course_key_from_curdir():
##     curdir = os.getcwd()
##     #log_msg('curdir = %s' % curdir)
##     for key in keys:
##         if curdir.find('/' + key +'/') > -1:
##             return key
##     log_msg('could not find any of %s \n' % keys)
##     log_msg('in curdir %s' % curdir)
    
## def get_lecture_base():
##     key = get_course_key_from_curdir()
##     if key:
##         base = base_dict[key]
##         lecture_base = os.path.join(classes_base, base)
##         return lecture_base

## def get_course_number():
##     key = get_course_key_from_curdir()
##     if key:
##         cn = course_num_dict[key]
##         return cn
    
#lb = get_lecture_base()
#log_msg('lecture_base = %s' % lb)

## def get_cur_date_str():
##     date_str = time.strftime('%m_%d_%y')
##     return date_str

## def get_date_from_path():
##     curdir = os.getcwd()
##     p = re.compile('/lectures/(\d+_\d+_\d+)')
##     q = p.search(curdir)
##     if q:
##         #q.group(1).split('_',2)
##         return q.group(1)
##     else:
##         return None

## def get_date_str():
##     date_str = get_date_from_path()
##     if not date_str:
##         date_str = get_cur_date_str()
##     return date_str

## def get_date_folder():
##     date_str = get_date_str()
##     lecture_base = get_lecture_base()
##     folder = os.path.join(lecture_base, date_str)
##     return folder

def _feather_helper(feather_radius=0):
    if feather_radius == None:
        return False, 0.0
    return True, feather_radius


def _radius_helper(radius):
    if isinstance(radius, tuple):
        return radius
    return radius, radius


def select_by_color(drawable, color, threshold = 0,
                    operation = 2,
                    antialias = False, feather_radius = 0,
                    sample_merged = False, select_transparent = False,
                    select_criterion = 0, \
                    feater_radius=0):
    if drawable == None:
        drawable = _active_drawable()
    do_feather, feather_radius = _feather_helper(feater_radius)
    feather_radius_x, feather_radius_y = _radius_helper(feather_radius)

    pdb.gimp_by_color_select_full(drawable, color, threshold, operation,
                                  antialias, do_feather, feather_radius_x,
                                  feather_radius_y, sample_merged,
                                  select_transparent, select_criterion)


def activate_notes_layer(img, name="Notes Layer"):
    ind = find_graph_ind(img, name=name)
    img.active_layer = img.layers[ind]


def move_resize_window():#timg, tdrawable):
    if Linux:
        import subprocess
        p = subprocess.Popen(['xdotool','getactivewindow'], \
                             stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, errors = p.communicate()
        win = output.strip()#get id of active window
        movecmd = 'xdotool windowmove %s 0 0' % win
        os.system(movecmd)
        #sizecmd = 'xdotool windowsize %s 1024 700' % win
        sizecmd = 'xdotool windowsize %s 1280 1000' % win
        os.system(sizecmd)
        ecmd = "xdotool key ctrl+shift+E"
        time.sleep(1.0)
        os.system(ecmd)


register(
        "move_resize_window",
        "Move and resize window for class lectures",
        "Move and resize window for class lectures",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Xtns/Languages/Ryan/_Move and Resize",
        "",
        [],
        [],
        move_resize_window)


def new_grid_image(pat=None, footer='', footer_x=1920):#timg, tdrawable):
    width = 2000
    #height = 1600
    height = 1300
    header_x = 1780
    footer_y = height - 80
    
    img = gimp.Image(width, height, RGB)

    white_layer = gimp.Layer(img, "White Layer", width, height, \
                             RGB_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(white_layer, WHITE_FILL)
    img.add_layer(white_layer)

    graph_layer = pdb.gimp_file_load_layer(img, graph_path)
    img.add_layer(graph_layer)

    new_name, slide_num = get_slide_num_filename(pat=pat)
    notes_name = "Notes Layer %0.4d" % int(slide_num)
    trans_layer = gimp.Layer(img, notes_name, width, height, \
                             RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(trans_layer, TRANSPARENT_FILL)
    img.add_layer(trans_layer)

    img.active_layer = trans_layer
    date_str = get_date_for_slide()
    date_str = date_str.replace('_','/')
    pdb.gimp_context_set_foreground((0,0,0))
    cn = get_course_number()
    font_size_header_footer = 40
    text_layer = pdb.gimp_text_fontname(img, trans_layer, header_x, 10, \
                                        "ME %s\n%s" % (cn, date_str), \
                                        0, True, font_size_header_footer, \
                                        1, "Sans")

    pdb.gimp_floating_sel_anchor(text_layer)
    
    text_layer2 = pdb.gimp_text_fontname(img, trans_layer, footer_x, footer_y, \
                                         footer+str(slide_num), \
                                         0, True, font_size_header_footer, \
                                         1, "Sans")


    pdb.gimp_floating_sel_anchor(text_layer2)
    #pdb.gimp_selection_all(img)
    #pdb.gimp_edit_clear(trans_layer)


    out1 = gimp.Display(img)
    gimp.displays_flush()
    pdb.gimp_image_clean_all(img)
    title_in = img.filename
    #log_msg('title_in=%s' % title_in)
    move_resize_window()
    return img
    
    
register("new_grid_image",
         "A new image for class lectures",
         "A new image for class lectures",
         "Ryan Krauss",
         "Ryan Krauss",
         "2009",
         "<Toolbox>/Xtns/Languages/Ryan/2009/_New Grid Image",
         "",#RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         new_grid_image)


register("set_lecture_path", \
         "Set the path for todays lectures", \
         "Set the path for todays lectures saving it in a pkl", \
         "Ryan Krauss", \
         "Ryan Krauss", \
         "2009", \
         "<Toolbox>/Xtns/Languages/Ryan/2009/Set Lecture Path", \
         "", \
         [], \
         [], \
         set_lecture_path)

         
import tkFileDialog
filetypes = [('png files', '*.png'), ('jpg files', '*.jpg'),\
             ('all files', '.*')]
jpgtypes = [('jpg files', '*.jpg'), ('png files', '*.png'),\
             ('all files', '.*')]
xcftypes = [('xcf file', '*.xcf')]

import tk_simple_dialog
import tk_msg_dialog
#?bob = tkSimpleDialog.askinteger?
#?tkSimpleDialog.askinteger?

def get_quiz_solution_number():
    myfolder = get_path_from_pkl()
    mypaths = rwkos.Find_in_top_and_sub_dirs(myfolder, 'quiz_*')
    qn = None
    if mypaths:
        path1 = mypaths[0]
        folder, fn1 = os.path.split(path1)
        pat = re.compile('quiz_([0-9]+)')
        q = pat.search(fn1)
        if q:
            qn_str = q.group(1)
            qn = int(qn_str)
    if qn is None:
        W = tk_simple_dialog.myWindow()
        qn_str = W.var.get()
        qn = int(qn_str)
##     log_msg('qn_str = %s' % qn_str)
##     log_msg('type(qn_str) = %s' % type(qn_str))
##     log_msg('qn = %s' % qn)
##     log_msg('type(qn) = %s' % type(qn))
    return qn

    
def get_quiz_solution_pattern(qn=None):
    if qn is None:
        qn = get_quiz_solution_number()
    pat = 'quiz_%0.2d_solution' % qn + '_%0.4d.jpg'
    return pat


def get_quiz_solution_filename():
    pat = get_quiz_solution_pattern()
    folder = get_path_from_pkl()    
    new_ind = rwkos.get_new_file_number(pat, folder)
    new_name = pat % new_ind
    return new_name#, new_ind
    

def new_quiz_solution_page():
    #how to get the quiz number?
    #new_grid_image(pat=pat, footer=footer)
    qn = get_quiz_solution_number()
    footer = 'Quiz %d Solution ' % qn
    pat = get_quiz_solution_pattern(qn)
    new_grid_image(pat=pat, footer=footer, footer_x=1500)
    

register(
        "new_quiz_solution_page",
        "A new image for quiz solutions",
        "A new image for quiz solutions",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Xtns/Languages/Ryan/2009/New _Quiz Solution Page",
        "",#RGB*, GRAY*",
        [],
        [],
        new_quiz_solution_page)


def red_brush():
    pdb.gimp_context_set_foreground((255,0,0))
    
    
register(
        "red_brush",
        "Set brush foreground to red",
        "Set brush foreground to red",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Brushes/_Red Brush",
        "",#RGB*, GRAY*",
        [],
        [],
        red_brush)


def black_brush():
    pdb.gimp_context_set_foreground((0,0,0))
    
    
register(
        "black_brush",
        "Set brush foreground to black",
        "Set brush foreground to black",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Brushes/_Black Brush",
        "",#RGB*, GRAY*",
        [],
        [],
        black_brush)


def blue_brush():
    pdb.gimp_context_set_foreground((0,0,255))
    
    
register(
        "blue_brush",
        "Set brush foreground to blue",
        "Set brush foreground to blue",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Brushes/_Blue Brush",
        "",#RGB*, GRAY*",
        [],
        [],
        blue_brush)


def find_if_open(imgname):
    #Pdb.set_trace()
    mylist = gimp.image_list()
    for img in mylist:
        curname = img.name
        if curname == imgname:
            return img
    #this line would be executed only if imgname was never found
    return None


def list_images():
    #Pdb.set_trace()
    mylist = gimp.image_list()
    for item in mylist:
        print('item = '+str(item))

register(
        "list_images",
        "Set brush foreground to blue",
        "Set brush foreground to blue",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Xtns/Languages/Ryan/2009/_List Images",
        "",#RGB*, GRAY*",
        [],
        [],
        list_images)


def green_brush():
    pdb.gimp_context_set_foreground((0,160,0))
    
    
register(
        "green_brush",
        "Set brush foreground to green",
        "Set brush foreground to green",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Lecture/Brushes/_Green Brush",
        "",#RGB*, GRAY*",
        [],
        [],
        green_brush)

    
# examples:
def open_it(initialdir=None):
    filename = tkFileDialog.askopenfilename()
    return filename

def open_xcf(initialdir=None, initialfile=None):
    filename = tkFileDialog.askopenfilename(initialfile=initialfile,
                                            initialdir=initialdir,
                                            filetypes=xcftypes)
    return filename


def open_jpg(initialdir=None, initialfile=None):
    filename = tkFileDialog.askopenfilename(initialfile=initialfile,
                                            initialdir=initialdir,
                                            filetypes=jpgtypes)
    return filename


def save_it():
    filename = tkFileDialog.askopenfilename()
    return filename


def my_save(img, drawable):
    ind = find_graph_ind(img)

    if ind:
        img.layers[ind].visible = False
        folder = get_path_from_pkl()
        myint = get_notes_layer_slide_num(img)
        new_name, slide_num = get_slide_num_filename(myint=myint)
        filename = save_as(initialdir=folder, initialfile=new_name)
        #log_msg('filename = ' + filename)
        if filename:
            pne, ext = os.path.splitext(filename)
            xcf_path = pne+'.xcf'
            pdb.gimp_xcf_save(1, img, drawable, xcf_path, xcf_path)
            flat_layer = pdb.gimp_image_flatten(img)
            #pdb.gimp_file_save(img, flat_layer, filename, filename)
            pdb.file_png_save(img, flat_layer, filename, filename, \
                              0, 0, 0, 0, 0, \
                              1, 1)
            pdb.gimp_image_clean_all(img)


register(
        "my_save",
        "Save grid image with grid not visible",
        "Save grid image with grid not visible",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/2009/_Save Grid Image",
        "RGB*, GRAY*",
        [],
        [],
        my_save)


def my_save2(img, drawable):
    #log_msg('in my_save2')
    ind = find_graph_ind(img)

    if ind:
        img.layers[ind].visible = False
    else:
        log_msg('did not find a graph ind')
        
    folder = get_path_from_pkl()
    log_msg('folder='+str(folder))
    myint = get_notes_layer_slide_num(img)
    log_msg('myint='+str(myint))
    title_in = img.filename
    log_msg('title_in = %s' % title_in)
    new_name = None
    if title_in:
        folder_in, name_in = os.path.split(title_in)
        fno, ext = os.path.splitext(name_in)
        name_in = fno + '.png'
        #log_msg('name_in = %s' % name_in)
        #log_msg('folder_in = %s' % folder_in)
        cn = get_course_number()
        my_ind = name_in.find('ME'+cn)
        #log_msg('my_ind = %s' % my_ind)
        if my_ind == 0:
            #log_msg('in the good case')
            folder = folder_in
            new_name = name_in
    #log_msg('new_name = %s' % new_name)
    if new_name is None:
        new_name, slide_num = get_slide_num_filename(myint=myint)
    filename = save_as(initialdir=folder, initialfile=new_name)
    log_msg('filename = ' + filename)
    if filename:
        pne, ext = os.path.splitext(filename)
        xcf_path = pne+'.xcf'
        pdb.gimp_selection_all(img)
        pdb.gimp_edit_copy_visible(img)
        img2 = pdb.gimp_edit_paste_as_new()
        pdb.gimp_xcf_save(1, img, drawable, xcf_path, xcf_path)
        folder, xcf_name = os.path.split(xcf_path)
        xcf_path = xcf_path.encode()
        xcf_name = xcf_name.encode()
        #log_msg('xcf_name='+xcf_name)
        #log_msg('type(img.filename)=%s' % type(img.filename))
        #log_msg('type(xcf_name)=%s' % type(xcf_name))
        img.filename = xcf_path
        #pdb.gimp_file_save(img, drawable, xcf_path, xcf_path)
        flat_layer = pdb.gimp_image_flatten(img2)
        #gimp.Display(img2)
        pdb.gimp_file_save(img2, flat_layer, filename, filename)
        pdb.gimp_image_delete(img2)
        if ind:
            img.layers[ind].visible = True
        pdb.gimp_image_clean_all(img)
        gimp.displays_flush()
        log_msg('after clean all')


register(
        "my_save2",
        "Save grid image with grid not visible",
        "Save grid image with grid not visible",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/2009/_Save Grid Image 2",
        "RGB*, GRAY*",
        [],
        [],
        my_save2)


def raise_img(img):
    #gimp.Display(img)#<-- this seems to re-open the image or create a
    #new Display for it
    gimp.displays_flush()
    time.sleep(0.5)
    move_resize_window()#timg, tdrawable)
    

def _open_by_int(next_int):
    new_name, new_ind = get_slide_num_filename(myint=next_int)
    print('new_name = ' + str(new_name))
    path_no_ext, ext = os.path.splitext(new_name)
    xcf_name = path_no_ext +'.xcf'
    img = find_if_open(xcf_name)
    if img is None:
        my_open(filename=xcf_name)
    else:
        raise_img(img)
    #pdb.gimp_selection_none(img)
    

def open_next(img, drawable):
    #This doesn't work perfectly.  It seems like it opens pngs instead
    #of xcfs (which makes sense if you look at get_slide_num_filename)
    myint = get_notes_layer_slide_num(img)
    next_int = myint + 1
    _open_by_int(next_int)


register(
        "open_next",
        "Open next image",
        "Open next image",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/2009/_Open Next Image",
        "RGB*, GRAY*",
        [],
        [],
        open_next)


def open_previous(img, drawable):
    #This doesn't work perfectly.  It seems like it opens pngs instead
    #of xcfs (which makes sense if you look at get_slide_num_filename)
    myint = get_notes_layer_slide_num(img)
    prev_int = myint - 1
    _open_by_int(prev_int)


register(
        "open_previous",
        "Open previous image",
        "Open previous image",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/2009/_Open Previous Image",
        "RGB*, GRAY*",
        [],
        [],
        open_previous)


def my_close(img, drawable):
    #pdb.gimp_display_delete(gimp._id2display(1))
    pdb.gimp_display_delete(img)


register(
        "my_close",
        "Close image",
        "Close image",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/2009/_Close Image",
        "RGB*, GRAY*",
        [],
        [],
        my_close)

    
    
def save_quiz(img, drawable):
    folder = get_path_from_pkl()
    new_name = get_quiz_solution_filename()

    ind = find_graph_ind(img)

    if ind:
        img.layers[ind].visible = False

    title_in = img.filename
    #log_msg('title_in = %s' % title_in)
    if title_in:
        cur_folder, cur_name = os.path.split(title_in)
        if cur_name.find('quiz_') == 0:
            new_name = cur_name
            folder = cur_folder
    filename = save_as_jpg(initialdir=folder, initialfile=new_name)
    filename = filename.encode()
    #log_msg('filename = ' + filename)

    if filename:
        flat_layer = pdb.gimp_image_flatten(img)
        pdb.gimp_file_save(img, flat_layer, filename, filename)
        img.filename = filename
        pdb.gimp_image_clean_all(img)
        gimp.displays_flush()


register(
        "save_quiz",
        "Save quiz image",
        "Save quiz image",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Image>/Filters/Ryan/2009/Save _Quiz Image",
        "RGB*, GRAY*",
        [],
        [],
        save_quiz)


def batch_xcf_to_png(file_pattern):
	#log_msg('pattern='+file_pattern)
	file_list=glob.glob(file_pattern)
	file_list.sort()
	for filename in file_list:
		#log_msg('filename='+filename)
		img = pdb.gimp_file_load(filename, filename)
                ind = find_graph_ind(img)
                #log_msg('ind='+str(ind))
                if ind:
                    img.layers[ind].visible = False
                    pne, ext = os.path.splitext(filename)
                    png_path = pne+'.png'
                    flat_layer = pdb.gimp_image_flatten(img)
                    log_msg('%s --> %s' % (filename, png_path))
                    pdb.gimp_file_save(img, flat_layer, png_path, png_path)  
##                     pdb.file_png_save(img, flat_layer, png_path, png_path, \
##                                       0, 9, 0, 0, 0, \
##                                       0, 0)                
		    #pdb.gimp_file_save(image, drawable, filename, filename)
		    pdb.gimp_image_delete(img)


register(
	"batch_xcf_to_png", "", "", "", "", "",
  	"<Toolbox>/Xtns/Languages/Ryan/_Batch XCF to PNG", "",
  	[
  	(PF_STRING, "file_pattern", "file_pattern", "*.xcf"),
  ],
  [],
  batch_xcf_to_png
  )
    

def my_open(dialog_func=open_xcf, filename=None):
    folder = get_path_from_pkl()
    if filename is None:
        filename = dialog_func(initialdir=folder)
    #img = pdb.gimp_file_load(1, filename, filename)
    img = pdb.gimp_file_load(filename, filename)
    ind = find_graph_ind(img)
    title_in = img.filename
    #log_msg('title_in=%s' % title_in)
    if ind:
        img.layers[ind].visible = True


    ind2 = find_notes_layer(img)
    if ind2:
        pdb.gimp_image_set_active_layer(img, img.layers[ind2])

    pdb.gimp_image_clean_all(img)

    #Set the current_slide if it is in the current lecture
    mydict = open_pickle()
    full_pat = os.path.join(mydict['lecture_path'], mydict['search_pat'])
    if filename.find(full_pat) == 0:
        cur_slide = slide_num_from_path(filename)
        mydict['current_slide'] = cur_slide
        save_pickle(mydict)
    
    out2 = gimp.Display(img)
    gimp.displays_flush()
    time.sleep(0.5)
    move_resize_window()#timg, tdrawable)
    #pdb.gimp_selection_none(img)


        
## register(
##         "my_open",
##         "Open grid image making grid visible",
##         "Open grid image making grid visible and setting Notes layer active",
##         "Ryan Krauss",
##         "Ryan Krauss",
##         "2009",
##         "<Image>/Filters/Ryan/_Open Grid Image",
##         "RGB*, GRAY*",
##         [],
##         [],
##         my_open)

register(
	"my_open", "", "", "", "", "",
  	"<Toolbox>/Lecture/_Open Grid Image", "",
  	[],
        [],
        my_open
)


def open_quiz():
    my_open(dialog_func=open_jpg)


register(
	"open_quiz", "", "", "", "", "",
  	"<Toolbox>/Xtns/Languages/Ryan/Open Q_uiz Image", "",
  	[],
        [],
        open_quiz
)



#############################################
#
#  Fall 2010 Versions
#
#############################################
## def save_all_slides():
##     img_list = gimp.image_list()
##     N = len(img_list)
##     print('img_list = ' + str(img_list))
##     #Pdb.set_trace()
##     mydict = open_pickle()
##     full_pat = os.path.join(mydict['lecture_path'], mydict['search_pat'])
##     success = True
##     for img in img_list:
##         curname = img.filename
##         if curname and curname.find(full_pat) == 0:
##             if pdb.gimp_image_is_dirty(img):
##                 out = my_save_2010(img)
##                 if not out:
##                     #if any one save fails, success is False
##                     success = False
##             else:
##                 print('not saving clean image: ' + curname)
##     return success



## def close_all(N=10):
##     if gimp.image_list():
##         for i in range(N):
##             disp = gimp._id2display(i)
##             if disp is not None:
##                 #Pdb.set_trace()
##                 try:
##                     pdb.gimp_display_delete(disp)
##                 except:
##                     print('problem deleting disp # ' + str(i))

def build_slide_path(mydict):
    pat = mydict['pat']
    filename = pat % mydict['current_slide']
    filepath = os.path.join(mydict['lecture_path'], filename)
    return filepath


def build_next_outline_path(mydict):
    pat = 'outline_%0.4i.png'
    ind = mydict['outline_slide'] + 1
    filename = pat % ind
    exclude_dir = os.path.join(mydict['lecture_path'], 'exclude')
    filepath = os.path.join(exclude_dir, filename)
    return filepath

    
def open_or_create_slide(mydict, verbosity=1):
    filepath = build_slide_path(mydict)
    if os.path.exists(filepath):
        if verbosity > 0:
            print('found:' + filepath)
        save_pickle(mydict)
        my_open(filename=filepath)
    else:
        print('filepath not found: ' + filepath)
        new_grid_image_2010()#this function saves the pickle


def check_for_next_outline_slide(mydict):
    outline_path = build_next_outline_path(mydict)
    return os.path.exists(outline_path)


def check_for_slide(mydict):
    slidepath = build_slide_path(mydict)
    return os.path.exists(slidepath)



def open_outline_png(pngpath):
    img = new_grid_image_2010()
    floating_sel = copy_png_to_img(pngpath, img, x_offset=25, \
                                   y_offset=25)
    if top_layer_is_TEMP(img, 1) or top_layer_is_Latex(img, 1):
        pdb.gimp_floating_sel_anchor(floating_sel)
    if top_layer_is_Latex(img):
        print('top_layer_is_Latex True')
        select_by_color(img.layers[0], (255,255,255))
        pdb.gimp_edit_clear(img.layers[0])
        pdb.gimp_selection_none(img)
        pdb.gimp_image_merge_down(img, img.layers[0],1)
    #pdb.gimp_selection_none(img)
        


def open_or_create_next_slide(save=True, close=True, force_no_outline=False):
    if save or close:
        success = _save_and_close(save=save, close=close)
        if not success:
            return
    mydict = open_pickle()
    next_slide = mydict['current_slide'] + 1
    mydict['current_slide'] = next_slide

    if check_for_slide(mydict):
        save_pickle(mydict)
        slidepath = build_slide_path(mydict)
        my_open(filename=slidepath)
        return
    
    if force_no_outline:
        outline_bool = False
    else:
        outline_bool = check_for_next_outline_slide(mydict)

    if outline_bool:
        outline_path = build_next_outline_path(mydict)
        next_outline_slide = mydict['outline_slide'] + 1
        mydict['outline_slide'] = next_outline_slide
        save_pickle(mydict)
        
        open_outline_png(outline_path)
    else:
        open_or_create_slide(mydict)



def open_or_create_next_slide_no_outline(save=True, close=True):
    return open_or_create_next_slide(save=save, close=close, \
                                     force_no_outline=True)


def open_or_create_next_slide_old(save=True, close=True):
    if save or close:
        success = _save_and_close(save=save, close=close)
        if not success:
            return
    mydict = open_pickle()
    next_slide = mydict['current_slide'] + 1
    mydict['current_slide'] = next_slide
    open_or_create_slide(mydict)


## def _save_and_close(save=True, close=True):
##     if save:
##         success = save_all_slides()
##     if close and success:
##         close_all()
##     return success

def open_previous_slide(save=True, close=True):
    if save or close:
        success = _save_and_close(save=save, close=close)
        if not success:
            return
    mydict = open_pickle()
    prev_slide = mydict['current_slide'] - 1
    mydict['current_slide'] = prev_slide
    open_or_create_slide(mydict)


def find_last_slide_ind():
    mydict = open_pickle()
    pat = mydict['pat']
    full_pat = os.path.join(mydict['lecture_path'], pat)
    for i in range(100):
        n = i + 1
        curpath = full_pat % n
        if not os.path.exists(curpath):
            n -= 1
            return n
        

def jump_to_first_slide(save=True, close=True):
    ## if save or close:
    ##     success = _save_and_close(save=save, close=close)
    ##     if not success:
    ##         return
    #mydict = open_pickle()
    #mydict['current_slide'] = 0
    #mydict['outline_slide'] = 0
    #save_pickle(mydict)
    W = tk_simple_dialog.reset_lecture_dialog()
    open_or_create_next_slide()
    #open_or_create_slide(mydict)


def jump_to_last_slide(save=True, close=True):
    ## if save or close:
    ##     success = _save_and_close(save=save, close=close)
    ##     if not success:
    ##         return
    ind = find_last_slide_ind()
    mydict = open_pickle()
    mydict['current_slide'] = ind - 1
    save_pickle(mydict)
    open_or_create_next_slide()
    

register("jump_to_first_slide",
         "Jump to first slide",
         "Jump to first slide",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Lecture/Jump/Jump to _First",
         "",#RGB*, GRAY*",
         [],
         [],
         jump_to_first_slide)


register("jump_to_last_slide",
         "Jump to last slide",
         "Jump to last slide",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Lecture/Jump/Jump to _Last",
         "",#RGB*, GRAY*",
         [],
         [],
         jump_to_last_slide)


def new_grid_image_2010(footer='', footer_x=1920):#timg, tdrawable):
    #print('in new_grid_image_2010')
    width = 2000
    #height = 1600
    height = 1300
    header_x = 1780
    footer_y = height - 80

    img = gimp.Image(width, height, RGB)

    white_layer = gimp.Layer(img, "White Layer", width, height, \
                             RGB_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(white_layer, WHITE_FILL)
    img.add_layer(white_layer)

    graph_layer = pdb.gimp_file_load_layer(img, graph_path)
    img.add_layer(graph_layer)

    new_name, slide_num = PGLU.get_slide_num_filename_2010()
    print('new_name = ' + new_name)
    mydict = open_pickle()
    notes_name = "Notes Layer %0.4d" % int(slide_num)
    trans_layer = gimp.Layer(img, notes_name, width, height, \
                             RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(trans_layer, TRANSPARENT_FILL)
    img.add_layer(trans_layer)

    img.active_layer = trans_layer
    date_str = mydict['date_stamp']
    #date_str = date_str.replace('_','/')
    pdb.gimp_context_set_foreground((0,0,0))
    cn = mydict['course_num']
    font_size_header_footer = 40
    text_layer = pdb.gimp_text_fontname(img, trans_layer, header_x, 10, \
                                        "ME %s\n%s" % (cn, date_str), \
                                        0, True, font_size_header_footer, \
                                        1, "Sans")

    pdb.gimp_floating_sel_anchor(text_layer)

    text_layer2 = pdb.gimp_text_fontname(img, trans_layer, footer_x, footer_y, \
                                         footer+str(slide_num), \
                                         0, True, font_size_header_footer, \
                                         1, "Sans")


    pdb.gimp_floating_sel_anchor(text_layer2)
    #pdb.gimp_selection_all(img)
    #pdb.gimp_edit_clear(trans_layer)

    new_path = os.path.join(mydict['lecture_path'], new_name)
    img.filename = new_path


    mydict['current_slide'] = slide_num
    save_pickle(mydict)
    
    out1 = gimp.Display(img)
    gimp.displays_flush()
    pdb.gimp_image_clean_all(img)
    ## title_in = img.filename
    ## log_msg('title_in=%s' % title_in)
    move_resize_window()
    #pdb.gimp_selection_none(img)
    return img


register("new_grid_image_2010",
         "A new image for class lectures",
         "A new image for class lectures",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Lecture/_New Grid Image",
         "",#RGB*, GRAY*",
         [],
         [(PF_IMAGE, 'img', 'the new image')],
         new_grid_image_2010)


register("open_or_create_next_slide",
         "Open next slide for class lectures",
         "Open or create next slide for class lectures",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Lecture/_Next Slide",
         "",#RGB*, GRAY*",
         [],
         [],#(PF_IMAGE, 'img', 'the next slide')],
         open_or_create_next_slide)


register("open_or_create_next_slide_no_outline",
         "Open next slide - but not an outline slide",
         "Open or create next slide for class lectures (no outline)",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Lecture/Next Slide - No _Outline",
         "",#RGB*, GRAY*",
         [],
         [],#(PF_IMAGE, 'img', 'the next slide')],
         open_or_create_next_slide_no_outline)



register("open_previous_slide",
         "Open previous slide for class lectures",
         "Open or create previous slide for class lectures",
         "Ryan Krauss",
         "Ryan Krauss",
         "2010",
         "<Toolbox>/Lecture/_Previous Slide",
         #"<Toolbox>/Xtns/Languages/Ryan/_Previous Slide",
         "",#RGB*, GRAY*",
         [],
         [],#(PF_IMAGE, 'img', 'the next slide')],
         open_previous_slide)


def zero_current_slide():
    mydict = open_pickle()
    mydict['current_slide'] = 0
    save_pickle(mydict)


register("zero_current_slide",
     "Set the current lecture slide number back to 0",
     "Set the current lecture slide number back to 0",
     "Ryan Krauss",
     "Ryan Krauss",
     "2010",
     "<Toolbox>/Lecture/_Zero Current Slide",
     "",
     [],
     [],
     zero_current_slide)




register(
        "my_save_2010",
        "Save grid image with grid not visible",
        "Save grid image with grid not visible",
        "Ryan Krauss",
        "Ryan Krauss",
        "2010",
        "<Image>/Lecture/_Save Grid Image 2010",
        "RGB*, GRAY*",
        [],
        [(PF_INT, 'success', 'Boolean integer for whether or not the image saved correctly')],
        my_save_2010)


def reset_pickle():
    """Use this at the beginning of a lecture to set the pickle to
    slide 0 of the correct class based on the time and day of the
    week."""
    debug = 4
    #debugging - set to first day of class
    if debug == 1:
        now = time.strptime('08/23/10 8:55', '%m/%d/%y %H:%M')
    elif debug == 2:
        now = time.strptime('08/24/10 12:15', '%m/%d/%y %H:%M')
    elif debug == 3:
        now = time.strptime('09/08/10 13:25', '%m/%d/%y %H:%M')
    elif debug == 4:
        now = time.strptime('01/13/11 19:25', '%m/%d/%y %H:%M')
    else:
        now = time.localtime()
    
    mydict = {}
    mydict['current_slide'] = 0
    mydict['outline_slide'] = 0
    mydict['date_stamp'] = time.strftime('%m/%d/%y', now)
    date_str = time.strftime('%m_%d_%y', now)

    found = False
    if (now.tm_wday in [0,2]) and (now.tm_hour < 11):
        found = True
        course = '458'
        root = '/home/ryan/siue/classes/mechatronics/%i/lectures/%s' % \
               (now.tm_year, date_str)
    elif (now.tm_wday in [1,3]) and (11 < now.tm_hour < 15):
        found = True
        course = '482'
        root = '/home/ryan/siue/classes/482/%i/lectures/%s' % \
               (now.tm_year, date_str)
    elif (now.tm_wday in [1,3]) and (18 < now.tm_hour < 22):
        found = True
        course = '592'
        root = '/home/ryan/siue/classes/nonlinear_controls/%i/lectures/%s' % \
               (now.tm_year, date_str)
    if (now.tm_wday == 2) and (now.tm_hour > 12):
        found = True
        course = '492'
        root = '/home/ryan/siue/classes/mobile_robotics/%i/lectures/%s' % \
               (now.tm_year, date_str)


    if found:
        mydict['course_num'] = course
        mydict['pat'] = 'ME' + course + '_' + date_str + '_%0.4i.xcf'
        mydict['search_pat'] = 'ME' + course +'_' + date_str
        mydict['lecture_path'] = rwkos.FindFullPath(root)
        save_pickle(mydict)
    else:
        msg = 'Could not determine the course\n' + \
              'based on the current day/time.\n' + \
              '\n' + \
              'now.tm_wday = %s\n' % now.tm_wday + \
              'now.tm_hour = %s\n' % now.tm_hour + \
              '\n' + \
              'Run the script gimp_lecture_prep.py.'
        W = tk_msg_dialog.myWindow(msg)


register(
        "reset_pickle",
        "Reset lecture pickle based on current day/time",
        "Reset lecture pickle based on current day/time",
        "Ryan Krauss",
        "Ryan Krauss",
        "2010",
        "<Toolbox>/Lecture/_Reset Pickle",
        "",
        [],
        [],
        reset_pickle)


def show_pickle():
    """Load the lecture pickle and display it on a Tk message dialog."""
    mydict = open_pickle()
    msg = ''
    line_pat = '%s: %s\n'
    for key, value in mydict.iteritems():
        curline = line_pat % (key, value)
        msg += curline
    W = tk_msg_dialog.myWindow(msg)


register(
        "show_pickle",
        "Show the lecture pickle.",
        "Show the lecture pickle.",
        "Ryan Krauss",
        "Ryan Krauss",
        "2010",
        "<Toolbox>/Lecture/_Show Pickle",
        "",
        [],
        [],
        show_pickle)

def edit_pickle():
    """Load and display the current lecture pickle in a
    dialog that allows editting the values"""
    W = tk_simple_dialog.lecture_pickle_dialog()


register(
        "edit_pickle",
        "Edit the lecture pickle.",
        "Edit the lecture pickle.",
        "Ryan Krauss",
        "Ryan Krauss",
        "2010",
        "<Toolbox>/Lecture/_Edit Pickle",
        "",
        [],
        [],
        edit_pickle)

#############################################
#
# End 2010
#
#############################################


##---------------------##
#
# This must be last
#
##---------------------##
main()

