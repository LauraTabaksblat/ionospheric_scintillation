import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
import scipy.interpolate
import os
matplotlib.rcParams['agg.path.chunksize'] = 10000

def ResidualReader(filename):
    f = open(filename,"r")

    ResiLst = []
    for i in f:
        Line = str(i)
        Time = Line[12:20].split(":")
        Resi = float(Line[83:90])
        TimeSec = float(Time[0]) * 3600 + float(Time[1]) * 60 + float(Time[2])
        ResiLst.append([TimeSec,Resi])

    return ResiLst

def Reading2(filename,filename2):
    f = open(filename,"r")
    CoordLst = [[float(x) for x in str(i).split()] for i in f]

    ResiLst = ResidualReader(filename2)
    
    b = 3

    for i in range(len(ResiLst)):
        if ResiLst[i][0] == CoordLst[b-1][3]:
            CoordLst[b-1].append(ResiLst[i][1])
        else:
            b += 1
            CoordLst[b-1].append(ResiLst[i][1])

    return CoordLst

def BinMaker(CoordLst):
    Bins = [[[]] * 72] * 36

    for i in CoordLst:
        Long = math.floor((i[0] / 5)) + 36
        Lat = math.floor((i[1] / 5)) + 18
        Bins[Lat][Long].extend(i[4:])
    
    for row in Bins:
        for col in row:

            if not col:
                col = 0
            else:
                col = math.sqrt((sum(j*j for j in col)/len(val)))

    return Bins

print(BinMaker((Reading2("LLH2.txt","nominal GOCE GPS residual data\GOCE.13.245_RDOD24hr.res"))))