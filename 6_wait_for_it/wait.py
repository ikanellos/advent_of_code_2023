#!/usr/bin/python

##########################
# AoC Day 6: Wait for it #
##########################
import sys 
##########################
# inits
input_file = sys.argv[1]
##########################
# Main

# Parse times and distances in a list
available_times     = []
record_distances = []
# margin of error - our desired value
margin_of_error = 1

with open(input_file) as f:
    for line in f:
        line = line.strip()
        pref, data = line.split(":")
        if "time" in pref.lower():
            available_times = [int(number) for number in data.strip().split(" ") if number]
        if "distance" in pref.lower():
            record_distances = [int(number) for number in data.strip().split(" ") if number]
'''
print ("Times:", available_times)
print ("Distances:", record_distances)
'''

# Distance travelled formula:
# button_press_time in range(0,button_times[i]+1)
# distance travelled button_press_time * button_times[i]- button_press_time

# Create a list of valid button press times for each race
for i in range(len(available_times)):

    # current record
    record = record_distances[i]
    # time available
    available_time = available_times[i]

    # List of winning button times (zero time will not move us at all, so ignore it)
    winning_button_times = [time for time in list(range(1, available_time+1)) if (available_time - time) * time > record]

    # Update error margin
    margin_of_error *= len(winning_button_times)

print (f"Error margin: {margin_of_error}")

# Join kerning for time
available_time = [str(time) for time in available_times]
available_time = "".join(available_time)
available_time = int(available_time)
# join kerning for distance
record_distance = [str(dist) for dist in record_distances]
record_distance = "".join(record_distance)
record_distance = int(record_distance)

winning_times   = [time for time in list(range(1, available_time+1)) if (available_time - time) * time > record_distance]
print ("Num winning times after kerning fix:", len(winning_times))


