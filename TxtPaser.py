#!/usr/bin/python
import os
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt
import math

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
    x, y, z = np.loadtxt(d, delimiter=',', usecols=(2, 3, 4), unpack=True)

    begin = np.where(x == 50000)[0]
    end = np.where(x == 0)[0]


    print begin, end

    plt.scatter(y[0:begin[0]-1], z[0:begin[0]-1])

    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    plt.savefig(filename + "_1.png")


    for k in range(begin[1], end[1]):
        z[k] = math.sqrt(z[k])

    for j in range(len(begin)):
        plt.scatter(x[begin[j]:end[j]], z[begin[j]:end[j]])

    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    plt.savefig(filename + "_2.png")
    plt.show()




for path in path_in:
    for root, dirs, files in os.walk(path):
        for i in files:
            ext = i.split('.')[-1]
            old_filename = i.split('.')[0]
            if ext == 'txt':
                process_file(i)


