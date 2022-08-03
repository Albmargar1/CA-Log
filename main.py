import PySimpleGUI as sg
import CustomElements
import draft
import log

sg.theme('DarkBlue14')
sg.set_options(font='Arial 16')

title = 'Welcome to Counter Attack Utility App!'
instructions = 'In case you want to record a new match:\n' \
               '1) Draft both teams.\n' \
               '2) Log your game.\n' \
               '\n' \
               'I recommend using \'Alt\' + \'Tab\' to switch between Tabletopia and this app window.'

layout = [[sg.Text(title, font='Arial 22')],
          [sg.Text(instructions)],
          [sg.Text(text='')],
          [CustomElements.cbutton(text='Draft'),
           CustomElements.cbutton(text='Log'),
           CustomElements.cbutton(text='Exit')]]

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