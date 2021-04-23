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
def Reading2(filename,filename2,day):
    #filename = a txt file with 4 columns (longitude, latitude, altitude, time)
    f = open(filename,"r")
    lines = f.readlines()
    del lines[0]
    #make a list of lists: [long, lat, alt, time]
    CoordLst = [[float(x) for x in str(i).split()] for i in lines]
    ResiLst = ResidualReader(filename2)

    for i in CoordLst:
        i[3] += day
    for i in ResiLst:
        i[0] += day

    b = 0
    for i in range(len(ResiLst)):

        #if the time of a a ResiLst couple [time, resi] equals the time of a coordinate --> add the residual to the coordlst; [long, lat, alt, time, resi]
        while ResiLst[i][0] != CoordLst[b][3]:
            b += 1
        CoordLst[b].append(ResiLst[i][1])

    return CoordLst

def CombineFiles():
    CoordLst = []
    day = 86400
    for i in range(2,31):
        PartLst = Reading2("Orbit Data\Write_LLH" + str(i) + ".txt","nominal GOCE GPS residual data\GOCE.13." + str(i + 243) +"_RDOD24hr.res",int(day * (i-2)))
        CoordLst += PartLst
    
    return CoordLst

#function to convert longitude and latitude into bins (starting bin is top left corner, 
#then finish row and start on next row at most left)
def BinMaker(CoordLst):

    #make list of empty lists:
    #360 columns, 180 rows
    Bins = [ [ [] for i in range(360)] for i in range(180)]

    #go from -90 -- 90 to 0 - 180
    #go from -180 -- 180 to 0 - 360
    #bin residuals in right bin

    for i in CoordLst:
        Long = math.floor(i[0]) + 180
        Lat = math.floor(i[1]) + 90
        Bins[Lat][Long] += i[4:]
    
    #print(Bins[0][0])
    #print(Bins[1][0])

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
    longit = []
    lat = []
    multitude = []
    for i in range(180):
        for j in range(360):
            longit.append(i)
            lat.append(j)
            multitude.append(Bins[i][j][0])
    plt.xlim(0,360)
    plt.ylim(0,180)
    plt.scatter(lat, longit, c=multitude, marker=',', cmap='Reds')
    return plt.show()

#CoordLst = Reading2("Orbit Data\Write_LLH2.txt","nominal GOCE GPS residual data\GOCE.13.245_RDOD24hr.res")
Bins = BinMaker(CombineFiles())
#print(Bins)
MakeImg(Bins)
