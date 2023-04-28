#!/usr/bin/env python3
import os
import sys
import datetime

if __name__ == "__main__":
    Folder = sys.argv[1]
    if Folder == "":
        print("checkdates.py [folder]")
        quit

    for root, dirs, files in os.walk(Folder):
        Elements = root.split("/")
        if len(Elements[-1]) == 8:
            Date = Elements[-1]
            Year = int(Date[:4])
            Month = int(Date[4:6])
            Day = int(Date[-2:])
            try:
                NewDate = datetime.datetime(Year,Month,Day)
            except ValueError:
                print(f'Invalid date: {Date}')