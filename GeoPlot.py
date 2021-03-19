import matplotlib
import matplotlib.pyplot as plt
import math
matplotlib.rcParams['agg.path.chunksize'] = 10000

def ResidualReader(filename):
    print("Performing Data Reading")
    f = open(filename,"r")

    ResiLst = []
    TimeLst = []
    for i in f:
        Line = str(i)
        
        Time = Line[12:20].split(":")
        print(Time)
        TimeSec = float(Time[0]) * 3600 + float(Time[1]) * 60 + float(Time[2])
        print(TimeSec) 
    
        if not TimeLst:
            TimeLst.append(TimeSec)
            Resi = float(Line[83:90])
            ResiLst.append([Resi])
        elif TimeSec != TimeLst[-1]:
            TimeLst.append(TimeSec)
            Resi = float(Line[83:90])
            ResiLst.append([Resi])
        else:
            Resi = float(Line[83:90])
            ResiLst[TimeLst.index(TimeSec)].append(Resi)

    NewResiLst = []
    for i in ResiLst:
        RMS = math.sqrt((sum(j*j for j in i))/len(i))
        NewResiLst.append(RMS)

    return NewResiLst, TimeLst
    
print(ResidualReader("nominal GOCE GPS residual data\GOCE.13.245_RDOD24hr.res"))
