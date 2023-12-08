#!/usr/bin/python

################################
# AoC Day 5 Solution in Python #
################################
# Import
import sys
import math
################################
def get_data_from_input(input_file: str) -> (str, list, dict):
    '''
    Read the input file. 
    Return:
        - a string representing the input tape string
        - a list representing the order of nodes in the map
        - a dictionary containing the next node based on each
        direction for each input node.
    '''
    tape_string = ""
    node_list = []
    directions_map = {}

    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                # If this works, we are at a map
                index    = line.index("=")
                node     = line[:index-1].strip()
                node_map = line[index+2:].strip()

                # Add node to list
                node_list.append(node)
                # Add node and map to directions
                left, right = node_map.replace(")", "").replace("(", "").split(", ")
                directions_map[node] = (left, right)

            # We are at the tape line
            except ValueError:
                tape_string = line.strip()
    
    # Done with file, return data structures
    return tape_string, node_list, directions_map
# ---------------------------- #
# Run tape on a starting node
def run_tape(tape: str, seed:str, directions: dict, final_node = 'ZZZ') -> str:
    '''
       Run the tape (str) starting from seed node
       and output the final node string if we follow
       the tape string on the directions mapping.
    '''
    # Direction should be L or R
    for offset, instruction in enumerate(tape):
        next_direction = 0 if instruction.lower() == 'l' else 1
        # Select next direction and update seed
        next_seed = directions[seed][next_direction]
        seed = next_seed
        if next_seed == final_node:
            break

    steps = offset + 1
    return seed, steps
# ---------------------------- #
def is_periodic(ghost_map: dict) -> bool:
    '''Return whether the map given has
       leads to result nodes that appear periodically
    '''

    for index in ghost_map:
        if not ghost_map[index]:
            return False
        # Check length of results
        else:
            at_least_one_len_3 = False
            for end_node in ghost_map[index]:        
                results_len = len(ghost_map[index][end_node])
                if results_len >= 3:
                    at_least_one_len_3 = True
                    diffs = [ghost_map[index][end_node][i+1] - ghost_map[index][end_node][i] for i in range(len(ghost_map[index][end_node])-1)]
                    if len(set(diffs)) != 1:
                        return False
            if not at_least_one_len_3:
                return False
                
    return True
# ---------------------------- #
# Run tape on a set of starting nodes
def run_ghost_tape(tape: str, seed_nodes: list, directions: dict, final_node_char = 'Z') -> str:
    '''
       Run the tape (str) starting from seed node set.
       Update ghost map with positions where we found
       items ending with 'z' for each original node
    '''

    step = 0 # we'll count up to 10000 let's say

    # Ghost map has as keys the indexes of the starting nodes
    ghost_map = {index: {}  for index, _ in enumerate(seed_nodes)}
    # Loop until we have periods of the appearance of end nodes
    while True:
        # print (f"Step: {step}")
        tape_index = (step) % len(tape)
        # print (f"Step {step} | Tape index: {tape_index} | Tape: {tape[tape_index]}")
        current_instruction = tape[tape_index]
        current_instruction_index = 0 if current_instruction.lower() == 'l' else 1
        # Now get next node for each node we have
        next_seed_nodes = []
        # Get all next steps
        for index, node in enumerate(seed_nodes):

            # print (f"Seed nodes: {seed_nodes}")
            # Select next direction and update seed
            next_node = directions[node][current_instruction_index]
            next_seed_nodes.append(next_node)

            # Add resulting node to dictionary of starting node
            if node.endswith('Z'):
                if node not in ghost_map[index]:
                    ghost_map[index][node] = [step]
                else:
                    ghost_map[index][node].append(step)

        seed_nodes = next_seed_nodes

        # Check if: 
        # a. All start nodes (given by indexes) have a non empty dictionary of results
        # b. At least one dictionary key shows a periodic appearance value
        if is_periodic(ghost_map):
            '''
            for index in ghost_map:
                for end_node in ghost_map[index]:
                    period = ghost_map[index][end_node][-1] - ghost_map[index][end_node][-2]
                    ghost_map[index][end_node].append(period)
            '''
            break

        step = step+1

    return ghost_map
################################
# inits
input_file = sys.argv[1]
if (len(sys.argv)) > 2:
    ghost = True
else:
    ghost = False
################################
# Main

tape, nodes, directions = get_data_from_input(input_file)

'''
# TESTING
print (f"Tape: {tape}")
print (f"Nodes: {nodes}")
print (f"Directions: {directions}")
'''
print (f"Tape length: {len(tape)}")

# Variable to store total num of steps
total_steps = 0
# The length of our tape. 
# Each time we run the tape on a starting node we do len(tape) steps
tape_len = len(tape)
# Flag to be sure we actually reached the desired node
final_node_reached = False

# Variable to store current node, or current node set
current_node = None

# Here implementation without parallel ghost structure
if not ghost:

    # Final node should be ZZZ
    final_node = 'ZZZ'

    # Get the starting node's (which should be AAA) index
    start_index = nodes.index('AAA')
    current_node = nodes[start_index]
    print (f"Starting node index: {start_index}. starting node: {current_node}")

    while not final_node_reached:

        # Run instruction tape on current input node
        current_node, steps = run_tape(tape, current_node, directions, final_node)
        # print (f"Current output node is: {current_node}")
        # Add another length of the tape to the number of steps
        total_steps += steps
        # print (f"Reached {current_node} in {steps} steps for this tape run")
        if current_node ==  final_node:
            final_node_reached = True
            break
else:

    # Get all node indexes for nodes that end with A
    ghost_indexes = [index for index, item in enumerate(nodes) if item.endswith('A')]
    print (f"Ghost indexes: {ghost_indexes}")

    # Here current nodes are the starting node set
    current_nodes = [nodes[item] for item in ghost_indexes]

    print (f"Starting nodes: {current_nodes}")

    # Run tape on current input set - the tape will run some repetitions 
    # to allow us to find a periodic appearance of particular solutions per starting node
    ghost_map = run_ghost_tape(tape, current_nodes, directions)

    periods = []
    # We need to get the gcd of the list periods
    for index in ghost_map:
        for end_node in ghost_map[index]:
            if len(ghost_map[index][end_node]) >= 3:
                period = ghost_map[index][end_node][-1] - ghost_map[index][end_node][-2]
                periods.append(period)
    # NOTE: this may have needed some extra processing if e.g., a periodic phase starts AFTER a certain number of steps.
    # Luckily this worked with periods starting from step 0
    print (f"Step periods: {periods}")
    lcm = math.lcm(*periods)

if not ghost and final_node_reached:
    print (f"Steps required: {total_steps}")
elif ghost:
    print (f"Multiple of all end node periods: {lcm}")
else:
    print (f"Final node wasn't reached!! Instead reached: {current_node}")




