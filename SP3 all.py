import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import math
import os


#functions
def reading_pos(p):
    
    for root,dirs,files in os.walk(p):
        for file in files:
            if file.endswith(".IDF"):
            
                with open(os.path.join(root, file), 'r') as f:
            
                    lines = f.readlines()
                    i=0
                    for line in lines:
                        
                        if i<=1:
                            if line[0]+line[1] == "PL":
                                x_pos.append(float(line.split()[1]))
                                y_pos.append(float(line.split()[2]))
                                z_pos.append(float(line.split()[3]))
                                
                                
                        if line[0] == '*': #where the measurement should start and stop(HOUR, MINUTE, SECOND)
                            if line.split()[4] == '21' and line.split()[5]=='0' and line.split()[6]=='0.00000000': 
                                i=i+1
                                

                f.close()             

def inter_linear(meas_num, pos): 
    time = []

    for j in range(meas_num): #number of point measured every 10 seconds
        time.append(j*10)

    f = scipy.interpolate.interp1d(time, pos,fill_value = "extrapolate")
    time_new = np.arange(0,2505600,1)
    pos_new = f(time_new)
    return pos_new , time_new, time

def plot_iteration():
    print("Enter what graph you want(x,y or z)")
    pos = input()
    pos_c = pos
    if pos == 'x':
        pos = x_pos
        pos_new = x_new
    elif pos == 'y':
        pos = y_pos
        pos_new = y_new
    elif pos == 'z':
        pos = z_pos
        pos_new = z_new
    
    plt.plot(time,pos, 'o', time_new,pos_new, '-')
    plt.xlabel("Time[sec]")
    plt.ylabel("Position on " + pos_c + "-axis[Km]")
    plt.show()

#variables
x_pos=[]
y_pos=[]
z_pos=[]
path = r"C:\Users\Stefi\Desktop\Data\GOCE precise science orbit"

#main
reading_pos(path)


[x_new,time_new,time] = inter_linear(250560,x_pos) 

y_new = inter_linear(250560,y_pos)[0]

z_new = inter_linear(250560,z_pos)[0]


plot_iteration()

#
#
#part 3, transformation from EFC to lon/lat
#
#

#Assumptions: as GOCE has a low elevation we are considering that it does not have a ellipsoidal orbit.
#             Thus, we can consider that R_equ and R_polar are relatively close, such that f = 0
#             This translates into e (eccentricity) = 0 and dz = 0
#             This symplification lets us consider N = R_equ    

# First, we will work on only one data point to see if the solution we used works.
# The solution will be tested using other programs that can obtain the coordinate transformation.


#-5073.646454   1584.258837   3910.342399 some x,y,z value to test
#        Calculated using some site        What we got
#Latitude  : 36.51888   deg N              -17.341105 which is basically 162 - 180
#Longitude : 162.65889   deg E             36.341365
#Height    : 228073.4   m                  227677.297 m

R_equ = 6371
def longitude(x,y):
    lgtude = []
    for i in range(len(x)):
        lda = math.degrees(math.atan2(y[i],x[i]))
        lgtude.append(lda)

    return lgtude

def latitude(x, y, z):
    ltude = []
    for i in range(len(x)):
        rho = math.degrees( math.atan( z[i] / ( math.sqrt ( x[i]**2 + y[i]**2 ) ) ) )
        ltude.append(rho)

    return ltude

def height(x, y, z):
    altitude = []
    for i in range(len(x)):
        h = math.sqrt( x[i]**2 + y[i]**2 + z[i]**2 ) - R_equ 
        altitude.append(h)

    return altitude

#testing de LLH for one day
def latlong(time):#give the number of seconds you want to get out the lat/long position for
    x_test=[]
    y_test=[]
    z_test=[]
    for i in range(time):
        x_test.append(x_new[i])
        y_test.append(y_new[i])
        z_test.append(z_new[i])
    return longitude(x_test,y_test) , latitude (x_test,y_test,z_test) , height (x_test,y_test,z_test)

[lg,lt,ht] =latlong(86400)

def write_latlong(a,b,c):

    LLH = open("LLH.txt","a")
    for i in range(86400):
        LLH.write(str(a[i]) + ' ' + str(b[i]) + ' ' + str(c[i]) + '\n')
write_latlong(lg,lt,ht)

print("done")

img = plt.imread("D:\\Downloads\\EarthMapping") #Just the map where image of Earth is stored.
fig, ax = plt.subplots()
ax.imshow(img, extent=[-180, 180, -90, 90]) #Scale figure to comply with our coordinates, so longtiude from -180 to 180 and latitude from -90 to 90

#from mpl_toolkits.mplot3d import Axes3D as ax  #
#fig = plt.figure()
#axi = fig.gca(projection = '3d')
#axi.plot(x_test,y_test,z_test)
#plt.show()












