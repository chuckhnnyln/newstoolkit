#!/usr/bin/env python3
import sys
import os
import subprocess

def CloneIt(OptionList):
    #Command = ['/usr/bin/rclone', 
    #            '--config', '/home/rose/.config/rclone/rclone.conf'] #Rose
    Command = ['/usr/local/bin/rclone',
                '--config', '/Users/chuck/.config/rclone/rclone.conf'] #Mac
    for item in OptionList:
        Command.append(item)
    result = subprocess.run(Command, capture_output=True, text=True)
    #print(f'~{result.returncode}')
    return result.returncode, result.stderr

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('reclone.py [same options as you\'d use for rclone]')
    
    OptionList = []
    for option in range(1,len(sys.argv)):
        OptionList.append(sys.argv[option])
    
    AttemptCount = 0
    FailSafe = 1000
    while True:
        AttemptCount = AttemptCount + 1
        if AttemptCount == FailSafe:
            print(f'Failsafe count ({FailSafe}) reached!')
            break
        print(f'Beginning attempt {AttemptCount}.')
        Result, Error = CloneIt(OptionList)
        if Result == 0 or Result == 9:
            print(f'Result code {Result}.')
            break
        print(f'Error code {Result} returned.')
        print(Error)
    print('Done!')