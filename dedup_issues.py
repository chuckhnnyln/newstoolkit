#!/usr/bin/env python3
import os
import requests
import xmltodict
import sys
#import subprocess
import shutil

def VeridianIssues(XMLSource):
    # Retrieve Issue list from Veridian for a title.
    VeridianList = []
    resp = requests.get(XMLSource)
    VeridData = xmltodict.parse(resp.content)
    try:
        Dates = VeridData["VeridianXMLResponse"]["DatesResponse"]["ArrayOfDate"]["Date"]
        for item in Dates:
            VeridianList.append(item['#text'])
    except:
        print('Error: Check to see if title exists')
    return VeridianList

def BuildDirList(SourceFolder):
    DirList = []
    for root, dirs, files in os.walk(SourceFolder):
        for item in dirs:
            DirList.append(item)
    return DirList
    
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("dedup_issues.py [directory]")
        quit()

    if not os.path.exists(sys.argv[1]):
        print('Directory not found.')
        print("dedup_issues.py [directory]")
        quit()

    PubCode = sys.argv[1]

    XMLSource = 'https://nyshistoricnewspapers.org/?a=cl&cl=CL2&f=XML&sp=' + PubCode
    VeridianList = VeridianIssues(XMLSource)
    DateList = BuildDirList(PubCode)

    for Date in DateList:
        for CheckDate in VeridianList:
            if Date == CheckDate:
                DestName = f'{PubCode}_dedup'
                if not os.path.exists(DestName): os.mkdir(DestName)
                print(f'{Date} already posted.')

                shutil.move(os.path.join(PubCode,Date),os.path.join(DestName,Date))
                continue