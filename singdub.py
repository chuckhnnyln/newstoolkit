#!/usr/bin/env python3
import os
import sys
from PIL import Image
import shutil

def BuildFileList(SourceFolder):
    #Searches the given folder for real TIFs to be worked on
    FileList = []
    for root, dirs, files in os.walk(SourceFolder):
        for item in files:
            if '._' in item:
                os.remove(os.path.join(root,item))
                pass
            if 'tif' in item or 'TIF' in item:
                FileList.append(os.path.join(root,item))
    if len(FileList) == 0:
        print(f'No tifs found in source folder {SourceFolder}!')
        sys.exit()
    return FileList


def MainLoop(SourceFolder, FileList):
    FileList.sort()
    for file in FileList:
        path = file.split("/")
        filename = path[1]
        print(f'Evaluating {filename}')
        im = Image.open(file)
        width, height = im.size
        if width > height:
            print(f'{width}x{height} Double! Moved!')
            shutil.move(file,os.path.join(SourceFolder,"doubles",filename))
        else:
            print(f'{width}x{height} Single! Leaving in place.')
            #shutil.move(file,os.path.join(SourceFolder,"singles",filename))

if __name__ == "__main__":

    if len(sys.argv)<2:
        print("Usage: singdub [folder]")
        sys.exit()
    
    SourceFolder = sys.argv[1]

    if not os.path.exists(SourceFolder):
        print("Source folder not found!")
        sys.exit()

    #if not os.path.exists(os.path.join(SourceFolder,"singles")):
    #    os.mkdir(os.path.join(SourceFolder,"singles"))
    
    if not os.path.exists(os.path.join(SourceFolder,"doubles")):
        os.mkdir(os.path.join(SourceFolder,"doubles"))

    print('Discovering files...')
    FileList = BuildFileList(SourceFolder)
    MainLoop(SourceFolder,FileList)

