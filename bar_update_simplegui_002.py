#!/usr/bin/env python
import PySimpleGUI as sg
from time import sleep

# !/usr/bin/env python
import PySimpleGUI as sg
from time import sleep

import PySimpleGUI as sg
import gc
import time


def CustomMeter():
    # layout the form
    layout = [[sg.Text('A custom progress meter')],
              [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')],
              [sg.Cancel()]]

    # create the form
    window = sg.Window('Custom Progress Meter').Layout(layout)
    progress_bar = window.FindElement('progress')
    # loop that would normally do something useful
    for i in range(1000):
        time.sleep(0.012)
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.Read(timeout=0)
        if event == 'Cancel' or event is None:
            break
        # update bar with loop value +1 so that bar eventually reaches the maximum
        progress_bar.UpdateBar(i + 1, 1000)
    # done with loop... need to destroy the window as it's still open
    window.Close()
    window = None
    layout = None
    gc.collect()
    del window
    return 'END PROGRESS'

# CustomMeter()
