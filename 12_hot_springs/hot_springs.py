#!/usr/bin/python
#################
# Imports
import sys
import re
#################
# Functions
def generate_strings(springs: str, total_broken_springs: int) -> list:
    '''Return list of valid strings by all possible replacements of "." and "?".'''

    spring_strings = []

    if "?" not in springs:
        if springs.count("#") == total_broken_springs:
            return [springs]
        else:
            return []
        
    # If we exceed the count of "#" we need overall, return
    if springs.count("#") > total_broken_springs:
        return []
    
    q_index         = springs.find("?")
    dot_string      = springs[:q_index] + "." + springs[q_index+1:]
    hashtag_string  = springs[:q_index] + "#" + springs[q_index+1:]

    spring_strings.extend(generate_strings(dot_string, total_broken_springs))
    spring_strings.extend(generate_strings(hashtag_string, total_broken_springs))

    return spring_strings
# ------------------------ #
def valid_strings(spring_strings: list, contig_data: list) -> int:
    '''Return the number of strings that satisfy the contiguous requirements.'''
    
    valid_counter = 0
    for spring in spring_strings:
        broken_springs = re.findall('#+', spring)
        broken_lengths = [len(seq) for seq in broken_springs]
        if broken_lengths == contig_data:
            valid_counter += 1

    return valid_counter
#################
# INITS
input_file = sys.argv[1]
unfold = None
if len(sys.argv) > 2:
    unfold = True
else:
    unfold = False
#################
line_counter = 1
total_combinations = 0
with open(input_file) as f:

    for line in f:
        line = line.strip()

        # Get data from input line
        springs, contiguous = line.split(" ")

        contiguous = [int(number) for number in contiguous.split(",")]

        total_broken = sum(contiguous)
        # print (f"Total broken: {total_broken}")

        # Get all strings that can be generated
        all_springs = generate_strings(springs, total_broken)
        # print (f"Number of valid strings: {len(all_springs)}")
        # print (f"All springs: {all_springs}")
        # print ()

        # Filter strings based on the condition of contig parts
        combinations = valid_strings(all_springs, contiguous)

        '''
        # Print diagnostics per line
        print ("\n----------------------------------")
        print (f"Combinations at line {line_counter}: {combinations}")
        print ("----------------------------------\n")
        '''       
        total_combinations += combinations
        #
        line_counter += 1

        if line_counter % 50 == 0:
            print (" " * 100, end = "\r")
            print (f"Processed {line_counter} lines...", end = "\r", flush=True)

print()
print (f"All combinations: {total_combinations}")