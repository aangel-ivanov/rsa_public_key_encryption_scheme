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
    """
    if n == 1: 
        return x 
    elif n % 2 == 0: 
        return (bin_exp(x, n/2, m) ** 2) % m
    else: 
        return ((bin_exp(x, (n - 1) / 2, m) ** 2) * x) % m

import random

def getPrime(n):
    """
    Generate n-bit prime.
    """
    random.seed(random.randint(0, 1000))

    def primeSieve(n):
        """
        Generate a list of primes
        less than or equal to n.
        """
        isPrime = [True for i in range(n + 1)]
        p = 2
        while n >= p * p:
            if isPrime[p] == True:
                for i in range(p * p, n + 1, p):
                    isPrime[i] = False
            p += 1

        primes = []
        for p in range(2, n + 1):
            if isPrime[p]:
                primes.append(p)
                
        return primes

    def getLowLevelPrime(n):
        '''
        Generate a number divisible
        by all elements in prime list.
        '''
        while True:
            num = random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)

            for prime in primeSieve(350):
                if num % prime == 0 and prime ** 2 <= num:
                    break
                else:
                    return num

    def isProbPrime(num, k):
        '''
        Miller-Rabin primality test on
        number num for k trials.
        '''

        # Find s such that num - 1 = 2^s * q, q odd
        d = num - 1
        s = 0
        while d % 2 == 0:
            d >>= 1 # d/= 2
            s += 1
        d = num - 1
        q = d // (2 ** s)

        def MRtrial(num):
            """
            Perform one trial of
            Miller-Rabin test.
            """

            # Pick test value
            a = random.randrange(1, num)

            # Fermat Test
            if pow(a, d, num) != 1:
                return False

            # Check if a^2 = 1 % n has solutions +/- 1
            if pow(a, q, num) == 1:
                return True
            else:
                for i in range(s):
                    if pow(a, (2 ** i) * q, num) == -1:
                        return True
                    else:
                        return False

        # Iterate for number of trials
        for i in range(k):
            if not MRtrial(num):
                return False
            else:
                return True

    # Get probable prime   
    if __name__ == '__main__':
    	while True:
         pc = getLowLevelPrime(n) # store the prime candidate
         if not isProbPrime(pc, 20):
             continue
         else:
             return pc
             break

p = getPrime(1024)
q = getPrime(1024)

while q == p:
    q = getPrime(1024)

n = p * q
r = (p - 1) * (q - 1)

def generate_e():
    e = random.randint(0, r)
    while gcd(e, r) != 1:  
        e = random.randint(0, r)
    return e
e = generate_e()

##### Solve the congruence: e * d = 1 (mod r), 1 < d < r
# by considering the Linear Diophantine Equation: 
# r * x + e * d = 1 ######

# Apply Extended Euclidean Algorithm:
d = eea(r, e)[2]

# Enforce the inequality:   
if d <= 0:
    while not 1 < d:
        d += r
else:
    while not d < r:
        d -= r


def encrypt(M, e, n):
    """
    Convert each letter in plaintext to numerical digits
    and encyrpt using public key.
    """
    return [bin_exp(ord(char), e, n) for char in M]


def decrypt(C, d, n):
    """
    Decrypt ciphertext using private key 
    and convert to plaintext.
    """
    split_C = [C[i:i+2] for i in range(0, len(C), 2)]
    # print(split_C)
    #for i in split_C:
        # print(i)
    return ''.join([chr(bin_exp(int(i), d, n)) for i in split_C])



if __name__ == '__main__':
    '''
    Check if script is the main program.
    '''
    
    print("*****************************************************")
    print("WELCOME TO THE RSA PUBLIC-KEY ENCRYPTION SCHEME")
    print("*****************************************************")
    
    while True:
        M = input("Enter your message: ")
        choose = input("Type '1' for encryption and '2' for decrytion: ")
        
        if choose == '1':
            print("*****************************************************")
            print("n =",n)
            print("ENCRYPTED MESSAGE:", 
                  ''.join(map(lambda x: str(x), encrypt(M, e, n))))
            print("*****************************************************")
            
        elif choose == '2':
            print("*****************************************************")
            print("n = ",n)
            print("r = ",r)
            print("d = ",d)
            print("DECRYPTED MESSAGE:", decrypt(M, d, n))
            print("*****************************************************")
            print("*****************************************************")    
    
    
# to do: 
        
# handle M > n (or find a way around it)
# introduce padding for encoding
