#!/usr/bin/env python3
# This script strips out pre-installed crap from Fedora 38

import os
import csv
import subprocess

def ReadCsv(File):
    Lines =[]
    with open(File) as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in filereader:
            Lines.append(row)
    return Lines

if __name__ == "__main__":
    if os.geteuid() != 0:
        exit("Sudo this you fool!")
    
    if not os.path.exists('fedora_38_packages.csv'):
        exit('fedora_38_packages.csv not found!')

    RemovalList = ReadCsv('fedora_38_packages.csv')

    Command = ['dnf', 'remove', '-y']

    for Package in RemovalList:
        Command.append(Package[0])

    print('Starting uninstalls...')
    result = subprocess.run(Command, capture_output=True, text=True)

    print('Done!')