#!/usr/bin/python
import os
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt
import math

path_in = [
    './',
]

def process_file(filename, beta, gama):
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

    begin = np.where(x == 30000)[0]
    end = np.where(x == 0)[0]

 #   plt.scatter(y[0:begin[0]-1], z[0:begin[0]-1])
 #   plt.xlabel('time (s)')
 #   plt.ylabel('voltage (mV)')
 #   plt.title('About as simple as it gets, folks')
 #   plt.grid(True)
 #   plt.savefig(filename + "_1.png")

    plt.figure()

    z1=z.copy()

    for k in range(begin[0], end[-1]):
    	z1[k] = pow(z[k], 1.0/beta)
    #   z[k] = math.sqrt(z[k])

    x1=x.copy()
    for k in range(begin[0], end[-1]):
    	x1[k] = pow(x[k]/z[k]/10000, 1.0/gama)


    color_list = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    marker_list = ['o', '1', '2', '3', '4', '8', 's', 'p', '*', 'h', 'v', '^', '<', '>']

    for j in range(len(begin)):
        plt.scatter(x1[begin[j]:end[j]-1], z1[begin[j]:end[j]-1], color=color_list[j%len(color_list)], marker=marker_list[j%len(marker_list)], s=10)

    plt.xlabel('$(H/M)^{1/\gamma}$')
    plt.ylabel('$M^{1/\\beta}$')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    plt.savefig("C:\Users\cyq\HighEntropyAlloy_program\CrFeRe\Arrott_plot/beta_{0}_gama_{1}.png".format(beta,gama))
#    plt.show()




for path in path_in:
    for root, dirs, files in os.walk(path):
        for i in files:
            ext = i.split('.')[-1]
            old_filename = i.split('.')[0]
            if ext == 'txt':
            	for beta in range(1,10):
            		for gama in range(10,20):
                		process_file(i, beta/10.0, gama/10.0)


