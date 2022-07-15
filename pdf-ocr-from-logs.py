#!/usr/bin/env python3
import sys
import os
from subprocess import call
from multiprocessing.dummy import Pool as ThreadPool

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

def OcrThePdf(Target):
    Command = f'ocrmypdf --clean --force-ocr --output-type pdf --optimize 0 --fast-web-view 0 {Target} {Target}'
    os.system(Command)

if __name__ == "__main__":

    if len(sys.argv)<3:
        print("Usage: pdf-ocr-from-logs [logfile]")
        sys.exit()
    
    FailCode = 'ocr'
    LogFile = sys.argv[1]

    if not os.path.exists(LogFile):
        print("Log file not found!")
        sys.exit()

    TargetFiles = ReadLog(LogFile,'ocr')
    
    pool = ThreadPool(3)
    pool.map(OcrThePdf, TargetFiles)
    pool.close()
    pool.join()
