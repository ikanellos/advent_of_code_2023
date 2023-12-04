#!/usr/bin/python

######################
# Day 4 of AoC 20024 #
######################
# Imports
import sys
######################
# Functions
def card_worth(winning_nums: str, holding_nums: str) -> int:

    # Make sets out of the number strings
    winning_set = set(winning_nums.strip().split(" "))
    holding_set = set(holding_nums.strip().split(" "))

    # Get intersection
    overlap = winning_set.intersection(holding_set)
    # If no winning numbers, score is 0
    if not overlap:
        return 0    
    # Otherwise score is 2 exponentiated, starting w/ 0 for a lenght of 1    
    exponent = len(overlap)-1
    return 2 ** exponent
        

######################
# Inits

# card data input
input_file = sys.argv[1]

# Running sum of winnings
winnings = 0

# Read line by line
with open(input_file) as f:
    for line in f:
        _, game = line.strip().split(":")
        winning_nums, holding_nums = game.strip().split("|")
        winning_nums = winning_nums.replace("  ", " ") # nums are aligned, so we need
        holding_nums = holding_nums.replace("  ", " ") # to remove extra spaces
        # Calculate worth of current card
        current_winning = card_worth(winning_nums, holding_nums)

        winnings += current_winning

print (f"Winnings: {winnings}")