'''
RSA PUBLIC-KEY ENCRYPTION SCHEME
 
BY: ALEXANDER A. IVANOV
'''


def gcd(a, b):
    """
    Euclidean Algorithm
    """
    while b != 0:
        (a, b) = (b, a % b)
    return a

def eea(a, b):
    """
    Extended Euclidean Algorithm. 
    Solve for integers x and y:
    ax + by = gcd(a, b)
    """
    if a == 0 :  
        return b, 0, 1
    else:
        gcd, x, y = eea(b % a, a)
        return gcd, y - (b // a) * x, x

def bin_exp(x, n, m): 
    """
    Compute x^n under 
    modulo m using binary 
    exponentiation, assuming that
    m > x (such that x % m = x).
    *** I replaced this with pow() ***.
    """
    if n == 1: 
        return x 
    elif n % 2 == 0: 
        return (bin_exp(x, n/2, m) ** 2) % m
    else: 
        return ((bin_exp(x, (n - 1) / 2, m) ** 2) * x) % m

import random

def MillerRabin(n, t):
    '''
    Miller-Rabin primality test on
    number n, n > 3, for k trials. 
    '''
    
    if n % 2 == 0:
        return False
    
    # Find s such that n - 1 = 2^s * r, r odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1 # d /= 2
        s += 1
    d = n - 1
    r = d // (2 ** s)
    
    
    for i in range(t + 1):
        
        a = random.randrange(2, n - 1)
        y = pow(a, r, n)
        
        if y != 1 and y != n - 1:
            j = 1
            while j <= s - 1 and y != n - 1:
                y = pow(y, 2, n)
                if y == 1:
                    return False
                j += 1
            if y != n - 1:
                return False
    return True

def getPrime(k):
    """
    Generate k-bit prime.
    """
    random.seed(random.randint(0, 1000))

    def primeSieve(B):
        """
        Generate a list of primes
        less than or equal to B.
        """
        isPrime = [True for i in range(B + 1)]
        p = 2
        while B >= p * p:
            if isPrime[p] == True:
                for i in range(p * p, B + 1, p):
                    isPrime[i] = False
            p += 1

        primes = []
        for p in range(2, B + 1):
            if isPrime[p]:
                primes.append(p)
                
        return primes

    def getPrimeCandidate(k):
        '''
        Generate a number divisible
        by all elements in prime list.
        '''
        while True:
            num = random.randrange(2 ** (k - 1) + 1, 2 ** k - 1)

            for prime in primeSieve(350):
                if num % prime == 0 and prime ** 2 <= num:
                    break
                else:
                    return num

    # Get probable prime   
    if __name__ == '__main__':
    	while True:
         pc = getPrimeCandidate(k) # store the prime candidate
         if not MillerRabin(pc, 20):
             continue
         else:
             return pc
             break
         
            
def getStrongPrime():
    """
    If desired, generate strong prime by Gordon's algorithm.
    (of approximately same bitlength as getPrime()).
    """
    s = getPrime(512)
    t = getPrime(512)
    
    i_0 = random.randint(1, 10)
    i = i_0
    r = 2 * i * t + 1
    while not MillerRabin(r, 10):
        i += 1
        r = 2 * i * t + 1
        
    p_0 = 2 * pow(s, r - 2, r) * s - 1
    
    j_0 = random.randint(1, 10)
    j = j_0
    p = p_0 + 2 * j * r * s
    while not MillerRabin(p, 10):
        j += 1
        p = p_0 + 2 * j * r * s
    
    return p

def generateKeys():
    
    p = getPrime(1024)
    q = getPrime(1024)
    
    # p = getStrongPrime()
    # q = getStrongPrime()
    
    while q == p:
        q = getPrime(1024)
        # q = getStrongPrime()
    
    
    n = p * q # Modulus for keys
    r = (p - 1) * (q - 1) # Euler's Totient
    
    def generate_e():
        """
        Generate the public key.
        """
        e = random.randint(2, r)
        while gcd(e, r) != 1:  
            e = random.randint(2, r)
        return e
    e = generate_e() # Public key
    
    # Solve the congruence: e * d = 1 (mod r), 1 < d < r
    # by considering the Linear Diophantine Equation: 
    # r * x + e * d = 1
    
    d = eea(r, e)[2] # Private key
    
    # Enforce the inequality:   
    if d <= 0:
        while not 1 < d:
            d += r
    else:
        while not d < r:
            d -= r   
    
    return e, d, n


import string

# TODO: add support for numbers

def encode(pt):
    """
    Encode plaintext pt into
    numerical digits.
    """
    dic = string.ascii_letters + string.punctuation + " "
    M = []
    for i in pt:
        M.append(dic.index(i))
    return M

# Encrypt and decrypt character by character 
# to satisfy RSA requirnment n > M 

def encrypt(M, public_key):
    return [pow(i, int(public_key[0]), int(public_key[1])) for i in M]

def decrypt(CT, private_key):
    CT = [char for char in CT]
    return [pow(i, private_key[0], private_key[1]) for i in CT]

def decode(DT):
    dic = string.ascii_letters + string.punctuation + " "
    msg = ''
    for i in DT:
        msg += dic[i]
    return msg

if __name__ == '__main__':
    '''
    Check if script is the main program.
    '''
    
    print("*****************************************************")
    print("WELCOME TO THE RSA PUBLIC-KEY ENCRYPTION SCHEME")
    print("*****************************************************")
    
    while True:
        
        choose = input("Type '1' to generate keys, '2' " 
                       "for encryption and '3' for decrytion: ")
        
        if choose == '1':
            keys = generateKeys()
            print("public key e = ",keys[0])
            print("private key d = ",keys[1])
            print("modulus n = ",keys[2])
            
        elif choose == '2':
            M = input("Enter your message: ")
            e = int(input("Type your public key e: "))
            n = int(input("Type your modulus n: "))
            public_key = [e, n]
            
            M = encode(M)
            C = encrypt(M, public_key)
            print(C)
            print("*****************************************************")
            # print("n = ",n)
            print("ENCRYPTED MESSAGE:", ''.join([str(i) for i in C]))
            print("*****************************************************")
            
        elif choose == '3':
            M = input("Enter your message: ")
            d = int(input("Type your private key d: "))
            n = int(input("Type your modulus n: "))
            private_key = [d, n]

            R = decrypt(C, private_key)
            print("*****************************************************")
            # print("n = ",n)
            # print("r = ",r)
            # print("d = ",d)
            print("DECRYPTED MESSAGE:", decode(R))
            print("*****************************************************")
            print("*****************************************************")   
