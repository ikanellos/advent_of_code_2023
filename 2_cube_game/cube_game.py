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
def game_possible(game_runs_list: list[dict]) -> bool:
    '''Return whether all game runs are valid or not'''

    for game_run in game_runs_list:
        if not game_run_possible(game_run):
            return False
    
    return True
# -------------------------------------------------------------------- #
def game_run_possible(game_dictionary: dict) -> bool:
    '''
    Return true if a game state validates the number of items specified
    
    Args:
        - game_cube_dictionary (dict): contains  a game state, storing 
                                       the number of cubes per color shown

    Returns:
        is_possible (Boolean): whether a game violates the number of max cubes per color or not
    '''
    global red_cubes
    global green_cubes
    global blue_cubes

    if "red" in game_dictionary and red_cubes < game_dictionary["red"]\
        or "blue" in game_dictionary and blue_cubes < game_dictionary["blue"]\
        or "green" in game_dictionary and green_cubes < game_dictionary["green"]:
        return False
    else:
        return True
##################################
# Initializations & Args

# Total number of cubes per type
red_cubes   = 12
green_cubes = 13 
blue_cubes  = 14

# File containing input
input_file = sys.argv[1]
# The running sum of valid game idexes
sum_of_indexes = 0
##################################
# Main function

# Read input
with open(input_file) as f:
    for line in f:

        line = line.strip()

        game_index, game_runs = get_game_dictionary(line)
        # print (f"Index: {game_index} | Runs: {game_runs}")

        is_game_possible = game_possible(game_runs)

        if is_game_possible:
            # print (f"Game: {game_index} is possible with: {game_runs}")
            sum_of_indexes += game_index
        '''
        else:
            print (f"Game: {game_index} is impossible with: {game_runs}")
        '''

print (f"Sum of indexes: {sum_of_indexes}")

        



