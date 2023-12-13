#!/usr/bin/python
#################
# Imports
import sys 
import editdistance
import os
#################
# Functions
def find_reflections(grid: dict, approximate: bool = False) -> tuple[int, str]:

    lines = grid["lines"]
    columns = grid["columns"]
    # Get horizontal candidates
    horizontal_candidates = []
    for index in range(len(lines)-1):
        if not approximate and lines[index] == lines[index+1]:
            horizontal_candidates.append(index+1)
        elif approximate and editdistance.eval(lines[index], lines[index+1]) <= 1:
            horizontal_candidates.append(index+1)
    
    '''
    print ("Horizontal candidates:")
    print (horizontal_candidates)
    '''
    
    # Check for each horizontal candidate if it truly reflects
    for candidate in horizontal_candidates:
        lines_before, lines_after = lines[:candidate], lines[candidate:]
        if are_reflections(lines_before, lines_after, approximate):
            return candidate, "horizontal"

    vertical_candidates = []
    for index in range(len(columns)-1):
        if not approximate and columns[index] == columns[index+1]:
            vertical_candidates.append(index+1)
        elif approximate and editdistance.eval(columns[index], columns[index+1]) <= 1:
            vertical_candidates.append(index+1)            
    
    '''
    print ("Vertical candidates:")
    print (vertical_candidates)
    '''
   
    # Check for each vertical candidate if it truly reflects
    for candidate in vertical_candidates:
        columns_before, columns_after = columns[:candidate], columns[candidate:]
        if are_reflections(columns_before, columns_after, approximate):
            return candidate, "vertical"

    return 0, "Error"
# ------------- #
def are_reflections(left: list, right: list, approximate: bool = False) -> bool:

    # There should be ONE smudge
    edit_distance_used = False

    # Remove the two elements which are mirrored
    first_left = left.pop(-1)
    first_right = right.pop(0)

    # Case where the smudge is ON the reflection line
    if first_left != first_right:
        edit_distance_used = True

    # Compare lines further away from reflection to check whether they reflect
    while left and right:

        check_left = left[-1]
        check_right = right[0]

        # Strict mode checks for direct equality
        if not approximate and check_left != check_right:
            return False       
        # Approximate mode allows for at least one change in the reflections
        elif approximate:
            if (edit_dist := editdistance.eval(check_left, check_right)) > 0:
                if not edit_distance_used and edit_dist == 1:
                    edit_distance_used = True
                    left.pop(-1)
                    right.pop(0)
                    continue
                else:
                    return False
                
        # Remove compared elements
        left.pop(-1)
        right.pop(0)
    
    # In approximate match mode, we should have had at least one approximate match
    if approximate and not edit_distance_used:
        return False 
    
    return True

#################
# Init
input_file = sys.argv[1]
approximate = False
if len(sys.argv) > 2:
    approximate = True
#################
# Main

# Get size of file to see if we are at the last line
size = os.path.getsize(input_file)

# A list of grids in the file, in which we must find a reflection
grid_counter = 0
# Add a full grid dictionary for each grid
grids = [{"lines": [], "columns": []}]
line_counter = 0
columns = []
previous_line = ""

# Accuulate values based on the problem's rules
acc = 0

with open(input_file) as f:
    for line in f:
        # Decrease counter of file size
        size -= len(line)

        line = line.strip()
        line_counter += 1

        # At empty line, go to new grid
        if line == "" or not size:
            line_counter = 0
            grid_counter += 1
            columns = []
            grids.append({"lines": [], "columns":[]})

            if not size:
                grids[grid_counter-1]["lines"].append(line) 
    

            # Add columns to last completed grid
            line_len = len(grids[grid_counter-1]["lines"][0])
            for character in range(line_len):
                column = [line[character] for line in grids[grid_counter-1]["lines"]]
                column = "".join(column)
                grids[grid_counter-1]["columns"].append(column)


            # Find possible reflections
            reflection_offset, reflection_direction = find_reflections(grids[grid_counter-1], approximate)
            
            # print (f"GRID {grid_counter} | Reflection: {reflection_direction} at index {reflection_offset}")

            if reflection_direction == "horizontal":
                acc +=  100 * reflection_offset
            elif reflection_direction == "vertical":
                acc += reflection_offset

            else:
                print (f"Error with grid {grid_counter-1}: no reflection found")
                sys.exit(0)


            # go to next line to avoid adding empty lines
            previous_line = ""
            # print ("\n--------------------\n")
            continue
        
        grids[grid_counter]["lines"].append(line)
        previous_line = line

# Remove last element in grid (will be empty)
grids.pop(-1)

# Print output
print (f"Accumulated: {acc}")

