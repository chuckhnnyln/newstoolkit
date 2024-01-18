#!/usr/bin/env python3
# scans folder, and places images in pairs together
# requires imagemagick installed 

import os
import sys
import subprocess

def Clean(root_dir):
    junk = ('._', '.DS_', 'Thumbs.db')

    for root, dirs, files in os.walk(root_dir):
        for name in files:
            for search in junk:
                if search in name:
                    if os.path.exists(os.path.join(root,name)): os.remove(os.path.join(root,name))

def FindJpgs(TargetFolder):
    FileList = []
    Extension = 'jpg'
    for root, dirs, files in os.walk(TargetFolder):
        for name in files:
            if name.endswith(Extension):
                FileList.append(os.path.join(root,name))
    FileList.sort()
    return FileList

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        print('Please specify a folder with images.')
        exit()
    
    TargetFolder = sys.argv[1]

    if not os.path.exists(TargetFolder):
        print('Target folder not found!')
        exit()

    OutputFolder  = TargetFolder + '_output'
    if not os.path.exists(OutputFolder): os.mkdir(OutputFolder)
    
    FileList = FindJpgs(TargetFolder)

    for index in range(0,len(FileList),2):
        Result = FileList[index].replace(TargetFolder,OutputFolder)
        Command = ['convert', FileList[index], FileList[index+1], '+append', Result]
        result = subprocess.run(Command, capture_output=True, text=True)