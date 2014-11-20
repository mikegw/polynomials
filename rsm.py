def binary(number):
    """Converts a number into binary"""
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

def rsm(base, power , modulus):
    """Exponetiation using repeated squaring"""
    exponent = binary(power)
    exponent.reverse()
    result = 1
    for i in exponent:
        if i == 1:
           result = (result * base) % modulus
        base = (base * base) % modulus
    if result % modulus == modulus -1:
        result = -1
    return result
