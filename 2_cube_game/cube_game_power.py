#!/usr/bin/python

##################################
# Prototyping game in python.    #
# Will then try porting to mojo. #
##################################
# IMPORTS
import sys
##################################
# Function definintions
def game_run_to_dict(game_run_string: str) -> dict:
    '''Returns a dictionary for red/green/blue numbers'''
    game_run_dictionary = {}
    game_run_string = game_run_string.strip()
    cube_data = game_run_string.strip().split(",")
    for cube in cube_data:
        cube = cube.strip()
        num_cubes, cube_color = cube.split(" ")
        num_cubes = int(num_cubes)
        # Add to game runs
        game_run_dictionary[cube_color] = num_cubes
    # Return dictionary
    return game_run_dictionary
# ------------------------------------------------------ #
def get_game_dictionary(input_line: str) -> dict:
    '''Split input line to individual games and the index'''
    game_index, game_data = input_line.split(":")
    # Get num of index
    game_index = int(game_index.replace("Game ", ""))  
    game_data  = game_data.split(";")
    game_data  = [game_run_to_dict(game) for game in game_data]

    return game_index, game_data
# -------------------------------------------------------------------- #
##################################
# Initializations & Args

# File containing input
input_file = sys.argv[1]
# The running sum of valid game idexes
sum_of_powers = 0
##################################
# Main function

# Read input
with open(input_file) as f:
    for line in f:

        line = line.strip()

        game_index, game_runs = get_game_dictionary(line)
        print (f"Index: {game_index} | Runs: {game_runs}")

        # To get the minimum number for each color we need to get the maximum of individual runs
        red_list = [item["red"] if "red" in item else 0 for item in game_runs]
        blue_list = [item["blue"] if "blue" in item else 0 for item in game_runs]
        green_list = [item["green"] if "green" in item else 0 for item in game_runs]

        min_red = max(red_list)
        min_blue = max(blue_list)
        min_green = max(green_list)

        min_power = min_red * min_blue * min_green
        # print (f"POWER:{min_power}|Red:{min_red}|Green:{min_green}|Blue:{min_blue}")

        sum_of_powers += min_power

print (f"Sum of powers: {sum_of_powers}")
        
    

        



