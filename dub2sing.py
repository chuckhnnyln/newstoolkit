#!/usr/bin/env python3

#Companion app to singdub.py
#This takes singdub's output and dynamically splits the images.

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


def MainLoop(SourceFolder, FileList, Gutter):
    FileList.sort()
    for file in FileList:
        path = file.split("/")
        filename = path[2]
        print(f'Evaluating {filename}')
        im = Image.open(file)
        width, height = im.size
        top = 0
        bottom = height
        for frame in ('_1','_2'):
            outfile = os.path.join(path[0],'singles',filename.replace('.',frame + '.'))
            if frame == '_1':
                Percent = .50 + (int(Gutter) / 100)
                left = 0
                right = round(width * Percent)
            if frame == '_2':
                Percent = .50 - (int(Gutter) / 100)
                left = round(width * Percent)
                right = width
            viewport = (left, top, right, bottom)
            imc = im.crop(viewport)
            imc.save(outfile)


if __name__ == "__main__":

    if len(sys.argv)<2:
        print("Usage: dub2sing [folder] [Gutter%]")
        print("[Gutter%] is optional, defaults to 5")
        sys.exit()
    
    SourceFolder = sys.argv[1]
    Gutter = 5
    if len(sys.argv) == 3:
        Gutter = sys.argv[2]

    SourceDoubles = os.path.join(SourceFolder,'doubles')
    SourceSingles = os.path.join(SourceFolder,'singles')

    if not os.path.exists(SourceDoubles):
        print("Source folder not found!")
        sys.exit()
    
    if not os.path.exists(SourceSingles):
        os.mkdir(SourceSingles)

    print('Discovering files...')
    FileList = BuildFileList(SourceDoubles)
    MainLoop(SourceDoubles,FileList,Gutter)

