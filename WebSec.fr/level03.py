import hashlib

sha1 = lambda x:hashlib.sha1(str(x)).hexdigest()

i = 0

while True:
    if sha1(i).startswith("7c00"):
        print(i)
        break
    i += 1


