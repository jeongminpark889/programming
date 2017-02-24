# programming
Airline seating programming assignment

Nikunj(16201361)
Jeongmin Park(16203906)

To Assign seats to each passenger according to the booking, 

Firstly, we create coneection to databese file to python and read csv.file as input.
Then, we made codes to check for the occupied seats and group them by row and seat.
To assign seats to customers at last, we put codes to check for the non-occupied seats and group them by row and seat.
For updating the matrices depenging on refused seats and seperated seats, we defined a fucntion as "update_tables()".
Also, we made functions to update the seating table and the metrics.
A "place_bookings" funtion checks the booking list and loops over the list one by one ,and calls the function(update_tables).
: "count_passengers_refused" counts for refused passengers in a booking
  "count_passengers_seperated" counts for seperated passengers in a booking
Finally, by funtions, 'final seating', we get the final seating table view and by 'final metrics', we get the final metrics table view with the updated values for passengers refused and passengers not seating together
customers and by booking numbers. Through tables and matrices, we checked the occupied seats and layout of customers in filght. Furthermore, we could obtain the table and matrices of customers refused and seperated. 
