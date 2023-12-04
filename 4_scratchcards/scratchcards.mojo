########################################
# Mojo implementation of scratchcards. #
# At my current understanding of the   #
# language I probably won't make it to #
# part 2. However, part 1 I might be   #
# able to solve using mojo's vectors.  #
# Complexity again will not be optimal #
# but it's better than nothing.        #
########################################
# Import
from sys import argv
from python import Python
from utils.vector import InlinedFixedVector
###########################################
# Function definitions
fn is_digit(input_string: String) raises -> Bool:
    '''Return whether string passed is an int.'''
    if input_string == '-': # minus character somehow passed int test
        return False
    try:
        let number: Int = atol(input_string)
        return True
    except:
        return False
# --------------------------------------- #
fn parse_line(inout file_index: Int, inout file_data: String, token: String ='\n') -> String:
    '''
    Get the part of the string (intended to be file contents or file line string) 
    until the next token string is encountered.
    '''

    # String we build to return
    var return_string: String = ""
    # Get current character
    var current_character = file_data[file_index]
    # Read characters until we find the toke we were looking for
    while current_character != token and file_index <= len(file_data):
        return_string += current_character
        file_index += 1
        current_character = file_data[file_index]
    # We found the token we were looking for. 
    # Increment file index to continue from next character
    file_index += 1
    
    return return_string
# --------------------------------------- #
fn parse_card_num(input_string: String) raises -> Int:
    '''Return the card number (int) from a string like "Card <num>".'''
    var num_buffer: String = ""
    for i in range(len(input_string)):
        let character: String = input_string[i]
        if is_digit(character):
            num_buffer += character

    let number: Int = atol(num_buffer)
    return number
# --------------------------------------- #
fn int_vector_from_string(input_string: String) raises -> InlinedFixedVector[Int, 25]:
    
    var num_vector = InlinedFixedVector[Int, 25](50)

    var num_buffer: String = ""
    for i in range(len(input_string)):
        let character = input_string[i]
        # Build our numbers
        if is_digit(character):
            num_buffer += character
        # Whitespace, or non number characters
        elif num_buffer != "":
            let current_num: Int = atol(num_buffer)
            num_vector.append(current_num)
            num_buffer = ""
    if num_buffer != "":
        let current_num: Int = atol(num_buffer)
        num_vector.append(current_num)      
    # Return the vector created
    return num_vector
# --------------------------------------- #
fn card_winnings(winning_vector: InlinedFixedVector[Int, 25], holding_vector: InlinedFixedVector[Int, 25]) -> Int:
    '''Return the winnings of a card based on a particular game.'''
    
    # Store the overlap of numbers
    var overlap: Int = 0

    for win in range(len(winning_vector)):
        let winning_num: Int = winning_vector.__getitem__(win)
        for held in range(len(holding_vector)):
            let holding_num: Int = holding_vector.__getitem__(held)
            if holding_num == winning_num:
                overlap += 1
                # No need to continue inner loop
                break
    # Winnings
    var win_val: Int = 0
    if overlap > 0:
        win_val = 2 ** (overlap-1)
    # print ("Winnings value:", win_val)
    return win_val
###########################################
# Main

fn main() raises:

    # Input file argument
    let input_file_string: String = argv()[1]
    # Variable containing string data to be read from the file
    var file_data: String = ""

    # Index of character in file string
    var file_index: Int = 0

    # A Vector of winning numbers - based on the file, there seem to be 10 winning numbers per line
    # However, to keep a single function for creating both vectors, we will go with the larer size, 
    # i.e., that of numbers held, which is equal to 25 per line given the input file.
    var winning_nums = InlinedFixedVector[Int, 25](50) # Add additional capacity - I may have miscounted

    # A Vector of numbers on card - based on the file, there are 25 numbers held on each card
    var nums_held = InlinedFixedVector[Int, 25](50)

    # Sum of winnings based on part 1
    var sum_winnings: Int = 0

    # Get complete file data in string
    with open(input_file_string, 'r') as f:
        file_data = f.read()

    # Parse substrings of the data, until end of file
    while file_index <= len(file_data):

        let current_card: String = parse_line(file_index, file_data, ':')
        let winning_num_string: String = parse_line(file_index, file_data, "|")
        let holding_num_string: String = parse_line(file_index, file_data, '\n')

        let card_num: Int = parse_card_num(current_card)
        
        winning_nums = int_vector_from_string(winning_num_string)
        nums_held    = int_vector_from_string(holding_num_string)
        # print ("Card num:", card_num)

        let current_win: Int = card_winnings(winning_nums, nums_held)
        sum_winnings += current_win

    # Print winnings result
    print ("Sum of winnings:", sum_winnings)


        
    
    
