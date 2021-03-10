import numpy as np
import random
import datetime


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

sections = data_divider("redpro.goce2730(1).13o")


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
for i in range(30): #makes a list with 30 sublists (can change) for the number of satellites to divide data per sat
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

    return [L1_loss,L2_loss],float_data_entry



def sat_list(return_list, sections): #takes a list with nr_of_sat amount of sublists to order the data and takes a list divided in sections
    data = return_list
    sections = sections
    for i in sections:
        column = i #one section [s1, s2, s3, etc.]
        
        date, satellites = header(i)
        
        column.pop(0)
        for a in range(0, len(satellites)):
            #connection = [True, False]
            connection, da  = llo_detector(column[2*a], column[(2*a)+1])
           
            if True in connection:
                #add to sat_list
                position = int(satellites[a])-1
                data[position].append([date, connection ])
            else:
                position = int(satellites[a])-1
                data[position].append([date, connection])
    return data


list_of_llo = sat_list(data, sections)
def date_subtraction(date1, date2):
    time1 = date1[-1] + date1[-2] + date1[-3] + date1[-4]

def satellite_cluster(data_list_for_one_sat):
    start_date = []
    for i in data_list_for_one_sat:
        if start_date == []:
            start_date = i
    
        
        
#print(list_of_llo)
        


#

# input = [[[yy],[mm],[dd],[hh],[mm],[ss]],[[True],[True]]
#          [[yy],[mm],[dd],[hh],[mm],[ss]],[[True],[True]]
#         ]

def identify_true_lol(totallist):
    actual_losses = []
    j = 0
    for inputlist in totallist:
        for data_instance in inputlist:
            if data_instance[1][0] == False and data_instance[1][1] == False:
                connection_est = inputlist.index(data_instance)
                break

        for data_instance in reversed(enumerate(inputlist)):
            if data_instance[1][0] == False and data_instance[1][1] == False:
                connection_lost = inputlist.index(data_instance)
                break
            
        for i in range(connection_est,connection_lost):
            if inputlist[i][1][0] == True or inputlist[i][1][1] == True:
                actual_losses[j].append(inputlist[i])

        j = j + 1

    return actual_losses

print(identify_true_lol(list_of_llo))
    
"""i = 0
connection_established = False
while inputlist[i][1][0] == False and inputlist[i][1][1] == False and connection_established = False:
    connection_established = True
     i_connection = i

    i = len(inputlist)
    connection_terminated = False
    while inputlist[i][1][0] == False and inputlist[i][1][1] == False and connection_established = False:
        connection_established = True
        i_connection = i
        """




"""
# takes the list and interprets which duration, which freq. , etc. 
for i in xx:  #xx - the list of the specific satellite
    sdate = xx[0]  #start date
    edate = xx[-1]   #end date
    duration = (edate[5]-sdate[5]) + (edate[4]-sdate[4]*60 + (edate[3]-sdate[3]*3600))  #loss of lock duration in seconds
    

 """



    
