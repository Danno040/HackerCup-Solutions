#!/usr/bin/python

INPUT_FILE_PATH = "./recover_the_sequence.txt" #"./recover_the_sequence_input.txt"

import math

# We will throw this if something didn't meet the constraints.
class FacebookShenanigansException(Exception): pass

def given_merge_sort(arr):
    """
    Implements the pseudo-code for merge_sort
    """
    n = len(arr)
    if n <= 1:
        return arr
    
    mid = int(math.floor(n/2))
    first_half = given_merge_sort(arr[0:mid])
    second_half = given_merge_sort(arr[mid:])
    return given_merge(first_half, second_half)
    
def given_merge(arr1, arr2):
    """
    Implements the pseudo-code for merge
    """
    result = []
    while len(arr1) > 0 and len(arr2) > 0:
        if arr1[0] < arr2[0]:
            print 1
            result.append(arr1[0])
            arr1.pop(0)
        else:
            print 2
            result.append(arr2[0])
            arr2.pop(0)
    
    result += arr1
    result += arr2
    return result
    
def checksum(arr):
    """
    Implements the pseudo-code for checksuming an array
    """
    result = 1
    for i in range(len(arr)):
        result = (31 * result + arr[i]) % 1000003
    return result

class TestCase:
    """
    """
    def __init__(self, n, output):
        # Your basic constructor.
        self.n = n
        self.output = output
        # Keeps track of how far into the input you are
        self.i = 0
        
    def __str__(self):
        # Give Python a little help printing TestCases
        return "< n = %s, output = %s >" % (self.n, self.output)
    
    def isValid(self):
        """
        """
        
        return True
    
    def reverse_sort(self, sequence):
        """
        Implements the pseudo-code for merge sort.
        """
        n = len(sequence)
        if n <= 1:
            return sequence
        
        mid = int(math.floor(n/2))
        first_half = self.reverse_sort(sequence[0:mid])
        second_half = self.reverse_sort(sequence[mid:])
        return self.reverse_merge(first_half, second_half)
    
    def reverse_merge(self, arr1, arr2):
        """
        Instead of actually sorting, we are going to move stuff around based on
        the output we were given.
        """
        result = []
        while len(arr1) > 0 and len(arr2) > 0:
            if self.output[self.i] == "1":
                #print 1
                result.append(arr1[0])
                arr1.pop(0)
            else:
                #print 2
                result.append(arr2[0])
                arr2.pop(0)
            self.i += 1
        
        result += arr1
        result += arr2
        return result
    
    def find_original_sequence(self):
        """
        Basically, here's the idea:
        Generate an index space like   [0, 1, 2, 3, 4]
        "sort" it using the output we are given.
        This results in something like [3, 0, 1, 4, 2]
        Which we know has values of:   [1, 2, 3, 4, 5]
        Now we know 0 = 2, 1 = 3, 2 = 5, 3 = 1, 4 = 4
        We now know the starting sequence was: [2, 3, 5, 1, 4]
        """
        # Index sequence. 0-(n-1)
        index_sequence = range(self.n)
        # Sort by using the given output
        new_index_sequence = self.reverse_sort(index_sequence)
        
        # Values from 1 to N
        proper_range = range(1, self.n+1)
        
        # We will hold the final result here.
        result = []
        
        # Go through 0 to n-1, place the correct value in that index
        for i in range(self.n):
            # Find where index i is in new_index_sequence
            correct_index = new_index_sequence.index(i)
            # Append the value that goes with that index
            result.append( proper_range[correct_index] )
        
        return result
        
# Holds the number of expected test cases
number_of_test_cases = -1

# Holds all of our test cases.
test_cases = []

# Open the input file
input_file = open(INPUT_FILE_PATH, "r")

n = -1

# Read in input file
for line in input_file.readlines():
    # Strip off the new lines (and prey I didn't miss one)
    trimmed_line = line.strip("\r\n")
    if number_of_test_cases == -1:
        try:
            number_of_test_cases = int(trimmed_line)
        except ValueError:
            raise FacebookShenanigansException("Couldn't turn %s into an int. Calling shenanigans and quitting." % trimmed_line)
    elif n == -1:
        n = int(trimmed_line)        
    else:
        output = trimmed_line
        new_test_case = TestCase(n, output)
        
        if new_test_case.isValid():
            test_cases.append(new_test_case)
            n = -1
        else:
            raise FacebookShenanigansException("Invalid Test Case!")

# All of the file is read in, we can close it.
input_file.close()

if number_of_test_cases != len(test_cases) :
    raise FacebookShenanigansException("Number of cases read (%s) did not match number (%s) expected. Calling shenanigans and quitting." % (len(test_cases), number_of_test_cases))

count_number = 1
for test_case in test_cases:
    # Find the original sequence
    sequence = test_case.find_original_sequence()
    # Output our results
    print "Case #%s: %s" % (count_number, checksum(sequence))
    
    count_number += 1