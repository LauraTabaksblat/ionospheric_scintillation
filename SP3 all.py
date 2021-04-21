import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import math
import os
import pickle
import matplotlib.cm as cm
from matplotlib.colors import LogNorm


#functions
def reading_pos(p,day):
    
    for root,dirs,files in os.walk(p):
            if files[day-2].endswith(".IDF"):
            
                with open(os.path.join(root, files[day-2]), 'r') as f:
            
                    lines = f.readlines()
                    i=0
                    for line in lines:
                        
                        if i == 1:
                            if line[0]+line[1] == "PL":
                                x_pos.append(float(line.split()[1]))
                                y_pos.append(float(line.split()[2]))
                                z_pos.append(float(line.split()[3]))
                                
                                
                        if line[0] == '*': #where the measurement should start and stop(HOUR, MINUTE, SECOND)
                            if (line.split()[3] == str(day) and line.split()[4] == '0' and line.split()[5]=='0' and line.split()[6]=='0.00000000') or (line.split()[3] == str(day+1) and line.split()[4] == '0' and line.split()[5]=='0' and line.split()[6]=='0.00000000') : 
                                i=i+1
                                

                f.close()             

def inter_linear(meas_num, pos): 
    time = []

    for j in range(meas_num): #number of point measured every 10 seconds
        time.append(j*10)

    f = scipy.interpolate.interp1d(time, pos,fill_value = "extrapolate")
    time_new = np.arange(0,meas_num*10,1)
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
#print("What day you want to measure",'\n')
#d = int(input())
#reading_pos(path,d)


#[x_new,time_new,time] = inter_linear(8640,x_pos) 

#y_new = inter_linear(8640,y_pos)[0]

#z_new = inter_linear(8640,z_pos)[0]


#plot_iteration()

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

R_equ = 6378
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

#t = 86400
#[lg,lt,ht] = latlong(t)

def write_latlong(a,b,c,time):

    LLH = open("LLH.txt","w")
    LLH.write("Longitude" +'    ' +  "Latitude" +'    ' + "Height" +'    ' + "Second" + '\n' )
    for i in range(time):
        LLH.write(str(a[i]) + ' ' + str(b[i]) + ' ' + str(c[i]) + ' ' + str(i) + '\n' )
#write_latlong(lg,lt,ht,t)




#[['13', '9', '2', '0', '7', '48.6080000'], [lg, lt, ht]]

result = []
for i in range(2,30):#0 to 28
    x_pos=[]
    y_pos=[]
    z_pos=[]

    reading_pos(path, i)

    [x_new,time_new,time] = inter_linear(8640,x_pos) #from here

    y_new = inter_linear(8640,y_pos)[0]

    z_new = inter_linear(8640,z_pos)[0]  #to here, it's just the interpolation
    
    [lg,lt,ht] = latlong(86400) #this will compute 3 lists
    hour = 0
    second = 0
    minute = 0
    for j in range(86400):

        flag = ['13' , '9' , i , hour , minute, second ]
        second = second + 1
        if second == 60 :
            second = 0
            minute = minute + 1
        if minute == 60:
            hour = hour +1
            minute = 0
        result.append(([flag,[lg[j],lt[j],ht[j]]]))


with open("time_list.txt", "rb") as fp:
    time_listread = pickle.load(fp)

loss_location_lst = []
unfound_lst = []

for loss in time_listread:
    timestamp = int(loss[0][2])*24*60*60 + int(loss[0][3])*60*60 + int(loss[0][4])*60 + int(float(loss[0][5]))
    
    if int(loss[0][2]) == int(result[timestamp][0][2]) and int(loss[0][3]) == int(result[timestamp][0][3]) and int(loss[0][4]) == int(result[timestamp][0][4]) and int(float(loss[0][5])) == int(float(result[timestamp][0][5])):
            
        loss_location_lst.append([result[timestamp][1],loss[1]])
    else:
        unfound_lst.append(timestamp)        

#print(unfound_lst)



#[0]= -180
#long +180
#lat + 90

coord_list = np.zeros([360,180], dtype = int) #360 rows , 180 cols

for loss in loss_location_lst:
    coord_list[int(loss[0][0])+180][int(loss[0][1]+90)] +=1

#print(coord_list)
    
img = plt.imread("EarthMapping.png")
fig, ax = plt.subplots()
ax.imshow(img, extent=[0, 360, 0, 180])        

cmaps = ['Greys']
longit = []
lat = []
multitude = []

C=[]
for i in range(0,360):
    for j in range(0,180):
        C.append(coord_list[i][j])
        if coord_list[i][j] != 0:
            
            longit.append(i)
            lat.append(j)
            multitude.append(coord_list[i][j])
            
plt.scatter( longit , lat , c = multitude, marker =',' ,cmap='Reds' )
print("done")

#plt.colorbar()
            
plt.show()


#cmaps['Sequential'] = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']














#from mpl_toolkits.mplot3d import Axes3D as ax  #
#fig = plt.figure()
#axi = fig.gca(projection = '3d')
#axi.plot(x_test,y_test,z_test)
#plt.show()


#










