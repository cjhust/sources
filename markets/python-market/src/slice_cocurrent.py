# -*- coding: utf-8 -*-
#!/usr/local/bin/python


import os
import sys
import termcolor
from optparse import OptionParser

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def SHOW(buf, color="green"):
    print termcolor.colored(buf, color) 

   
def INFO(buf, cr=True):
    if cr:
        print termcolor.colored(buf, "grey")
    else:
        print termcolor.colored(buf, "grey"),


def ERROR(buf, cr=True):
    if cr:
        print termcolor.colored(buf, "red")
    else:
        print termcolor.colored(buf, "red"),


class DATA():

    def __init__(self, title, xlable, ylable):
        plt.title(title)
        plt.xlabel(xlable)
        plt.ylabel(ylable)
        plt.axis([0, 64, 0, 200])
        
    def get_data_from_file(self, input):
        linelist = open(input).readlines()

        result = {
            "xlable" : [],
            "ylable" : [],
        }

        ylable_flag = 0
        for line in linelist:
            #sleep0.01 sleep0.05 ...
            itemlist = line.split()
            if (ylable_flag == 0):
                for item in itemlist[1:]:
                    result["ylable"].append(item)
                    result[item] = []
                ylable_flag = 1
            else:
                result["xlable"].append(itemlist[0])

                for i in range(1, len(itemlist)):
                    ylable = result["ylable"][i-1]
                    item = itemlist[i]

                    result[ylable].append(item)
        #for linelist ends
        return result

    def draw(self, result, output):
        xlable = result["xlable"]
        ylable = result["ylable"]
        if (len(xlable) == 0) or (len(ylable) == 0):
            ERROR("NO xlables or ylables")
            sys.exit()

        for item in ylable:
            ydatas = result[item]
            label = "$%s$"         %(item)
            plt.plot(result["xlable"], ydatas, ".-", label=label)
            plt.legend()
            plt.savefig("slice_cocurrent.png")
        #for ends


def slice_cocurrent_draw(input, output):
    title = "slice cocurrent optimize"
    xlable = "cocurrent"
    ylable = "Time(s)"

    data = DATA(title, xlable, ylable)
    result = data.get_data_from_file(input)
    data.draw(result, output)


if __name__ == "__main__":
    usage = "usage: %prog [option]"
    parser = OptionParser(usage)
    
    parser.add_option("-i", dest="input", default="datas/in.txt", help="set the inputfile")
    parser.add_option("-o", dest="output", default="slice.png", help="set the outfile")
    
    (options, args) = parser.parse_args()

    slice_cocurrent_draw(options.input, options.output)

