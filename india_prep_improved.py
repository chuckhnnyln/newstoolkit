#!/usr/bin/env python3
import sys
import os
import subprocess

if __name__ == "__main__":

    rClonePath = '/usr/local/bin/rclone' #Mac
    #rClonePath = '/usr/bin/rclone' #Fedora
    rCloneConfig = '/Users/chuck/.config/rclone/rclone.conf' #Mac
    #rCloneConfig = '/home/rose/.config/rclone/rclone.conf' #Fedora-Rose
    #rCloneConfig = '/home/beulah/.config/rclone/rclone.conf' #Fedora-Beulah

    if len(sys.argv) == 1:
        print('india_prep_improved.py [folder]')
        exit()

    BatchName = sys.argv[1]
    
    print(f'Starting scan of {BatchName}')
    Command = [rClonePath, 'ls', 
        '--config', rCloneConfig, 
        'aleister:datadrive/_staging/' + BatchName]
    #Result = subprocess.run(Command, capture_output=True, text=True)
    Result = subprocess.check_output(Command, text=True).splitlines()
    Paths =[]
    for item in Result: #Pulls remote path from rclone
        FilePath = item.split(" ")
        Paths.append(FilePath[-1])
    BoxList = [""]
    for item in Paths: #Finds the box names add to a list
        Box = item.split("/")[0]
        if not Box in BoxList:
            BoxList.append(Box)
    BoxList.remove("")
    BoxList.remove(".DS_Store")
    print("Box list built. Starting rclone.")

    for Box in BoxList:
        Command = [rClonePath, 'copy', 
                    '--config', rCloneConfig,
                    '--include', '*.tif', '--include', '*.TIF',
                    'aleister:datadrive/_staging/' + BatchName + '/'+ Box +'/frames',
                    BatchName + '/' + Box]
        Result = subprocess.run(Command, capture_output=True, text=True)
    print("Done!")