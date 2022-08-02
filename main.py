import PySimpleGUI as sg
import definitions
import random
import functions
import draft
import log

layout = [[sg.Button(button_text='Draft'),
           sg.Button(button_text='Log'),
           sg.Button(button_text='Exit')]]

window = sg.Window('LOG', layout)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):  # always check for closed window
        break

    if event == 'Draft':
        draft_values = draft.draft()

    if event == 'Log':
        log.log()

window.close()