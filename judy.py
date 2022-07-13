#!/usr/bin/env python3
import os
import sys
import fitz
import re

def BuildFileList(SourceFolder):
    #Searches the given folder for real PDFs to be worked on
    FileList = []
    for root, dirs, files in os.walk(SourceFolder):
        for item in files:
            if '._' in item:
                os.remove(os.path.join(root,item))
                pass
            if 'pdf' in item or 'PDF' in item:
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
        Pdf = fitz.open(File)
    except:
        Results['read'] = 'fail'
        Results['multipage'] = 'untested'
        Results['layered'] = 'untested'
        Results['dimension'] = 'untested'
        Results['rotate/2up'] = 'untested'
        Results['ocr'] = 'untested'
        Results['filesize'] = 'untested'
        Results['datename'] = 'untested'
        return Results
    
    Results['read'] = 'pass'

    #Multipage Test
    Pages = len(Pdf)
    if Pages > 1:
        Results['multipage'] = 'fail'
    else:
        Results['multipage'] = 'pass'

    #Multiimage / layered Test
    Page = Pdf[0]
    ImageList = Page.get_images()
    if len(ImageList) > 1:
        Results['layered'] = 'fail'
    else:
        Results['layered'] = 'pass'     

    #Dimensions Test
    FirstImage = ImageList[0]
    Width = FirstImage[2]
    Height = FirstImage[3]
    if Width > 5000:
        Results['dimension'] = 'fail'
    else:
        Results['dimension'] = 'pass'    

    #Rotation Test
    if Width > Height:
        Results['rotate/2up'] = 'fail'
    else:
        Results['rotate/2up'] = 'pass'            

    #OCR Test
    Text = Page.get_text('words')
    if len(Text) < 1:
        Results['ocr'] = 'fail'
    else:
        Results['ocr'] = 'pass' 

    Pdf.close()

    #File size test
    FileSize = os.path.getsize(File)
    if FileSize > 5000000: #In bytes, 5MB
        Results['filesize'] = 'fail'
    else:
        Results['filesize'] = 'pass'

    #Date Name check
    FileName = os.path.basename(File)
    DateListed1 = re.findall('(?<!\d)\d{8}(?!\d)',FileName)
    DateListed2 = re.findall('\d{4}-[0-1][0-9]-[0-3][0-9]',FileName)
    if len(DateListed1) == 0 and len(DateListed2) == 0:
        Results['datename'] = 'fail'
    else:
        Results['datename'] = 'pass'
    return Results

def PrettyOutput(FailTally, FileList):
    #Prints the results for the user
    FileCount = len(FileList)
    print(f'Judy evaluated {FileCount} pdfs...')
    for key in FailTally:
        print(f'{key}: {FailTally[key]} fails')

def MainLoop(FileList, SourceFolder):
    #This does most of the work
    LogName = 'judy_' + SourceFolder + '_log.txt'
    FailList = []
    FailTally = {'read': 0, 'multipage': 0, 'layered': 0, 'dimension': 0, 'rotate/2up': 0, 'ocr': 0, 'filesize': 0, 'datename': 0}
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
        print("Usage: judy [folder]")
        sys.exit()
    
    SourceFolder = sys.argv[1]

    if not os.path.exists(SourceFolder):
        print("Source folder not found!")
        sys.exit()

    print('Discovering files...')
    FileList = BuildFileList(SourceFolder)
    print('Evaluating files...')
    MainLoop(FileList, SourceFolder)