#
# Project 1: CTA L analysis app
# description: This app goes through some general stats like number of stations, stops or ride entries
# Name: Karol Cieslikowski / UIN:662075108
#

import sqlite3
import matplotlib.pyplot as plt
import datetime


##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()

    print("General stats:")

    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone()
    print("  # of stations:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone()
    print("  # of stops:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone()
    print("  # of ride entries:", f"{row[0]:,}")
    
    dbCursor.execute("Select min(Ride_Date) From Ridership;")
    row = dbCursor.fetchone()
    start_date = row[0]
    dbCursor.execute("Select max(Ride_Date) From Ridership;")
    row = dbCursor.fetchone()
    last_date = row[0]
    print("  date range:", f"{start_date[:10]} - {last_date[:10]}")
    
    dbCursor.execute("Select sum(Num_Riders) From Ridership;")
    row = dbCursor.fetchone()
    total_ridership = row[0]
    print("  Total ridership:", f"{total_ridership:,}")

    dbCursor.execute("Select sum(Num_Riders) From Ridership Where Type_of_Day = 'W';")
    row = dbCursor.fetchone()
    weekday_ridership_pers = row[0]/total_ridership
    print("  Weekday ridership:", f"{row[0]:,}", f"({weekday_ridership_pers:.2%})")

    dbCursor.execute("Select sum(Num_Riders) From Ridership Where Type_of_Day = 'A';")
    row = dbCursor.fetchone()
    saturday_ridership_pers = row[0]/total_ridership
    print("  Saturday ridership:", f"{row[0]:,}", f"({saturday_ridership_pers:.2%})")

    dbCursor.execute("Select sum(Num_Riders) From Ridership Where Type_of_Day = 'U';")
    row = dbCursor.fetchone()
    holiday_ridership_pers = row[0]/total_ridership
    print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({holiday_ridership_pers:.2%})")
    
    print()

# Command 1  
# input a partial station name from the user (sql wildcards _ and % allowed)
# and retrieve the stations are "like" the users input
def partial_name(dbConn) :

  print()
  dbCursor = dbConn.cursor()
  qwery = input('Enter partial station name (wildcards _ and %): ')
  sql = "Select * From Stations Where Station_Name like ? Order By Station_Name;"
  dbCursor.execute(sql, [qwery])
  rows = dbCursor.fetchall()
  if rows:
      for row in rows:
          print(*row, sep=' : ')
  else:
      print("**No stations found...")
  print()
  
# Command 2
# output the ridership at each station, in ascending order by station name
def ridership_each_station(dbConn):

  print("** ridership all stations **")
  dbCursor = dbConn.cursor()
  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  row = dbCursor.fetchone()
  total_ridership = row[0]
  sql = '''
  Select Station_ID, Station_Name
  From Stations
  Order By Station_Name
  ;'''
  dbCursor.execute(sql)
  stations = dbCursor.fetchall()
  for station_ID, station_name in stations:
      sql = "Select Sum(Num_Riders) From Ridership Where station_ID=?"
      dbCursor.execute(sql, [station_ID])
      riders = dbCursor.fetchone()[0]
      persents = riders/total_ridership
      print(f"{station_name} : {riders:,} ({persents:.2%})")
  print()

# Command 3  
# output the top 10 stations in terms of ridership,
# in descending order by ridership if least=False
# Command 4
# output the least 10 stations in terms of ridership
# in ascending order by ridership if least=True
def ridership_top_10(dbConn, least=False):

  if least:
    print("** least-10 stations **")
    order = 'ASC'
  else:
    print("** top-10 stations **")
    order = 'DESC'
  dbCursor = dbConn.cursor()

  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  row = dbCursor.fetchone()
  total_ridership = row[0]
  
  sql = f'''
  Select Station_ID, Sum(Num_Riders) as Total
  From Ridership
  Group By Station_ID
  Order By Total {order}
  ;'''

  dbCursor.execute(sql)
  rows = dbCursor.fetchmany(10)
  
  for station_ID, riders in rows:
      sql = "Select Station_Name From Stations Where station_ID=?"
      dbCursor.execute(sql, [station_ID])
      station_name = dbCursor.fetchone()[0]
      persents = riders/total_ridership
      print(f"{station_name} : {riders:,} ({persents:.2%})")
  print()


# Command 5
# input a line color from the user and output all the stop names
# that are a part of that line, in ascending order
def show_stops_colour(dbConn):

  color = input("\nEnter a line color (e.g. Red or Yellow): ")
  #.strip().capitalize()
  
  dbCursor = dbConn.cursor()
  # dbCursor.execute("Select Line_ID From Lines where Color like ?;",[color])
  dbCursor.execute('''
  Select Stop_Name, Direction, ADA
  From Stops
  Inner Join StopDetails
  on Stops.Stop_ID = StopDetails.Stop_ID
  Inner Join Lines
  on StopDetails.Line_ID = Lines.Line_ID
  Where Lines.Color like ?
  Order By Stop_Name asc
  ;''',[color])
  rows = dbCursor.fetchall()
  #if row is not None:
   #   line_ID = row[0]
  #else:
    #  print("**No such line...\n")
   #   return
  # dbCursor.execute('''
  # Select Stop_Name, Direction, ADA
  #From Stops
  #Where Stop_ID in (Select Stop_ID From StopDetails Where line_ID=?)
  #Order By Stop_Name ;''',[line_ID])
  #rows = dbCursor.fetchall()
  if len(rows) == 0:
    print("**No such line...\n")
    return
    
  for row in rows:
      if row[2] == 1:
          acces = 'yes'
      else:
          acces = 'no'
      print(f"{row[0]} : direction = {row[1]} (accessible? {acces})")
  print()

# this is a function used for rest of the function like
# ridership_by_month and ridership_by_year
def plot_ridership(rows, x_lbl, y_lbl, title):
  x = []
  y = []
  for row in rows:
    x.append(row[0])
    y.append(row[1])
  plt.xlabel(x_lbl)
  plt.ylabel(y_lbl)
  plt.title(title)
  plt.plot(x,y)
  plt.show()

# outputs the total ridership by month in ascending order by month
# After the output, the user is given an option to plot the data

def ridership_by_month(dbConn):

  print("** ridership by month **")
  dbCursor = dbConn.cursor()
  sql = '''
  Select strftime('%m', Ride_Date) as month, Sum(Num_Riders)
  From Ridership
  Group By month
  Order By month;
  '''
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  for row in rows:
    print(f"{row[0]} : {row[1]:,}")
  print()
  to_plot = input('Plot? (y/n) \n').lower().strip()
  if to_plot == 'y':
    plot_ridership(rows, 'month', 'number of riders(*10^8)', 'monthly ridership')
    print()

# outputs the total ridership by year in ascending order by year
# After the output, the user is given an option to plot the data
def ridership_by_year(dbConn):

  print("** ridership by year **")
  dbCursor = dbConn.cursor()
  sql = '''
  Select strftime('%Y', Ride_Date) as year, Sum(Num_Riders)
  From Ridership
  Group By year
  Order By year;
  '''
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  for row in rows:
    print(f"{row[0]} : {row[1]:,}")
  print()
  to_plot = input('Plot? (y/n) \n').lower().strip()
  if to_plot == 'y':
    plot_ridership(rows, 'year', 'number of riders(*10^8', 'yearly ridership')
    print()


# this function is used for the 8th command where it needs two stations
def show_plot_two_stations(st1, st2, Station1_Name, Station2_Name, year):

  x1 = [int(datetime.datetime.strptime(st[0], "%Y-%m-%d").strftime('%j')) for st in st1]
  y1 = [st[1] for st in st1]
  x2 = [int(datetime.datetime.strptime(st[0], "%Y-%m-%d").strftime('%j')) for st in st2]
  y2 = [st[1] for st in st2]

  plt.xlabel('day')
  plt.ylabel('number of riders')
  plt.plot(x1,y1, label = Station1_Name)
  plt.plot(x2,y2, label = Station2_Name)
  plt.title(f"riders each day of {year}")
  plt.legend()
  plt.show()


# Inputs a year and the names of two stations (full or partial name)
# and then outputs the daily ridership at each station for that year
# Since the output would be quite long, you should only output
# the first 5 days and last 5 days for each station
def plot_two_stations(dbConn):

  dbCursor = dbConn.cursor()

  year = input("\nYear to compare against? ").strip()
  station_1 = input("\nEnter station 1 (wildcards _ and %): ")
  sql = "Select * From Stations Where Station_Name like ?;"
  dbCursor.execute(sql, [station_1])
  rows = dbCursor.fetchall()
  if len(rows) < 1:
    print("**No station found...\n")
    return
  elif len(rows) > 1:
    print("**Multiple stations found...\n")
    return
  Station_1_Name = rows[0][1]
  Station_1_ID = rows[0][0]

  station_2 = input("\nEnter station 2 (wildcards _ and %): ")
  sql = "Select * From Stations Where Station_Name like ?;"
  dbCursor.execute(sql, [station_2])
  rows = dbCursor.fetchall()
  if len(rows) < 1:
    print("**No station found...\n")
    return
  elif len(rows) > 1:
    print("**Multiple stations found...\n")
    return
  Station_2_Name = rows[0][1]
  Station_2_ID = rows[0][0]

  sql = '''
  Select strftime('%Y-%m-%d', Ride_Date) as date, Sum(Num_Riders)
  From Ridership
  Where strftime('%Y', Ride_Date) = ? and Station_ID = ?
  Group By date
  Order By date;
  '''

  dbCursor.execute(sql,[year, Station_1_ID])
  st1 = dbCursor.fetchall()

  dbCursor.execute(sql,[year, Station_2_ID])
  st2 = dbCursor.fetchall()  

  print(f"Station 1: {Station_1_ID} {Station_1_Name}")
  for row in st1[:5] + st1[-5:]:
    print(f"{row[0]} {row[1]}")

  print(f"Station 2: {Station_2_ID} {Station_2_Name}")
  for row in st2[:5] + st2[-5:]:
    print(f"{row[0]} {row[1]}")
    
  print()
  to_plot = input('Plot? (y/n) \n').lower().strip()
  if to_plot == 'y':
      show_plot_two_stations(st1, st2, Station_1_Name, Station_2_Name, year)
      print()

  
# out the plot, where we plot the locations of the stations
# overlaying a map of Chicago. The map is provided as an image file
def plot_map(rows, color):

  x = [row[2] for row in rows]
  y = [row[1] for row in rows]

  image = plt.imread("chicago.png")
  xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
  plt.imshow(image, extent=xydims)
  plt.title(color + "line")

  if (color.lower() == "purple-express"):
    color = "Purple"

  plt.plot(x, y, "o", c=color)

  for row in rows:
    plt.annotate(row[0], (row[2]+0.02, row[1]+0.02))

  plt.xlim([-87.9277, -87.5569])
  plt.ylim([41.7012, 42.0868])
  plt.show()


# Input a line color from the user and output all station names
# that are of that line in ascending order
def color_station_names(dbConn):

  color = input("\nEnter a line color (e.g. Red or Yellow): ").strip().capitalize()
  if "-" in color:
      color = "-".join([word.capitalize() for word in color.split("-")])

  dbCursor = dbConn.cursor()
  dbCursor.execute("Select Line_ID From Lines Where Color=?;",[color])
  row = dbCursor.fetchone()
  if row is not None:
    line_ID = row[0]
  else:
    print("**No such line...\n")
    return
  dbCursor.execute('''
  Select Distinct  Stations.Station_Name, Stops.Latitude, Stops.Longitude
  From Stops, Stations
  Where Stops.Stop_ID in (Select Stop_ID From StopDetails Where line_ID=?)
  And Stops.Station_ID = Stations.Station_ID
  Order By Stations.Station_Name
  ;''',[line_ID])

  rows = dbCursor.fetchall()
  for row in rows:
    print(f"{row[0]} : ({row[1]}, {row[2]})")
  print()
  to_plot = input('Plot? (y/n) \n').lower().strip()
  if to_plot == 'y':
    plot_map(rows, color)
    print()             
  

def main():

  print('** Welcome to CTA L analysis app **')
  print()
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  print_stats(dbConn)
  while True:
      user_input = input("Please enter a command (1-9, x to exit): ").lower().strip()
      if user_input == 'x':
          break
      elif user_input == '1':
          partial_name(dbConn)
      elif user_input == '2':
          ridership_each_station(dbConn)
      elif user_input == '3':
          ridership_top_10(dbConn)
      elif user_input == '4':
          ridership_top_10(dbConn, True)
      elif user_input == '5':
          show_stops_colour(dbConn)
      elif user_input == '6':
          ridership_by_month(dbConn)
      elif user_input == '7':
          ridership_by_year(dbConn)
      elif user_input == '8':
          plot_two_stations(dbConn)
      elif user_input == '9':
          color_station_names(dbConn)
      else:
          print('**Error, unknown command, try again...\n')
  print()


if __name__ == "__main__":
    main()

#
# done
#
