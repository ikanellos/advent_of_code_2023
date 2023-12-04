#!/usr/bin/python

######################
# Day 4 of AoC 20024 #
######################
# Imports
import sys
######################
# Functions
def card_worth(winning_nums: str, holding_nums: str) -> int:
    '''Returns the winning of a particular scratch card game'''
    # Make sets out of the number strings
    winning_set = set(winning_nums.strip().split(" "))
    holding_set = set(holding_nums.strip().split(" "))

    # Get intersection
    overlap = winning_set.intersection(holding_set)
    # If no winning numbers, score is 0
    if not overlap:
        return 0, 0
    # Otherwise score is 2 exponentiated, starting w/ 0 for a lenght of 1    
    exponent = len(overlap)-1
    return 2 ** exponent, exponent+1
# --------------------------------------------------------- #
def update_instances(card_num: int, num_overlap: int, instance_data: dict)-> dict:
    '''Update card instance count based on current card number and winnings'''
    card_copies = 0 # how many copies of the card we have
    # Add the index to the dictionary if we don't have it
    if card_num not in instance_data:
        instance_data[card_num] = 1 
        card_copies = 1
    else:
        # Card already in data
        instance_data[card_num] += 1
        card_copies = instance_data[card_num] # num of copies after adding the current one
    
    # Starting offset for updating card data is card_num + 1
    for card_copy_num in range(card_num+1, card_num+1+num_overlap):
        if card_copy_num not in instance_data:
            instance_data[card_copy_num] = card_copies
        else:
            instance_data[card_copy_num] += card_copies
    
    return instance_data
######################
# Inits

# card data input
input_file = sys.argv[1]

# Running sum of winnings
winnings = 0

# A Dictionary of card instance data for part 2
card_data = {}

# Read line by line
with open(input_file) as f:
    for line in f:
        card_num, game = line.strip().split(":")
        # Get card number from string
        card_num = int(card_num.replace("Card ", ""))
        winning_nums, holding_nums = game.strip().split("|")
        winning_nums = winning_nums.replace("  ", " ") # nums are aligned, so we need
        holding_nums = holding_nums.replace("  ", " ") # to remove extra spaces
        # Calculate worth of current card
        current_winning, num_overlap = card_worth(winning_nums, holding_nums)
        # Update counts of card instances at current iteration
        card_data = update_instances(card_num, num_overlap, card_data)
        # Running sum for part 1
        winnings += current_winning
    
# Current card num is final game. 
# Remove the cards with a larger number from dictionary
invalid_card_nums = [item for item in card_data.keys() if item > card_num]
# print (f"Invalid card nums: {invalid_card_nums}")
for invalid_num in invalid_card_nums:
    card_data.pop(invalid_num)

# Get sum of instances:
total_cards = sum(card_data.values())

print (f"Winnings: {winnings}")
print (f"Total cards: {total_cards}")