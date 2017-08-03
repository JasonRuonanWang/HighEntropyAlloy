#!/usr/bin/python
import os
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt


path_in = [
    './',
]

def process_file(filename):
    # open file
    fp = open(filename,"r")

    # skip the first line, title line
    fp.readline()

    # read the rest
    wholestring = fp.read()
    d = StringIO(unicode(wholestring))

    # load the lines into numpy arrays
    # load Column 0 into x, and Column 2 into y
    x, y = np.loadtxt(d, delimiter=',', usecols=(0, 2), unpack=True)

    # do some calculation on x and y to get z
    z = (x + y) / 2

    # get the length of x to use as the horizontal axis
    t = np.arange(0, len(x))

    plt.plot(t,x)
    plt.plot(t,y)
    plt.plot(t,z)
    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    plt.savefig(filename + ".png")
    plt.show()

for path in path_in:
    for root, dirs, files in os.walk(path):
        for i in files:
            ext = i.split('.')[-1]
            old_filename = i.split('.')[0]
            if ext == 'txt':
                process_file(i)


