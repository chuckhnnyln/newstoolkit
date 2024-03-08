#!/usr/bin/env python3

import os
import sys
import fitz
from PIL import Image
#from subprocess import call
from multiprocessing.dummy import Pool as ThreadPool

def BuildFileList(SourceFolder, ExtensionList):
    # Returns full absolute path of target files as a list.
    FileList = []
    for root, dirs, files in os.walk(SourceFolder):
        for item in files:
            for Extension in ExtensionList:
                if item.endswith(Extension):
                    FileList.append(os.path.join(root,item))
    FileList.sort()
    return FileList

def Clean(root_dir):
    junk = ('._', '.DS_', 'Thumbs.db')
    junk_count = 0
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            for search in junk:
                if search in name:
                    junk_count = junk_count+1
                    if os.path.exists(os.path.join(root,name)): os.remove(os.path.join(root,name))
    print(f"\nRemoved {junk_count} junk files from {root_dir}.")

def ExtractImages(FileList):
    for Item in FileList:
        Pdf = fitz.open(Item)
        print(f'Working on {Item}.')
        for PageIndex in range(len(Pdf)):
            Page = Pdf[PageIndex]
            ImageList = Page.get_images()

            for ImageIndex, Img in enumerate(ImageList, start=1):
                xref = Img[0]
                pix = fitz.Pixmap(Pdf, xref)

                ItemName = Item.replace('.pdf','.tif')
                if pix.width >= 300:
                    if not os.path.exists(ItemName):
                        pix.save(ItemName)

if __name__ == '__main__':

    if len(sys.argv)==1:
        print("No directory specified!")
        quit()

    TargetDir = sys.argv[1]
    Clean(TargetDir)
    FileList = BuildFileList(TargetDir,"pdf")
    ExtractImages(FileList)

    # Pass the file list to workers to complete
    pool = ThreadPool(3)
    pool.map(ExtractImages, FileList)
    pool.close()
    pool.join()
