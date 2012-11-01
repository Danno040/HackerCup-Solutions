#!/usr/bin/python

INPUT_FILE_PATH = "./auction_input.txt"

# We will throw this if something didn't meet the constraints.
class FacebookShenanigansException(Exception): pass


""" 
        Get the factors for a number 
        (Note: Not optimised for tail recursion) 
"""  
def factor(n):  
        if n == 1: return [1]  
        i = 2  
        limit = n**0.5  
        while i <= limit:  
                if n % i == 0:  
                        ret = factor(n/i)  
                        ret.append(i)  
                        return ret  
                i += 1  
  
        return [n]  

class Product:
    """
    Object to represent a product. Keeps track of price, weight, and product number.
    """
    def __init__(self, p, w, i):
        self.p = p
        self.w = w
        self.i = i
        
    def __repr__(self):
        return "< p = %s, w = %s, i = %i >" % (self.p, self.w, self.i)

class TestCase:
    """
    Holds the test case details and offers a method to find how many bargains and
    terrible deals for that case.
    
    Can check if the test case is within the constrains:
    >> tc = TestCase(5,1,3,4,7,1,0,1,2)
    >> print tc.isValid()
    True
    
    To get how many terrible deals and how many bargains exist:
    >> tc = TestCase(5,1,3,4,7,1,0,1,2)
    >> print tc.findNumberOfTerribleDealsAndBargains()
    (3, 3)
    
    """
    def __init__(self, n, p1, w1, m, k, a, b, c, d):
        # Your basic constructor.
        self.n = n
        self.p1 = p1
        self.w1 = w1
        self.m = m
        self.k = k
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def isValid(self):
        """
        Checks if Test Case values are within the contraints.
        """
        # 1 <= N <= 10^18
        if self.n < 1 or self.n > (10**18):
            return False
        
        # 1 <= M, K <= 10^7
        if self.m < 1 or self.m > (10**7):
            return False
        
        if self.k < 1 or self.k > (10**7):
            return False
        
        # 1 <= p1 <= M
        if self.p1 < 1 or self.p1 > self.m:
            return False
        
        # 1 <= w1 <= K
        if self.w1 < 1 or self.w1 > self.k:
            return False
        
        # 0 <= A,B,C,D <= 10^9
        max_of_abcd = max(self.a, self.b, self.c, self.d)
        if max_of_abcd < 0 or max_of_abcd > (10**9):
            return False
        
        return True
    
    def findNumberOfTerribleDealsAndBargains(self):
        """
        Does the work for finding the number of bargains and terrible deals.
        
        Returns a tuple: (terrible deals, bargains)
        """
        # Determine a "full cycle". A full cycle is when every possible value has
        # been seen.
        print "m = %s, k = %s" % (self.m, self.k)
        m_plus_k = self.m * self.k
        min_m_k = m_plus_k
        #factors_of_m = factor(self.m)
        #factors_of_k = factor(self.k)
        #print factors_of_m, factors_of_k
        #min_m_k = min(factors_of_m) * min(factors_of_k)
        
        full_cycle = min(min_m_k, self.n)
        print "Full Cycle in", full_cycle
        
        # Set up Pi-1. I call it pi, because i-1 is weird for a variable name
        pi = self.p1
        wi = self.w1
        print pi, wi
        
        # Create arrays to hold the bargains and terrible deals. Seed it with the
        # first product. We will remove products as we prove they aren't bargain or
        # terrible deals. 
        possible_bargains = [Product(self.p1,self.w1,1)]
        possible_terribles = [Product(self.p1,self.w1,1)]
        
        # We do range(2, full_cycle+1) because want to go from 2 to N (or M+K)
        for i in range(2, full_cycle+1):
            # Calculate the price of this item
            pi = ((self.a*pi+self.b)%self.m)+1
            # Calculate the weight of this item
            wi = ((self.c*wi+self.d)%self.k)+1
            print pi, wi
            # Check if this bargain is preferred over other bargain in the bin
            # Use add_product to determine if this product should be added to the bin
            add_product = True
            # Use remove_products to keep track of which products need to be removed
            # from the bin
            remove_products = []
            
            for bargain in possible_bargains:
                if (bargain.p < pi and bargain.w <= wi) or (bargain.p <= pi and bargain.w < wi):
                    # The bargain in the bin is preferred. Current product not a bargain.
                    add_product = False
                    
                    # Because this product was definitely not a bargain, we can stop
                    break
                elif (pi < bargain.p and wi <= bargain.w ) or (pi <= bargain.p and wi < bargain.w ):
                    # This product would be preferred. Possible bargain is not a 
                    # bargain. Remove possible bargain from bin, and add the current
                    # one.
                    remove_products.append(bargain)
                else:
                    # The current product would not be preferred over other bargain.
                    # And visa versa. Add it to bargain.
                    pass
            
            # Remove any bargains that aren't bargins       
            for bargain in remove_products:
                possible_bargains.remove(bargain)
            
            # Add the product to the bin, if we've determined it's a bargain   
            if add_product:
                possible_bargains.append(Product(pi, wi, i))
            
            
            # Check if this bargain is a more terrible deal then the ones in the bin
            add_product = True
            remove_products = []
            for terrible in possible_terribles:
                if (terrible.p < pi and terrible.w <= wi) or (terrible.p <= pi and terrible.w < wi):
                    # The current product is worse than the product in the bin.
                    # Remove that product, add the current one
                    remove_products.append(terrible)
                elif (pi < terrible.p and wi <= terrible.w ) or (pi <= terrible.p and wi < terrible.w ):
                    # The current product would be preferred over terrible.
                    # Do not add this product
                    add_product = False
                    
                    # Because we've determined this is not a terrible deal, we can
                    # stop
                    break
                else:
                    # The current product would not be preferred over this terrible
                    # deal. And visa versa. Add it to terrible deals bin.
                    pass
            
            # Remove any terrible deals we determined aren't that terrible.
            for terrible in remove_products:
                possible_terribles.remove(terrible)
            
            # Add the product to the terrible deals, if we've determined it so.
            if add_product:
                possible_terribles.append(Product(pi, wi, i))
        
        # Now that we have seen all possible values, we need to see how many times
        # we cycled through the values.
        
        print possible_terribles
        print possible_bargains
        
        # Number of full cycles will be 1, if we use N instead of M+K. However, if
        # M+K was less than N, we came out ahead and value can be greater than one.        
        number_of_full_cycles = self.n//(m_plus_k)
        
        # If there was not an even number of cycles, we need to see how far we made
        # it into the last cycle.
        remaining_positions = self.n%(m_plus_k)
        
        # Multiply the number of deals by how many times every value was seen
        total_terribles = number_of_full_cycles * len(possible_terribles)
        total_bargains = number_of_full_cycles * len(possible_bargains)
        
        # If a complete cycle wasn't complete, account for the deals that were seen.
        if remaining_positions != 0:
            for p in possible_terribles:
                if p.i <= remaining_positions:
                    total_terribles += 1
            
            for p in possible_bargains:
                if p.i <= remaining_positions:
                    total_bargains += 1
        
        # Return the results
        return total_terribles, total_bargains
    
        
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
        n, p1, w1, m, k, a, b, c, d = trimmed_line.split(" ")
        try:
            new_test_case = TestCase(int(n), int(p1), int(w1), int(m), int(k), int(a), int(b), int(c), int(d))
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
    
    bargains, terrible = test_case.findNumberOfTerribleDealsAndBargains()
    
    # Output our results
    print "Case #%s: %s %s" % (count_number, bargains, terrible)
    
    count_number += 1
