############################
# Still a lot of trouble   #
# with basic string mani-  #
# pulation. Hope I'll get  #
# the hang of it instead   #
# of basically reading     #
# characters...            # 
############################
# Imports
from python import Python
from sys import argv
############################
# Functions
fn game_index_string(input_string: String, index: Bool = True) -> String:
    '''Get game index part of string.'''

    # Find index until no more split matches are found
    let split_index: Int = input_string.find(":", 0)
    # Tuple to return
    var return_string: String = ""
    if index:
        return_string = input_string[:split_index]
    else:
        return_string = input_string[split_index+1:]
    return return_string
# ------------------------ #
fn is_valid_game_run(game_runs: String, max_red: Int, max_green: Int, max_blue: Int) -> Bool:
    '''Return whether a game is valid or not.'''

    var string_built: String = ""
    var current_int: Int = 0
    var int_parsed: Bool = False # A flag to know whether int has been parsed

    # Loop the string character by character. Construct parsed ints for count and 
    # remaining parsed string for color. Compare resulting color/int and return false if we have a violation
    for index in range(len(game_runs)):

            let character = game_runs[index]

            # Ignore whitespace
            if character == " ":
                continue

            # End of stats for a particular cube or game
            if character == ',' or character == ';' or character == '\n':
                '''
                print ("\n--------------------------")
                print ("Color string:", string_built)
                print ("Number found:", current_int)
                print ("--------------------------\n")
                '''
                # print (current_int, " - ", string_built)
                # Check validity
                if string_built == "red" and current_int > max_red:
                    return False 
                if string_built == "blue" and current_int > max_blue:
                    return False
                if string_built == "green" and current_int > max_green:
                    return False
                if string_built != "red" and string_built != "blue" and string_built != "green":
                    print ("STRANGER STRINGS:", string_built)

                string_built = ""
                current_int = 0
                int_parsed = False

                # print ("Reset to string: ", string_built, " Int:", current_int, "Parsed:", int_parsed)
                continue

            
            string_built += character

            # If we can parse an int, update it
            try:
                current_int = atol(string_built)
                # print ("Current_int:", current_int)
            except:
                if not int_parsed:
                    string_built = character
                    int_parsed = True

    # At the end of the file we may have omitted the last entry
    if string_built != "":
        if string_built == "red" and current_int > max_red:
            return False 
        if string_built == "blue" and current_int > max_blue:
            return False
        if string_built == "green" and current_int > max_green:
            return False
        if string_built != "red" and string_built != "blue" and string_built != "green":
            print ("STRANGER STRINGS:", string_built)              

    return True
# -------------------------------------------------------------- #
def rgb_power(game_runs: String) -> Int:

    '''Return max values of rgb in partiuclar set of game runs.
       Use the same logic employed in valid game check to build
       Game Run string, but replace rbg with current maximum at
       the end of the line.
    '''

    var red_max: Int    = 0
    var green_max: Int  = 0
    var blue_max: Int   = 0
    var string_built: String = ""
    var current_int: Int = 0
    var int_parsed: Bool = False

    # Loop line
    for index in range(len(game_runs)):

            let character = game_runs[index]
            # Skip whitespace
            if character == " ":
                continue

            # End of stats for a particular color in particular run
            if character == ',' or character == ';' or character == '\n' or index == len(game_runs)-1:
                
                if index == len(game_runs)-1 and character!='\n':
                    string_built += character
                '''
                print ("\n--------------------------")
                print ("Color string:", string_built)
                print ("Number found:", current_int)
                print ("--------------------------\n")
                '''
                if string_built == "red" and current_int > red_max:
                    red_max = current_int
                if string_built == "blue" and current_int > blue_max:
                    blue_max = current_int
                if string_built == "green" and current_int > green_max:
                    green_max = current_int

                string_built = ""
                current_int = 0 
                int_parsed = False 
                # Skip to next char
                continue   

            string_built += character                               

            # If we can parse an int, update it
            try:
                current_int = atol(string_built)
                # print ("Current_int:", current_int)
            except:
                if not int_parsed:
                    string_built = character
                    int_parsed = True

    let cube_power: Int = blue_max * green_max  * red_max
    # print ("RED:", red_max, "GREEN:", green_max, "BLUE:", blue_max)
    # print ("Power calculated: ", cube_power)
    return cube_power
############################

# MAIN function
fn main() raises:

    # Read file line by line - use python interoperability
    let file_opener = Python.evaluate('open')
    # Input file argument
    let input_file_string: String = argv()[1]
    # print ("Input file: ", input_file_string)

    # Max number of red, green, blue cubes
    let max_red: Int    = 12
    let max_green: Int  = 13
    let max_blue: Int   = 14

    # Running counter of valid index sum
    var valid_index_sum = 0
    # Cube Power sum
    var cube_power_sum: Int = 0

    # File handler for input file
    var handle = file_opener(input_file_string, 'r')
    # Loop lines
    for line in handle:
        let line_string = line.to_string().replace('\n', '')
        # print (line_string)
        var index_string: String = game_index_string(line_string)
        let games_string: String = game_index_string(line_string, False)
        index_string = index_string.replace("Game ", "")
        let index_int: Int = atol(index_string)
        # Check if a game if valid
        let valid_game: Bool = is_valid_game_run(games_string, max_red, max_green, max_blue)
        # If it is valid, then add its index
        if valid_game:
            valid_index_sum += index_int
        # Get power for current game
        let cube_power: Int = rgb_power(games_string)
        # Increment running sum
        cube_power_sum += cube_power

    print ("Valid index sum:", valid_index_sum)
    print ("Cube power: ", cube_power_sum)
        
