"""
Vinicius Miranda de Pinho

December 2019

Pyhtin and Arduino Analog port ready

Rev 001


"""

import pyfirmata2
import time
from time import sleep
import serial
from pyfirmata2 import Arduino
import PySimpleGUI as sg
from serial import Serial
import PySimpleGUI as sg
from time import sleep
import time
import serial

"""  **************************8  Simplegui layout ***********************************************"""

sg.change_look_and_feel('DefaultNoMoreNagging')  # Remove line if you want plain gray windows

layout = [[sg.Text('Test FCT Amplimax ver. 1.0 - Elsys-2019')],
          [sg.Text('')],
          [sg.Text('S/N: ', size=(3, 1), key='-SER3-'), sg.Input(key='-IN-')],
          [sg.Text('_____________________________')],
          [sg.Text('All Test will below:            Timer sec:', size=(27, 1)), sg.Text('0', size=(6, 1), key='timer')], # Output label for Serial
          [sg.Output(size=(80, 10), key='output_20')],
          [sg.Text('Status FCT : '), sg.Text('S/N:', key='-SER1-'), sg.Text('', size=(20, 1), key='-SER2-')],
          [sg.Txt('>> ', size=(80, 1), text_color='orange', key='output_2')],
          [sg.Txt('>> ', size=(80, 1), text_color='green', key='output_3')],
          [sg.Txt('>> ', size=(80, 1), text_color='red', key='output_4')],
          [sg.Submit('[ Start ]'), sg.Cancel('[ Close FCT ]')]]

window = sg.Window('FCT  Voltage Test _ ELSYS  MANAUS', layout, location=(200, 100))

"""**************************    end  layout *********************************************************"""

''' *************************** Variables for stop loop***********************'''

timer_test_total = 0

# sg.change_look_and_feel('Dark Blue 8')
'''*****************************  End of global loop **************************'''


def analog_read_ao():
    #  ***************************Start internal variable****************************

    out_of_loop = 0

    # ****************************  End of global loop **************************
    while out_of_loop <= 2:
        if out_of_loop == 0:
            print("Serial Port is available...")
            window['output_4'].update(">>", background_color='#D7DBDD', text_color='red')  # Clear variable
            window['output_3'].update(">>", background_color='#D7DBDD', text_color='green')  # Clear variable
            window['output_2'].update("[ --Testing-- ]", background_color='yellow', text_color='black')
        window['-SER2-'].update(serial_number)
        window['-IN-'].update("")  # clear variable IN
        sg.OneLineProgressMeter('Testing Voltage PCB', out_of_loop + 1, 3, 'key')
        window.Refresh()
        print("Reading all voltages...")
        board = pyfirmata2.Arduino('/dev/ttyUSB0')
        it = pyfirmata2.util.Iterator(board)
        it.start()
        analog_input0 = board.get_pin('a:0:i')
        analog_input1 = board.get_pin('a:1:i')
        analog_input2 = board.get_pin('a:2:i')
        sleep(2)
        """  ******************   Analog port - A0 *************************"""
        analog_value0 = analog_input0.read()
        sleep(0.2)
        volts = float(5)
        out_a0_volts = ((analog_value0 * volts) / 1)
        print(f'Voltage port A0:  {"%.2f" % out_a0_volts}')
        time.sleep(0.2)
        """  ******************   Analog port - A1 *************************"""
        analog_value1 = analog_input1.read()
        volts = float(5)
        out_a1_volts = ((analog_value1 * volts) / 1)
        print(f'Voltage port A1: {"%.2f" % out_a1_volts}')
        time.sleep(0.2)
        """  ******************   Analog port - A2 *************************"""
        analog_value2 = analog_input2.read()
        volts = float(5)
        out_a2_volts = ((analog_value2 * volts) / 1)
        print(f'Voltage port A2: {"%.2f" % out_a2_volts}')
        time.sleep(0.2)
        """ *********************  Ending Analog port ************************"""
        out_of_loop += 1
        if out_of_loop == 1:
            print(f'Measure Volts checking: ..33 %')
        if out_of_loop == 2:
            print(f'Measure Volts checking: ..65 %')
            window['output_2'].update("Closing data...", background_color='yellow', text_color='black')
            window.Refresh()
        if out_of_loop == 3:
            window['output_2'].update(">")
            print(f'Measure Volts checking: ..100 %')
            window['output_2'].update(">>", background_color='#D7DBDD', text_color='orange')
            window['output_3'].update("[ - -PASS- - ]", background_color='#58D68D', text_color='black')
            window.Refresh()
        if out_of_loop == 3:
            a0 = float("%.2f" % out_a0_volts)
            a1 = float("%.2f" % out_a1_volts)
            a2 = float("%.2f" % out_a2_volts)
            print("Measures Voltage Done !")
            window.FindElement('[ Start ]').Update(disabled=False)
            window.FindElement('[ Close FCT ]').Update(disabled=False)
            window.Refresh()
            print("################ Final Test ###########################")
            return a0, a1, a2
    else:
        print("Reading Voltage code: 001")


def arduino_serial_check():
    try:
        serial_number1 = values['-IN-']
        window['output_2'].update(">>", background_color='#D7DBDD', text_color='orange')
        window['output_3'].update(">>", background_color='#D7DBDD', text_color='green')  # Clear variable
        window['-SER2-'].update(serial_number1)
        window['output_4'].update("-- Serial Port Testing --")
        print(f'Serial Number : {serial_number1}')
        board = pyfirmata2.Arduino('/dev/ttyUSB0')
        it = pyfirmata2.util.Iterator(board)
        it.start()
        analog_result = (analog_read_ao())
        window['timer'].update("11")
        window.Refresh()
    except serial.SerialException:
        print("Serial Port not available")
        window.FindElement('[ Start ]').Update(disabled=False)
        sg.PopupError('[ 0002 - Serial Port problem! Call Support ]')  # Shows red error button
        window['-IN-'].update("")  # clear variable IN
        print("################ FAILED #################################")
        window.Refresh()
        window['timer'].update("12")
        window.Refresh()


while True:  # The Event Loop
    event, values = window.read()
    # print(event, values
    window['timer'].update("3")
    window.Refresh()

    if event in (None, 'Exit', '[ Close FCT ]'):
        break
    else:

        if event in '[ Start ]':
            if str(values['-IN-']) == "":
                window.FindElement('[ Start ]').Update(disabled=True)
                window.Refresh()
                print("Serial is empty!")
                window['output_2'].update(">>", background_color='#D7DBDD', text_color='orange')
                window['output_3'].update(">>", background_color='#D7DBDD', text_color='green')  # Clear variable
                window['output_4'].update("[ -- FAILED -- ]", background_color='red', text_color='black')
                sg.PopupError('[ 0001 - Attention! No Serial Number ]')  # Shows red error button
                window.FindElement('[ Start ]').Update(disabled=False)
                window.Refresh()
                window['timer'].update("5")
                window.FindElement('output_20').Update()
                window.Refresh()
            else:
                serial_number = values['-IN-']
                window['output_2'].update(">>", background_color='#D7DBDD', text_color='orange')
                window['output_3'].update(">>", background_color='#D7DBDD', text_color='green')  # Clear variable
                window['-SER2-'].update(serial_number)
                window['output_4'].update("-- Serial Port Testing --", background_color='#85929E')
                print("Serial Port Test started! Waiting.... ")
                print("#######################################################")
                window.FindElement('[ Start ]').Update(disabled=True)
                window.FindElement('[ Close FCT ]').Update(disabled=True)
                window.Refresh()
                sleep(2)
                arduino_serial_check()
                window['timer'].update("6")
                window.Refresh()

                # print no resulted de def analog read
                # analog_result = (analog_read_ao())
# print(analog_result)

# print(analog_result[0])

# print(analog_result[1])

# print(analog_result[2])


window.close()
