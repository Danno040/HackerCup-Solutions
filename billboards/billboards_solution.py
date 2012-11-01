#!/usr/bin/python

INPUT_FILE_PATH = "./billboards.txt"

# For checking test cases for validity
import re
contains_invalid_chars = re.compile("[^a-zA-Z0-9\ ]+")
contains_double_space = re.compile("\ \ ")

# We will throw this if something didn't meet the constraints.
class FacebookShenanigansException(Exception): pass

class TestCase:
    """
    This will hold the details of an individual test case.
    >> tc = TestCase(20, 6, "hacker cup")
    >> print tc
    Width = 20, Height = 6, Text = hacker cup
    
    It can also test if the test case is valid (within the constraints)
    
    >> print tc.isValid()
    True
    >> invalid_test_case = TestCase(2000, 10, "i love hacking")
    >> print invalid_test_case.isValid()
    False
    
    """
    def __init__(self, width, height, text):
        # Your basic constructor.
        self.height = height
        self.width = width
        self.text = text
        self.tokens = text.split(" ")
        
    def __str__(self):
        # Give Python a little help printing TestCases
        return "Height = %s, Width = %s, Text = %s" % (self.height, self.width, self.text)
    
    def isValid(self):
        """
        Check if the test case is within the constraints.
        They are as follows:
        1 <= W, H <= 1000
        The text will contain only lower-case letters a-z, upper-case letters A-Z,
            digits 0-9 and the space character
        The text will not start or end with the space character, and will never
            contain two adjacent space characters
        The text in each case contains at most 1000 characters 
        """
        # Check height constraints
        if self.height > 1000 or self.height < 1:
            return False
        
        # Check width constraints
        if self.width > 1000 or self.width < 1:
            return False
        
        # Check text length constraint
        if len(self.text) > 1000:
            return False
        
        # Check there are only a-z, A-Z, 0-9, and spaces
        if contains_invalid_chars.search(self.text) != None:
            return False
        
        # Check there are no double spaces
        if contains_double_space.search(self.text) != None:
            return False
        
        # Check it does not begin or end with a space
        if self.text.startswith(" ") or self.text.endswith(" "):
            return False
        
        return True
    
    def maxFontSizeOnOneLine(self):
        """
        Does a quick calculation to tell you how big a font size would allow all the
        words to find on one line.
        
        This provides a good starting point for size iterations.
        """
        return self.width//len(self.text)
        
    def maxFontSizeForLongestWord(self):
        """
        Does a quick calculation to tell you how big a font size would allow the 
        longest word to fit.
        
        This provides a good maximum point for size iterations.
        """
        longest_word = max(self.tokens, key=len)
        return self.width//len(longest_word)
        
    
    def fontWillFit(self, font_size):
        """
        Checks if the given font size will work for the height and width of the
        billboard.
        
        One might say, "this is where the magic happens."
        """
        
        # Will the whole string fit on one line. Not needed, but a good sanity check.
        if len(text) * font_size < self.width and font_size > self.height:
            return True
        
        # Keep track of how many lines we are going to use
        number_of_lines = 1
        
        # Holds the length of the current line
        current_line_length = 0
        
        for token in self.tokens:
            # Current word's length, in inches
            length = len(token) * font_size
            
            # Check if the single token is too big for one line  
            if length > self.width:
                # If it is, this font is too big.
                return False
            
            # Check for one of the following three cases:
            # 1. There are no words on this line
            # 2. The token with a space can be added to the current line, without 
            #    exceeding allowed width.
            # 3. Neither 1 nor 2
            if current_line_length == 0:
                # In this case, just add the length to the current_line_length
                # The key here? No space.
                current_line_length += length
            elif length+current_line_length+(1*font_size) <= self.width:
                # This word (with a space) will fit on the current line.
                current_line_length += length+(1*font_size)
            else:
                # This word is the beginning of a new line.
                # Add one to the number of lines
                number_of_lines += 1
                # Set the new line length equal to the length of the current token.
                current_line_length = length
        
        # Check that we haven't exceeded the height with out number of lines
        if number_of_lines*font_size > self.height:
            return False
        
        # If everything went according to plan, this font will work.
        return True
        
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
        width, height, text = trimmed_line.split(" ", 2)
        try:
            new_test_case = TestCase(int(width), int(height), text)
        except ValueError:
            raise FacebookShenanigansException("Couldn't turn either %s or %s into an int. Calling shenanigans and quitting." % (height, width))
        
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
    
    # Binary Search for the biggest font
    low = test_case.maxFontSizeOnOneLine()
    high = test_case.maxFontSizeForLongestWord()
    font_size = low
    
    # Check if the high works
    if test_case.fontWillFit(high):
        #print "high font fits", high
        font_size = high
    else:
        # Do binary search
        font_size = 0
        while low < high:
            mid = (low+high) // 2
            #print "Testing font size ", mid
            if(test_case.fontWillFit(mid)):
                low = mid+1
                if font_size < mid:
                    font_size = mid
            else:
                high = mid
    
    
    # Output our results
    print "Case #%s: %s" % (count_number, font_size)
    
    count_number += 1
