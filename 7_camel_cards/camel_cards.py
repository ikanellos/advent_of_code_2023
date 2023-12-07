#!/usr/bin/python

##########################
# AoC Day 6: Wait for it #
##########################
import sys 
##########################
# Functions
def get_hand_tuple(hand_string: str) -> tuple:
    '''
    From a hand string, return a 5-tuple of numbers 
    corresponding to each card's strenth in order
    '''
    cards_mapping = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    tuple_list = []
    for card in hand_string:
        if card in cards_mapping:
            tuple_list.append(cards_mapping[card])
        else:
            tuple_list.append(int(card))

    return tuple(tuple_list)
# ------------------------- #
def get_joker_tuple(hand: tuple) -> tuple:
    '''Map an input tuple hand to its best corresponding hand w/ jokers set'''
    hand_card_counts = {}
    joker_count = 0
    for card in hand:
        if card == 11:
            joker_count += 1
            continue
        if card not in hand_card_counts:
            hand_card_counts[card] = 1
        else:
            hand_card_counts[card] += 1 

    joker_tuple = hand

    # Joker should be turned into the best count card
    if joker_count == 5:
        joker_tuple = (13,) * 5    
    # Only one value in dictionary besides joker -> all jokers turn to that value
    elif len(hand_card_counts) == 1:
        single_value = list(hand_card_counts.keys())[0]
        joker_tuple = (single_value, ) * 5 
    else:
        count_tuples = [(key, val) for key, val in hand_card_counts.items()]
        # Sort by count desc and value desc
        count_tuples = sorted(count_tuples, key=lambda x: (x[1], x[0]), reverse=True)
        # Best card will be the first element
        highest_count_card = count_tuples[0][0]
        # Replace joker with card of best value
        joker_list = list(hand)
        joker_list = [highest_count_card if item == 11 else item for item in hand]
        joker_tuple = tuple(joker_list)          
    #
    return joker_tuple
# ------------------------- #
def get_hand_bid_map(input_file: str, joker: bool) -> dict:
    '''Read a file line by line and return a dictionary of card_tuple => bid'''
    hand_bid_map = {}
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            hand, bid = line.split(" ")

            hand_tuple = get_hand_tuple(hand)
            # Add to total mapping
            hand_strength = get_hand_strength(hand_tuple)
            hand_bid_map[hand_tuple] = {"bid": int(bid), "strength": hand_strength}

            # Add a joker-based tuple and strength if needed
            if joker:
                joker_tuple = get_joker_tuple(hand_tuple)
                # Testing. Joker tuple doesn't need to be stored, since it turns to a different
                # tuple upon comparing to hands of the same strength
                # print (f"Joker tuple for {hand_tuple} is {joker_tuple}")
                # hand_bid_map[hand_tuple]["joker_tuple"] = joker_tuple
                hand_bid_map[hand_tuple]["joker_strength"] = get_hand_strength(joker_tuple)

    # Return the dictionary parsed
    return hand_bid_map
# ------------------------- #
def get_hand_strength(hand_tuple: tuple) -> int:
    '''Return the type of card set, mapped to ints'''

    hand_card_counts = {}
    for card in hand_tuple:
        if card not in hand_card_counts:
            hand_card_counts[card] = 1
        else:
            hand_card_counts[card] += 1    

    # print ("Hand card counts:")
    # print (hand_card_counts)
    hand_set_length = len(hand_card_counts)

    # Check if five of a kind
    if hand_set_length == 1:
        return 7
    # Check four of a kind or full house
    if hand_set_length == 2:
        min_card_count = min(hand_card_counts.values())
        # Four of a kind
        if min_card_count == 1:
            return 6
        # full house
        return 5
    # Check if three of a kind or two pairs
    if hand_set_length == 3:
        max_card_count = max(hand_card_counts.values())
        # Three of a kind
        if max_card_count == 3:
            return 4
        # Two pairs
        return 3
    # Check single pair
    if hand_set_length == 4:
        return 2
    # Value of type high card
    return 1
# ------------------------- #
def replace_joker(hand: tuple, inverse: bool = False) -> tuple:
    '''Replaces the joker values of a hand with 0, or 0 values with joker'''
    hand_list = list(hand)
    replaced_list = []
    for card in hand_list:
        if inverse and card == 0:
            replaced_list.append(11)
        elif not inverse and card == 11:
            replaced_list.append(0)
        else:
            replaced_list.append(card)
    return tuple(replaced_list)
# ------------------------- #
# INITS
input_file = sys.argv[1]
# If any extra argument is given we consider
# it as specifying the joker rule to be set
joker = False
if len(sys.argv) > 2:
    joker = True
# ------------------------- #
print (f"Joker rule: {joker}")
# Read all hands into a map
hand_bids = get_hand_bid_map(input_file, joker)

# Rank 1 is for weakest hand
ranks = 1

# Loop card strengths from lowest to strongest
for strength in range(1, 8):

    # Get tuples or currently examined strength

    # If J is not joker, simply get the hands with the current strength from map
    if not joker:
        hands_w_strength = [hand for hand in hand_bids if hand_bids[hand]["strength"] == strength]
    # If J is joker, we filter based on the joker strength calculated
    else:
        hands_w_strength = [hand for hand in hand_bids if hand_bids[hand]["joker_strength"] == strength]

    # Next we need to order hands from weakest to strongest. 
    # Sort by all values in the tuples. 
    if not joker:
        hands_w_strength_sorted = sorted(hands_w_strength, key = lambda x: (x[0], x[1], x[2], x[3], x[4]))
    # If we have J as a joker, we need to replace these hands with hands where J -> 0
    else:
        # Replace joker values with 0 in list
        hands_w_strength_sorted = [replace_joker(hand) for hand in hands_w_strength]
        # Now sort from weakest to strongest
        hands_w_strength_sorted = sorted(hands_w_strength_sorted, key = lambda x: (x[0], x[1], x[2], x[3], x[4]))

    # Assign ranks. Our list has hands in ascending order of strength
    for hand in hands_w_strength_sorted:
        # Given there may be joker replacements, our tuples won't correspond to 
        # the map. We need to turn them back, and this turned back tuple is used
        # in our map. If no joker is ser, the tuple stays unchanged.
        if joker:
            hand_key = replace_joker(hand, inverse=True)
        else:
            hand_key = hand
        # Add the rank to the current bid
        hand_bids[hand_key]["rank"] = ranks
        # Increment ranks
        ranks += 1

    # print ("\n------------------\n")

# Calculate total winnings based on the ranks
'''
print ("Final hands:")
print (hand_bids)
print ()
print ()
'''
# Calculate total winnings as sum(bid * rank)
total_winnings = 0
for hand in hand_bids:
    bid = hand_bids[hand]["bid"]
    rank = hand_bids[hand]["rank"]
    total_winnings += bid * rank

print (f"Total winnings: {total_winnings}")


