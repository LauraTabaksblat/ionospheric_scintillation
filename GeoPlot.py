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
        
        Time = Line[11:20].split(":")
        print(Time)
        Time[0] = float(Time[0]) * 3600
        Time[1] = float(Time[1]) * 60
        Time[2] = float(Time[2])
        TimeSec = sum(Time)
        print(TimeSec) 
    
        if TimeSec not in TimeLst:
            TimeLst.append(TimeSec)
            Resi = float(Line[83:90])
            ResiLst.append([Resi])
        elif TimeSec in TimeLst:
            Resi = float(Line[83:90])
            ResiLst[TimeLst.index(TimeSec)].append(Resi)

    return ResiLst, TimeLst
    
print(ResidualReader("nominal GOCE GPS residual data\GOCE.13.245_RDOD24hr.res"))