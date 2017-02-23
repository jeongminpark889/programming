
# coding: utf-8

# In[ ]:

#********************************** Airline Seating Assignment ********************************** 

#******************** Nikunj(16201361),Jeongmin Park(16203906)***************************************

#*************** importing all the necessary libraries***********************************

import numpy as np 
import collections
from numpy import matrix
import pandas as pd 
import sqlite3
from __future__ import division, print_function 
import math

#******creating connection to the databse**************************

con = sqlite3.connect('/Users/Nikunj/Downloads/airline_seating.db')
con.text_factory = str  
cur = con.cursor()           #cursor


# Reading the input CSV file
def file_read_total_bookings():
    total_bookings=pd.read_csv('/Users/Nikunj/Downloads/bookings.csv', names=['passsenger_name','passenger_count'])
    total_count = np.array([total_bookings['passenger_count']])
    total_bookings_array=np.array(total_bookings)
    #print(total_count)
    return total_bookings_array, total_count

total_bookings_array,total_count=file_read_total_bookings()


# Checking for the occupied seats and grouping themby row,seat
def seats_occupied_in_seating_table_db():
    seats_occupied_in_seating = []
    for row in cur.execute('select row, seat,name from seating where name != "" group by row,seat '):
        seats_occupied_in_seating.append(row)
        seats_occupied_in_seating_array=list(seats_occupied_in_seating)
        seats_occupied_in_seating_array=np.array(seats_occupied_in_seating_array)
    return seats_occupied_in_seating_array

seats_occupied_in_seating_array=seats_occupied_in_seating_table_db()
print(seats_occupied_in_seating_array)


# Checking for the non-occupied seats and grouping themby row,seat
def seats_not_occupied_in_seating_table_db():
    seats_not_occupied_in_seating = []
    for row in cur.execute('select row, seat,name from seating where name = "" group by row,seat '):
        seats_not_occupied_in_seating.append(row)
        Seats_no_occupied_array=list(seats_not_occupied_in_seating)
        Seats_no_occupied_array=np.array(Seats_no_occupied_array)
    return Seats_no_occupied_array

Seats_no_occupied_array=seats_not_occupied_in_seating_table_db()
print(Seats_no_occupied_array)


# Defining a function to update the table metrics
def update_metrics_table_in_db(count_passengers_refused,count_passengers_seperated):
    cur.execute('''INSERT INTO metrics(passengers_refused,passengers_separated)
                  VALUES(?,?)''', (count_passengers_refused,count_passengers_seperated))
    
    return


#DEfining a function to update the seating table and also update teh metrics tablle 

def update_tables(cnt_book,cnt_name_passenger,counter,seats_occupied_in_seating_array):
    count_passengers_refused=0
    count_passengers_seperated=0
    data = cur.execute('''SELECT * From seating''')
    data=data.fetchall()
    array_seperated_passengers=[]
    for j in xrange(counter,counter+cnt_book,1):
            if Seats_no_occupied_array[j][2]=="":
                Seats_no_occupied_array[j][2]=cnt_name_passenger
                
                cur.execute('''UPDATE seating SET name=? WHERE row=? and seat=?''', (cnt_name_passenger,Seats_no_occupied_array[j][0],Seats_no_occupied_array[j][1]))
                #if Seats_no_occupied_array[j][2]
                update_metrics_table_in_db(count_passengers_refused,count_passengers_seperated)
                array_seperated_passengers.append(Seats_no_occupied_array[j][0])
                
    #print(array_seperated_passengers)
    if len(array_seperated_passengers)!=1 & len(set(array_seperated_passengers))!=1:
        most_common = collections.Counter(array_seperated_passengers).most_common()[1]
        count_passengers_seperated=most_common[1]
        update_metrics_table_in_db(count_passengers_refused,count_passengers_seperated)
        
                     
    return Seats_no_occupied_array


# This functions checks the bookimng list and loops over the list one by one and calls the function(update_tables)

def place_bookings(total_bookings_array,total_count=file_read_total_bookings(),seats_occupied_in_seating_array=seats_occupied_in_seating_table_db()):
    counter=0
    count_passengers_refused=0                    #count for refused passengers in a booking
    count_passengers_seperated =0                 #count for seperated passengers in a booking
    for i in range(total_bookings_array.shape[0]):
        cnt_book=total_bookings_array[i][1]
        cnt_name_passenger=total_bookings_array[i][0]
        if i==0:
            counter=0
        if i!=0:
            counter=counter +total_bookings_array[i-1][1]
             
   
        Max_rows_seating =Seats_no_occupied_array.shape[0]
        #print(Max_rows_seating)
        if counter+cnt_book<=Max_rows_seating :
             update_tables(cnt_book,cnt_name_passenger,counter,seats_occupied_in_seating_array)
        
        if counter+cnt_book>Max_rows_seating : 
             count_passengers_refused= cnt_book
            
             update_metrics_table_in_db(count_passengers_refused,count_passengers_seperated) #updating the metrics table
                
    return Seats_no_occupied_array 

