import lineup
import draft
import PySimpleGUI as sg

layout = [[sg.Button('Draft'), sg.Button('Lineup'), sg.Button('Exit')]]

window = sg.Window('CA Log', layout)

while True:
    event, values = window.read()

    prev_element = window.find_element_with_focus()

    if event in (sg.WIN_CLOSED, 'Exit'):  # always check for closed window
        break

    if event == 'Draft':
        draft.create_draft()

    if event == 'Lineup':
        lineup.create_lineup()

    if event == 'Match':
        lineup.create_lineup()

window.close()