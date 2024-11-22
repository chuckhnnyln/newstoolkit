#!/usr/bin/env python3
# Chuck's Nearly Universal Python Template
# Version 1 - 20240415

import os
import csv
import sys
#from multiprocessing.dummy import Pool as ThreadPool
#import multiprocessing
#import subprocess

def BuildDirList(SourceFolder):
    DirList = []
    for root, dirs, files in os.walk(SourceFolder):
        for item in dirs:
            DirList.append(os.path.join(root,item))
    DirList.sort()
    return DirList

def BuildFileList(SourceFolder, ExtensionList):
    # Returns full absolute path of target files as a list.
    FileList = []
    for root, dirs, files in os.walk(SourceFolder):
        for item in files:
            for Extension in ExtensionList:
                if item.endswith(Extension):
                    FileList.append(os.path.join(root,item))
    FileList.sort()
    return FileList

def ReadCsv(SourcePath):
    FileContents = []
    with open(SourcePath,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            FileContents.append(row)
    csvfile.close()
    return FileContents

def WriteCsv(FileContents, SourcePath):
    # SourcePath assumes a filename last: dogs/cats/list.txt
    DestPath = os.path.dirname(SourcePath)
    if not os.path.exists(DestPath):
        os.makedirs(DestPath)

    with open(SourcePath,'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        for row in SourcePath:
            csvwriter.writerow(row)
    csvfile.close()

def Clean(root_dir):
    # Removes Windows & Mac sidecar files
    junk = ('._', '.DS_', 'Thumbs.db')
    junk_count = 0

    for root, dirs, files in os.walk(root_dir):
        for name in files:
            for search in junk:
                if search in name:
                    junk_count = junk_count + 1
                    if os.path.exists(os.path.join(root,name)): os.remove(os.path.join(root,name))

def RunIt():
    Command = ['/usr/local/bin/rclone',
                '--config', '/Users/chuck/.config/rclone/rclone.conf']
    result = subprocess.run(Command, capture_output=True, text=True)
    return result.returncode, result.stderr

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error out instructions")
        quit()

    if not os.path.exists(sys.argv[1]):
        print('Directory not found.')
        print("Error out instructions")
        quit()

    Example = sys.argv[1]

    # Multuprocessing: Pass the file list to workers to complete
    #pool = ThreadPool(multiprocessing.cpu_count() - 1)
    #pool.map(FUNCTION, FileList)
    #pool.close()
    #pool.join()
