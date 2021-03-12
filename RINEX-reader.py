import numpy as np
import random
import datetime
import matplotlib.pyplot as plt

def data_divider(file): #divides rinex file into easier to read sections
    f = open(file, 'r')

    lines = f.readlines()
    lines_noheader = lines[15:(len(lines))]  #removes the top header from the rinex file (no important data for loss of lock info)
    count = 0
    sections = []

    while count < len(lines_noheader):
        words = lines_noheader[count].split(" ") 
        for i in words:
            if i == "":
                words.remove("")

        nr_of_sat = int(words[7]) #determines where it cuts the list to create one data section
        sections.append(lines_noheader[count:count+1+(2*nr_of_sat)]) # one section is one block of dat (subheader+ nr_of_sat*2 lines)
        count+=(nr_of_sat *2)+1
    return(sections)

sections = data_divider("repro.goce2450.13o")


def header(column):  #takes one section
    header = column[0]
    words = header.split(" ")
    header = []
    for i in words:
        if i != "":
            header.append(i)
    
    date = header[0:6]
    
    satellites = header[8:-1]
    return(date, satellites) #returns a list with [year, month, day, hour, minute ,second] and a list with all the sat_nrs [2,7, 4, 18, etc.]

data = []
for i in range(40): #makes a list with 30 sublists (can change) for the number of satellites to divide data per sat
    data.append([])



def llo_detector(string1, string2):
    data_entry = string1.split(" ")
    data_entry.extend(string2.split(" "))

    while ("" in data_entry):
        data_entry.remove("")
    while ("\n" in data_entry):
        data_entry.remove("\n")

    L1_loss = False
    L2_loss = False
    if len(data_entry) == 9:
        if data_entry[1] == '1':
            L1_loss = True
        elif data_entry[2] == '1':
            L2_loss = True
    elif len(data_entry) == 10:
        L1_loss = True
        L2_loss = True

    while ("1" in data_entry):
        data_entry.remove("1")

    float_data_entry = []
    for i in data_entry:
        float_data_entry.append(float(i))

    return [L1_loss,L2_loss]#,float_data_entry



def sat_list(return_list, sections): #takes a list with nr_of_sat amount of sublists to order the data and takes a list divided in sections
    data = return_list
    sections = sections
    for i in sections:
        column = i #one section [s1, s2, s3, etc.]
        
        date, satellites = header(i)
        
        column.pop(0)
        for a in range(0, len(satellites)):
            #connection = [True, False]
            connection = llo_detector(column[2*a], column[(2*a)+1])
           
            if True in connection:
                #add to sat_list
                position = int(satellites[a])-1
                data[position].append([date, connection ])
            else:
                position = int(satellites[a])-1
                data[position].append([date, connection])
    return data


list_of_llo = sat_list(data, sections)


def date_subtraction(date1, date2): # makes the assumption that everything remains in the same month
    time1 = float(date1[-1]) + (float(date1[-2])  + (float(date1[-3]) + float(date1[-4])*24)*60)*60
    time2 = float(date2[-1]) + (float(date2[-2])  + (float(date2[-3]) + float(date2[-4])*24)*60)*60

    delta_time = time2-time1
    return delta_time

def satellite_cluster(data_list_for_one_sat):
    return_list = []
    cluster = []
    start_date = data_list_for_one_sat[0][0]
    cluster.append(data_list_for_one_sat[0])
    count = 1

    while count < len(data_list_for_one_sat):
        if date_subtraction(start_date, data_list_for_one_sat[count][0]) <= 1.01:
            cluster.append(data_list_for_one_sat[count])
            start_date = data_list_for_one_sat[count][0]
            
        else:
            return_list.append(cluster)
            cluster = []
            cluster.append(data_list_for_one_sat[count])
            start_date = data_list_for_one_sat[count][0]
        count+=1
    return_list.append(cluster)
    return return_list





def identify_true_lol(inputlist):
    ignore_section = False # Could be problematic
    actual_losses =[]
    for data_instance in inputlist:
        if data_instance[1] != [False,True]:
            connection_est = inputlist.index(data_instance)
            break
        if inputlist.index(data_instance) == len(inputlist)-1:
            ignore_section = True
            
    #print(connection_est)
    j=0
    #print(inputlist[-j-1][1][0],inputlist[-j-1][1][1],inputlist[-j-2][1][0],inputlist[-j-2][1][1])

    if ignore_section == False:
        for j in range(0,len(inputlist)):
        
            if j == len(inputlist)-1:
                break
            if inputlist[-j-1][1] != [False,True]:
                connection_lost = len(inputlist) - j
                break        
            if (inputlist[-j-1][1] == [False,True] and inputlist[-j-2][1] != [False,True]):
                connection_lost = len(inputlist)-j-1
                break

    #print(connection_lost)    

        for i in range(connection_est, connection_lost):
            #print(i)
            if inputlist[i][1][0] == True or inputlist[i][1][1] == True:
                actual_losses.append(inputlist[i])

    print(actual_losses)

    return actual_losses

# testlist = [[['13', '9', '7', '0', '0', '0.6000000'], [True,True]], [['13', '9', '7', '0', '0', '1.6000000'], [False, True]], [['13', '9', '7', '0', '0', '2.6000000'], [True, False]], [['13', '9', '7', '0', '0', '3.6000000'], [False, False]], [['13', '9', '7', '0', '0', '4.6000000'], [True, True]], [['13', '9', '7', '0', '0', '5.6000000'], [True, False]], [['13', '9', '7', '0', '0', '6.6000000'], [False, True]], [['13', '9', '7', '0', '0', '7.6000000'], [False, True]], [['13', '9', '7', '0', '0', '8.6000000'], [False, True]]]
list_of_actual_lol = []
for i in range(40): #makes a list with 30 sublists (can change) for the number of satellites to divide data per sat
    list_of_actual_lol.append([])
#print(testlist)
#print(identify_true_lol(testlist))
for i in list_of_llo:
    true_lol = []
    count = list_of_llo.index(i)
    if i != []:
        sat_list = satellite_cluster(i)
        for a in sat_list:
            
            new = identify_true_lol(a)
            
            true_lol += new 
    
    
    if true_lol !=[]:
        list_of_actual_lol[count] = true_lol  


print(list_of_actual_lol)

# takes the list and interprets which duration, which freq. , etc. 
def duration_cal(lol_lst):   #list of all the lol of all the satellites [ each satellite[ each second[[datetime],[True,False]], .....   ]   loss of locking points only
    dur_lst = []  #a new list for storing duration and frequency
    for sat_num in lol_lst:  #for each satellite
        if sat_num != []:
            sdate = sat_num[0][0] #start date
            for i in range(len(sat_num)-1):
                edate = sat_num[i][0] #end date is being keep updated
                #if int(sat_num[i+1][0][5]-sat_num[i][0][5]) != 1 or sat_num[i+1][0][4]!=sat_num[i][0][4] or sat_num[i+1][0][3]!=sat_num[i][0][3] or sat_num[i+1][0][2]!=sat_num[i][0][2]:  #if the time is not continous, it is the "end" of loss of connection
                if (float(sat_num[i+1][0][5])-float(sat_num[i][0][5]) > 1 and int(float(sat_num[i+1][0][5])-float(sat_num[i][0][5])) != -59) or (float(sat_num[i+1][0][4])!=float(sat_num[i][0][4]) and int(float(sat_num[i+1][0][5])-float(sat_num[i][0][5])) != -59):
                    print(sdate,edate)
                    duration = (float(edate[5])-float(sdate[5])) + (float(edate[4])-float(sdate[4]))*60 + (float(edate[3])-float(sdate[3]))*3600 + (float(edate[2])-float(sdate[2]))*3600*24 #calculating the duration (days to seconds)
                    if sat_num[i][-1] == [True,True]:  #if both frequency lost connection, store as [1,2]
                        freq = [1,2]
                    else:  #if one of the frequencies lost, find the index+1, either 1 or 2
                        freq = sat_num[i][-1].index(True)+1
                    dur_lst.append([freq,duration])
                    sdate = sat_num[i+1][0] #new start date
            #when the list of that satellite is ran out, the last date time will be the end date
                if(i == len(sat_num)-2):
                    edate = sat_num[i+1][0] 
                    duration = (float(edate[5])-float(sdate[5])) + (float(edate[4])-float(sdate[4]))*60 + (float(edate[3])-float(sdate[3]))*3600 + (float(edate[2])-float(sdate[2]))*3600*24
                    if sat_num[i][-1] == [True,True]:  #if both frequency lost connection, store as [1,2]
                        freq = [1,2]
                    else:  #if one of the frequencies lost, find the index+1, either 1 or 2
                        freq = sat_num[i][-1].index(True)+1
                    dur_lst.append([freq,duration])
    return(dur_lst)

#time of each loss of lock for each frequency
def dur_per_freq(dur_lst):
    L1_lst = []
    L2_lst = []
    for i in dur_lst:
        if i[0] == 1:
            L1_lst.append(i[1])
        elif i[0] == 2:
            L2_lst.append(i[1])
        else:
            L1_lst.append(i[1])
            L2_lst.append(i[1])
    return(L1_lst,L2_lst)

dur_lst = duration_cal(list_of_actual_lol)
print(dur_lst)
L1_lst,L2_lst = dur_per_freq(dur_lst)
print(L1_lst,L2_lst)
for i in L2_lst:
    if i>500:
        L2_lst.remove(i)
        print('I am removed')
plt.hist(L2_lst, bins = 100)#int(max(L2_lst)-min(L2_lst)))
plt.xlabel('Durations')
plt.ylabel('No. of times')
plt.show()




    
