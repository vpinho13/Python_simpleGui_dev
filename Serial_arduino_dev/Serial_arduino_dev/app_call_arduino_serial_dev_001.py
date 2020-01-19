import time


class CallDaq:

    def __init__(self):
        self.result_a0 = 'nan'
        self.result_a1 = 'nan'
        self.serial_timer = 0

    def daq_measure_call(self):
        """
         Name: Vinicius Miranda de Pinho
         Date: 20 Jan 2020
         Rev: 0001
         Target: Call all analog port for Arduino and print time test total
        :return:
        """
        import arduino_analog_samples_001 as ad1
        time.sleep(3)
        ad1.daqBegin.open_serial()

        print(ad1.daqBegin.result())
        print(ad1.daqBegin.status_voltage_range_a0())
        self.result_a0 = ad1.daqBegin.status_voltage_range_a0()
        print(self.result_a0)

        print('_________________________________________')

        print(ad1.daqBegin.result_a1())
        print(ad1.daqBegin.status_voltage_range_a1())
        self.result_a1 = ad1.daqBegin.status_voltage_range_a1()
        print(self.result_a1)
        print(ad1.daqBegin.test_time)
        self.serial_timer = ad1.daqBegin.test_time
        print(self.serial_timer)


call_daq1 = CallDaq()
# call_daq1.daq_measure_call()
# help(daq_measure_call)
