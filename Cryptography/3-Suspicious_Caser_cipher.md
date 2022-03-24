#                       Suspicious Caesar Cipher(Crypto)

### Instruction

**We RSA encrypted the flag, but forgot to save the private key. Is it possible to recover
the flag without it?**

## The Code

**The challenges provided a source code for the encryption ```suspicious_caesar_chipher.py```**

```Python
from Crypto.Util.number import getStrongPrime
from fractions import gcd
from secret import flag

def get_key(e=65537, bit_length=2048):
    while True:
        p = getStrongPrime(bit_length, e=e)
        q = getStrongPrime(bit_length, e=e)
        if gcd(e, (p - 1) * (q - 1)) == 1:
            return e, p * q

def encrypt(e, n, m):
    return [((ord(c) ** e) % n) for c in m]

e, n = get_key()

print("Generated key:")
print(e)
print(n)

print("Encrypted flag:")
print(encrypt(e, n, flag))

```
**Included is also the output of the script suspicious_caesar_cipher.out. Unfortunately running the script quickly reveals, that the secret library is missing, so we can’t just execute the script and win.**


# Exploit
**To the exploit the problem, we will modify the existing code.** 
**We know ```e,n``` encription algorythm and encrypted flag data from the output file. So we can reuse the available data and encryption algorythm to encrypt all the possible singlecharacters and then check the encrypted data against them.**

```Python
# Read the provided output file and define a list of possible characters
filename = "suspicious_caesar_cipher.out"
possible_chars = "0123456789abcdef{}CTF"

# encrypt function taken from provided script
def encrypt(e, n, m):
    return [((ord(c) ** e) % n) for c in m]

# Read all the data from the provided output file (e, n, encrypted flag)
with open(filename) as f:
    content = f.readlines()

e = int(content[1])
n = int(content[2])

encrypted_data = content[4].replace("L","").replace("[","").replace("]","").replace("\n","")
encrypted_data = encrypted_data.split(', ')
enc_data = list(map(int, encrypted_data))

# Create a dictionary (translation table) by encrypting all possible characters
code_table = {}
for c in possible_chars:
    crypted = int(encrypt(e, n, c)[0])
    code_table[crypted] = c

# Check each entry in encrypted flag for corresponding char in code_table
for i in encrypted_data:
    print(code_table.get(int(i)), end = '')
```

**Run Code! to get flag:)**
