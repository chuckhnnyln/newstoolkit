#!/usr/bin/env python3
import sys
import os
import subprocess

if __name__ == "__main__":
    Folder = sys.argv[1]

    if not os.path.exists(Folder):
        print("Folder not found!")
        exit()
    
    for root, dirs, files in os.walk(Folder):
        for File in files:
            Path = os.path.join(root,File)
            try:
                Command = ['/usr/local/bin/pdfinfo', '-f', '1', 
                        '-l', '100000', '-box', Path]
                result = subprocess.run(Command, capture_output=True, text=True)
            except:
                print(f'Fail: {Path}')