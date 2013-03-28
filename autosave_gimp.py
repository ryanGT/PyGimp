#!/usr/bin/env python

import tempfile, os, glob
from time import *
from gimpfu import *

home_dir = os.path.expanduser('~')
autosave_dir = os.path.join(home_dir,'gimpautosave')

if not os.path.exists(autosave_dir):
    os.mkdir(autosave_dir)

def autosave_now():
    for img in gimp.image_list():
        print('img.name = ' + img.name)
        filename = os.path.join(autosave_dir, img.name)
        print('filename = ' + filename)
        pdb.gimp_xcf_save(1, img, img.active_drawable, \
                          filename, filename)

        
register("autosave_now",
         "Quickly save the current images into the gimpautosave directory",
         "Quickly save the current images into the gimpautosave directory",
         "public domain",
         "public domain",
         "2012",
         "<Toolbox>/File/Autosave Now",
         "RGB*, GRAY*",
         [],
         [],
         autosave_now)


def autosave():
    backupInterval = 30

    backupFiles = {}
    print "Autosave activated"

    while 1:
        sleep(backupInterval)

        print ctime(time())

        curImages = {}
        for k in gimp.image_list():
            curImages[k.ID] = k

        curIDs = curImages.keys()
        oldIDs = backupFiles.keys()

        newIDs = [x for x in curIDs if x not in oldIDs];
        delIDs = [x for x in oldIDs if x not in curIDs];

        # create (empty) backup files for new images
        for id in newIDs:
            #prefix = 'gimpbackup-ID' + str(id) + '-'
            #fn = tempfile.mkstemp(prefix = prefix, suffix = '.xcf')
            img = curImages[id]
            fn = os.path.join(autosave_dir, img.name)
            #os.close(fn[0])
            #backupFiles[id] = fn[1]
            backupFiles[id] = fn

        # remove closed images' backups
        for id in delIDs:
            filename = backupFiles[id]
            del(backupFiles[id])
            try:
                os.remove(filename)
            except:
                print "ERROR: ", sys.exc_info()[0]

        # backup images
        for id, filename in backupFiles.iteritems():
            img = curImages[id]
            try:
                print "saving " + img.name + '-' + str(id) + ' to ' + filename
                pdb.gimp_xcf_save(1, img, img.active_drawable, filename, 
filename)
            except:
                print "ERROR: ", sys.exc_info()[0]




register(
        "autosave",
        "Autosave hack",
        "Periodically saves all opened images to a temp directory",
        "public domain",
        "public domain",
        "2009",
        "<Toolbox>/File/Activate Autosave",
        "RGB*, GRAY*",
        [],
        [],
        autosave)

def purge_autsave_dir():
    pat = os.path.join(autosave_dir, '*.xcf')
    xcf_files = glob.glob(pat)
    for curfile in xcf_files:
        os.remove(curfile)


register("purge_autsave_dir",
         "Delete all *.xcf files in the gimpautosave directory",
         "Delete all *.xcf files in the gimpautosave directory",
         "public domain",
         "public domain",
         "2012",
         "<Toolbox>/File/Purge Autosave Directory",
         "RGB*, GRAY*",
         [],
         [],
         purge_autsave_dir)


main()
