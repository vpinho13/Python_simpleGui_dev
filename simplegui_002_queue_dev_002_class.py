import PySimpleGUI as sg
import threading
import time
import queue
import bar_update_simplegui_002 as bc
import serial

lock = threading.Lock()
# queue used to communicate between the gui and long-running code
gui_queue = queue.Queue()


def arduino(gui_queue, name):
    print(f'I am inside {name}')
    try:
        import app_call_arduino_serial_dev_001 as ac
        ac.call_daq1.daq_measure_call()
        with lock:
            gui_queue.put('{} ::: done'.format('Done Serial'))
            print("End Bar Progress")
        print('End Arduino')
    except AttributeError:
        print("Serial port code main")
    except serial.SerialException:
        print("Serial Port Error: Code 000")


def counter2(name):
    print(f'I am inside thread {name}')
    for i in range(10):
        time.sleep(1)
        print(i)
    print('End counter 2')
    return


def counter(gui_queue, name):
    print(f'I am inside {name}')
    # gui_queue.put('{} ::: done'.format(name))
    # bc.CustomMeter()
    with lock:
        gui_queue.put('{} ::: done'.format(bc.CustomMeter()))
        print("End Bar Progress")
        return


def thread():
    tr1 = threading.Thread(target=counter, args=(gui_queue, 'tr1'))
    tr2 = threading.Thread(target=arduino, args=(gui_queue, 'tr2'))
    tr3 = threading.Thread(target=counter2, args=('tr3',))
    tr1.daemon = True
    tr1.start()
    tr2.daemon = True
    tr2.start()
    tr3.daemon = True
    tr3.start()
    return


def main_gui():
    layout = [
        [sg.Text('Your typed chars appear here:'),
         sg.Text(size=(20, 1), key='-OUTPUT-')],
        [sg.Input('', key='-IN-')],
        [sg.Button('Show'), sg.Button('Update'), sg.Button('Exit')],
        [sg.Multiline(default_text='Test FCt will be started\n\r', size=(140, 30), autoscroll=True,
                      do_not_clear=True,
                      key='output')]]

    window = sg.Window('Window Title', layout)

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break
        if event == 'Show':
            # change the "output" element to be the value of "input" element
            window['-OUTPUT-'].update(values['-IN-'])
            window.FindElement('output').Update('Update button')
            print('Show button has press')
            window.FindElement('output').Update('Show button has press')
            window.Refresh()
            start = time.perf_counter()
        try:
            message = gui_queue.get_nowait()  # see if something has been posted to Queue
        except queue.Empty:  # get_nowait() will get exception when Queue is empty
            message = None  # nothing in queue so do nothing

        # if message received from queue, then some work was completed
        if message is not None:
            # print(message)
            window.FindElement('output').Update(message)
            window.Refresh()
        if event == 'Update':
            print('Update button')
            window.FindElement('output').Update('Running .....')
            window['-OUTPUT-'].update(values['-IN-'])
            thread()  # will call threading here at same time ##########################################################
        if event == 'Popup':
            sg.popup_non_blocking('This is a popup showing that the GUI is running', grab_anywhere=True)
            # print(self.temp)
    # if user exits the window, then close the window and exit the GUI func

    window.close()


if __name__ == '__main__':
    main_gui()
    print('Exit Program')
