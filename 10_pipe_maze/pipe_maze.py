#!/usr/bin/python
#################
# Imports
import sys 
#################
# Functions
def valid_next_coords(symbol: str, coords: tuple) -> list:
    '''Return possible next coordinates for the symbol.'''

    # Recall, increasing y is down, increasing x is right
    x, y = coords[0], coords[1]
    if symbol == "|":
        return [(x, y-1), (x, y+1)]
    if symbol == "-":
        return [(x-1, y), (x+1, y)]
    if symbol == "F":
        return [(x, y+1), (x+1,y)]
    if symbol == "7":
        return [(x, y+1), (x-1, y)]
    if symbol == "L":
        return [(x, y-1), (x+1, y)]
    if symbol == "J":
        return [(x, y-1), (x-1, y)]
    # if we get to a non pipe there is no next move
    if symbol == ".":
        return []
    return []

# ------------------------------------------------------- #

def run_path(start_symbol: str, start_coords: tuple, grid: dict) -> list:
    '''
    Return an empty list if the path starting at start 
    coords with start symbol ends at an invalid move. 
    Else, return the list of coordinates of a path 
    starting and ending at start coords
    '''

    next = None
    symbol = start_symbol
    path = [start_coords]
    examined_coords = {start_coords} # Don't add initial coordinates until the end

    # Keep track of previous corrdinates to check validity of next move
    prev = start_coords
    # Loop until we hit a dead end or conclude a path
    while next != start_coords:
        # Get a list of possible next moves - these are always 2 at maximum
        next_coord_list = valid_next_coords(symbol, prev)
        # If no next coordinates are possible, we are at a dead end
        if not next_coord_list:
            return []
        # If we can get back to start as a next move, select it
        if len(path) > 3 and start_coords in next_coord_list:
            next = start_coords
            symbol = start_symbol
        # otherwise select the move to a coordinate we haven't been to yet
        else:
            # Next coordinate
            next = [item for item in next_coord_list if item not in examined_coords and item in grid]
            # If no such next move exists, we hit a dead end
            if not next:
                return []
            # Get coordinates and symbol of next position
            next = next[0]
            # What is the current symbol?
            symbol = grid[next]
        
        # Check validity of next symbol given the previous position
        # 1. if x decreased
        if prev[0] > next[0]:
            # We shouldn't need to check previous symbol given the next valid ones
            # if prev_symbol in {"-", "7", "J"} and symbol not in {"-", "L", "F"}:
            if symbol not in {"-", "L", "F"}:
                return []
        # 2. if x increased
        elif prev[0] < next[0]:
            if symbol not in {"-", "7", "J"}:
                return []
        # 3. if y decreased (going up)
        elif prev[1] > next[1]:
            if symbol not in {"|", "7", "F"}:
                return []
        # 4. if y increased (going down)
        elif prev[1] < next[1]:
            if symbol not in {"|", "J", "L"}:
                return []            

        # Increase path
        path.append(next)
        examined_coords.add(next)

        prev = next
    
    # If we get to the end, return the path
    return path

#################
# Init
input_file = sys.argv[1]
#################
# Main

# We keep a grid of coordinates 
# that map to a symbol. 
grid = {}

# Keep a list of valid symbols
symbols = {"|", "-", "L", "J", "7", "F", ".", "S"}

## CREATE GRID
line_counter = 0
start_coords = None
with open(input_file) as f:

    for line in f:
        line = line.strip()

        for index, character in enumerate(line):
            coords = (index, line_counter)
            grid[coords] = character

            if character == "S":
                start_coords = coords

        line_counter += 1
#################################
print (f"Starting at: {start_coords}")

# Try each starting symbol for S.
# Call the traversing function and 
# return the path if a loop is done, 
# or an empty list otherwise. When 
# we get the correct loop, stop an keep path

path = []
for start_symbol in symbols:

    if start_symbol == "S" or start_symbol == ".":
        continue

    path = run_path(start_symbol, start_coords, grid)
    # If we found the loop, no need to check other symbols
    if path:
        path.pop()
        break

print (f"Loop found for starting symbol: {start_symbol}")
# print (f"Path: {path}")
print (f"Half length of path: {int(len(path)/2)}")


