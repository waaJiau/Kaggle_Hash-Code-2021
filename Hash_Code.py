# -*- coding= utf-8 -*-
from collections import defaultdict, Counter
from random import shuffle
import time

sTime = time.time()
#~ ------------------------------------------------------------------------------------------------------------------------------
#~ ------    Import information
#~ ------------------------------------------------------------------------------------------------------------------------------
#? ======================== input the name of data file ========================
data = ".\Data\hashcode.in"

#& ------------------------------------------------------------------------------------------------------------------------------
#& ------    Initializing Condition
#& ------------------------------------------------------------------------------------------------------------------------------
#? ====================== reading the content of data file =====================
with open( data, mode= "r") as f:
    temp = f.readlines()

data_cont = [ line.rstrip( "\n") for line in temp]

#? ========= getting the initial condition from first line of data file ========
first_line = data_cont[ 0].split()
duration, intersections, streets, cars, score = [ int( ele) for ele in first_line]

#? ===== slicing the parts of streets information and cars trip information ====
street_lines = data_cont[ 1: streets +1]
car_lines = data_cont[ streets +1:]

#? ============== preparing the storage space of result dataframe ==============
streets_df = {}
cars_df = {}

#$ ------------------------------------------------------------------------------------------------------------------------------
#$ ------    Defined class
#$ ------------------------------------------------------------------------------------------------------------------------------
def street_information( line: str) -> list:
    temp = line.split( " ") # would be split into 4 parts, ( start, end, name of street, length of street)

    name = temp[ 2]
    start = int( temp[ 0])
    end = int( temp[ 1])
    length = int( temp[ 3])

    return name, [ start, end, length]

def road_trip( line: str) -> list:
    temp = line.split( " ")

    total_road = int( temp[ 0])
    trip = temp[ 1:]

    return total_road, trip

#! ------------------------------------------------------------------------------------------------------------------------------
#! ------    Running Code
#! ------------------------------------------------------------------------------------------------------------------------------
#? ===================== organized the streets information =====================
for line in street_lines:
    str_name, str_infor = street_information( line= line)
    streets_df[ str_name] = str_infor                           # data type: name of street: information of street

#? ==================== organized the cars trip information ====================
for count, line in enumerate( car_lines, 1):
    _, trip = road_trip( line= line)
    cars_df[ count] = trip                                      # data type: car no.: road trip

#todo ================ road catergorize to severl intersections ================
trip_map_destination = {}
for streetname, infor in streets_df.items():
    # just checking how many intersection that been used
    trip_map_destination[ streetname] = infor[ 1]               #* is the total number of intersections putting in the first line on answer sheet

#todo ===== counting the amount of incoming streets for each intersections =====
incoming_count = defaultdict( Counter)
for car, trip in cars_df.items():
    for streetname in trip:
        # double dictionary data type, because want to count incoming streets
        incoming_count[ trip_map_destination[ streetname]][ streetname] += 1        #* could output the no. of intersection and how many number of incoming streets

#@ ================== calculating about traffic light setting ==================
schedules = []
for num_inter in range( intersections):
    #* =================== relisting the incoming_count list ===================
    arr = list( incoming_count[ num_inter].items())
    schedules.append( arr)

#@ ======================= Parse solution into submission ======================
submission = []
submission.append( [ len( schedules)])
for num_inter, road_trip in enumerate( schedules):
    if not road_trip:
        submission[ 0][ 0] -= 1
        continue
    submission.append( [ num_inter])
    submission.append( [ len( road_trip)])

    for streetname, green_light in road_trip:
        submission.append( [ streetname, green_light])

#? ===== writting to the submission.csv =====
output_cont = "\n".join( " ".join( str( ele) for ele in element) for element in submission)

with open( "submission.csv", mode= "w") as file:
    file.write( output_cont)

eTime = time.time()
print( "", "****************************************************************************************", "", sep= "\n")
print( "Total Spending Time: {} min, {} sec".format( ( eTime - sTime) //60, round( ( eTime - sTime) %60)))
print( "", "****************************** End of Calculating Database *****************************", "", sep= "\n")
