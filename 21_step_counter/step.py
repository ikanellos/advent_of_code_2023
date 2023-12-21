#!/usr/bin/python
#################
import sys
#################
# Functions
def get_grid(input_file: str) -> dict:
    '''Return a dict of tuple(coords) -> symbol'''
    grid = {}
    line_counter = 0
    with open(input_file) as f:
        for line in f:
            line = line.strip()

            for index, character in enumerate(line):
                coords = (index, line_counter)
                grid[coords] = character

                if character == "S":
                    # Start coordinates will be outside grid
                    grid[(-1, -1)] = coords

            line_counter += 1
    #
    return grid
# ------------- #
def next_steps(coords: set, grid: dict) -> set:
    '''Return a set of possible next positions if grid allows it.'''

    new_coords = set()
    # For each coordinate we have in the grid...
    for coord in coords:
        # ... get x, y and possible next x,y
        x, y = coord

        neighbour_coords = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        # Filter neighbour coords by validity: 
        # they should exist on the grid and they should not contain a "#" 
        # NOTE: "and they should not be in a previous position" <- according to the example, we don't care about this
        valid_next_coords = [coord for coord in neighbour_coords if coord in grid and grid[coord] != "#"]
        # print (f"Valid next coords: {valid_next_coords}")

        # Add to new positions
        for valid_next_coord in valid_next_coords:
            new_coords.add(valid_next_coord)
    # Return set of new coordinates
    return new_coords
#################
# Init
input_file = sys.argv[1]
step_num   = int(sys.argv[2])
#################
# Main

# Get grid of input in a dictionary
grid = get_grid(input_file)
start_coords = grid.pop((-1,-1))
# print (f"Start at: {start_coords}")

step_counter = 1
step_coords  = {0: {start_coords}}
# Keep track of coordinates in previous steps to avoid going back
prev_step   = None 
for step in range(step_num):
    # Get a number of possible next steps.
    next_step_coords = next_steps(step_coords[step], grid)
    step_coords[step_counter] = next_step_coords
    # Increment step counter
    step_counter += 1


final_step_positions = step_coords[step_num]
# print (f"Final step coordinates: {final_step_positions}")
print (f"Positions on grid: {len(final_step_positions)}")

# for step in step_coords:
#     print (f"At {step} steps: {step_coords[step]}")

