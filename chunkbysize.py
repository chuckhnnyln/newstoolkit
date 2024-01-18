#!/usr/bin/env python3

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

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("chunkbysize.py [directory] [size in GB]")
        print("Size optional will assume 100 if not specified.")
        quit()

    if not os.path.exists(sys.argv[1]):
        print('Directory not found.')
        print("chunkbysize.py [directory] [size in GB]")
        print("Size optional will assume 100 if not specified.")
        quit()

    Folder = sys.argv[1]
    if len(sys.argv) == 3:
        MaxSizeGB = sys.argv[2]
    else:
        MaxSizeGB = 100
    
    print(f'Max chunk size set to {MaxSizeGB}GB.')
    MaxSizeB = int(MaxSizeGB) * 1000000000

    Clean(Folder)
    
    Extensions = ['pdf','PDF']
    FileList = BuildFileList(Folder,Extensions)

    Chunk = 1
    Size = 0

    for item in FileList:
        if not os.path.exists(f'{Folder}_{Chunk}'): os.mkdir(f'{Folder}_{Chunk}')
        Size += os.stat(item).st_size
        print(f'{item} : {Size} {MaxSizeB} : Chunk {Chunk}')

        #Command = ['rsync', '-R', os.path.join(root,f), f'{Folder}_{Chunk}']
        #    result = subprocess.run(Command, capture_output=True, text=True)

        if Size >= MaxSizeB:
            Chunk = Chunk + 1
            Size = 0