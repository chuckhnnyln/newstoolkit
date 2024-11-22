#!/usr/bin/env python3
import sys
import os
from subprocess import call
from multiprocessing.dummy import Pool as ThreadPool

def FindTargets(Folder,Extension):
    TargetFiles = []
    for root, dirs, files in os.walk(Folder):
        for name in files:
            if name.endswith(Extension):
                TargetFiles.append(os.path.join(root,name))
    TargetFiles.sort()
    return TargetFiles

def OcrThePdf(Target):
    FilePath, Ext = os.path.splitext(Target)
    FinalPath = FilePath + '.pdf'
    if not os.path.exists(FinalPath):
        print(f'Starting {Target}')
        Command = "ocrmypdf --clean --image-dpi 300 --output-type pdf --optimize 0 --fast-web-view 0 '" + Target + "' '" +  FinalPath + "'"
        #Command = "ocrmypdf --clean --force-ocr --image-dpi 300 --output-type pdf --optimize 0 --fast-web-view 0 '" + Target + "' '" +  FinalPath + "'"
        #print(Command)
        os.system(Command)
    else:
        print(f'Already done. Skipping {FinalPath}')

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

if __name__ == "__main__":

    if len(sys.argv)<3:
        print("Usage: ocr-directory [ext] [folder]")
        sys.exit()
    
    Folder = sys.argv[2]
    Extension = sys.argv[1]

    if not os.path.exists(Folder):
        print("Folder not found!")
        sys.exit()

    Clean(Folder)

    TargetFiles = FindTargets(Folder,Extension)
    
    pool = ThreadPool(3)
    pool.map(OcrThePdf, TargetFiles)
    pool.close()
    pool.join()