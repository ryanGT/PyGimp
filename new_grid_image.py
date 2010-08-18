#!/usr/bin/python

import os, glob, re
import time
import math
from gimpfu import *
import rwkos
import pdb as Pdb

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
     get_path_from_pkl, graph_path, get_date_for_slide, get_slide_num_filename, \
     log_msg

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


def find_graph_ind(img, name='graph_paper_2000_by_1200.png'):
    N = len(img.layers)
    for n in range(N):
        if img.layers[n].name == name:
            return n


def find_notes_layer(img, name='Notes Layer'):
    N = len(img.layers)
    for n in range(N):
        if img.layers[n].name.find(name) == 0:
            return n


def get_notes_layer_slide_num(img, name='Notes Layer'):
    ind = find_notes_layer(img, name)
    layer_name = img.layers[ind].name
    N = len(name)
    rest = layer_name[N:]
    #log_msg('rest:'+rest)
    rest = rest.strip()
    if rest:
        myint = int(rest)
        log_msg('myint:%i'%myint)
        return myint
    else:
        return None


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
        sizecmd = 'xdotool windowsize %s 1250 950' % win
        os.system(sizecmd)
        ecmd = "xdotool key ctrl+shift+E"
        time.sleep(0.7)
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
    height = 1200
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


    gimp.Display(img)
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
         "<Toolbox>/Xtns/Languages/Ryan/_New Grid Image",
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
         "<Toolbox>/Xtns/Languages/Ryan/Set Lecture Path", \
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
        "<Toolbox>/Xtns/Languages/Ryan/New _Quiz Solution Page",
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
        "<Toolbox>/Xtns/Languages/Ryan/_Red Brush",
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
        "<Toolbox>/Xtns/Languages/Ryan/_Black Brush",
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
        "<Toolbox>/Xtns/Languages/Ryan/_Blue Brush",
        "",#RGB*, GRAY*",
        [],
        [],
        blue_brush)

def find_if_open(imgname):
    Pdb.set_trace()
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
        "<Toolbox>/Xtns/Languages/Ryan/_List Images",
        "",#RGB*, GRAY*",
        [],
        [],
        list_images)


def green_brush():
    pdb.gimp_context_set_foreground((0,255,0))
    
    
register(
        "green_brush",
        "Set brush foreground to green",
        "Set brush foreground to green",
        "Ryan Krauss",
        "Ryan Krauss",
        "2009",
        "<Toolbox>/Xtns/Languages/Ryan/_Green Brush",
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

    
def save_as(initialdir=None, initialfile=None):
    filename = tkFileDialog.asksaveasfilename(initialdir=initialdir, \
                                              initialfile=initialfile, \
                                              filetypes=filetypes)
    return filename


def save_as_jpg(initialdir=None, initialfile=None):
    filename = tkFileDialog.asksaveasfilename(initialdir=initialdir, \
                                              initialfile=initialfile, \
                                              filetypes=jpgtypes)
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
        "<Image>/Filters/Ryan/_Save Grid Image",
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
        "<Image>/Filters/Ryan/_Save Grid Image 2",
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
        "<Image>/Filters/Ryan/_Open Next Image",
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
        "<Image>/Filters/Ryan/_Open Previous Image",
        "RGB*, GRAY*",
        [],
        [],
        open_previous)


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
        "<Image>/Filters/Ryan/Save _Quiz Image",
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
    gimp.Display(img)
    gimp.displays_flush()
    time.sleep(0.5)
    move_resize_window()#timg, tdrawable)

        
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
  	"<Toolbox>/Xtns/Languages/Ryan/_Open Grid Image", "",
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

##---------------------##
#
# This must be last
#
##---------------------##
main()

