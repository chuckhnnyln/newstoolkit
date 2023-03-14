#!/usr/bin/env python3
import os
import sys
from PyPDF2 import PdfReader, PdfWriter

def FindFiles(SourceDirectory,Ext):
    FileList = []
    for root, dirs, files in os.walk(SourceDirectory):
        for item in files:
            if item.endswith(Ext):
                FileList.append(item)
    return FileList

def Clean(root_dir):
    junk = ('._', '.DS_', 'Thumbs.db')
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            for search in junk:
                if search in name:
                    if os.path.exists(os.path.join(root,name)): os.remove(os.path.join(root,name))

def SplitPdfs(SourceDirectory, FileList, TargetDirectory):
    TotalFiles = len(FileList)
    FileCount = 0
    for file in FileList:
        SourcePath = os.path.join(SourceDirectory,file)
        pdf = PdfReader(SourcePath)
        FileCount = FileCount + 1

        print(f'({FileCount}/{TotalFiles}) {file}: {len(pdf.pages)} pages')

        for page in range(len(pdf.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf.pages[page])

            filename = file.split(".")
            pagenum = page + 1

            OutputFilename = f'{TargetDirectory}/{filename[0]}_{pagenum:0>3}.pdf'

            print(f'Saving: {OutputFilename}')

            with open(OutputFilename, 'wb') as out:
                pdf_writer.write(out)

if __name__ == "__main__":
    SourceDirectory = sys.argv[1]
    TargetDirectory = SourceDirectory + "_split"

    if not os.path.exists(TargetDirectory):
        os.mkdir(TargetDirectory)
    
    Clean(SourceDirectory)
    FileList = FindFiles(SourceDirectory,'pdf')
    SplitPdfs(SourceDirectory,FileList,TargetDirectory)
