import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
import scipy.interpolate
import os
import matplotlib.colors as colors
import matplotlib.cm as cm
from PIL import Image
matplotlib.rcParams['agg.path.chunksize'] = 10000

#READ RESIDUAL FILES -- RETURNS LIST OF COUPLE [time, residual]
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

#READ GPS LOCATION
def Reading2(filename,filename2):
    #filename = a txt file with 4 columns (longitude, latitude, altitude, time)
    f = open(filename,"r")

    #make a list of lists: [long, lat, alt, time]
    CoordLst = [[float(x) for x in str(i).split()] for i in f]

    ResiLst = ResidualReader(filename2)
    
    b = 3

    for i in range(len(ResiLst)):
        #if the time of a a ResiLst couple [time, resi] equals the time of a coordinate --> add the residual to the coordlst; [long, lat, alt, time, resi]
        if ResiLst[i][0] == CoordLst[b-1][3]:
            CoordLst[b-1].append(ResiLst[i][1])

        #if the time is not equal, go to next CoordLst element and append the residual there
        else:
            b += 1
            CoordLst[b-1].append(ResiLst[i][1])

    return CoordLst

#function to convert longitude and latitude into bins (starting bin is top left corner, 
#then finish row and start on next row at most left)
def BinMaker(CoordLst):

    #make list of empty lists:
    #72 columns, 36 rows
    BinRow = [ [] for i in range(72)]
    Bins = [ BinRow for i in range(36)]

    #go from -90 -- 90 to 0 - 36
    #go from -180 -- 180 to 0-72
    #bin residuals in right bin
    for i in CoordLst:
        Long = math.floor((i[0] / 5)) + 36
        Lat = 18 - math.floor((i[1] / 5))
        Bins[Lat][Long].extend(i[4:])
    
    #take rms of residuals in each bin
    for row in Bins:
        for col in row:
            if not col:
                col.append(0.0)
            else:
                rms = round(math.sqrt((sum(j*j for j in col)/len(col))),5)
                col.clear()
                col.append(rms)

    return Bins

def MakeImg(Bins):
    C = []
    longit = []
    lat = []
    multitude = []
    for i in range(36):
        for j in range(72):
            C.append(Bins[i][j][0])
            if Bins[i][j][0] != 0:
                longit.append(i)
                lat.append(j)
                multitude.append(Bins[i][j][0])
    plt.xlim(0,72)
    plt.ylim(0,36)
    plt.scatter(lat, longit, c=multitude, marker=',', cmap='Reds')
    return plt.show()

Bins = BinMaker((Reading2("Orbit Data\LLH2.txt","nominal GOCE GPS residual data\GOCE.13.245_RDOD24hr.res")))
#print(Bins)
MakeImg(Bins)
