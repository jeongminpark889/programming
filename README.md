# programming
programming
import numpy as np 
from numpy import matrix
import pandas as pd 
import sqlite3
from __future__ import division, print_function 
import math
con = sqlite3.connect('airline_seating.db')
con.text_factory = str
cur = con.cursor()
def file_read_total_bookings():
    total_bookings=pd.read_csv('bookings.csv', names=['passsenger_name','passenger_count'])
    total_count = np.array([total_bookings['passenger_count']])
    total_bookings_array=np.array(total_bookings)
    #print(total_count)
    return total_bookings_array, total_count

total_bookings_array,total_count=file_read_total_bookings()

def seats_occupied_in_seating_table_db():
    seats_occupied_in_seating = []
    for row in cur.execute('select row, seat,name from seating where name != "" group by row,seat '):
        seats_occupied_in_seating.append(row)
        seats_occupied_in_seating_array=list(seats_occupied_in_seating)
        seats_occupied_in_seating_array=np.array(seats_occupied_in_seating_array)
    return seats_occupied_in_seating_array

seats_occupied_in_seating_array=seats_occupied_in_seating_table_db()
print(seats_occupied_in_seating_array)

def seats_not_occupied_in_seating_table_db():
    seats_not_occupied_in_seating = []
    for row in cur.execute('select row, seat,name from seating where name = "" group by row,seat '):
        seats_not_occupied_in_seating.append(row)
        Seats_no_occupied_array=list(seats_not_occupied_in_seating)
        Seats_no_occupied_array=np.array(Seats_no_occupied_array)
    return Seats_no_occupied_array

Seats_no_occupied_array=seats_not_occupied_in_seating_table_db()
print(Seats_no_occupied_array)


def update_tables(cnt_book,cnt_name_passenger,counter):
    data = cur.execute('''SELECT * From seating''')
    data=data.fetchall()
    for j in xrange(counter,counter+cnt_book,1):
          if Seats_no_occupied_array[j][2]=="":
                Seats_no_occupied_array[j][2]=cnt_name_passenger
                cur.execute('''UPDATE seating SET name=? WHERE row=? and seat=?''', (cnt_name_passenger,Seats_no_occupied_array[j][0],Seats_no_occupied_array[j][1]))
           
                
    return 
def place_bookings():
    counter=0
    
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
             update_tables(cnt_book,cnt_name_passenger,counter)
                
    return Seats_no_occupied_array    
Seats_final_occupied_array=place_bookings()
print(Seats_final_occupied_array)

for row in cur.execute('select * from seating'):
    print(row)
