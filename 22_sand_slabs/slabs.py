#!/usr/bin/python
#################
# Imports
import sys
#################
# Functions
def initial_grid(input_file: str) -> dict:
    '''Read the input file and create a 3d grid dictionary.'''

    # The dictionary we create will contain a 6 tuple.
    # This will correspond to start-end (x,y,z).
    # Each brick is assigned its number
    grid = {}
    line_counter = 0
    with open(input_file) as f:
        for line in f:
            line = line.strip()

            start, end = line.split("~")
            a,b,c = start.split(",")
            x,y,z = end.split(",")
            # For each z coordinate get the x-y rectangle occupied
            grid[line_counter] = (int(a),int(x),int(b),int(y),int(c),int(z))
        
            line_counter += 1
    #
    return grid
# ------------- #
def has_settled(brick: tuple, settled_grid: dict) -> bool:
    '''Return true if a brick cannot fall further.'''

    # Get all bricks at 1 z-index below
    brick_low_z = brick[4]
    # We may be on the ground already, no need to check if we are dropping further
    if brick_low_z == 1:
        return True
    # brick_high_z = brick[1]
    brick_x1 = brick[0]
    brick_x2 = brick[1]
    brick_y1 = brick[2]
    brick_y2 = brick[3]

    bricks_below = [item for item in settled_grid.items() if item[1][5] == brick_low_z-1]
 
    # If no candidate bricks are there to stop the fall, brick hasn't settled
    if not bricks_below:
        return False
    
    for below_brick in bricks_below:

        # Get coordinates of brick below
        (x1,x2,y1,y2,_,_) = below_brick[1]

        if (brick_x1 <= x2 and brick_x1 >= x1 or brick_x2 <= x2 and brick_x2 >= x1 or x1 >= brick_x1 and x1 <= brick_x2) and\
           (brick_y1 <= y2 and brick_y1 >= y1 or brick_y2 <= y2 and brick_y2 >= y1 or y1 >= brick_y1 and y1 <= brick_y2):
            return True

        # Wrong condition
        # if (x1 <= brick_x1 and x2 >= brick_x2 or brick_x1 <= x1 and brick_x2 >= x2)\
        #     and (y1 <= brick_y1 and y2 >= brick_y2 or brick_y1 <= y1 and brick_y2 >= y2):
        #     return True
        
    # If no collision found, brick hasn't settled
    return False
# ------------- #
def free_fall(free_fall_grid: dict) -> dict:
    '''Return the grid after the free fall of the bricks.'''

    settled_grid = {}
    total_bricks = len(free_fall_grid)
    brick_count = 0
    print (f"Total bricks to drop: {total_bricks}")

    # Start free fall from the bricks most close to the ground
    for brick_data in sorted(free_fall_grid.items(), key=lambda x: x[1][4]):
        brick_count += 1
        if brick_count % 100 == 0:
            print (" " * 100, end = "\r")
            print (f"Checked {brick_count} bricks, or {int(brick_count*100/total_bricks)}%", end = "\r", flush=True)
        brick_id = brick_data[0]
        brick    = brick_data[1]
        # Initialize to brick data (starting z for brick).
        brick_new_z = brick 

        if not settled_grid:
            # when no items have fallen, we simply go to the ground
            settled_grid[brick_id] = (brick[0], brick[1], brick[2], brick[3], 1, brick[5]-brick[4]+1)
        else:
            # Check if brick has settled. Otherwise fall 1 z at a time and check again
            while not (has_settled(brick_new_z, settled_grid)):          
                brick_new_z = (brick_new_z[0], brick_new_z[1], brick_new_z[2], brick_new_z[3], brick_new_z[4]-1, brick_new_z[5]-1)    
                # print (f"Z now is: {brick_new_z[4]}")
                if brick_new_z[4] <= 0:
                    print ("Below ground!!!")
                    sys.exit(0)
            # print (f"Brick {brick_id} settled at height: {brick_new_z[4]} and x {brick_new_z[0]}-{brick_new_z[1]}, y {brick_new_z[2]}-{brick_new_z[3]}")
            # Here the brick has settled so we update the settled grid
            settled_grid[brick_id] = brick_new_z

    print ()
    return settled_grid
# ------------- #
def bricks_support(settled_grid: dict) -> dict:
    '''From the settled grid, return a dictionary with a set of supported bricks for each brick.'''

    support_dict = {}

    for brick in settled_grid:

        if brick not in support_dict:
            support_dict[brick] = set()

        (brick_x1, brick_x2, brick_y1, brick_y2, _, brick_z2) = settled_grid[brick]

        supported_candidates = [brick for brick in settled_grid if settled_grid[brick][4] == brick_z2+1]
        supported_bricks = []
        # Filter candidates based on whether they are actually supported 
        for candidate in supported_candidates:

            (cx1, cx2, cy1, cy2, _, _) = settled_grid[candidate]

            if (cx1 <= brick_x2 and cx1 >= brick_x1 or cx2 <= brick_x2 and cx2 >= brick_x1 or brick_x1 >= cx1 and brick_x1 <= cx2) and\
            (cy1 <= brick_y2 and cy1 >= brick_y1 or cy2 <= brick_y2 and cy2 >= brick_y1 or brick_y1 >= cy1 and brick_y2 <= cy2):
                supported_bricks.append(candidate)

        # Add all supported bricks to the brick key
        # NOTE: we could maybe avoid adding entries for bricks that don't support anything
        support_dict[brick] = supported_bricks

    # Invert the support dict to get sets of bricks and a list of their supporting bricks
    supported_by = {}
    supported_by["none"] = set()
    for brick, supported_bricks in support_dict.items():

        # Add to set of bricks not supported by others
        if not supported_bricks:
            supported_by["none"].add(brick)

        for supported in supported_bricks:
            if supported not in supported_by:
                supported_by[supported] = set()
            supported_by[supported].add(brick)

    # Return supported by
    return supported_by       

# ------------- #
def test_levels(settled_grid: dict) -> None:
    '''Function to debug the settled grid. Check that no x-y overlap on any level.'''
    
    # NOTE: this function is not used in the main code. It was used for testing correctness
    levels = {settled_grid[brick][4] for brick in settled_grid}
    print (f"Levels:{levels}")

    for level in sorted(list(levels)):
        
        bricks = [settled_grid[item] for item in settled_grid if settled_grid[item][4] == level or settled_grid[item][4] <= level and settled_grid[item][5] >= level]
        print (f"Bricks in level {level}: {bricks}")

        # xy plane coordinates occupied
        coordinates = set()
        for brick in bricks:
            x_range=range(brick[0], brick[1]+1)
            y_range=range(brick[2], brick[3]+1)
            print (f"Examining brick: {brick}")
            for x in x_range:
                for y in y_range:
                    if (x,y) not in coordinates:
                        coordinates.add((x,y))
                    else:
                        print (f"Coordinates: ({x},{y}) already examined for this level!!")
                        sys.exit(0)

        print (f"Coordinates occupied in {level}: {coordinates}")

    sys.exit(0)
    return
          
#################
# Init
input_file = sys.argv[1]
#################
# Main

# Get grid of bricks in the air
free_fall_grid = initial_grid(input_file)

# Get grid after all bricks have fallen
print ("Getting settled grid:")
settled_grid = free_fall(free_fall_grid)

# We should be able to delete the initial grid now
free_fall_grid = None

# DEBUG
# test_levels(settled_grid)

'''
# TESTS
print ("After falling:")
for item in sorted(settled_grid.items(), key=lambda x: (x[1][4]), reverse=True):
    print (f"{item[0]} => {item[1]}")
print ("\n-------------\n")
'''
# Find support relationships
supported_by = bricks_support(settled_grid)

'''
# TESTS
for brick in supports:
    print (f"Bricks {brick} supported by: {supports[brick]}")
'''

# Get bricks that are the only ones supporting some other brick
bricks_singly_responsible_for_some_other_brick = [supported_by[item] for item in supported_by if len(supported_by[item]) == 1 and item != "none"]
bricks_singly_responsible_for_some_other_brick = set().union(*bricks_singly_responsible_for_some_other_brick)
# print (f"Bricks singly responsible: {bricks_singly_responsible_for_some_other_brick}")
print (f"Num of bricks solely responsible for keeping another in place: {len(bricks_singly_responsible_for_some_other_brick)}")
print (f"These cannot be removed. Hence, out of a total of {len(settled_grid)} items, we can remove {len(settled_grid)-len(bricks_singly_responsible_for_some_other_brick)}")