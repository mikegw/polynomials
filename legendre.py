#This first function converts a number into binary
#for use in the repeated squaring method.
def binary(number):
    p = number
    binary_digits = []
#Find digits a1>a2>...>an such that p = 2^a1 + 2^a2 + ... + 2^an
    while p > 0:
        q = p
        i = -1
        while q >= 1:
            q = (q/2)
            i += 1
        binary_digits.append(i)
        p -= 2**(binary_digits[len(binary_digits)-1])
#if p was 0, this will give an empty list
    if binary_digits == []:         
        return []
    else:
#Form a list [b1,b2,...,bn]
#such that p has binary representation b1b2..bn
        number_in_binary = []
        for i in range(binary_digits[0] + 1):
            if binary_digits.count(binary_digits[0] - i) == 1:
                number_in_binary.append(1)
            else:
                number_in_binary.append(0)
        return number_in_binary


#The next function calculates base^power mod modulus,
#using the repeated squaring method.
def rsm(base, power , modulus):
#First it converts the power into a binary list.
    exponent = binary(power)
    exponent.reverse()
#Starting with result = "base ^ 0",
    result = 1
#it goes through the binary list in increasing powers of 2,
#and if the binary digit is 1, it multiplies the result by the current base,
#modulo the modulus, before squaring the base for use in the next loop.
    for i in exponent:
        if i == 1:
           result = (result * base) % modulus
        base = (base * base) % modulus
    if result % modulus == modulus -1:
        result = -1
    return result

#This function uses Euler's Criterion to calculate the value of
#the legendre symbol (a,p)           
def legendre(a, p):
    return(rsm(a, (p-1)/2, p))


#This function calculates the Jacobi symbol (a,p) using Euler's Criterion,
#multiplicativity and the result (2/p) = (-1)^((p^2 -1)/8)
def jacobi(a,p):
    if a == 1:
        return 1
    if a % p == 0:
        return 0
    elif a % 2 == 0:
        return (-1)**(int((p**2 -1)/8)) * jacobi(a/2, p)
    else:
        return ((-1)**(int((a-1)*(p-1)/4))) * jacobi(p % a, a)


#This function calculates the square root of a mod p, using Tonelli's algorithm.
def squareroot(a,p):
#To avoid unnecessary work, if a = 1 we can simply output +1 and -1.
    if a == 1:
        print(a, "&", 1, "&", -1, "\\\\")
    else:
#It first calculates alpha, n and s such that p-1 = 2^alpha * s where s is odd,
#and n is a quadratic non-residue.
        q = p-1
        alpha = 0
        while True:
            if q % 2 == 0:
                alpha += 1
                q = q/2
            else:
                break
        s = int((p-1)/(2**alpha))
        n = 1
        while True:
            if legendre(n,p) == 1:
                n += 1
            else:
                break
#Then it computes b = n^s (mod p)
        b = rsm(n,s,p)
#It now solves the congruence y^2 ≡ a^s (mod p) by substituting
#y ≡ b^r (mod p) and solving for the binary digits of r.
        r = []
#To do this, for each r_i it first calculates the exponent.
        for i in range(alpha-1):
            e = 0
            for j in range(len(r)):
                e += r[j]*2**j
#It then calculates b^((p-1 - e)*(p-1)/2**(i+1)) using modular exponentiation,
            z1 = rsm(b,(p-1-e),p)
            z2 = rsm(z1,(int((p-1)/(2**(i+1)))),p)
#and multiplies this by a^(s*(p-1)/(2^(i+2))
#(see the solution to q4 for more details)
            z3 = rsm(a**s,int((p-1)/(2**(i+2))),p)
            z = z2 * z3 % p
#Now, if the answer is 1, then r_i is 0,
            if z == 1:
                r.append(0)
#and if the answer is minus 1, then r_i is 1.
            elif z == p-1:
                r.append(1)
            else:
                break
#Once it has solved for the binary digits of r, it calculates y = b^r (mod p)
#(Note: since r is currently the list of binary digits, I have used the letter e
#to represent the number itself.)
        e = 0
        for j in range(len(r)):
            e += r[j]*2**j
        y = rsm(b,e,p)
#Finally, if y is a square root of a^s where is odd, then y*(a^-(s-1)/2) is
#the square root of a (since then (y*(a^-(s-1)/2))^2 = (a^s)*(a^-s)*a = a)
        y = y*rsm(a,p-1-(int((s-1)/2)),p) % p
        if y**2 % p == a:
            print(p, a, "&", y,"&", p-y, "\\\\")
        else:
            print("ERROR")


#The rest of this program consists of bits of code used to
#answer questions 1 to 5, including creating LaTeX tables.



#Create a list of 100 random integers for use in Q1
y = []
import random
for i in range(100):
    y.append(random.randint(1,30275233))


#Create a 9-column LaTeX table containing legendre symbols for
#100 random integers, keeping track of no. of a with (a,30275233) = 1
x = []
t = 0 #tally
for i in y:
    z = legendre(i, 30275233)
    if z == 1:
        t += 1    
    x.append((i, z, t))
for i in range(int(len(x)/3)):
    print(x[3*i][0], "&", x[3*i][1], "&", x[3*i][2], "&", x[3*i+1][0],
          "&", x[3*i+1][1], "&", x[3*i+1][2], "&", x[3*i+2][0], "&",
          x[3*i+2][1], "&", x[3*i+2][2], "\\\\")
print(x[99][0], "&", x[99][1], "&", x[99][2])

#Create a 9-column LaTeX table containing legendre symbols for a in 1,...,100,
#keeping track of no. of a with (a,30275233) = 1
x = []
t = 0
for i in range(1, 100):
    z = legendre(i, 30275233)
    if z == 1:
        t += 1
    x.append((i,z,t))
for i in range(int(len(x)/3)):
    print(x[3*i][0], "&", x[3*i][1], "&", x[3*i][2], "&",
        x[3*i+1][0], "&", x[3*i+1][1], "&", x[3*i+1][2], "&",
        x[3*i+2][0], "&", x[3*i+2][1], "&",  x[3*i+2][2], "\\\\")
print(100,"&",legendre(100, 30275233),"&", t + 1)

#p = 30275233, all quadratic residues mod p between 1 and 20
for i in range(1,21):
    if legendre(i,30275233) == 1:
        squareroot(i,30275233)
    else:
        print(i,"&", "Not a quadratic residue", "\\\\")
        
#A few other values of p and a
#p = 77377, congruent to 1 mod 8
y = []
import random
for i in range(3):
    y.append(random.randint(1,77377))
for i in y:
    if legendre(i,77377) == 1:
        squareroot(i,77377)
    else:
        print(77377, i,"&", "Not a quadratic residue", "\\\\")

#p = 786431, congruent to 1 mod 8.
y = []
for i in range(3):
    y.append(random.randint(1,786431))
for i in y:
    if legendre(i,786431) == 1:
        squareroot(i,786431)
    else:
        print(786431, i,"&", "Not a quadratic residue", "\\\\")

#p = 111181111, congruent to 3 mod 4
y = []
for i in range(2):
    y.append(random.randint(1,111181111))
for i in y:
    if legendre(i,111181111) == 1:
        squareroot(i,111181111)
    else:
        print(111181111, i,"&", "Not a quadratic residue", "\\\\")

#p = 1234133, congruent to 5 mod 8
y = []
for i in range(2):
    y.append(random.randint(1,1234133))
for i in y:
    if legendre(i,1234133) == 1:
        squareroot(i,1234133)
    else:
        print(1234133, i,"&", "Not a quadratic residue", "\\\\")









