#!/usr/bin/env python3
import sys
import os
import subprocess

def getlist(path):
    TitleList = []
    for f in os.listdir(path):
        if f != path and os.path.isdir(os.path.join(path,f)):
            TitleList.append(os.path.join(path,f))
    TitleList.sort()
    return TitleList

if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        print('cloneatnine.py [folder]')
    
    if not os.path.exists(sys.argv[1]):
        print('Batch not found!')
    
    Folder = sys.argv[1]
    BatchList = []
    BatchList = getlist(Folder)

    for BatchPath in BatchList:
        BatchName = BatchPath.split('/')[1]
        print(f'Cloning {BatchName}')
        Command = ['/usr/bin/rclone', 'copy', 
            '--config', '/home/rose/.config/rclone/rclone.conf',
            '--log-level', 'INFO',
            '--log-file', BatchPath + '_reclone_log.txt',
            BatchPath, 
            'veridian:upload.2977.dlconsulting.com/FromNNYLN/' + BatchName]
        result = subprocess.run(Command, capture_output=True, text=True)
    print('Finished.')
