#!/usr/bin/env python3
import os
import sys

def Clean(root_dir):
    junk = ('._', '.DS_', 'Thumbs.db')
    junk_count = 0

    for root, dirs, files in os.walk(root_dir):
        for name in files:
            for search in junk:
                if search in name:
                    junk_count = junk_count+1
                    if os.path.exists(os.path.join(root,name)): os.remove(os.path.join(root,name))

if __name__ == "__main__":

    if len(sys.argv)==1:
        print("No directory specified!")
        quit()

    size = 0
    Folder = sys.argv[1]
    Clean(Folder)
    
    for path, dirs, files in os.walk(Folder):
        for f in files:
            fp = os.path.join(path, f)
            size += os.stat(fp).st_size
    
    MBsize = round(size / 1000000,1)
    GBsize = round(MBsize / 1000000,1)

    if MBsize > float(1000):
        print(f'\n{Folder} = {MBsize} MB')
    else:
        print(f'\n{Folder} = {GBsize} GB')