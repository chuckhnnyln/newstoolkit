#!/usr/bin/env python3
import os
import sys

def count(root_dir,extension):
    search = []
    file_count = 0

    for root, dirs, files in os.walk(root_dir):
        for name in files:
            if name.endswith(extension):
                if len(search) > 0:
                    if search in name:
                        file_count = file_count+1
                else:
                    file_count = file_count+1
    return file_count

if __name__ == "__main__":
    RootFolder = sys.argv[1]

    Duplicates = RootFolder + "_duplicates"
    Unpacked = RootFolder + "_unpacked"

    if not os.path.exists(Duplicates):
        print(f'{Duplicates} not found!')
        exit()
    
    if not os.path.exists(Unpacked):
        print(f'{Unpacked} not found!')
        exit()   
    
    Targets = []
    Dups = os.scandir(Duplicates)
    for item in Dups:
        SubDups = os.scandir(os.path.join(Duplicates,item.name))
        for subitem in SubDups:
            Targets.append(os.path.join(Duplicates,item.name,subitem.name))

    for entry in Targets:
        DupFileCount = count(entry,"pdf")
        Folder = entry.split("/")
        Dash = Folder[1].find('-')
        Slug = Folder[1][0:Dash]
        OriginalEntry = os.path.join(Unpacked,Slug,Folder[2])
        OrigFileCount = count(OriginalEntry,"pdf")

        print(f'{entry} :: {DupFileCount}')
        print(f'{OriginalEntry} :: {OrigFileCount}')
        if DupFileCount == OrigFileCount:
            print("Match!")
        else:
            print("Mismatch!")