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
    Command = "ocrmypdf --clean --force-ocr --output-type pdf --optimize 0 --fast-web-view 0 '" + Target + "' '" +  FinalPath + "'"
    print(Command)
    #os.system(Command)

if __name__ == "__main__":

    if len(sys.argv)<3:
        print("Usage: ocr-directory [ext] [folder]")
        sys.exit()
    
    Folder = sys.argv[2]
    Extension = sys.argv[1]

    if not os.path.exists(Folder):
        print("Folder not found!")
        sys.exit()

    TargetFiles = FindTargets(Folder,Extension)
    
    pool = ThreadPool(3)
    pool.map(OcrThePdf, TargetFiles)
    pool.close()
    pool.join()