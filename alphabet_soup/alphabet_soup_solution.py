#!/usr/bin/python

# Michael Feineman's answer to the Alphabet Soup Problem

INPUT_FILE_PATH = "./alphabet_soup.txt"

# For checking test cases for validity
import re
test_case_invalid_chars = re.compile("[^A-Z\ ]+")

# For removing unwanted characters from the input string
not_hackercup_letters = re.compile("[^HACKERUP]+")

# We will throw this if something didn't meet the constraints.
class FacebookShenanigansException(Exception): pass

class TestCase:

    def __init__(self, text):
        # Your basic constructor.
        self.text = text
        self.counts = { "H" : 0, "A" : 0, "C" : 0, "K" : 0, "E" : 0, "R" : 0, "U" : 0, "P" : 0}
    
    def isValid(self):
        """
        Check if the test case is within the constraints.
        They are as follows:
        Sentences contain only the upper-case letters A-Z and the space character
        Each sentence contains at least one letter, and contains at most 1000
            characters, including spaces 
        """
        # Check text length constraint
        if len(self.text) > 1000 and len(self.text) >= 1:
            return False
        
        # Check there are only A-Z and spaces
        if test_case_invalid_chars.search(self.text) != None:
            return False
        
        return True
        
    def howManyHackerCups(self):
        # Does the work of finding how many times you could make HACKERCUP from the
        # input
        
        # Remove any letter that is not in HACKERCUP
        new_text = not_hackercup_letters.sub("", self.text)
        
        # Count how many of each letter we have
        for letter in self.counts.keys():
            self.counts[letter] = new_text.count(letter)
        
        # Need two C's for every 1 of every other letter
        self.counts["C"] = self.counts["C"] // 2
        
        # Whatever letter we have the fewest of is our limiting case.
        return min(self.counts.values())
        
# Holds the number of expected test cases
number_of_test_cases = -1

# Holds all of our test cases.
test_cases = []

# Open the input file
input_file = open(INPUT_FILE_PATH, "r")

# Read in input file
for line in input_file.readlines():
    # Strip off the new lines (and prey I didn't miss one)
    trimmed_line = line.strip("\r\n")
    if number_of_test_cases == -1:
        try:
            number_of_test_cases = int(trimmed_line)
        except ValueError:
            raise FacebookShenanigansException("Couldn't turn %s into an int. Calling shenanigans and quitting." % trimmed_line)
            
    else:
        text = trimmed_line
        new_test_case = TestCase(text)
        
        if new_test_case.isValid():
            test_cases.append(new_test_case)
        else:
            raise FacebookShenanigansException("Invalid Test Case!")

# All of the file is read in, we can close it.
input_file.close()

if number_of_test_cases != len(test_cases) :
    raise FacebookShenanigansException("Number of cases read (%s) did not match number (%s) expected. Calling shenanigans and quitting." % (len(test_cases), number_of_test_cases))

count_number = 1
for test_case in test_cases:
    
    # Ask for the answer from test_case.
    number_of_cups = test_case.howManyHackerCups()
    
    # Output our results
    print "Case #%s: %s" % (count_number, number_of_cups)
    
    count_number += 1
