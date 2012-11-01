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

def AVsB(a, b):
    if (a.p < b.p and a.w <= b.w) or (a.p <= b.p and a.w < b.w):
        # A Preferred OVER B.
        return 1
    elif (b.p < a.p and b.w <= a.w) or (b.p <= a.p and b.w < a.w):
        # B Preferred OVER A.
        return -1
    else:
        # Neither is preferred over the other
        return 0

class Product:
    def __init__(self, p, w, i):
        self.p = p
        self.w = w
        self.i = i
        
    def __repr__(self):
        return "< p = %s, w = %s, i = %i >" % (self.p, self.w, self.i)


n = 36 
p1 = 1
w1 = 1 
m = 4 
k = 9 
a = 1 
b = 0 
c = 1 
d = 0

"""
# Test 3 settings
n = 1581945094
p1 = 9999991
w1 = 1
m = 9999991
k = 9999989
a = 159999857
b = 489999556
c = 549999396
d = 719999209
"""

factors_of_m = factor(m)
factors_of_k = factor(k)
min_factor_of_m = min(factors_of_m)
min_factor_of_k = min(factors_of_k)
min_m_k = min_factor_of_m + min_factor_of_k

full_cycle = min(min_m_k, n)
pi = p1
wi = w1

possible_bargains = [Product(p1,w1,1)]
possible_terribles = [Product(p1,w1,1)]

bargains_points = [Product(p1,w1,1), Product(p1,w1,1)]
terribles_points = [Product(p1,w1,1), Product(p1,w1,1)]

for i in range(2, full_cycle+1):
    if i%10000 == 0:
        print i, "of", full_cycle
    pi = ((a*pi+b)%m)+1
    wi = ((c*wi+d)%k)+1
    cp =  Product(pi, wi, i)
    #print "current_product = ", cp
    
    point_one_test = AVsB(cp, bargains_points[0])
    point_two_test = AVsB(cp, bargains_points[1])
    if point_one_test == 1 and point_two_test  == 1:
        # Current was better than both. Definitely not a terrible deal.
        #print "Current was better than both. All bargins invalid."
        possible_bargains = [cp]
        bargains_points = [cp, cp]
    elif point_one_test == 0 and point_two_test  == 0:
        # Deal was on par with other deals. Add it to the possibles.
        #print "Deal was on par with other deals. Add it to the possibles."
        bargains_points.pop()
        bargains_points.append(cp)
        possible_bargains.append(cp)
    elif point_one_test == -1 and point_two_test  == -1:
        # Current Product worse than our two points. All deals invalid.
        #print "Current Product worse than our two points. Not a bargin."
        pass

    elif (point_one_test == 0 or point_two_test == 0) and (point_one_test == -1 or point_two_test  == -1):
        # Deal was on par with one, and worse than another.
        # Ignore
        pass
    else:
        # One of the two points was not a terrible deal. Start again.
        #print "One of the two points was not a bargin deal. Start again."
        #print "pt, start = ", possible_bargains
        for bargain in possible_bargains:
            if AVsB(cp, terrible) == 1:
                possible_bargains.remove(bargain)
        possible_bargains.append(cp)
        #print "pt, finish = ", possible_bargains
        if( len(possible_bargains) < 2 ):
            bargains_points = [cp, cp]
        else:
            bargains_points = [possible_terribles[0], possible_terribles[1]]
    
    point_one_test = AVsB(cp, terribles_points[0])
    point_two_test = AVsB(cp, terribles_points[1])
    if point_one_test == 1 and point_two_test  == 1:
        # Current was better than both. Definitely not a terrible deal.
        #print "Current was better than both. Definitely not a terrible deal."
        pass
    elif point_one_test == 0 and point_two_test  == 0:
        # Deal was on par with other deals. Add it to the possibles.
        #print "Deal was on par with other deals. Add it to the possibles."
        terribles_points.pop()
        terribles_points.append(cp)
        possible_terribles.append(cp)
    elif point_one_test == -1 and point_two_test  == -1:
        # Current Product worse than our two points. All deals invalid.
        #print "Current Product worse than our two points. All deals invalid."
        possible_terribles = [cp]
        terribles_points = [cp, cp]
    elif (point_one_test == 0 or point_two_test == 0) and (point_one_test == 1 or point_two_test  == 1):
        # Deal was on par with one, and better than another.
        # Ignore
        pass
    else:
        # One of the two points was not a terrible deal. Start again.
        #print "One of the two points was not a terrible deal. Start again."
        #print "pt, start = ", possible_terribles
        for terrible in possible_terribles:
            if AVsB(cp, terrible) == -1:
                possible_terribles.remove(terrible)
        possible_terribles.append(cp)
        print "pt, finish = ", possible_terribles
        if( len(possible_terribles) < 2 ):
            terribles_points = [cp, cp]
        else:
            terribles_points = [possible_terribles[0], possible_terribles[1]]

print len(possible_terribles), possible_terribles
print len(possible_bargains), possible_bargains

number_of_full_cycles = n/(m+k)
remaining_positions = n%(m+k)
total_terribles = number_of_full_cycles * len(possible_terribles)
total_bargains = number_of_full_cycles * len(possible_bargains)

for p in possible_terribles:
    if p.i <= remaining_positions:
        total_terribles += 1

for p in possible_bargains:
    if p.i <= remaining_positions:
        total_bargains += 1

print "total_terribles =", total_terribles
print "total_bargains =", total_bargains
"""
full_cycle = min(max(m,k), n)
pi = p1
wi = w1
products = [Product(p1,w1,1)]

for i in range(2, n+1):
    pi = ((a*pi+b)%m)+1
    wi = ((c*wi+d)%k)+1
    products.append(Product(pi, wi, i))

bargain_positions = []
terrible_positions = []

for product in products:
    print "Current product: ", product
    is_bargain = True
    is_terrible = True
    for possible_better in products:
        if possible_better.i == product.i:
            # Ignore self
            pass
        elif possible_better.p < product.p and possible_better.w <= product.w:
            #print "Possible better is better!"
            is_bargain = False
        elif possible_better.p <= product.p and possible_better.w < product.w:
            #print "Possible better is better! p2"
            is_bargain = False
        elif product.p < possible_better.p and product.w <= possible_better.w:
            #print "There is a worse product than this one"
            is_terrible = False
        elif product.p <= possible_better.p and product.w < possible_better.w:
            #print "There is a worse product than this one"
            is_terrible = False
            
    if is_bargain:
        print "Adding to bargains"
        bargain_positions.append(product.i)
        #bargains += 1
        
    if is_terrible:
        print "Adding to terrible"
        terrible_positions.append(product.i)
        #terrible += 1

print "bargain_positions =", bargain_positions
print "terrible_positions =", terrible_positions


products = [ Product(p1, w1, 1) ]
print "P[1] =", p1
print "W[1] =", w1
print ""
pi = p1
wi = w1
for i in range(2, n+1):
    pi = ((a*pi+b)%m)+1
    wi = ((c*wi+d)%k)+1
    products.append(Product(pi, wi, i))
    print "P[%s] = %s" % (i, pi)
    print "W[%s] = %s" % (i, wi)
    print ""
    
print products
sorted_prices = list(products)
sorted_prices.sort(key=lambda product: product.p)
sorted_weights = list(products)
sorted_weights.sort(key=lambda product: product.w)  

# A is better than B:
# if Cost A < Cost B and Weight A <= Weight B -- OR --
# if Cost A <= Cost B and Weight A < Weight B
bargains = 0
terrible = 0
for product in sorted_prices:
    print "Current product: ", product
    is_bargain = True
    is_terrible = True
    for possible_better in sorted_weights:
        if possible_better.i == product.i:
            # Ignore self
            pass
        elif possible_better.p < product.p and possible_better.w <= product.w:
            #print "Possible better is better!"
            is_bargain = False
        elif possible_better.p <= product.p and possible_better.w < product.w:
            #print "Possible better is better! p2"
            is_bargain = False
        elif product.p < possible_better.p and product.w <= possible_better.w:
            #print "There is a worse product than this one"
            is_terrible = False
        elif product.p <= possible_better.p and product.w < possible_better.w:
            #print "There is a worse product than this one"
            is_terrible = False
            
    if is_bargain:
        print "Adding to bargains"
        bargains += 1
        
    if is_terrible:
        print "Adding to terrible"
        terrible += 1
        
print "bargains =", bargains
print "terrible =", terrible
    
    #print "Product %s is better than %s other products (by weight)" % (product.i, 4-weight_index)
    #print "Product %s is better than %s other products (by price)" % (product.i, 4-price_index)
"""

"""
for product in products:
    print "data.addRow([%s, %s, null]);" % (product.i, product.p)
    print "data.addRow([%s, null, %s]);" % (product.i, product.w)

    data.addRow([1, 2, null]);
    data.addRow([1, null, 3]);
    data.addRow([2, 1, null]);
    data.addRow([2, null, 1]);
    data.addRow([3, 5, null]);
    data.addRow([3, null, 2]);
    data.addRow([4, 4, null]);
    data.addRow([4, null, 5]);
    data.addRow([5, 3, null]);
    data.addRow([5, null, 7]);
    data.addRow([6, 2, null]);
    data.addRow([6, null, 6]);

    data.addRow([2, 3, null]);
    data.addRow([1, 1, null]);
    data.addRow([5, 2, null]);
  data.addRow([4, 5, null]);
  data.addRow([3, 7, null]);
  data.addRow([2, 6, null]);
  data.addRow([1, 3, null]);
  data.addRow([5, 1, null]);
data.addRow([4, 2, null]);
  data.addRow([3, 5, null]);
  data.addRow([2, 7, null]);
"""
    