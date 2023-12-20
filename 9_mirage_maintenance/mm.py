#!/usr/bin/python
#################
import sys
#################
# functions
def all_zero(input_list: list) -> bool:
    '''Return true if all elements in the input list are 0.'''

    list_elements = set(input_list)
    if len(list_elements) > 1:
        return False
    
    if len(list_elements) == 1 and list(list_elements)[0] == 0:
        return True
    
    return False

# -------------------------------------------------- #

def create_diff_sequences(input_list: list) -> list:
    '''Return a list of lists. Each next list contains the differences of previous sequential elements.'''

    # First add the initial input list
    output_lists = [input_list]
    # Loop until the last list contains only zero elements
    while not all_zero(output_lists[-1]):

        # The latest produced list is at the end of output_lists
        latest_list = output_lists[-1]
        # Work with previous list
        new_list = [item-latest_list[index] for index, item in enumerate(latest_list[1:])]

        output_lists.append(new_list)

    # print (f"Final output lists: {output_lists}")

    return output_lists

# ------------------------------------ #

def get_next(sequences: list) -> int:
    '''Get the next value of the first sequence in sequences by following the pyramid rule.'''

    # Start at the end, move to the front
    last_seq = sequences.pop(-1)
    last_val = last_seq [-1]
    for seq_index in range(len(sequences), 0, -1):
        previous_last_val = sequences[seq_index-1][-1]
        sequences[seq_index-1].append(last_val + previous_last_val)
        last_val = sequences[seq_index-1][-1]
    
    # Return the last appended element of first sequence
    return sequences[0][-1]


#################
# Init
input_file = sys.argv[1]
#################
# Main

# Get each list from the file input
input_lists = []
acc = 0
with open(input_file) as f:
    for line in f:
        line = line.strip()

        add_list = line.split(" ")
        add_list = [int(element) for element in add_list]
        input_lists.append(add_list)

        sequences = create_diff_sequences(add_list)
        next_val  = get_next(sequences)

        acc += next_val

print (f"Accumulated: {acc}")




