#!/usr/bin/python
#################
import sys
#################
# Functions
def find_expand_columns(grid: dict) -> list:
    '''Return columns to be expanded'''
    max_x = max([item[0] for item in grid.keys()])
    max_y = max([item[1] for item in grid.keys()])
    expand_cols = set()
    for x in range(max_x+1):
        expand = True
        for y in range(max_y+1):
            if grid[(x,y)] != ".":
                expand = False
        if expand:
            expand_cols.add(x)
    
    return expand_cols
# ------------- #
def galaxy_coords(grid: dict) -> list:
    '''Return a list of coordinates containing galaxies.'''

    galaxies = []
    for item in grid:
        if grid[item] == "#":
            galaxies.append(item)
    return galaxies

# ------------- #
def create_grid(input_file: str) -> dict:
    grid = {}
    rows = set()

    line_counter = 0
    with open(input_file) as f:
        for line in f:
            line = line.strip()

            # If line only contains ".", expand it already
            
            for index, character in enumerate(line):
                grid[(index, line_counter)] = character
            
            # Instead of expanding, just keep account of the line
            if len(set(line)) == 1 and list(set(line))[0] == ".":
                rows.add(line_counter)

            line_counter+=1 

    return grid, rows
# ------------- #         
def print_grid(grid: dict) -> None:

    max_x = max([item[0] for item in grid.keys()])
    max_y = max([item[1] for item in grid.keys()])

    for y in range(max_y+1):
        for x in range(max_x+1):
            print (grid[(x,y)], end = "")
        print ()
#################
input_file = sys.argv[1]
expansion = None
if len(sys.argv) > 2:
    try:
        expansion = int(sys.argv[2])
    except:
        expansion = 2
else:
    expansion = 2
#################
print (f"Empty lines x{expansion}")


grid, rows = create_grid(input_file)
columns = find_expand_columns(grid)

print (f"Rows to expand: {rows}")
print (f"Columns to expand: {columns}")

# No need to expand grid, we take into account the rows/cols 
# for expansion when calculating manhattan distance later

# Get coordinates of galaxies
galaxies = galaxy_coords(grid)
galaxies = sorted(galaxies, key=lambda x: (x[0],x[1]))
# print (f"Galaxies at: {galaxies}")

# Get all pairs
pairs = set()
for index in range(len(galaxies)):
    for other_index in range(index+1, len(galaxies)):
        pairs.add((galaxies[index], galaxies[other_index]))

# Testing
# print ("Galaxy pairs:")
# print (sorted(list(pairs), key=lambda x: (x[0][0], x[0][1])))
# print (f"Number of pairs: {len(pairs)}")

distance_accumulator = 0
distance = 0
# Loop pairs and calculate distances
for galaxy_pair in pairs:

    # If x or y are equal, the distance depends on the other dimention
    g1, g2 = (galaxy_pair)
    x1, y1 = (g1)
    x2, y2 = (g2)

    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    # Manhattan distance since we move only on x and y plane. No diagonal to be measured.
    distance = x2-x1 + y2-y1
    # Take into account the expansions: for each row/col in the range, 
    # expand it as many times as needed. Remember: 1 time is already calculated
    # Add range for expanded columns
    for col in columns:
        if col <= x2 and col >= x1:
            distance += expansion-1
    # Same for rows
    for row in rows:
        if row <= y2 and row >= y1:
            distance += expansion-1
    
    # print (f"Distance for galaxies {g1}, {g2} => {distance}")

    # Accumulate values
    distance_accumulator += distance

# Distances should be found by manhattan and hypotenuse
print (f"Accumulated distances: {distance_accumulator}")