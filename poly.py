import mod
import rsm
import copy
import random
import legendre

#First it is necessary to create an object that behaves like a polynomial.

class poly(object):
    """An object which behaves like a polynomial over a finite field
       Coefficients are in ascending orders of x (a0 + a1x + a2x^2 etc...)"""
#When creating a new polynomial, the imputs are a list of coefficients, and the degree of the field."""
    def __init__(self, coeffs, p):
#If the list of coefficients is empty, the polynomial is given the constant coefficient a0 = 0.
        if coeffs == []:
            coeffs =[0]
#The polynomial is given the attribute "degree".
        self.__degree = len(coeffs)-1
#Each element of the list of coefficients should be a "modp" object; any that are not, are made to be.
        for i in range(len(coeffs)):
            if not isinstance(coeffs[i], mod.modp):
                coeffs[i] = mod.modp(coeffs[i],p)
        self.__coeffs = coeffs
        self.p = p
#This next method builds the output displayed when you "print" a polynomial.
    def __str__(self):
        s = ""
        for i in range(len(self.coeffs)):
            if i == 0:
                s += str(self.coeffs[i])
            elif i > 0 and self.coeffs[i] > 0:
                s += " + " + str(self.coeffs[i]) + "x^" + str(i)
            elif i > 0 and self.coeffs[i] < 0:
                s += " - " + str(-self.coeffs[i]) + "x^" + str(i)
        return s

#Since some operations could rewrite the coefficients or degree of the polynomial, these two attributes
#are made private.
    @property
    def coeffs(self):
        return self.__coeffs
    @property
    def degree(self):
        return self.__degree

#The polynomials are equipped with the standard operations to make later code seem more intuitive.
#Note:  When the interpreter sees "a + b", it first checks to see whether a has an "__add__" operation
#       which is compatible with both a and b. If it cannot find one, it then checks to see if b has a
#       "__radd__" operation that is compatible. If neither exist, it returns an error.
#       It behaves similarly for *,//,% and any other binary operation.

    def __add__(self, other):
#To allow addition of scalars and polynomials, the __add__ method first checks to see if "other" is a poly,
# and converts it into one if it isn't one already.
        if not isinstance(other, poly):
            other = poly([other],self.p)
#Now it creates an empty list big enough to hold the coefficients of the sum of the two polynomials.
        sum_terms = [0] * max(len(self.coeffs),len(other.coeffs))
#Despite my best efforts, when interpretting f = f + g, the coefficients of f are rewritten.
#Thus, so as not to change the original polynomial, it is necessary to create a copy of "self"
#for use in the calculations.
        for i in range(len(self.coeffs)):
            sum_terms[i] = copy.deepcopy(self.coeffs[i])
#Now the method carries out the addition,
        for i in range(len(other.coeffs)):
            sum_terms[i] = sum_terms[i] + other.coeffs[i]
#and then removes any trailing coefficients which are 0,
#(ie 0 + 1x + 0x^2 + 3x^3 + 0x^4 + 0x^5 becomes 0 + 1x + 0x^2 + 3x^3)
        if not sum_terms == [] and not sum_terms == [0]:
            while sum_terms[len(sum_terms) -1] == 0:
                sum_terms = sum_terms[:-1]
#and returns a new polynomial with the coefficients calculated.
        return poly(sum_terms, self.p)

#Since addition is commutative, the right addition simply makes sure both variables are polys,
#and then passes the variables through to the left addition.
    def __radd__(self,other):
        if not isinstance(other, poly):
            copy = poly([other],self.p)
        return poly.__add__(self, copy)

#The multiplication and right multiplication methods have exactly the same format as addition. 
    def __mul__(self, other):
        if not isinstance(other, poly):
            other = poly([other],self.p)
        product_terms = [0] * ((len(self.coeffs)-1) + (len(other.coeffs)-1)+1)
        for i in range(len(self.coeffs)):
            for j in range(len(other.coeffs)):
                product_terms[i+j] = self.coeffs[i] * other.coeffs[j] + product_terms[i+j]
        while product_terms[len(product_terms) -1] == 0:
            product_terms = product_terms[:-1]
        return poly(product_terms, self.p)
    def __rmul__(self, other):
        if not isinstance(other, poly):
            copy = poly([other],self.p)
        return poly.__mul__(self, copy)
#This next method allows subtraction.
    def __neg__(self):
        for i in range(len(self.coeffs)):
            self.coeffs[i] = -self.coeffs[i]
#This next method tests whether two polynomials are equal by comparing coeffs.
    def __eq__(self,other):
        if not isinstance(other, poly):
            other = poly([other],self.p)
        if self.degree != other.degree:
            return False
        for i in range(self.degree+1):
            if self.coeffs[i] != other.coeffs[i]:
                return False
        else:
            return True
#This method allows powers (again using the repeated squaring method):
    def __pow__(self, other):
        result = poly([1], self.p)
        base = copy.deepcopy(self)
        exponent = legendre.binary(other)
        exponent.reverse()
        for i in exponent:
            if i == 1:
               result = (result * base)
            base = (base * base)
        return result
#This method is a division algorithm. It returns the quotient.
    def __floordiv__(self, other):
        if not isinstance(other, poly):
            other = poly([other],self.p)
        remainder = copy.deepcopy(self.coeffs)
        quotient = [mod.modp(0,self.p)] * (len(self.coeffs) - len(other.coeffs)+ 1)
        for i in range (len(self.coeffs) - len(other.coeffs) + 1):
        #First it calculates "coeff" such that (self_n)*x^n = coeff*(other_m)*x^m,
        #where m and n are the leading coefficients of self and other respectively.
            coeff = remainder[len(self.coeffs)-i-1]*mod.modp(
                legendre.rsm(other.coeffs[len(other.coeffs)-1].val, self.p-2, self.p), self.p)
        #It then adds "coeff" to the appropriate power of x in "quotient".
            quotient[len(self.coeffs) - len(other.coeffs)-i] = quotient[len(self.coeffs) - len(other.coeffs)-i] + coeff
        #It then subtracts coeff*(the appropriate coefficient of "other") from each coefficient of the remainder.
            for j in range(len(other.coeffs)):
                q = mod.modp.__neg__(coeff * other.coeffs[len(other.coeffs)-j-1])
                remainder[len(self.coeffs)-i-j-1] = remainder[len(self.coeffs)-i-j-1] + q
        #Finally, it removes any trailing "0" coefficients.
        if len(quotient) > 0:
            while quotient[len(quotient) -1] == 0:
                quotient = quotient[:-1]
                if len(quotient) == 0:
                    break

        return poly(quotient, self.p)

#The __mod__ method is exactly the same as the __floordiv__ method,
#except that it returns the remainder instead of the quotient.
    def __mod__(self, other):
        if not isinstance(other, poly):
            other = poly([other],self.p)
        remainder = copy.deepcopy(self.coeffs)
        quotient = [mod.modp(0,self.p)] * (len(self.coeffs) - len(other.coeffs)+ 1)
        for i in range (len(self.coeffs) - len(other.coeffs) + 1):
            coeff = remainder[len(self.coeffs)-i-1]*mod.modp(legendre.rsm(other.coeffs[len(other.coeffs)-1].val, self.p-2, self.p), self.p)
            quotient[len(self.coeffs) - len(other.coeffs)-i] = quotient[len(self.coeffs) - len(other.coeffs)-i] + coeff
            for j in range(len(other.coeffs)):
                remainder[len(self.coeffs)-i-j-1] = remainder[len(self.coeffs)-i-j-1] + mod.modp.__neg__(coeff * other.coeffs[len(other.coeffs)-j-1])
        if len(remainder) > 0:
            while remainder[len(remainder) -1] == 0:
                remainder = remainder[:-1]
                if len(remainder) == 0:
                    break
        return poly(remainder, self.p)


#Now we define a function "gcd" which gives the highest common factor of two polynomials over a finite field.
def gcd(f,g,p = ""):
#First the function makes sure it has the proper variables
#(two polynomials or one polynomial and one list of coefficients or two lists of coefficients and a modulus)
    if not isinstance(f, poly) and isinstance(g, poly):
        f = poly(f, g.p)
        if p == "":
            p = f.p
    elif not isinstance(g, poly) and isinstance(f, poly):
        g = poly(g, f.p)
        if p == "":
            p = f.p
    elif not isinstance(f, poly) and not isinstance(g, poly) and p == "":
            print("Must specify p")
            return
    elif p != "":
        f = poly(f, p)
        g = poly(g, p)          


#Next, it decides which polynomial has the highest degree.
    if f.degree >= g.degree:
        c = copy.deepcopy(f)
        d = copy.deepcopy(g)
    else:
        c = copy.deepcopy(g)
        d = copy.deepcopy(f)
#Finally it runs Euclid's algorithm to determine the highest common factor.
#At each stage it prints "r_(i-2) = q_(i)*r_(i-1) + r_(i)".
    remainder = [c , d]
    while True:
        remainder.append(copy.deepcopy(remainder[-2] % remainder[-1]))
#Note: it runs until the remainder is 0,
        if remainder[-1].coeffs == [0]:
            break
#and then returns the previous remainder, dividing through by the leading coeff.
    return remainder[-2] // remainder[-2].coeffs[-1]


##This function implements modular exponentiation by repeated squaring
##in the case where the modulus is a polynomial.
def poly_modular_rsm(a, exp, mod):
    result = poly([1], a.p)
    base = copy.deepcopy(a)
    exponent = legendre.binary(exp)
    exponent.reverse()
    for i in exponent:
        if i == 1:
           result = (result * base) % mod
        base = (base * base) % mod
    return result


#This next function calculates square roots using the method described in question 7.
def square_root(a,p):
#First it creates the polynomial "(x^p - x) mod (x^2 - a)"
    f = poly([-a,0,1],p)
    g = poly([0,1], p)
    g = poly_modular_rsm(g,p,f)
    g = g + poly([0,-1],p)
#Then it finds the highest common factor of f and g
    h = gcd(f,g)
#Now, it generates a random "small" v, and tries (x + v)^((p−1)/2) − 1  mod (x^2 - a)
    vlist = []
    for i in range(int(f.p-1/2)):
        vlist.append(i)
    random.shuffle(vlist)
    trial_no = 0
    for v in vlist:
        trial_v = poly_modular_rsm(poly([v,1],f.p),(int((f.p-1)/2)) + -1, f)
        trial = gcd(trial_v,h)
        trial_no += 1
#If the gcd is a linear factor, then it has found a root, and hence both roots.
##        if trial.degree == 1:
##            return(str(trial), "&", str(trial.coeffs[0]), "&",
##                   str(-trial.coeffs[0]), "&", trial_no)
        if trial.degree == 1:
            return(trial_no)
        if trial_no == 200:
            break
    return("Error")



#This function calculates the roots of a polynomial f using an extension of the method
#in question 7.
def root(f):
    h = copy.deepcopy(f)
# First it generates a random "small" v, and tries (x + v)^((p−1)/2) − 1
    vlist = []
    for i in range(1000):
        vlist.append(i)
    random.shuffle(vlist)
    trial_no = 0
    roots = []
    for v in vlist:
        trial_v = poly_modular_rsm(poly([v,1],f.p),(int((f.p-1)/2)),h) + -1
        trial = gcd(trial_v,h)
        trial_no += 1
#If the gcd is a linear factor, then it has found a root.
        if trial.degree == 1:
#The root is added to a list of roots.
            roots.append(trial)
#It then divides the polynomial by this root and tries again.
            h = h // trial
        trial_no += 1
#If the polynomial remaining is of degree 0, then all roots have been found,
#and the function returns them.
        if h.degree == 0:
            break
#If after 100 trials, the degree is still not 0, then the function assumes that all roots have been found,
#and returns them, along with the remaining polynomial. 
        if trial_no == 100:
            break
    list_of_roots = []
    for i in roots:
        list_of_roots.append(str(i))
    product = 1
    for i in roots:
        product = product * i

    print(f)    
    print(list_of_roots)
    if trial_no == 100:
        if not f % product == 0:
            print("ERROR")
            return("ERROR")
        print(f, "= (", product, ") * (", f // product, ")")
    return(roots)


#The rest of this program consists of bits of code used to generate LaTeX tables and program test output.


##Creating Table 5
##
##t = 0
##l = []
##while t <5:
##    r = random.randint(0,66)
##    if l.count(r) == 0 and legendre.legendre(r,67) == 1:
##        l.append(r)
##        t += 1
##for i in l:
##    print(i, square_root(i,67))
##    print(i, square_root(i,67))
##    print(i, square_root(i,67))
##
##t = 0
##l = []
##while t <5:
##    r = random.randint(0,3510)
##    if l.count(r) == 0 and legendre.legendre(r,3511) == 1:
##        l.append(r)
##        t += 1
##for i in l:
##    print(i, square_root(i,3511))
##    print(i, square_root(i,3511))
##    print(i, square_root(i,3511))

##trials = [0]*15
##n = 0
##while n < 500:
##    r = random.randint(1,103)
##    if legendre.legendre(r, 103) == 1:
##        t = square_root(r, 103)
##        trials[t] += 1
##        n += 1
##print(trials)


##for i in range(40):
##    if legendre.legendre(i,103) == 1:
##        print(str(square_root(i,103)))

##        if trial.degree == 1 and roots.count(trial) == 0:
##            roots.append(trial)
##        trial_no += 1
##        if len(roots) == 2:
##            break
##        if trial_no == 50:
##            break
##    list_of_roots = []
##    for i in roots:
##        list_of_roots.append(str(i))
##    print(list_of_roots, trial_no)
##    return(roots)

##print("gcd =", gcd([5,5,6,1],[3,6,13,1], 109), "\n")
##print("gcd =", gcd([4,9,2,1],[9,7,3,1],131), "\n")
##print("gcd =", gcd([12,9,3,1],[4,12,6,1],157), "\n")

##root(poly([6,0,12,5,1], 35564117))
##root(poly([4,7,3,1,1], 35564117))
##root(poly([8,3,15,4,1], 35564117))

