#               The Impossible User

### This encryption service will encrypt almost any plaintext. Can you abuse the implementation
    to actually encrypt every plaintext.

## Code
'''
from Crypto.Cipher import AES
from flask import Flask, request
from secret import flag, aes_key, secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['DEBUG'] = False
flag_user = 'impossible_flag_user'

class AESCipher():
    def __init__(self):
        self.key = aes_key
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        self.pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self, plaintext):
        return self.cipher.encrypt(self.pad(plaintext)).encode('hex')

    def decrypt(self, encrypted):
        return self.unpad(self.cipher.decrypt(encrypted.decode('hex')))

@app.route("/")
def main():
    return "%s" % open(__file__).read()

@app.route("/encrypt")
def encrypt():
    try:
        user = request.args.get('user').decode('hex')
        if user == flag_user:
            return 'No cheating!'
        return AESCipher().encrypt(user)
    except:
        return 'Something went wrong!'

@app.route("/get_flag")
def get_flag():
    try:
        if AESCipher().decrypt(request.args.get('user')) == flag_user:
            return flag
        else:
            return 'Invalid user!'
    except:
        return 'Something went wrong!'

if __name__ == "__main__":
  app.run()
'''

## What we need to do?
   We need to use 'encrypt()' function to encrypt hex value of the string 'impossible_flag_user' and use the encode output with function get_flag() to obtain the flag. Unfortunatly we can see that program will not let us encrypt hex value of 'impossible_flag_user' string directly - 'if user == flag_user': return 'No cheating!'. There has to be another way.

## ECB - Electronic Code Book
    The simplest of the encryption modes is the Electronic Codebook (ECB) mode (named after conventional physical codebooks[9]). The message is divided into blocks, and each block is encrypted separately.

    The disadvantage of this method is a lack of diffusion. Because ECB encrypts identical plaintext blocks into identical ciphertext blocks, it does not hide data patterns well. In some senses, it doesn’t provide serious message confidentiality, and it is not recommended for use in cryptographic protocols at all.

    ECB mode can also make protocols without integrity protection even more susceptible to replay attacks, since each block gets decrypted in exactly the same way

## How to ?

""Let's convert the string we need to encode to get the flag impossible_flag_user tp hex"".
    
    >>> "impossible_flag_user".encode("utf-8").hex()
    '696d706f737369626c655f666c61675f75736572'

By the way, you can go the other way in python with:

    >>> print(bytes.fromhex('696d706f737369626c655f666c61675f75736572'))
    b'impossible_flag_user'

So if I try to encrypt this hex.

    $ curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=696d706f737369626c655f666c61675f75736572
    No cheating!%

"I fail!"
So We need to find a way to encrypt this hex.

## Block length in ECB
AA == 1010 1010, 8b(bits) = 1B (Byte)

    $ curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=AA
    3217c32e368e89920cea99583ae86775%
    $ curl curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=$(python -c "print ('AA' * 1)")
    3217c32e368e89920cea99583ae86775%
    ...
    $ curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    5ccf4f293069356119727b54a94b6455%
    $ curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=$(python -c "print ('AA' * 15)")
    5ccf4f293069356119727b54a94b6455%
    $ curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    d4196601ecd309321037aaac6b9c76c52f28487624c5f1476e9fb265d2b47349%
    $ curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=$(python -c "print ('AA' * 16)")
    d4196601ecd309321037aaac6b9c76c52f28487624c5f1476e9fb265d2b47349%


We are looking when will the size of the cypher text increase, on that point we have
found our block size;
'AA' * 16 = 16 byte block length.

As the string we need 'impossible_flag_user' in hex (696d706f737369626c655f666c61675f75736572) is 20 bytes long, the encryption will paid it and we know that it will take two block, so 32 bytes.

We need to fill that two block with our own padding data, and the encrypted data in the third block will be the encrypted value of hex string 'impossible_flag_user'.

    $ curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=$(python -c "print ('AA' * 32)")696d706f737369626c655f666c61675f75736572
    d4196601ecd309321037aaac6b9c76c5d4196601ecd309321037aaac6b9c76c5939454b054b7379b0709a270b894025c707ece4f0913868ec5df07d131b0822d%
    $ curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=$(python -c "print ('BB' * 32)")696d706f737369626c655f666c61675f75736572
    8567ae611bbabfc1afdc017801641bea8567ae611bbabfc1afdc017801641bea939454b054b7379b0709a270b894025c707ece4f0913868ec5df07d131b0822d%
    $ curl https://345a7860397bb4fb.247ctf.com/encrypt\?user=$(python -c "print ('CC' * 32)")696d706f737369626c655f666c61675f75736572
    9715ba717c61975196d018dd1376075f9715ba717c61975196d018dd1376075f939454b054b7379b0709a270b894025c707ece4f0913868ec5df07d131b0822d%

The last 32 bytes are the encrypted value of string 'impossible_flag_user' that we need.

We can see that only the first 32 bytes are changing and the last 32 stay the same, so our theory is okay. We can now copy the last 32 bytes and fill them in the get_flag() function to obtain the flag:

    $ curl https://345a7860397bb4fb.247ctf.com/get_flag\?user=939454b054b7379b0709a270b894025c707ece4f0913868ec5df07d131b0822d

""Now you got flag!""