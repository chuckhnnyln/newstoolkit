#!/usr/bin/env python3
import sys
import os
from subprocess import call
from multiprocessing.dummy import Pool as ThreadPool

def FindTargets(Folder):
    TargetFiles = []
    for root, dirs, files in os.walk(Folder):
        for name in files:
            if name.endswith('jpg'):
                TargetFiles.append(os.path.join(root,name))
    TargetFiles.sort()
    return TargetFiles


def OcrThePdf(Target):
    RootPath = '/home/rose/Staging/FromProduction/nnyln-second-quarter-2022'
    FinalPath = os.path.join(RootPath, Target)
    Command = "ocrmypdf --clean --force-ocr --output-type pdf --optimize 0 --fast-web-view 0 '" + FinalPath + "' '" +  FinalPath + "'"
    os.system(Command)

if __name__ == "__main__":

    if len(sys.argv)<2:
        print("Usage: ocr-directory-jpg [folder]")
        sys.exit()
    
    #FailCode = 'ocr'
    Folder = sys.argv[1]

    if not os.path.exists(Folder):
        print("Folder not found!")
        sys.exit()

    TargetFiles = FindTargets(Folder)
    
    #pool = ThreadPool(3)
    #pool.map(OcrThePdf, TargetFiles)
    #pool.close()
    #pool.join()
