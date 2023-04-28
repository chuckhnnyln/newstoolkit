#!/usr/bin/env python3
import sys
import os
import shutil

def clean(root_dir):
    print("Cleaning junk files...")
    junk = ('._', '.DS_', 'Thumbs.db')

    for root, dirs, files in os.walk(root_dir):
        for name in files:
            for search in junk:
                if search in name:
                    if os.path.exists(os.path.join(root,name)): os.remove(os.path.join(root,name))

def RemoveEmptyFolders(TargetDir):
    walk = list(os.walk(TargetDir))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            os.remove(path)

if __name__ == "__main__":
    TargetFolder = sys.argv[1]

    if not os.path.exists(TargetFolder):
        print(f"{TargetFolder} doesn't exist.")
        exit()

    clean(TargetFolder)

    #Find all the issues
    FolderList = []
    for root, dirs, files in os.walk(TargetFolder):
        for item in dirs:
            if len(item) == 10:
                FolderList.append(item)
    
    FolderList.sort()

    for Issue in FolderList:
        IssueName = Issue[:8]
        Order = Issue[9:]
        
        SourceIssuePath = os.path.join(TargetFolder,Issue)
        DestIssuePath = os.path.join(TargetFolder,IssueName)
        
        if not os.path.exists(DestIssuePath):
            os.mkdir(DestIssuePath)

        for root, dir, FileList in os.walk(SourceIssuePath):
            for File in FileList:
                NewFile = File.replace("_0","_" + Order)
                if os.path.exists(os.path.join(SourceIssuePath,File)):
                    shutil.move(os.path.join(SourceIssuePath,File), os.path.join(DestIssuePath,NewFile))
                    #print(os.path.join(SourceIssuePath,File) + " " + os.path.join(DestIssuePath,NewFile))
    
    #RemoveEmptyFolders(TargetFolder)
