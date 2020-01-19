"""
Vinicius Miranda de Pinho


Jan 2020 - 12

PySimpleGUI serial number test  and now serial port arduino

rev 0002 (initial)

status : developing

"""

import PySimpleGUI as sg
from time import sleep
from datetime import datetime
import time
from PySimpleGUI import sgprint_close
import app_call_arduino_serial_dev_001 as ap1

import multiprocessing as mp


class Daq1:

    def __init__(self, window, serial_number, print_debug, sg_close, time_stamp_str):
        self.serial_number = serial_number
        self.window = window
        self.print_debug = print_debug
        self.sg_close = sg_close
        self.time_stamp_str = time_stamp_str
        self.start = 0
        self.finish = 0
        f'Finished in {round(self.finish - self.start, 3)} seconds'

        # sg.change_look_and_feel('DefaultNoMoreNagging')  # Remove line if you want plain gray windows
        sg.change_look_and_feel('Reddit')  # Remove line if you want plain gray windows
        self.print_debug = sg.EasyPrint

        layout = [[sg.Text('Test FCT  Amplimax')],
                  [sg.T('S/N :', size=(4, 1)), sg.InputText(key='my_input')],
                  [sg.Txt('', size=(25, 1), key='line4')],
                  [sg.Button('[ START ]', button_color=('black', '#9df5ed'), key='button1')],
                  [sg.Txt('___________________________________________________________', size=(80, 1), key='line1')],
                  [sg.Txt('Test Status:  ', size=(35, 1), key='line2')],
                  [sg.Txt(' > ', size=(25, 1), key='line3')],
                  [sg.Multiline(default_text='Test FCt will be started\n\r', size=(220, 40), autoscroll=True,
                                do_not_clear=True,
                                key='output')],
                  [sg.Txt(' Ver.1.0                Develop by VP Corp. 2020', size=(80, 1), font=('Helvetica', 8),
                          key='line5')]]
        # [sg.Txt('', size=(90, 30), key='output')]]

        self.window = sg.Window('Serial Number - Factory test', return_keyboard_events=True).Layout(layout)

        timer = 0

        while True:
            event, values = self.window.Read()
            if event is None or event == 'Exit':
                break
            print(f'focus = {self.window.FindElementWithFocus().Key}')
            if self.window.FindElementWithFocus().Key == 'button1' or event == 'button1':
                self.window.FindElement('output').Update(
                    "[ Start ] ---- >  Test will be running...")  # yellow back text
                self.start = time.perf_counter()
                self.window.FindElement('line2').Update("Running...", background_color='#f0f2a5')
                print(f'focus = {self.window.FindElementWithFocus().Key}')
                print("button_1")
                timer = timer + 1
                print(timer)
                self.window.FindElement('button1').Update(disabled=True)
                self.window.FindElement('button1').Update(button_color=('black', '#e8dd8e'))  # first black  sec yellow
                self.window.FindElement('button1').Update(text=" [ RUNNING ]")
                # window.FindElementWithFocus().Key = 'my_input'
                self.window.FindElement('button1').set_focus(force=False)
                self.window.FindElement('my_input').set_focus(force=True)
                # print(f'focus = {window.FindElementWithFocus().Key}')
                self.serial_number = values['my_input']
                print(f'serial digitado: {self.serial_number}')
                self.window.FindElement('line3').Update(self.serial_number)
                self.print_debug(self.serial_number)
                self.window.Refresh()
                self.time_stamp()
                self.p1 = 'nan'

    def time_stamp(self):
        self.print_debug(self.time_stamp_str)
        print('Current Timestamp : ', self.time_stamp_str)
        self.serial_open()

    def counter_serial(self):
        print("pr1 start here")
        for i in range(0, 100, 10):
            time.sleep(2)
            self.window.FindElement('output').Update(i)
            self.window.Refresh()

    def measure_analog(self):
        try:
            print("Serial Begin at 9600")
            self.window.FindElement('output').Update("Serial Begin at 9600")
            self.window.Refresh()

            ap1.call_daq1.daq_measure_call()
            self.window.FindElement('output').Update(ap1.call_daq1.result_a0)
            self.window.Refresh()

            print(f'S/N: {self.serial_number}')
            sleep(2)
            print("Finish Program")

        except(AttributeError, Exception) as e:
            print("Serial Port code 000")

    def serial_open(self):
        print(len(self.serial_number))
        if str(self.serial_number) == "":
            print("String empty !")
            self.window.FindElement('my_input').update("")  # clear variable IN
            self.window.Refresh()
            sleep(3)
            self.window.Refresh()
            print("I am here")
            # self.window.FindElement('button1').Update(disabled=False)
            self.window.Refresh()
            self.window.FindElement('my_input').set_focus(force=True)
            self.window.Refresh()
            self.window.FindElement('output').Update("String empty !")
            self.window.FindElement('button1').Update(button_color=('black', '#9df5ed'))  # blue button
            self.window.FindElement('button1').Update(text=" [ START ]")
            self.window.FindElement('line2').Update("Failed...", background_color='#f28a49')  # red back text
            self.window.Refresh()
            self.sg_close()
            self.window.FindElement('button1').Update(disabled=False)
            self.window.Refresh()

        else:
            print("####################################################")
            print("serial will open here")
            self.window.FindElement('my_input').update("")  # clear variable IN
            sleep(3)
            self.window.Refresh()
            print("I am here")
            self.window.Refresh()
            self.window.FindElement('my_input').set_focus(force=True)
            self.window.Refresh()
            # window.FindElement('button1').set_focus(force=True)
            # window.FindElement('my_input').set_focus(force=True)
            self.check_serial()

    def check_serial(self):
        size_of_serial = 10
        print(len(str()))
        if len(self.serial_number) >= int(size_of_serial):
            print("Serial NUmber match")
            self.print_debug("Serial NUmber match")
            self.window.Refresh()
            sleep(4)
            self.sg_close()
            self.measure_analog()  # call DAQ1 measure here
            self.window.FindElement('my_input').set_focus(force=True)
            self.window.Refresh()
            sleep(3)
            self.window.FindElement('output').Update(

                f'GSM_1:             PASS\n'
                f'VOLTAGE_1:     PASS\n'
                f'CURRENT_1:    PASS\n'
                f'GSM                  PASS\n'
                f'VOLTAGE          PASS\n'
                f'CURRENT         PASS\n'
                f'{self.time_stamp_str}')

            self.window.Refresh()
            self.sg_close()
            self.window.FindElement('button1').Update(disabled=False)
            self.window.Refresh()
            self.window.FindElement('button1').Update(button_color=('black', '#9df5ed'))  # blue button
            self.window.FindElement('button1').Update(text=" [ START ]")
            self.window.FindElement('line2').Update("PASS ", background_color='#86c47a')  # green back text
            self.finish = time.perf_counter()
            print(f'Finished in {round(self.finish - self.start, 3)} seconds')
            self.window.Refresh()
        else:
            print(len(self.serial_number))
            print("serial number not match")
            self.print_debug("serial number not match")
            self.window.FindElement('output').Update("Error: -- > Serial Number not Match")
            self.window.Refresh()
            self.window.FindElement('my_input').set_focus(force=True)
            self.window.Refresh()
            sleep(3)
            self.sg_close()
            self.window.FindElement('button1').Update(disabled=False)
            self.window.Refresh()
            self.window.FindElement('button1').Update(button_color=('black', '#9df5ed'))  # blue button
            self.window.FindElement('button1').Update(text=" [ START ]")
            self.window.FindElement('line2').Update("Failed...", background_color='#f28a49')  # red back text
            self.window.Refresh()


# Returns a datetime object containing the local date and time
datetime1 = datetime.now()
timestamp = datetime1.strftime("%d-%b-%Y (%H:%M:%S.%f)")

daq1 = Daq1('serial', 'windows', 'debug', sgprint_close, timestamp)
