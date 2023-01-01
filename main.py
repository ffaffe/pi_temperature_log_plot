# author = ffaffe
# date = Dec 2022

# import the squad
from time import time, strftime
import time
import csv
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display

# create sensor object
ts1 = "/sys/bus/w1/devices/28-20320c4c8f8e/w1_slave"

# create csv time variable and header
dat_time = strftime("%c")
header = ['time', 'temp']
x = 0

# mpl x limit counter variables
i = int(0)
j = int(50)
j_upper = j*2

# time delay variable for sensor reads\plot refreshes
delay = 1

# mpl figure to write results to
#fig = plt.figure()
fig, ax = plt.subplots(figsize=(5, 2.5), layout='constrained')
ax.set_xlabel('Time (arb.)') 
ax.set_ylabel('Temperature (\u2103)')
ax.tick_params(
    axis = 'x',
    which = 'both',
    bottom = False,
    top = False,
    labelbottom = False)
    
#plt.axis([0,1,0,50])
#fig, ax = plt.set_ylabel('Temperature u"\u2103" C')

# write header only 
with open ('/home/ffaffePi/Desktop/temp_log.csv', 'w') as f:            # open csv file ***r+ allows read and write operation    
    # create writer
    writer = csv.writer(f)
    writer.writerow(header)         # add header to file

# print start message
print('logging begins')


# program start
while True:
    t = open(ts1, "r")
    data = t.read()
    t.close()                                         # caused bug --> closed csv, locking later read attempts
    (discard, sep, reading) = data.partition('t=')
    temp = float(reading)/1000

    #create time variable
    time_cur = x
    x += 1

    # print time and date BEFORE write **DEBUG**
    print(time_cur, temp)
    
    with open ('/home/ffaffePi/Desktop/temp_log.csv', 'r+') as f:            # open csv file ***r+ allows read and write operation    
        # write data to csv
        data = [time_cur, temp]
        writer = csv.writer(f)
        writer.writerow(data)
        
        # print time and date AFTER write direct from csv **DEBUG**
       
        # reader object
        reader = csv.reader(f)
        next(reader, None)             # skip header
        # create list from csv
        rows = list(reader)            # legacy??
        # read last row
        # print(rows, '\n')            # **DEBUG**
        # final_line = rows[-1]
        # print(final_line)
        
        
        ### it's plotting time baby

        #fig, ax = plt.subplots()
        #plt.rcParams["figure.figsize"] = [7.00, 3.50]
        #plt.rcParams["figure.autolayout"] = True
        columns = ["time", "temp"]
        df = pd.read_csv("temp_log.csv", usecols=columns)
        #display(df)                                          # **DEBUG**
        # df = df.astype({"time": str, "temp": str})          # converts column types

        # plot that data        
        ax.plot(df.time, df.temp)
                
        # pause that shit for your vieing pleasure (adjust for desired effect;
        # seizure mode-paint drying, 0.01-10)
        plt.pause(delay)
        
        plt.xlim(0, int(time_cur))
        
        xlim1 = plt.xlim()
        print(xlim1)
        
        size = df.size
        #print(size)                      # **DEBUG**
        #print(i, j)                      # **DEBUG**
        if size >= (100):
            plt.xlim(i, j)
            i += 1
            j += 1

plt.show()

