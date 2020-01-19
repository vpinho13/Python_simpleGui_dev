import arduino_analog_samples_001 as ad1
import time


start = time.perf_counter()

# ad1.daqBegin.result()
# ad1.daqBegin.result_a1()
ad1.daqBegin.open_serial()

print(ad1.daqBegin.result())
print(ad1.daqBegin.status_voltage_range_a0())

print('_________________________________________')

print(ad1.daqBegin.result_a1())
print(ad1.daqBegin.status_voltage_range_a1())

time.sleep(3)
#
# # ad1.daqBegin.result()
# # ad1.daqBegin.result_a1()
# ad1.daqBegin.open_serial()
# print(ad1.daqBegin.result())
# print(ad1.daqBegin.result_a1())

finish = time.perf_counter()

print(f'Finished at {round(finish - start, 3)} seconds')
