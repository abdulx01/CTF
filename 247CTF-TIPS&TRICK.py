from os import remove
from pwn import *
import re

io = remote('43e328df9f92c3fa.247ctf.com',50054)

print(io.recvline())
print(io.recvline())

for i in range(500):
    math = io.recvline().decode('utf-8')
    nums = re.findall(r'\d+',math)

    nums1 = int(nums[0])
    nums2 = int(nums[1])

    result = str(nums1 + nums2)
    final = (result+'\r\n').encode('utf-8')
    io.sendline(final)
    io.recvline()
    print('the operation',i,'hash been done with a',result)

print(io.recvline())
 