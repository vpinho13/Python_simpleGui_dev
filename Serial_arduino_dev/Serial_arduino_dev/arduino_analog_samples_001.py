"""
Vinicius Miranda de Pinho


Python 3.6 serial Arduino

Made new software for arduino port

rev 001 fully works

19  jan 2020

Arduino Serial Port with measure range.


"""

# !/usr/bin/python3

from pyfirmata2 import Arduino
import time
import serial
from time import sleep
from pyfirmata2 import Arduino, util
import gc


class DaqMain:
    try:

        def __init__(self):

            self.start = 0

            self.start = time.perf_counter()

            self.finish = 0

            self.test_time = 0

            self.volts = float(5)

            self.result_voltage = 'nan'

            self.output = 'nan'

            self.output0 = 'nan'

            self.output1 = 'nan'

            self.port_a0 = 'nan'

            self.port_a1 = 'nan'

            self.message = "DAQ status update"

            self.board = Arduino('/dev/ttyUSB0')

            self.board.digital[13].write(1)

            self.it = util.Iterator(self.board)

            self.it.start()

            self.analog_0 = self.board.get_pin('a:0:i')
            self.analog_1 = self.board.get_pin('a:1:i')
            print("Stable Serial port timer")
            sleep(4)

        def open_serial(self):
            self.message = "Testing running now..."
            self.board = Arduino('/dev/ttyUSB0')
            self.board.digital[13].write(1)
            self.it = util.Iterator(self.board)
            self.it.start()
            print("Measure will start")
            sleep(3)
            self.analog_0 = self.board.get_pin('a:0:i')
            self.analog_1 = self.board.get_pin('a:1:i')
            sleep(2)
            # self.result()
            # self.result_a1()
            return "Serial open successful"

        def analog_volts(self):
            self.result_voltage = ((self.analog_0 * self.volts) / 1)
            # print("%.2f" % self.result_voltage)
            self.output = ("%.2f" % self.result_voltage)
            # return str(self.output)

        def result(self):
            while True:
                self.board.digital[13].write(1)
                # print(self.analog_0.read())
                self.port_a0 = self.analog_0.read()
                self.result_voltage = ((self.port_a0 * self.volts) / 1)
                print("%.2f" % self.result_voltage)
                self.output0 = ("%.2f" % self.result_voltage)
                self.status_voltage_range_a0()
                return 'ANALOG A0'

        def result_a1(self):
            while True:
                self.board.digital[13].write(0)
                self.port_a1 = self.analog_1.read()
                self.result_voltage = ((self.port_a1 * self.volts) / 1)
                print("%.2f" % self.result_voltage)
                self.output1 = ("%.2f" % self.result_voltage)
                sleep(1)
                self.status_voltage_range_a1()
                return 'ANALOG A1'

        def status_voltage_range_a0(self):
            if 3.9 <= float(self.output0) <= 5:
                return 'PASS A0'
            else:
                return 'FAIL A0'

        def status_voltage_range_a1(self):
            if 3.9 <= float(self.output1) <= 5:
                return 'PASS A1'
            else:
                return 'FAIL A1'

        def close_port(self):
            self.board.exit()
            self.finish = time.perf_counter()
            self.test_time = f'Finished at {round(self.finish - self.start, 3)} seconds'
            return

    except serial.SerialException:
        print("Serial Port Error: Code 000")
    except TypeError:
        print("code 002 Serial stooped")
    except AttributeError:
        print("Serial port code 000")
    except Exception as e:
        print(e)


try:
    daqBegin = DaqMain()
    daqBegin.close_port()
    # daqBegin.result()
    # daqBegin.result_a1()
except serial.SerialException:
    print("Serial Port Error: Code 000")
except TypeError:
    print("code 002 Serial stooped")
except AttributeError:
    print("Serial port code 000")
except Exception as e:
    print(e)
