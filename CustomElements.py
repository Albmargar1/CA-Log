import PySimpleGUI as sg

def cbutton(text,
           key='',
           color=('#FFFFFF', '#385494'),
           font='Arial 16',
           size=(8,1)):

    return sg.Button(button_text=text,
                     key=text if key == '' else key,
                     button_color=color,
                     font=font,
                     size=size,
                     border_width=2)


def cinput(key,
           text='',
           size=(6,1),
           justification='center',
           expand_x=True,
           background_color='#385494',
           text_color='#FFFFFF',
           font='Arial 16',
           enable_events=False,
           initial_focus=False):

    return sg.Input(key=key,
                    default_text=text,
                    size=size,
                    justification=justification,
                    expand_x=expand_x,
                    background_color=background_color,
                    text_color=text_color,
                    font=font,
                    enable_events=enable_events,
                    focus=initial_focus)