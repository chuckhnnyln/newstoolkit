#!/usr/bin/env python3
from distutils.log import Log
import sys
import os
import shutil

def ReadLog(LogFile,FailCode):
    f = open(LogFile, 'r')
    LogContents = f.read().splitlines()
    TargetFiles = []
    for line in LogContents:
        if FailCode in line:
            Comma = line.find(',')
            TargetFiles.append(line[:Comma])
    f.close()
    return TargetFiles

def MakeCell(LogFile,FailCode):
    SansPrefix = LogFile[LogFile.find('_') + 1:]
    SansSuffix = SansPrefix[:SansPrefix.find('_')]
    CellName = "cell-" + FailCode + "_" + SansSuffix
    if not os.path.isdir(CellName):
        os.mkdir(CellName)
    return CellName    

def CopyToCell(TargetFiles, CellName):
    for file in TargetFiles:
        OriginPath = file[file.find('/') + 1:]
        os.makedirs(os.path.dirname(os.path.join(CellName,OriginPath)), exist_ok=True)
        shutil.copy2(file, os.path.join(CellName,OriginPath))

if __name__ == "__main__":

    if len(sys.argv)<3:
        print("Usage: bailiff [fail code] [logfile]")
        sys.exit()
    
    FailCode = sys.argv[1]
    LogFile = sys.argv[2]
    CodeList = ['read', 'multipage', 'layered', 'dimension', 'rotate/2up', 'ocr', 'filesize', 'datename']

    if FailCode not in CodeList:
        print("Not fail code!")
        sys.exit()

    if not os.path.exists(LogFile):
        print("Log file not found!")
        sys.exit()
    
    CellName = MakeCell(LogFile,FailCode)
    TargetFiles = ReadLog(LogFile,FailCode)
    CopyToCell(TargetFiles,CellName)
