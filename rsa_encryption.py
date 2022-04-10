'''
RSA PUBLIC-KEY ENCRYPTION SCHEME
 
BY: ALEXANDER A. IVANOV
'''

# Checks if prime
def isPrime(x):
    for n in range(2, int(x ** 0.5) + 1):
        if x % n == 0:
            return False
        return True

# Euclidean Algorithm
def gcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a

# Extended Euclidean Algorithm
def eea(a, b): # solve for x and y: ax + by = gcd(a, b)
    # Base Case 
    if a == 0 :  
        return b, 0, 1
             
    gcd, x1, y1 = eea(b % a, a) 
     
    # Update x and y using results of recursive 
    # call 
    x = y1 - (b//a) * x1 
    y = x1 
    
    return gcd, x, y

# Solve linear congruence
def lin_congru(a, b, m):
    if b == 0:
        return 0

    if a < 0:
        a = -a
        b = -b

    b %= m
    while a > m:
        a -= m

    return (m * lin_congru(m, -b, a) + b) // a


# Coding table

import pandas as pd

def split(message):
    return [char for char in message]
   
encryptionkey = pd.read_csv(r"C:\Users\alexa\OneDrive\Desktop\encryptionkey.csv",
                            sep=',', names=['Character', 'Byte'], header=None, skiprows=[0]) 
df = pd.DataFrame(data=encryptionkey)
df['Character'] = df['Character'].astype(str)
df['Byte'] = df['Byte'].astype(str)


# Coding message

def generate_coded_message(message_split):
    coded_message = ""
    
    for i in range(len(message_split)):
        j = message_split[i]
        try:
            coded_char = encryptionkey.loc[encryptionkey['Character'] == j, 'Byte'].iloc[0]
            # To handle if character is not in our decryption list
        except:
            print('unrecognized character')
            coded_char = '@@@'
            
        coded_message = coded_message + str(coded_char)
    return coded_message

# Decoding message

def decode(message):
        new_word = ''
        decoded_message = []
        for i in range(0, len(message), 2):
            j = message[i:i + 2]
            index_nb = df[df.eq(j).any(1)]
            df2 = index_nb['Character'].tolist()
            s = [str(x) for x in df2]
            decoded_message = decoded_message + s
        new_word = ''.join(decoded_message)
        return new_word


print("WELCOME TO THE RSA PUBLIC-KEY ENCRYPTION SCHEME")
print("*****************************************************")


import random 
#random.seed(random.randint(0, 1000))
random.seed(1)

# initialise primes
# minPrime = 0
# maxPrime = 1000
# primes = [i for i in range(minPrime, maxPrime) if isPrime(i)]
# p = random.choice(primes)
# q = random.choice(primes)

# test values
p = 5
q = 11
e = 3

n = p * q
r = (p - 1) * (q - 1)

# def generate_e():
#     e = random.randint(0, r)
#     while gcd(e, r) != 1:
#         e = random.randint(0, r)
#     return e
# e = generate_e()


# Solve the congruence: e * d = 1 (mod r), 1 < d < r
# by considering the Linear Diophantine Equation: r * x + e * d = 1

# Apply Extended Euclidean Algorithm:
d = eea(r, e)[2]

# satisfy the inequality:   
if d <= 0:
    while not 1 < d:
        d = d + r
else:
    while not d < r:
        d = d - r

def encrypt(M, e, n):
    return lin_congru(1, M ** e, n)

def decrypt(C, d, n):
    return lin_congru(1, C ** d, n)


while True:
    M = input("Enter your message: ")
    print("*****************************************************")
    M_coded = generate_coded_message(split(M))
    coded_message_str = str(M_coded)
    choose = input("Type '1' for encryption and '2' for decrytion: ")
    
    if choose == '1':
        print("*****************************************************")
        print('CODED MESSAGE:', str(M_coded))
        print("ENCRYPTED MESSAGE:", encrypt(int(M_coded), e, n))
        print("*****************************************************")
    elif choose == '2':
        print("*****************************************************")
        print("DECRYPTED MESSAGE:", decrypt(int(M), d, n))
        print('DEDCODED MESSAGE:', decode(str(decrypt(int(M), d, n))))
        print("*****************************************************")
    else:
        choose = input("Type '1' for encryption and '2' for decrytion: ")
      
      
