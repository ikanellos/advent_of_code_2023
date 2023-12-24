#!/usr/bin/python
#################
# Imports
import sys 
#################
# Functions
# ------------- #
def print_grid(grid, path = []):

    symbols = {"|", "-", "L", "J", "7", "F"}
    print ()

    path = set(path)

    for coord in sorted(grid.keys(), key=lambda x: (x[1],x[0])):
        x, y = coord

        if x == 0 and y != 0:
            print()

        if not path:
            print (grid[(x,y)], end ="")
        
        else:
            if (x,y) in path or grid[(x,y)] not in symbols:
                print (grid[(x,y)], end ="")
            else:
                print (".", end = "")   
        
    print ("\n\n")
# ------------- #

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
def get_direction(prev: tuple, next: tuple) -> str:
    '''Return the direction of movement between two tiles.'''

    # Direction will be in {'s', 'n', 'e', 'w'}
    if (prev[0] < next[0]):
        direction = "e"
    elif (prev[0] > next[0]):
        direction = "w"
    elif (prev[1] < next[1]):
        direction = "s"
    else:
        direction = "n"

    return direction

# ------------------------------------------------------- #
def new_outside(direction: str, new_direction: str, outer_lambda):
    '''Return a new lambda function that maps to the outside of a tile.'''

    new_outer_lambda = lambda x: x # dummy identity
    outer_x, outer_y = outer_lambda((0,0))

    if direction == "s":
        if new_direction == "w":
            # decrease y
            if outer_x < 0:
                new_outer_lambda = lambda coords: (coords[0], coords[1]-1)
            else:
                new_outer_lambda = lambda coords: (coords[0], coords[1]+1)
        elif new_direction == "e":
            if outer_x < 0:
                new_outer_lambda = lambda coords: (coords[0], coords[1]+1)
            else:
                new_outer_lambda = lambda coords: (coords[0], coords[1]-1)            


    elif direction == "n":
        if new_direction == "e":
            if outer_x < 0:
                new_outer_lambda = lambda coords: (coords[0], coords[1]-1)
            else:
                new_outer_lambda = lambda coords: (coords[0], coords[1]+1)
        elif new_direction == "w":
            if outer_x < 0:
                new_outer_lambda = lambda coords: (coords[0], coords[1]+1)  
            else:
                new_outer_lambda = lambda coords: (coords[0], coords[1]-1)            

    elif direction == "w":
        if new_direction == "n":
            if outer_y > 0:
                new_outer_lambda = lambda coords: (coords[0]-1, coords[1])
            else:
                new_outer_lambda = lambda coords: (coords[0]+1, coords[1])
        elif new_direction == "s":
            if outer_y < 0:
                new_outer_lambda = lambda coords: (coords[0]-1, coords[1])
            else:
                new_outer_lambda = lambda coords: (coords[0]+1, coords[1])
    
    elif direction == "e":
        if new_direction == "n":
            if outer_y > 0:
                new_outer_lambda = lambda coords: (coords[0]+1, coords[1])
            else:
                new_outer_lambda = lambda coords: (coords[0]-1, coords[1])
        elif new_direction == "s":
            if outer_y > 0:
                new_outer_lambda = lambda coords: (coords[0]-1, coords[1])
            else:
                new_outer_lambda = lambda coords: (coords[0]+1, coords[1])

    return new_outer_lambda
# ------------------------------------------------------- #
def mark_outside_path(grid: dict, path: list) -> dict:
    '''Run the path found and mark blocks to the left and right of the direction we are going.'''

    # For quicker lookup, unordered
    path_set = set(path)

    # Keep a set of coordinates that are marked as outside
    outside_coords = set()

    # Get the upper-left-most tile in path
    upper_left_most_tile = sorted(path, key=lambda x: (x[1],x[0]))[0]
    # print (f"Upper left most tile in path is: {upper_left_most_tile} with symbol: {grid[(upper_left_most_tile)]}")

    upper_leftmost_index = path.index(upper_left_most_tile)
    path = path[upper_leftmost_index:] + path[:upper_leftmost_index]
    # Close the loop of the path. 
    # This will be useful when we walk the path, 
    # in order to know the direction we are going until the loop closes.

    path.append(path[0])
    # print (f"Rewound path: ")
    # print (path)

    # A lambda function that maps current tile to outside one.
    # Will be updated at each corner.
    outer_tile = lambda x: x # dummy initialization

    # Start walking the path. 
    for index, coords in enumerate(path[:-1]):

        # We should be guaranteed to start going right, or down,
        # given that we start at the upper-left most pipe.
        if coords == path[0]:
            direction = get_direction(coords, path[index+1])

            # Set initial mapping function.
            if direction == "s":
                outer_tile = lambda coords: (coords[0]-1, coords[1])
            elif direction == "e":
                outer_tile = lambda coords: (coords[0], coords[1]-1)
            else:
                print (f"Unexpected direction: {direction}")
                sys.exit(0)                

            # Paint the outside tile
            out_coords = outer_tile(coords)
            if out_coords in grid and out_coords not in path_set:
                grid[out_coords] = "X"
                outside_coords.add(out_coords)
            continue
        
        # Get the outside tile
        out_coords = outer_tile(coords)

        # Check if outside is in grid (i.e., not outside our coordinates)
        # and if it is not a path tile
        if out_coords in grid and out_coords not in path:
            # Mark as outside
            grid[out_coords] = "X"
            outside_coords.add(out_coords)

        # Now if we have reached a turn, we need to update the outside function
        if grid[coords] in {"J", "7", "F", "L"}:

            new_direction = get_direction(coords, path[index+1])
            # Create new lambda for mapping the outside
            outer_tile = new_outside(direction, new_direction, outer_tile)
            # Get new outside tile and mark if possible
            out_coords = outer_tile(coords)
            if out_coords in grid and out_coords not in path:
                grid[out_coords] = "X" 
                outside_coords.add(out_coords)

            # Update direction
            direction = new_direction      

    # Mark remaining outside coords
    new_outside_coords = outside_coords
    # Visit new neighbouring coordinates for all those marked outside.
    # Mark the ones found that don't belong to the path. Add them to the
    # set of visited coordinates and update the grid. When there are no
    # new visited coordinates, we are finished
    while new_outside_coords:
        # Set of new coordinates reached
        new_outside_coords = set()
        for outside_coord in outside_coords:
            x,y = outside_coord
            neighbours = [(x+1,y), (x-1,y), (x, y+1), (x,y-1)]
            valid_neighbours = [neighbour for neighbour in neighbours if neighbour in grid and neighbour not in path_set and neighbour not in outside_coords]
            new_outside_coords = new_outside_coords.union(set(valid_neighbours))
            # Mark on grid
            for neighbour in valid_neighbours:
                grid[neighbour] = "X"
        
        outside_coords = outside_coords.union(new_outside_coords)

    return grid
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
        
# print ("Starting grid is:")
# print_grid(grid)

# print (f"Starting at: {start_coords}")

# Try each starting symbol for S.
# Call the traversing function and return the path 
# if a loop is done, or an empty list otherwise. 
# When we get the correct loop, stop and keep path.

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
print (f"Longest distance in path: {int(len(path)/2)}")
# Replace S symbol with correct one
grid[start_coords] = start_symbol

# Loop the path and mark all adjacent outside blocks.
# Then, expand outside blocks to their neighbours, 
# except if they hit a path block
grid = mark_outside_path(grid, path)

# Just testing
# print_grid(grid, path)

# Get remaining "." or pipes that don't belong in the main loop in grid that aren't marked
remaining_dot_chars_in_grid = [coord for coord in grid if coord not in path and grid[coord] != "X"]
# print (f"Enclosed tiles at: {remaining_dot_chars_in_grid}")
print (f"Total enclosed tiles: {len(remaining_dot_chars_in_grid)}")


