#!/usr/bin/env python3
import PySimpleGUI as sg
import sys

#GUI Global Settings
sg.theme('BlueMono')
TitleFont = ('Arial', 14, 'bold')
Font = ('Arial', 12, 'normal')
Pad = (10,10)

def GetFolderDialog(AppTitle):
    global TitleFont, Font, Pad
    ChooseTargetLayout = [  [sg.Text('Please choose target folder.')],
                            [sg.Input(size = (25,1), key = '_FILEPATH_'), sg.FolderBrowse(button_text = 'Browse', enable_events = True)],
                            [sg.Button('Next', pad = (Pad)), sg.Button('Quit', pad = (Pad))]    ]
    ChooserWindow = sg.Window(AppTitle, ChooseTargetLayout, font=(Font))
    while True:
        event, values = ChooserWindow.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            sys.exit()
        if event == '_FILEPATH_':
            ChooserWindow['_FILEPATH_'].update(values['Browse'])
        if event == 'Next':
            if values['_FILEPATH_'] != '':
                ChooserWindow.close()
                return values['_FILEPATH_']

if __name__ == "__main__":
    Test = GetFolderDialog("Test v1")
    print(Test)