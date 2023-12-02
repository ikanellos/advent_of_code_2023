####################################
# The code is very messy and could #
# benefit from better organization/#
# optimization. This is normal, I'm#
# trying out mojo for the first    #
# time and have trouble navigating #
# and understanding the available  #
# documentation just now. For lack #
# of time I will leave the code in #
# its messy state.                 #
####################################
# Imports
from sys import argv
####################################
fn main() raises:

    # File data string
    var file_data: String = ""

    let input_file: String = argv()[1]

    # Read all text data into a string
    with open(input_file, 'r') as f:
        file_data = f.read()
    
    # This variable will hold each character we iterate over
    var character: String = ""
    # This fill hold our sum total of calibrations read
    var sum_of_calibrations: Int = 0
    # This will tell us if we encountered a number while iterating characters
    var num_detected: Bool = False
    # This will construct each individual calibration numbers
    var num_constructed: Int = 0
    # This will hold the last int encountered while looping the character stream
    var current_int: Int = 0

    # String is seen as an array by mojo - we loop over its indexes
    for i in range(len(file_data)):
        
        # Get the current character
        character = file_data[i]
        # Try to turn character to int. If we can't we ignore 
        # it, except if newline, or we are at end of string
        try:
            # Convert character to int
            current_int = atol(character)
            # if we haven't failed, then it means we met a number.
            # if it is the first number we met, then set the flag
            # and start constructing the calibration number
            if not num_detected:
                num_constructed = 10 * current_int
                num_detected = True
        # Do nothing, if we can't convert character to int
        except:
            pass

        # If we have a newline, then the last char we could convert to int
        # will be the least significant digit of our number
        if character == '\n' or i == len(file_data)-1:
            # Construct actual calibration number
            num_constructed += current_int
            # Add it to running total
            sum_of_calibrations += num_constructed

            # Re initialize flags and constructed numbers
            num_constructed = 0
            num_detected = False

    print (sum_of_calibrations)

            


    
