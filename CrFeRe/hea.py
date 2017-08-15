#!/usr/bin/python
import os
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt
import math


path_in = [
    './',
]

min_slope = 10000
min_slope_beta = 0
min_slope_gama = 0

fig = plt.figure()

def calculate_slope(xlist, ylist):

    '''
    slope = []
    for i in xrange(len(xlist) - 1):
        slope.append( (ylist[i+1]-ylist[i]) / (xlist[i+1]-xlist[i]) )

    slope_variance = np.var(slope)
    slope_mean = np.mean(slope)

    return slope_variance/np.mean(ylist)
    '''
    slope = []
    for i in xrange(len(xlist) - 1):
        slope.append( (ylist[i+1]-ylist[i]) / (xlist[i+1]-xlist[i]) )
    return np.mean(slope) / (np.mean(ylist) / np.mean(xlist)), math.sqrt(np.var(slope)) / (np.mean(ylist) / np.mean(xlist))

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

    z1=z.copy()

    for k in range(begin[0], end[-1]):
        z1[k] = pow(z[k], 1.0/beta)
    #   z[k] = math.sqrt(z[k])

    x1=x.copy()
    for k in range(begin[0], end[-1]):
    	x1[k] = pow(x[k]/z[k]/10000, 1.0/gama)

    color_list = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    marker_list = ['o', '1', '2', '3', '4', '8', 's', 'p', '*', 'h', 'v', '^', '<', '>']

    slope_mean = []
    slope_var = []
    for j in range(len(begin)):
        plt.scatter(x1[begin[j]:end[j]-1], z1[begin[j]:end[j]-1], color=color_list[j%len(color_list)], marker=marker_list[j%len(marker_list)], s=10)
        sm, sv = calculate_slope(x1[begin[j]:end[j]-1], z1[begin[j]:end[j]-1])
        slope_mean.append(sm)
        slope_var.append(sv)

    slope_mean_mean = np.mean(slope_mean)
    slope_mean_var = np.var(slope_mean)
    slope_var_mean = np.mean(slope_var)
    slope_var_var = np.var(slope_var)

    print beta, gama, "mm=", slope_mean_mean, "mv=", slope_mean_var, "vm=",  slope_var_mean, "vv=", slope_var_var

    global min_slope, min_slope_beta, min_slope_gama
    if slope_var_mean < min_slope:
        min_slope = slope_var_mean
        min_slope_beta = beta
        min_slope_gama = gama


    min_y = min(z1[begin[0]:end[-1]])
    max_y = max(z1[begin[0]:end[-1]])
    min_x = min(x1[begin[0]:end[-1]])
    max_x = max(x1[begin[0]:end[-1]])

    ax = fig.add_subplot(111)
    ax.set_xlim([min_x - (max_x-min_x) / 10, max_x + (max_x-min_x) / 10])
    ax.set_ylim([min_y - (max_y-min_y) / 10, max_y + (max_y-min_y) / 10])
    plt.xlabel('$(H/M)^{1/\gamma}$')
    plt.ylabel('$M^{1/\\beta}$')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    if not os.path.exists("./plots"):
        os.makedirs("./plots")
    plt.savefig("./plots/beta_{0}_gama_{1}.png".format(beta,gama))
    plt.clf()
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


print "Optimal Beta and Gama found:", min_slope_beta, min_slope_gama

