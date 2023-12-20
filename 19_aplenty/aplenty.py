#!/usr/bin/python
#################
# Imports
import sys 
import math
#################
# Functions
def path_combinations(rule):
    '''
    Given a rule which describes a path leading to an accepting state,
    examine all constraints for all letters and set their upper and lower
    boundaries. Then calculate the product of these ranges and return it. 
    '''

    # Each letter can take values from 1 to 4000. These will be adjusted 
    # as we parse rules in the current Accepting path that is examined.
    letter_ranges = {"x": [1,4000], "m": [1, 4000], "a": [1,4000], "s": [1,4000]}

    # The rule path is passed as a string. We split it to get individual rules
    rule_list = rule.split(" ")
    #remove "in" rule which is always at the start of a path.
    rule_list.pop(0) 

    # Loop rules, update letter ranges based on each rule
    for rule in rule_list:
        next_rule_removed = rule.split(":")[0]
        individual_rules  = next_rule_removed.split("&")

        for individual_rule in individual_rules:
            letter = individual_rule[0]
            comp   = individual_rule[1]
            value  = int(individual_rule[2:])

            if comp == "<":
                letter_ranges[letter][1] = value-1
            else:
                letter_ranges[letter][0] = value+1
    
    letter_ranges_to_combine = [item[1]-item[0]+1 for item in letter_ranges.values()]
    path_value = math.prod(letter_ranges_to_combine)
    return path_value
    
# --------------------------------------- #
def rewrite_rule(rule):
    '''
    Rewrite rule to keep implicit inequalities whenever we proceed 
    from one rule to the next. The input is given as a list.
    '''
    rewritten_rules = [rule[0]]
    for i, r in enumerate(rule):
        if i != 0:

            prev_inequality = rule[i-1].split(":")[0]
            prev_character, prev_comparator, prev_num = prev_inequality[0], prev_inequality[1], int(prev_inequality[2:])

            if prev_comparator == ">":
                additional_rule = prev_character + "<" + str(prev_num+1)
            else:
                additional_rule = prev_character + ">" + str(prev_num-1)
        
            # Get previous inserted rules
            prev_updated_rule = rewritten_rules[i-1].split(":")[0]
            # If last part is same letter, only add a flipped version of the letter's rule
            prev_updated_rule = "&".join(prev_updated_rule.split("&")[:-1]).strip()
            if prev_updated_rule != "":
                additional_rule = prev_updated_rule + "&" + additional_rule

            if ":" in r:
                rule_to_append = additional_rule + "&" + r
            else:
                rule_to_append = additional_rule + ":" + r
            
            rewritten_rules.append(rule_to_append)

    return rewritten_rules
# ------------------------------------------------------------ #
def traverse_rules(rule_dictionary, rule="in", rule_seq = "in"):
    '''DFS on rule_dictionary, adding paths that lead to A state in a global list valid_paths.'''

    global valid_paths
    # By recursively calling this function, and for each rule
    # examining all child rules in order, we essentially do a
    # DFS traversal of the rule tree. We keep the complete
    # sequence of rules in the traversal, and add paths that 
    # lead to an A at the end to the valid_paths list.
    for sub_rule in rule_dictionary[rule]:
        value_constraint = ""
        if ":" in sub_rule:
            value_constraint, sub_rule = sub_rule.split(":")

        # If the rule we ended up on is an accept or reject, we are at the end of a traversal....
        if sub_rule == "A" or sub_rule == "R":
            # Only add path if it leads to an A. At an R we do nothing
            if sub_rule == "A":
                valid_paths.append(rule_seq + " " +  value_constraint + ":" + sub_rule )  
        #... otherwise we need to traverse the next rule
        else:
            new_rule_seq = rule_seq + " " + value_constraint + ":" + sub_rule 
            traverse_rules(rule_dictionary, sub_rule, new_rule_seq)

# ------------------------------------------------------------------ #
def item_passes(item, rule_dictionary, rule="in"):
    '''Apply the rules -> recursive function until we get to R or A.
       Function used in part 1 of the day.

    Args:
        - item (dict): the x,m,a,s item to check.
        - rule_dictionary (dict): the dictionary containing all input rules.
        - rule (str): the rule to be examined in the current call.
    '''
    for sub_rule in rule_dictionary[rule]:
        # Check if rule applies, else go to next rule
        if ":" in sub_rule:
            operation, next_rule = sub_rule.split(":")

            character, comparator, value = operation[0], operation[1], operation[2:]
            if comparator == ">":
                if item[character] > int(value):
                    if next_rule == "A":
                        return True
                    elif next_rule == "R":
                        return False
                    else:
                        return item_passes(item, rule_dictionary, rule=next_rule)
            elif comparator == "<":
                if item[character] < int(value):
                    if next_rule == "A":
                        return True
                    elif next_rule == "R":
                        return False
                    else:
                        return item_passes(item, rule_dictionary, rule=next_rule)
            else:
                print (f"Unknown comparator: {comparator}")
                sys.exit(0)

        # No check, just a next rule
        else:
            if sub_rule == "A":
                return True
            elif sub_rule == "R":
                return False
            else:
                next_rule = sub_rule.strip()
                return item_passes(item, rule_dictionary, next_rule)


#################
input_file = sys.argv[1]
valid_paths = [] # Store here paths that lead to an Accepting end
#################
# Main


# Keep a dictionary w/ the rules
rules = {}

# Items to be passed to rules
items = []

# Parse data here
with open(input_file) as f:
    for line in f:

        line = line.strip()

        if not line:
            continue
        # Parse items
        if line.startswith("{"):

            # Get xmas params
            xmas = line.replace("}", "").replace("{", "").split(",")
            # Put them in a dictionary and store in the list
            item = {xmas_item.split("=")[0]: int(xmas_item.split("=")[1]) for xmas_item in xmas}
            items.append(item)

        # parse rule and add it to rules dictionary
        else:
            rule_name, rules_string = line.split("{")
            rule_list = rules_string.replace("}", "").split(",")

            rules[rule_name] = rule_list
# End of data parsing

############
## PART 1 ##
############               
accumulator = 0
# Check for each item if it ends up in accepting state,
# and if so, add the sum of its values to the accumulator
for item in items:

    if item_passes(item, rules):
        accumulator += sum(item.values())

print (f"Final accumulated value: {accumulator}")

############
## PART 2 ##
############
# We need to traverse all paths that lead to an accepting state.
# We also rewrite each rule, so that when an inequality is not 
# satisfied and we select the next rule, this is identical to 
# the opposite of the previous inequality holding. 
# When we have all paths that lead to an accepting state, we can
# confine the ranges for each letter based on all rules of the path.

############################################
# Rewrite rules with implicit inequalities #
# when a particular route wasn't selected. #
# Each time a next rule is used, we need   #
# to take into account that the opposite   #
# of the previous rule holds in addition   #
# to the new rule added.                   #
############################################
for rule_key in rules:
    rules[rule_key] = rewrite_rule(rules[rule_key])


# Do a dfs traversal and keep only paths 
# that end on an A. The following function
# modifies the global "valid_paths" parameter
# adding each such path that ends on an accepting state.
traverse_rules(rules)

# Loop all valid paths created by the previous function.
# For each path we calculate the total combinations given
# by the product of the range of each letter.
all_combinations = 0
for path in valid_paths:
    current_addend    = path_combinations(path)
    all_combinations += current_addend

print (f"All combinations: {all_combinations}")
 
