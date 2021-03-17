import matplotlib
import matplotlib.pyplot as plt
import math
matplotlib.rcParams['agg.path.chunksize'] = 10000

def ResidualReader(filename):
    print("Performing Data Reading")
    f = open(filename,"r")

    AngLst = []
    ResiLst = []
    CountLst = []
    
    for i in f:
        Line = str(i)
        Ang = float(Line[59:64])
        AngLst.append(Ang)
        Resi = float(Line[83:90])
        ResiLst.append(Resi)
    
    NewAngLst = []
    NewResiLst = []
    for i in range(len(AngLst)):
        if AngLst[i] not in NewAngLst:
            NewAngLst.append(AngLst[i])
            NewResiLst.append([ResiLst[i]])
        elif AngLst[i] in NewAngLst:
            NewResiLst[NewAngLst.index(AngLst[i])].append(ResiLst[i])

    for i in range(len(NewAngLst)):
        CountLst.append(len(NewResiLst[i]))
    
    VeryNewResiLst = []
    for i in NewResiLst:
        RMS = math.sqrt((sum(j*j for j in i))/len(i))
        VeryNewResiLst.append(RMS)

    return VeryNewResiLst, NewAngLst, CountLst

def MakeGraph(day):
    print("Making Image for day " + str(day))
    name = ["nominal","redundant"]
    plt.figure()
    
    for i in range(2):
        Resi,Ang, Count = ResidualReader(name[i] + " GOCE GPS residual data\GOCE.13." + str(day) + "_RDOD24hr.res")
        plt.subplot(2,2,i+1)
        plt.scatter(Ang,Resi,s=0.1)
        plt.ylabel('Phase Residual (m)')
        plt.xlabel('Receiver Elavation Angle (degree)')
        plt.title("GOCE " + name[i] + " receiver phase residual vs elevation angle")
        plt.xlim(0,90)
        plt.ylim(0,0.02)
        plt.grid()
        
        plt.subplot (2,2, i+3)
        plt.scatter(Ang, Count, s = 0.1)
        plt.ylabel("Number of observations")
        plt.xlabel("Receiver Elevation Angle (degree)")
        plt.title("GOCE " + name[i] + " number of observations vs elevation angle")

    plt.tight_layout()
    plt.savefig("Residual GPS data graphs\Residuals day " + str(day) + ".png")


for i in range(245,274):
    MakeGraph(i)
