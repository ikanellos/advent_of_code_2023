#################################
# Imports                       #
from sys import argv
#################################
# FUNCTIONS
# Sliding window to see if string is contained in longer string and return the index.
# If small string is not contained in the larger one, return negative index
fn contains_string(long_string: String, small_string: String, forward: Bool = True) -> Int:

    let small_string_length = len(small_string)
    let long_string_length  = len(long_string)

    var step: Int = 1
    var start: Int = 0
    var stop: Int = long_string_length-small_string_length+1


    # Set up range and steps for loop
    if not forward:
        start = long_string_length-small_string_length+1
        stop  = 0
        step = -1
    
    # Test setup
    # print ("Start:", start, "|Stop:", stop, "|Step:", step)

    # Apply sliding window on long string starting from the beginning of the string
    for i in range(start, stop, step):
        # Get slice of the smaller substring's length
        let long_string_substring = long_string[i:i+small_string_length]
        if long_string_substring == small_string:
            return i

    # We get here if no match was found
    return -1
# ------------------------------------------------------------------------ #
# Function to get first appearing number in string.
# Returns a number found in the string and the index where it is found in the string
fn number_from_string(input_string: String, from_start: Bool = True) -> Tuple[Int, Int]:
    
    # List of number literals
    let nums_list = VariadicList("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    # Our number to return
    var number_in_string: Int = -1
    # Offset index of string
    var offset: Int = -1
    
    for number in range(len(nums_list)):
        let number_string = nums_list.__getitem__(number)
        let new_offset = contains_string(input_string, number_string, from_start)
        let new_number = number+1
        if from_start:
            if (new_offset >=0 and offset < 0) or (new_offset < offset and new_offset >=0):
                offset = new_offset
                number_in_string = new_number
        else:
            if (new_offset >= 0 and offset < 0) or (new_offset >= offset and new_offset >=0):
                offset = new_offset
                number_in_string = new_number
    
    if offset < 0:
        number_in_string = -1

    let index_and_num = Tuple(offset, number_in_string)
    # May be -1 if no string is included   
    return index_and_num
############################################################################

# MAIN function
fn main() raises:


    # Input file
    let input_file: String = argv()[1]
    # File data which will be read
    var file_data: String = ""
    # Running string created by looping lines
    var string_built: String = ""
    # first and last digit indices
    var first_digit_index: Int = -1
    var last_digit_index: Int = -1
    var first_digit: Int = -1
    var last_digit: Int = -1
    # Running character
    var character: String = ""
    # Variable to construct the number of each line
    var num_constructed: Int = 0
    # Running total
    var running_total: Int = 0

    # Read all text data into a string
    with open(input_file, 'r') as f:
        file_data = f.read()

    # Loop character stream
    for i in range(len(file_data)):

        character = file_data[i]
        string_built += character

        # Try to parse int
        try:
            let int_parsed = atol(character)
            if first_digit_index < 0:
                first_digit_index = len(string_built)-1
                last_digit_index  = len(string_built)-1
                first_digit = int_parsed
                last_digit = int_parsed
            else:
                last_digit_index = len(string_built)-1
                last_digit = int_parsed
        # Do nothing here
        except:
            pass


        if character == '\n' or i == len(file_data)-1:

            if character == '\n':
                string_built = string_built[:-1]

            # print ("String compiled: ", string_built)
            let first_num_from_string = number_from_string(string_built)
            let last_num_from_string  = number_from_string(string_built, False)

            # Get indexes of string based nums
            let first_num_from_string_index = first_num_from_string.get[0, Int]()
            let last_num_from_string_index  = last_num_from_string.get[0, Int]()
            
            '''
            print ("First number:", first_num_from_string.get[1, Int](), " | Last number:", last_num_from_string.get[1, Int]())
            print ("First number index:", first_num_from_string_index, " | Last number index:", last_num_from_string_index)
            print ("First digit parsed: ", first_digit, " | Last digit parsed: ", last_digit)
            print ("Found at positions: ", first_digit_index, " and ", last_digit_index)
            '''

            # Construct the number now
            if (first_num_from_string_index >= 0 and first_num_from_string_index < first_digit_index) or first_digit_index < 0: 
                num_constructed = first_num_from_string.get[1, Int]() * 10
            else:
                num_constructed = first_digit * 10   

            # least significant digit now
            if (last_num_from_string_index >= 0 and last_num_from_string_index > last_digit_index) or last_digit_index < 0:
                num_constructed += last_num_from_string.get[1, Int]()

            else:
                num_constructed += last_digit
            '''
            print ("Constructed number: ", num_constructed)
            print()
            '''

            running_total += num_constructed


            
            # Reinitialize
            string_built = ""
            character = ""
            num_constructed = 0
            first_digit_index = -1
            last_digit_index = -1 
            first_digit = -1
            last_digit = -1

    # Print final result
    print (running_total)