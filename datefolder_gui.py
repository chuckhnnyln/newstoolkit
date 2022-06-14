#!/usr/bin/env python3
import os
import PySimpleGUI as sg
import sys
import queue
import threading


#GUI Global Settings
sg.theme('BlueMono')
TitleFont = ('Arial', 14, 'bold')
Font = ('Arial', 12, 'normal')
Pad = (10,10)
TitleVersion = 'DateFolder V1'

def GUIchooseTarget ():
    global TitleFont, Font, Pad, TitleVersion
    ChooseTargetLayout = [  [sg.Text('Please choose target folder.')],
                            [sg.Input(size = (25,1), key = '_FILEPATH_'), sg.FolderBrowse(button_text = 'Browse', enable_events = True)],
                            [sg.Text('What file extension? (Case sensitive!)')],
                            [sg.Input(size = (5,1), default_text= 'pdf', key = '_EXT_')],
                            [sg.Button('Next', pad = (Pad)), sg.Button('Quit', pad = (Pad))]    ]
    ChooserWindow = sg.Window(TitleVersion, ChooseTargetLayout, font=(Font))
    while True:
        event, values = ChooserWindow.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            sys.exit()
        if event == '_FILEPATH_':
            ChooserWindow['_FILEPATH_'].update(values['Browse'])
        if event == 'Next':
            if values['_FILEPATH_'] != '' and values['_EXT_'] != '':
                ChooserWindow.close()
                return values['_FILEPATH_'], values['_EXT_']

def ScanForFiles (RootDir, Extension):
    FileList = []
    for root, dirs, files in os.walk(RootDir):
        for item in files:
            print(item)
            if '._' in item:
                os.remove(os.path.join(root,item))
                continue
            if Extension in item:
                FileList.append(os.path.join(root,item))
    if FileList:
        return FileList
    else:
        print('Found no files')
        sys.exit()

def GUIFindDate (FileList):
    global TitleFont, Font, Pad, TitleVersion
    FolderName = ''
    ExampleFileName = os.path.basename(FileList[0])
    ExampleLength = len(ExampleFileName)
    MidPoint = round(ExampleLength / 2)
    ModeList = ['YYYYMMDD', 'YYYY-MM-DD']
    FindDateLayout = [  [sg.Text('Example filename:'), sg.Text(ExampleFileName, font = TitleFont)],
                        [sg.Text('Select first character of date:')],
                        [sg.Slider(range = (1,ExampleLength - 11), resolution = 1, tick_interval = 5, orientation = 'h', enable_events = True, size=(50,10), default_value = MidPoint, key = '_SLIDER_')],
                        [sg.Text('Example folder name:'), sg.Text(text = '', font = TitleFont, key = '_FOLDERNAME_')],
                        [sg.Text('Mode:'), sg.Listbox(ModeList, default_values = 'YYYYMMDD', select_mode = 'LISTBOX_SELECT_MODE_SINGLE', size = (15,3), no_scrollbar = True, key = '_MODE_')],
                        [sg.Button('Next', pad = (Pad)), sg.Button('Quit', pad = (Pad))]]
    FindDateWindow = sg.Window(TitleVersion, FindDateLayout, font=(Font))
    while True:
        event, values = FindDateWindow.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            sys.exit()
        if event == '_SLIDER_' or event == '_MODE_':
            StartChar = int(values['_SLIDER_'] - 1)
            Mode = values['_MODE_']
            Mode = Mode[0]
            if Mode == 'YYYYMMDD':
                EndChar = StartChar + 8
                FolderName = ExampleFileName[StartChar:EndChar]
                FindDateWindow['_FOLDERNAME_'].update(FolderName)
                FindDateWindow['_SLIDER_'].update(range = (1,ExampleLength - 11))
            if Mode == 'YYYY-MM-DD':
                EndChar = StartChar + 10
                FolderName = ExampleFileName[StartChar:EndChar]
                FolderName = FolderName.replace('-','')
                FindDateWindow['_FOLDERNAME_'].update(FolderName)
                FindDateWindow['_SLIDER_'].update(range = (1,ExampleLength - 13))
            if Mode == 'YYYYMMDDEEE': #Not selectable... need more information to program.
                EndChar = StartChar + 11
                FolderName = ExampleFileName[StartChar:EndChar]
                FindDateWindow['_FOLDERNAME_'].update(FolderName)
        if event == 'Next':
            if FolderName != '':
                FindDateWindow.close()
                return StartChar, EndChar

def MoveTheFiles (WorkID, GUIqueue):
    global FileList, StartChar, EndChar
    Progress = 0
    GUIqueue.put(Progress)
    for item in FileList:
        FileName = os.path.basename(item)
        FolderName = FileName[StartChar:EndChar]
        FolderName = FolderName.replace('-','')
        PathName = os.path.dirname(item)
        if os.path.exists(os.path.join(PathName,FolderName)):
            os.rename(os.path.join(item), os.path.join(PathName, FolderName, FileName))
        else:
            os.mkdir(os.path.join(PathName,FolderName))
            os.rename(os.path.join(item), os.path.join(PathName, FolderName, FileName))
        Progress = Progress + 1
        GUIqueue.put(Progress)
    GUIqueue.put('done')

def GUIpleaseWait (FileList, GUIqueue):
    global TitleFont, Font, TitleVersion
    NumFiles = len(FileList)
    DisplayMessage = "Please wait. This will take some time. There are " + str(NumFiles) + " files to process."
    PleaseWaitLayout = [    [sg.Text(DisplayMessage)],
                            [sg.ProgressBar(100, orientation = "h",\
                            size = (50,20), border_width = 0,\
                            key='-PROGRESS_BAR-', bar_color=("white","#7186C7"))],
                            [sg.Button('Cancel')]  ]
    PleaseWaitWindow = sg.Window(TitleVersion, PleaseWaitLayout, font=(Font))
    Message = 0
    while True:
        event, values = PleaseWaitWindow.Read(timeout=25)
        if event == sg.WIN_CLOSED or event == 'Cancel' or Message == 'done':
            PleaseWaitWindow.close()
            sys.exit()
        try:
            Message = GUIqueue.get_nowait()
        except queue.Empty:
            Message = 0
        else:
            if Message != 'done':
                PercentComplete = int(round((int(Message)) * 100 / NumFiles))
                #print(f'{Message} : {PercentComplete}')
                PleaseWaitWindow['-PROGRESS_BAR-'].update(PercentComplete)

if __name__ == "__main__":
    RootDir, Extension = GUIchooseTarget()
    FileList = ScanForFiles(RootDir, Extension)
    StartChar, EndChar = GUIFindDate(FileList)
    GUIqueue = queue.Queue()
    WorkID = 0
    ThreadID = threading.Thread(target=MoveTheFiles, args=(WorkID, GUIqueue,), daemon=True)
    ThreadID.start()
    GUIpleaseWait(FileList, GUIqueue)
    sys.exit()
