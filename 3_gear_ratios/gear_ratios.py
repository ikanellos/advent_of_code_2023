#!/usr/bin/python

#############################
# Advent of code 2023 day 3 #
#############################
# Imports
import sys 
#############################
# Function definitions

def is_digit(character: str) -> bool:
    '''Return true if character is a digit'''
    try:
        char_digit = int(character)
    except:
        return False
    return True
# -------------------------------------------------- #
def num_index_dict(num_string: str, current_index: int) -> list:
    '''Return a list containing the number as int, a tuple 
       (start_idx, end_idx), and a boolean valued false, 
       denoting whether the number has been added to the 
       running sum.
    '''
    num_string_len = len(num_string)
    num = int(num_string)
    return [num, (current_index - num_string_len + 1, current_index), False]
# -------------------------------------------------- #
def get_line_data_dict(input_line: str) -> dict:
    '''Return a dictionary with numbers and valid symbols along with their indexes'''
    data_dict = {}
    # List of symbol indexes
    data_dict["symbol_indexes"] = []
    data_dict["num_indexes"] = []
    data_dict["star_indexes"] = []
    # buffer of nums
    num_buffer = ""
    for index, character in enumerate(input_line):
        # Create a running buffer of number string
        if is_digit(character):
            num_buffer += character
        else:
            if num_buffer:
                num_struct = num_index_dict(num_buffer, index-1)
                data_dict["num_indexes"].append(num_struct)
                num_buffer = ""
            # Add the symbol index, ignore dots
            if character != '.':
                data_dict["symbol_indexes"].append(index)
                # Add a star related index to the dictionary
                if character == '*':
                    # we will keep an empty list along with the star index,
                    # in order to store here the numbers adjacent to it
                    data_dict["star_indexes"].append(index)



    if num_buffer:
        num_struct = num_index_dict(num_buffer, index)
        data_dict["num_indexes"].append(num_struct)
    # Return line data
    return data_dict
# ---------------------------------------------------------- #
# ---------------------------------------------------------- #
def get_star_adjacent_nums(star: list, gear_grid: dict) -> list:
    '''Return a list of numbers adjacent to the star coordinates, based on the gear grid'''

    # Star coordinates
    star_x = star[0]
    star_y = star[1]
    # Initial empty list
    star_adjacent_nums = []

    # Check previous line
    if gear_grid[star_y-1]:
        for num in gear_grid[star_y-1]["num_indexes"]:
            if star_x >= num[1][0]-1 and star_x <= num[1][1]+1:
                star_adjacent_nums.append(num[0])

    # Check current line
    for num in gear_grid[star_y]["num_indexes"]:
        if star_x >= num[1][0]-1 and star_x <= num[1][1]+1:
            star_adjacent_nums.append(num[0])        

    # Check next line if exists
    if gear_grid[star_y+1]:
        for num in gear_grid[star_y+1]["num_indexes"]:
            if star_x >= num[1][0]-1 and star_x <= num[1][1]+1:
                star_adjacent_nums.append(num[0]) 

    # Return list of adjacent numbers   
    return star_adjacent_nums
    
#############################
# Arguments & Init
input_file = sys.argv[1]

#############################

# MAIN.

# The initial idea was to build a grid where only
# symbols of interest, i.e., numbers and non '.' symbols
# will be stored along with their coordinates. I started
# with a brute force approach where I would store all line
# data, with the idea to remove it afterwards, given that
# theoretically for task1 I could simply compare each line
# from the file to itself and the previous one. The aim was
# to then refine the code and not keep a complete dictionary
# to avoid too much memory usage.

# Luckily, task2 turns out is simplified a lot if we already
# have the grid stored so that we can check it against '*' 
# symbols. The only addition made to the code was to store
# star symbol coordinates while doind task1 and then looping
# over the star symbol coordinates and comparing against the
# adjacent numbers. If adjacent numbers are 2, then we multiply
# them and add them to the total gear sum.

line_index = 0
sum_of_valid_numbers = 0
gear_grid  = {} # store our complete number and symbol data here
star_coords = [] # this will hold star coordinates, for us to examine adjacent numbers after the grid is completed
# Sum of star gear ratios
sum_star_gear_ratios = 0
with open(input_file) as f:
    for line in f:

        line = line.strip()

        # Add new dictionary
        gear_grid[line_index] = {}

        # Get complete line data
        line_data_dictionary = get_line_data_dict(line)
        # Get star coordinates in current line
        current_star_coords = [(x_offset, line_index) for x_offset in line_data_dictionary["star_indexes"]]
        # Add star coordinates to complete set of star coordinates
        if current_star_coords:
            star_coords.extend(current_star_coords)
        # Remove star indexes from dictionary (no longer needed)
        line_data_dictionary.pop("star_indexes")
        # Add current data to gear_grid
        gear_grid[line_index] = line_data_dictionary

        # Check numbers against line itself
        for index in gear_grid[line_index]["symbol_indexes"]:
            for number in gear_grid[line_index]["num_indexes"]:
                index_diffs = {index-number_index for number_index in number[1]}
                # If we have a difference of 1 or -1 we have an adjacent number
                if 1 in index_diffs or -1 in index_diffs:
                    number[2] = True
                    sum_of_valid_numbers += number[0]

        # Check numbers against previous line
        if line_index-1 in gear_grid:
            # Check symbol against previous line numbers
            for index in gear_grid[line_index]["symbol_indexes"]:
                for number in gear_grid[line_index-1]["num_indexes"]:
                    # Skip over numbers already added.
                    # A number is adjacent if the symbol index falls within the number index range
                    if not number[2] and index <= number[1][1]+1 and index >= number[1][0]-1:
                        number[2] = True
                        sum_of_valid_numbers += number[0]

            # Check number against previous line symbols
            for number in gear_grid[line_index]["num_indexes"]:
                for index in gear_grid[line_index-1]["symbol_indexes"]:
                    # Ignore numbers already added
                    if not number[2] and index <= number[1][1]+1 and index >= number[1][0]-1:
                        number[2] = True
                        sum_of_valid_numbers += number[0]

        # Increment index
        line_index += 1

# Check the star coordinate adjacencies
for star in star_coords:
    # Store numbers adjacent to the star
    star_adjacent_nums = get_star_adjacent_nums(star, gear_grid)
    # print (f"Star adjacent nums for {star}:{star_adjacent_nums}")
    # Here the length should be 2
    if len(star_adjacent_nums) == 2:
        # print (f"Star at {star} is a valid gear!")
        gear_ratio = star_adjacent_nums[0] * star_adjacent_nums[1]
        sum_star_gear_ratios += gear_ratio
    

'''
print ("\n\n")
for offset in gear_grid:
    print (f"{offset}:{gear_grid[offset]}")
print ("\n------------------\n")
print ("Star coordinates:")
print (star_coords)
'''
print (f"Sum of gear parts: {sum_of_valid_numbers}")
print (f"Sum of star gears: {sum_star_gear_ratios}")


