import matplotlib
import matplotlib.pyplot as plt
import math
matplotlib.rcParams['agg.path.chunksize'] = 10000

def ResidualReader(filename):
    f = open(filename,"r")

    AngLst = []
    ResiLst = []
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

    VeryNewResiLst = []
    for i in NewResiLst:
        RMS = math.sqrt((sum(j*j for j in i))/len(i))
        VeryNewResiLst.append(RMS)

    return VeryNewResiLst, NewAngLst

name = ["nominal","redundant"]

for i in range(2):
    Resi,Ang = ResidualReader(name[i] + " GOCE GPS residual data\GOCE.13.246_RDOD24hr.res")
    plt.subplot(2,1,i+1)
    plt.scatter(Ang,Resi,s=0.1)
    plt.ylabel('Phase Residual (m)')
    plt.xlabel('Receiver Elavation Angle (degree)')
    plt.title("GOCE " + name[i] + " receiver phase residual vs elevation angle")
    
plt.tight_layout()
plt.show()
