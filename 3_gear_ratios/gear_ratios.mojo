#########################################
# Having written the python code,       #
# and seen a small tutorial of how      #
# to use the InlineFixedVector          #
# datastructure provided by mojo, I     #
# will try to tackle this differently   #
# here. Instead of a dictionary of      #
# all coordinates and numbers/symbols   #
# I will try to create vertors of       #
# numbers and symbols along with their  #
# indexes. Then I will only loop the    #
# numbers for part 1, see if they are   #
# adjacent to some symbol and if so     #
# I will count them. For part 2 I will  #
# loop the symbols only (checking for   #
# star) and check for each one which    #
# numbers are adjacent. Still feels as  #
# if I'm writing glorified assembly but #
# I'm starting to understand mojos data-#
# types...                              #
# Complexities aren't great here-O(n^2) #
# but the focus is still to understand  #
# mojo's builtins.                      #
#########################################
# Imports
from python import Python
from sys import argv
from utils.vector import InlinedFixedVector
from math import abs
##########################################
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
# -------------------------------------- #
fn gear_adjacent(number_x_start: Int, number_x_end: Int, number_y: Int, symbol_vector: InlinedFixedVector[Tuple[Int, Int, Int], 200]) -> Bool:
    # Loop over symbols, only when their y coordinate is number_y +/- 1
    for symbol_index in range(len(symbol_vector)):

        let symbol_tuple: Tuple[Int, Int, Int] = symbol_vector.__getitem__(symbol_index)
        let symbol_y: Int = symbol_tuple.get[2, Int]()
        if abs(symbol_y - number_y) > 1:
            continue
        else:
            let symbol_x: Int = symbol_tuple.get[1, Int]()
            let symbol_data_index: Int = symbol_tuple.get[0, Int]()
                
            if symbol_x >= number_x_start - 1 and symbol_x <= number_x_end + 1:
                return True 
    # All line adjacent symbols examined, none adjacent to number coords
    return False
# -------------------------------------- #
fn make_num_tuple(num_string: String, file_index: Int, x_index: Int, y_index: Int) raises -> Tuple[Int, Int, Int, Int]:
    '''Create a tuple as required by the number coordinate vector.'''
    let num_string_len: Int = len(num_string)
    let num_parsed: Int = atol(num_string)
    let correct_file_index: Int = file_index-len(num_string)
    '''
    print ("Num parsed:", num_parsed)
    print ("Index:", correct_file_index)
    print ("X-index:", x_index-len(num_string))
    print ("X-index end:", x_index)
    '''
    let tuple_to_return: Tuple[Int, Int, Int, Int] = Tuple(correct_file_index, x_index-len(num_string)+1, x_index, y_index)
    return tuple_to_return
# -------------------------------------- #
fn star_gear_adjacent(star_x: Int, star_y: Int, number_vector: InlinedFixedVector[Tuple[Int, Int, Int, Int], 200], file_data: String) raises -> Int:
    '''Return product of numbers adjacent to symbols, if 2 nums are adjacent.'''

    # This may be an actual correct usage, since we know here that few numbers will be adjacent
    var adjacent_nums: InlinedFixedVector[Int, 5] = InlinedFixedVector[Int, 5](10) 
    for num_index in range(len(number_vector)):

        let num_tuple: Tuple[Int, Int, Int, Int] = number_vector.__getitem__(num_index)
        let num_y: Int = num_tuple.get[3, Int]()
        # Ignore nums in different lines
        if abs(star_y - num_y) > 1:
            continue

        let file_index: Int = num_tuple.get[0, Int]()
        let num_start_x: Int = num_tuple.get[1, Int]()
        let num_end_x: Int = num_tuple.get[2, Int]()

        if star_x >= num_start_x - 1 and star_x <= num_end_x + 1:
            let adjacent_num_str: String = file_data[file_index:file_index+(num_end_x-num_start_x)+1]
            let adjacent_num: Int = atol(adjacent_num_str)
            # print ("Found star-adjacency for:", adjacent_num)
            adjacent_nums.append(adjacent_num)
            # quick kill if too many numbers
            if len(adjacent_nums) > 2:
                return 0

    var product: Int = 0
    # If two nums are adjacent to the star
    if len(adjacent_nums) == 2:
        product = adjacent_nums.__getitem__(0) * adjacent_nums.__getitem__(1)
        # print ("Product is:", product)
    
    return product
##########################################

# Main
fn main() raises:

    # Input file argument
    let input_file_string: String = argv()[1]
    # Variable containing string data to be read from the file
    var file_data: String = ""

    # Line counter
    var y_index: Int = 0
    # An index to count offsets within lines
    var x_index: Int = 0

    # A buffer string adding digit characters
    var num_string: String = ""

    # Let's say that our vector of symbols will contain about 150
    # symbols (there's 140 lines in my input, not all contain symbols)
    var symbol_coordinates = InlinedFixedVector[Tuple[Int, Int, Int], 200](2000) # Total capacity of 2000
    # Let's say that the numbers will be much fewer, e.g., 10 per line
    var num_coordinates    = InlinedFixedVector[Tuple[Int, Int, Int, Int], 200](2000) # add a capacity for 2000 more

    # Create a vector only for star symbols
    var star_coordinates = InlinedFixedVector[Tuple[Int, Int, Int], 100](1000) 
    
    # Sum of gears for part 1
    var gear_sum: Int = 0 # sum the numbers adjacent to symbols
    # Sum of star part adjacent number product for part 2
    var star_gear_sum: Int = 0
    
    # Get all file data in a string
    with open(input_file_string, 'r') as f:
        file_data = f.read()

    # Loop all data in the file
    for file_index in range(len(file_data)):
        # Get current character in data file string
        let current_character: String = file_data[file_index]
    
        # Update indexes new line
        if current_character == '\n':
            # If we have reached the end of a line, we need to possibly parse the number
            if num_string != "":
                # Add number to vector of nums
                let coordinate_tuple: Tuple[Int, Int, Int, Int] = make_num_tuple(num_string, file_index, x_index-1, y_index)
                num_coordinates.append(coordinate_tuple)
                # Clear lengt of number string
                num_string = ""

            # Reset line indexes to correct values
            x_index = 0
            y_index += 1

            # Skip to next character                
            continue

        let digit: Bool = is_digit(current_character)

        # Add to vector if not '.'. If we have a number 
        # string buffered, add it to the number vectors
        if not digit:
            # If we have parsed a number
            if num_string != "":
                let coordinate_tuple: Tuple[Int, Int, Int, Int] = make_num_tuple(num_string, file_index, x_index-1, y_index)
                num_coordinates.append(coordinate_tuple)
                # Clear lengt of number string
                num_string = ""
            
            # If our character is not a dot, we add the symbol coordinates
            if current_character != '.':
                let coordinate_tuple: Tuple[Int, Int, Int] = Tuple(file_index, x_index, y_index)
                # Add to vector
                symbol_coordinates.append(coordinate_tuple)
                # Add to star coords if *
                if current_character == '*':
                    star_coordinates.append(coordinate_tuple)
        
        # Parse a number if the character is a digit
        if digit:
            num_string += current_character
            # print ("Num string became:", num_string)

        
        # increment line index
        x_index += 1

        # Final checks if we are at the last offset. 
        # We may have an unfinished number
        if file_index == len(file_data)-1:
            # If we have parsed a number
            if num_string != "":
                let coordinate_tuple: Tuple[Int, Int, Int, Int] = make_num_tuple(num_string, file_index+1, x_index-1, y_index)
                # Add number to vector of nums
                # let coordinate_tuple: Tuple[Int, Int, Int, Int] = Tuple(file_index_correct, x_index-len(num_string), x_index-1, y_index)
                num_coordinates.append(coordinate_tuple)            

    '''
    # TESTING VECTORS CREATED
    # Check if all things entered correctly
    for x in range(len(symbol_coordinates)):

        let coordinate_tuple: Tuple[Int, Int, Int] = symbol_coordinates.__getitem__(x)
        let symbol: String = file_data[coordinate_tuple.get[0, Int]()]
        let x_coord: String = coordinate_tuple.get[1, Int]()
        let y_coord: String = coordinate_tuple.get[2, Int]()

        print ("Symbol:", symbol, "at:", x_coord, ",", y_coord)

    # Loop number coordinates
    for x in range(len(num_coordinates)):

        let coordinate_tuple: Tuple[Int, Int, Int, Int] = num_coordinates.__getitem__(x)
        let start_index: Int = coordinate_tuple.get[0, Int]()
        let x_coord_start: Int = coordinate_tuple.get[1, Int]()
        let x_coord_end: Int = coordinate_tuple.get[2, Int]()
        let num_len = x_coord_end - x_coord_start
        let y_coord: String = coordinate_tuple.get[3, Int]()
        let num_string: String = file_data[start_index:start_index+num_len+1]

        print ("Num:", num_string, "at:", x_coord_start,"-", x_coord_end, "/", y_coord)
    '''

    # PART 1: for part 1 we only need to find numbers that are adjacent to symbols.
    # We loop through each number and if at least one symbol is found to be adjacent,
    # we add the number to the sum. No need to examine further symbols afterwards,
    # simply proceed to the next number
    for number_index in range(len(num_coordinates)):

        let number_tuple: Tuple[Int, Int, Int, Int] = num_coordinates.__getitem__(number_index)
        let number_x_start: Int = number_tuple.get[1, Int]()
        let number_x_end: Int = number_tuple.get[2, Int]()
        let number_y: Int = number_tuple.get[3, Int]()
        let file_data_index: Int = number_tuple.get[0, Int]()
        let number: Int = atol(file_data[file_data_index:file_data_index+(number_x_end-number_x_start)+1])

        # Create a function 'gear_adjacent(number_x_start, number_x_end, number_y, symbol_coordinates)'
        if gear_adjacent(number_x_start, number_x_end, number_y, symbol_coordinates):
            # Add number to sum
            # print ("Number:", number, "is adjacent to gear")
            gear_sum += number

    # Iterate over stars
    for star_index in range(len(star_coordinates)):
        let star_tuple = star_coordinates.__getitem__(star_index)
        let star_y: Int = star_tuple.get[2, Int]()
        let star_x: Int = star_tuple.get[1, Int]()

        let partial_sum: Int = star_gear_adjacent(star_x, star_y, num_coordinates, file_data)
        # Partial sum will be 0 if conditions are not met, so it won't affect total sum
        star_gear_sum += partial_sum
    

    print ("Sum of gear parts:", gear_sum)
    print ("Sum of star gear parts:", star_gear_sum)







