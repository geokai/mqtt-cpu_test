# This file was created on 13/01/17
# Author: George Kaimakis


# Get processor and memory usage percentage and print to console.


from time import sleep
import psutil


while(True):

    # get the system performance data:
    ramPercent = psutil.virtual_memory().percent
    cpuPercent = psutil.cpu_percent(interval=0)
    # print (f" CPU: {cpuPercent}%   RAM: {ramPercent}%")
    print (f",cpu_%,{cpuPercent},mem_%,{ramPercent}")
    sleep(5)
