#!/usr/bin/env python3
import os
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

def BuildFileList(SourceFolder):
    #Searches the given folder for real tifs to be worked on
    FileList = []
    for root, dirs, files in os.walk(SourceFolder):
        for item in files:
            if '._' in item:
                os.remove(os.path.join(root,item))
                pass
            if 'tif' in item or 'TIF' in item or 'jpg' in item:
                FileList.append(os.path.join(root,item))
    if len(FileList) == 0:
        print(f'No pdfs found in source folder {SourceFolder}!')
        sys.exit()
    return FileList

def DisplayIt(List):
    for item in List:
        print(item)

def EvalFile(File):
    #This evaluates each file and returns the findings.
    Results = {}
    
    #File 'open' test
    try: 
        Target = Image.open(File)
    except:
        Results['read'] = 'fail'
        Results['rotate/2up'] = 'untested'
        return Results
    
    Results['read'] = 'pass'

    #Rotation Test
    Width, Height = Target.size
    if Width > Height:
        Results['rotate/2up'] = 'fail'
    else:
        Results['rotate/2up'] = 'pass'            

    Target.close()

    return Results

def PrettyOutput(FailTally, FileList):
    #Prints the results for the user
    FileCount = len(FileList)
    print(f'Judy evaluated {FileCount} pdfs...')
    for key in FailTally:
        print(f'{key}: {FailTally[key]} fails')

def MainLoop(FileList, SourceFolder):
    #This does most of the work
    LogName = 'india-check_' + SourceFolder + '_log.txt'
    FailList = []
    FailTally = {'read': 0, 'rotate/2up': 0}
    for File in FileList:
        Results = EvalFile(File) #Evaluate each file
        Message = FindFails(File, Results) #Create a message detailing results
        FailList.append(Message) #Create log list
        FailTally = TallyFails(Results, FailTally) #Tally up those failures
    FailList.sort()
    LogIt(LogName, FailList) #write the log file
    PrettyOutput(FailTally,FileList) #let the user know what the results were

def LogIt(LogName, List):
    #Yup, logs it to the log file.
    if os.path.exists(LogName):
        os.remove(LogName)
    File = open(LogName, 'a')
    for item in List:
        File.write(item + '\n')
    File.close()

def FindFails(File, Results):
    #Searches through the results on a file and outputs the log message
    Fails = []
    for key, val in Results.items():
        if val == 'fail':
            Fails.append(key)
    Message = File
    for item in Fails:
        Message = Message + ", " + item
    return Message

def TallyFails(Results, FailTally):
    #This adds the results from a single results to the running tally
    for key, val in Results.items():
        if val == 'fail':
            KeyValue = FailTally.get(key)
            KeyValue = KeyValue + 1
            Update = {key: KeyValue}
            FailTally.update(Update)
    return FailTally

if __name__ == "__main__":

    if len(sys.argv)<2:
        print("Usage: india_check [folder]")
        sys.exit()
    
    SourceFolder = sys.argv[1]

    if not os.path.exists(SourceFolder):
        print("Source folder not found!")
        sys.exit()

    print('Discovering files...')
    FileList = BuildFileList(SourceFolder)
    print('Evaluating files...')
    MainLoop(FileList, SourceFolder)