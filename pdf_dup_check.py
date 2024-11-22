#!/usr/bin/env python3
# Chuck Henry 2024
# Requires Poppler and pdf2image installed, written on MacOS
# Creates a tif of each PDF file

import os
import sys
from pdf2image import convert_from_path
from PIL import Image
import imagehash
import shutil
Image.MAX_IMAGE_PIXELS = 1000000000

def Display(List):
    for item in List:
        print(item)

def BuildFolderList(SourceFolder):
    FolderList = []
    for root, dirs, files in os.walk(SourceFolder):
        for item in files:
            if 'pdf' in item or 'PDF' in item:
                FolderList.append(root)
    if len(FolderList) == 0:
        print(f'No pdfs found in source folder {SourceFolder}!')
        sys.exit()
    CleanFolderList = list(dict.fromkeys(FolderList)) #Remove duplicate entries
    CleanFolderList.sort()
    return CleanFolderList

def BuildFileList(SourceFolder):
    #Searches the given folder for real PDFs to be worked on
    FileList = []
    for root, dirs, files in os.walk(SourceFolder):
        for item in files:
            if '._' in item:
                os.remove(os.path.join(root,item))
                pass
            if 'pdf' in item or 'PDF' in item:
                FileList.append(os.path.join(root,item))
    if len(FileList) == 0:
        print(f'No pdfs found in source folder {SourceFolder}!')
        sys.exit()
    FileList.sort()
    return FileList

def FindDups(PdfList):
    global BitDiff
    PdfList.sort()
    FileCount = len(PdfList)
    FirstImage = ''
    DupPdfs = []
    for x in range(FileCount-1):
        if FirstImage == '':
            FirstImage = convert_from_path(PdfList[x])
        SecondImage = convert_from_path(PdfList[x+1])
        FirstHash = imagehash.phash(FirstImage[0])
        SecondHash = imagehash.phash(SecondImage[0])
        Diff = FirstHash - SecondHash
        if Diff <= BitDiff:
            print(f'{PdfList[x+1]} is a duplicate of {PdfList[x]}. Diff: {Diff}')
            DupPdfs.append(PdfList[x+1])
        FirstImage = SecondImage
    if len(DupPdfs) != 0:
        MoveDups(DupPdfs)

def MoveDups(DupPdfs):
    for File in DupPdfs:
        OldFolderName = File.split("/")[0]
        NewFolderName = OldFolderName + '_dups'
        Destination = File.replace(OldFolderName,NewFolderName)
        DestPath = os.path.dirname(Destination)
        if not os.path.exists(DestPath):
            os.makedirs(DestPath)
        shutil.move(File, Destination)

if __name__ == '__main__':

    BitDiff = 15

    if len(sys.argv) == 1:
        print("No directory or extension specified!")
        print("pdf_dup_check.py [directory]")
        print("IE: pdf_dup_check.py MyFolder")
        quit()

    RootDir = sys.argv[1]

    # Find target files
    FolderList=[]
    FolderList = BuildFolderList(RootDir)

    for Folder in FolderList:
        Diffs = []
        PdfList = BuildFileList(Folder)
        print(Folder)
        Dups = FindDups(PdfList)
