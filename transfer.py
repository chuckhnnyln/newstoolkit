#!/usr/bin/env python3
import subprocess
import sys

def RemoteDir(Source,RemotePath):
    global RcloneConfig
    DirListing = []
    Command = ['/usr/local/bin/rclone', 'lsd', 
        '--config', RcloneConfig,
        Source + ':' + RemotePath]
    result = subprocess.run(Command, capture_output=True, text=True)
    ResultList = result.stdout.split("\n")
    #Cleaning the stdout to something usable
    for item in ResultList:
        if len(item) > 0:
            columns = item.split("        -1 ")
            DirListing.append(columns[2])
    return DirListing

def CopyDir(Source,SourcePath,LocalDestPath):
        global RcloneConfig
        Command = ['/usr/local/bin/rclone', 'copy', 
        '--config', RcloneConfig,
        '--include', '*.tif',
        Source + ":" + SourcePath, 
        LocalDestPath]
        result = subprocess.run(Command, capture_output=True, text=True)

if __name__ == "__main__":
    Source = 'aleister'
    RemotePath = 'DataDrive/_staging'
    LocalPath = '/Users/chuck/Desktop'
    RcloneConfig = '/Users/chuck/.config/rclone/rclone.conf'
    ShipmentListing = []

    if len(sys.argv) > 1:
        ShipmentListing.append(sys.argv[1])
    else:
        #Get the list of shipments available
        ShipmentListing = RemoteDir(Source,RemotePath)

    #Do each shipment
    for shipment in ShipmentListing:
        print(f'Starting {shipment}...')
        SourceShipmentPath = RemotePath + "/" + shipment
        BoxList = RemoteDir(Source,SourceShipmentPath)
        #Do each box inside the shipment
        for box in BoxList:
             BoxSourcePath = SourceShipmentPath + "/" + box + "/" + "frames"
             BoxLocalPath = LocalPath + "/" + shipment + "/" + box
             CopyDir(Source,BoxSourcePath,BoxLocalPath)