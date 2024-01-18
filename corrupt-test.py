#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil

def Scan(Folder):
    ErrorList = []
    for root, dirs, files in os.walk(Folder):
        for File in files:
            Path = os.path.join(root,File)
            try:
                Command = ['/usr/bin/pdfinfo', Path]
                result = subprocess.run(Command, capture_output=True, text=True)
                if result.returncode == 1:
                    print(f'Error: {Path}')
                    ErrorList.append(Path)
                else:
                    for line in map(str,result.stdout.splitlines()):
                        if line.startswith('Pages') and not line == "Pages:           1":
                            print(f'Page-Count-Error: {Path}')
                            ErrorList.append(Path)
            except:
                print(f'Read-Fail: {Path}')
                ErrorList.append(Path)
    return ErrorList

def Copy(Folder, ErrorList):
    CorruptRoot = Folder + '_corrupt'
    print("Copying corrupt files.")
    for file in ErrorList:
        outfile = file.replace(Folder,CorruptRoot)
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        shutil.copy2(file, outfile)

def Delete(Folder, ErrorList):
    print("Deleting corrupt files.")
    for file in ErrorList:
        os.remove(file)

def Output(Folder, ErrorList):
    print("Writing corrupt filelist to file.")
    FileName = Folder + "_corrupt-filelist.txt"
    if os.path.exists(FileName):
        os.remove(FileName)
    File = open(FileName, 'a')
    for item in ErrorList:
        File.write(item + '\n')
    File.close()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('corrupt-test.py [Folder] [-c]opy [-d]elete [-o]utput')
        exit()
    Folder = sys.argv[1]
    if not os.path.exists(Folder):
        print("Folder not found!")
        exit()
    Option = ""
    if len(sys.argv) > 2:
        Option = sys.argv[2]
    ErrorList = Scan(Folder)
    match Option:
        case "-c":
            Copy(Folder,ErrorList)
        case "-d":
            Delete(Folder,ErrorList)
        case "-o":
            Output(Folder,ErrorList)
        case _:
            pass
    print('Done!')
