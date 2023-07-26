#!/usr/bin/env python3
# zipper.py mainfile col# zipperfile col#
import sys
import os
import csv

def ReadCsv(File):
    Lines =[]
    with open(File) as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in filereader:
            Lines.append(row)
    return Lines

def WriteCsv(File, Contents):
    with open(File, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        for row in Contents:
            filewriter.writerow(row)

if __name__ == "__main__":

    if len(sys.argv) < 5:
        print('Not enough arguments!')
        print("zipper.py mainfile col# zipperfile col#")
        exit()

    MainFile = sys.argv[1]
    MainColumn = sys.argv[2]
    ZipperFile = sys.argv[3]
    ZipperColumn = sys.argv[4]

    MainColumn = int(MainColumn) - 1
    ZipperColumn = int(ZipperColumn) - 1

    if not os.path.exists(MainFile):
        print(f"Main File {MainFile} doesn't exist.")
        exit()

    if not os.path.exists(ZipperFile):
        print(f"Zipper File {ZipperFile} doesn't exist.")
        exit()

    MainContents = ReadCsv(MainFile)
    ZipperContents = ReadCsv(ZipperFile)

    ResultContents = []
    for item in MainContents:
        for line in ZipperContents:
            if item[MainColumn] == line[ZipperColumn]:
                count = 0
                for element in line:
                    if count != ZipperColumn:
                        item.append(element)
                    count += 1
        ResultContents.append(item)
    
    WriteCsv('output.csv', ResultContents)