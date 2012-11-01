#!/usr/bin/python

INPUT_FILE_PATH = "./squished_status.txt" #"./squished_status_input.txt" #

import re
whitespace_re = re.compile("[\s]+")


# We will throw this if something didn't meet the constraints.
class FacebookShenanigansException(Exception): pass

class TestCase:
    """
    
    """
    def __init__(self, m, encoded_status):
        # Your basic constructor.
        self.m = m
        self.encoded_status = encoded_status
        
    def __str__(self):
        # Give Python a little help printing TestCases
        return "<m = %s, encoded_status = %s>" % (self.m, self.encoded_status)
    
    def isValid(self):
        """
        Check if the test case is within the constraints.
        
        I used to do this, now I don't give a shit.
        """
        
        return True
    
    def is_valid_grouping(self, number):
        if number <= self.m:
            return True
        else:
            return False
    
    def make_groupings(self):        
        # We will use this to hold final digits
        single_numbers = []
        
        # We need to make sure there are no zeros, because they are a weird case.
        prev_n = self.encoded_status[0]
        for i, n in enumerate(self.encoded_status[1:]):
            if n == "0":
                prev_n = prev_n+n
            else:
                # This number wasn't a zero, so make sure it fits under M
                if int(prev_n) > self.m:
                    return 0
                # Add the number to our list
                single_numbers.append(prev_n)
                # Prepare for the next number
                prev_n = n
        
        # Check if the last number fits under M
        if int(prev_n) > self.m:
            return 0
        # Add that to our list of numbers
        single_numbers.append(prev_n)
        
        # How many numbers to we have?
        total_numbers = len(single_numbers)
        
        permutation_list = []
        
        # Work through our list of numbers, marking down the spaces they occupy
        for i in range(total_numbers):
            # Mark the standing by itself case
            permutation_list.append([i,i])
            
            # Can we make a two digit number that fits under M?
            if i+1 < total_numbers and self.is_valid_grouping(int(single_numbers[i]+single_numbers[i+1])):
                # If yes, mark down its start and end
                permutation_list.append([i,i+1])
                
                # Can we make a three digit number that fits under M?
                if i+2 < total_numbers and self.is_valid_grouping(int(single_numbers[i]+single_numbers[i+1]+single_numbers[i+2])):
                    permutation_list.append([i,i+2])
        
        # Set up our permutations starts_with list
        sw = [ 0 ] * total_numbers
        # Starts with (total_numbers+1) should always be one.
        sw.append(1)
        
        # Work our way up, counting the permutations we've seen.
        for starts, ends in reversed(permutation_list):
            sw[starts] += sw[ends+1]
        
        # By the time we are done, sw[0] is the correct answer.
        return sw[0]
    
        
# Holds the number of expected test cases
number_of_test_cases = -1

# Holds all of our test cases.
test_cases = []

# Open the input file
input_file = open(INPUT_FILE_PATH, "r")

# Read the whole file to a string
input_string = input_file.read()

# All of the file is read in, we can close it.
input_file.close()

# Replace all whitespace with " "
input_string = whitespace_re.sub(" ", input_string).strip()

# Split on space
input_list = input_string.split(" ")

# We will use a negative value for m to mark that we haven't read it yet.
m = -1

# Read in input file
for line in input_list:
    # Strip off the new lines (and prey I didn't miss one)
    trimmed_line = line.strip("\r\n")
    if number_of_test_cases == -1:
        try:
            number_of_test_cases = int(trimmed_line)
        except ValueError:
            raise FacebookShenanigansException("Couldn't turn %s into an int. Calling shenanigans and quitting." % trimmed_line)
    elif m == -1:
        m = int(trimmed_line)
    else:
        status = trimmed_line
        new_test_case = TestCase(m, status)
        
        if new_test_case.isValid():
            test_cases.append(new_test_case)
            m = -1
        else:
            raise FacebookShenanigansException("Invalid Test Case!")


if number_of_test_cases != len(test_cases) :
    raise FacebookShenanigansException("Number of cases read (%s) did not match number (%s) expected. Calling shenanigans and quitting." % (len(test_cases), number_of_test_cases))

count_number = 1
for test_case in test_cases:
    
    number_of_groupings = test_case.make_groupings() % 0xfaceb00c
    print "Case #%s: %s" % (count_number, number_of_groupings)
    
    count_number += 1
