#!/usr/bin/env python3
import os
import sys
from PIL import Image
#from PyPDF2 import PdfReader, PdfWriter

def FindFiles(SourceDirectory,Ext):
    FileList = []
    for root, dirs, files in os.walk(SourceDirectory):
        for item in files:
            if item.endswith(Ext):
                FileList.append(item)
    return FileList

def Clean(root_dir):
    junk = ('._', '.DS_', 'Thumbs.db')
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            for search in junk:
                if search in name:
                    if os.path.exists(os.path.join(root,name)): os.remove(os.path.join(root,name))

def SplitTifs(SourceDirectory, FileList, TargetDirectory):
    TotalFiles = len(FileList)
    FileCount = 0
    for file in FileList:
        SourcePath = os.path.join(SourceDirectory,file)

        tif = Image.open(SourcePath)
        FileCount = FileCount + 1

        TiffPages = tif.n_frames

        print(f'({FileCount}/{TotalFiles}) {file}: {TiffPages} pages')

        FixedName = file.split('.')

        for i in range(TiffPages):
            pagenum = i + 1
            OutputFilename = f'{TargetDirectory}/{FixedName[0]}_{pagenum:0>3}.tif'
            try:
                tif.seek(i)
                tif.save(OutputFilename)
            except EOFError:
                continue

if __name__ == "__main__":
    SourceDirectory = sys.argv[1]
    TargetDirectory = SourceDirectory + "_split"

    if not os.path.exists(TargetDirectory):
        os.mkdir(TargetDirectory)
    
    Clean(SourceDirectory)
    FileList = FindFiles(SourceDirectory,'tif')
    SplitTifs(SourceDirectory,FileList,TargetDirectory)
