                                More Cookie - PicoCTF


Description:
    I forgot cookie can be modified client-side, so now I decide to encrypt them!

Solution:
---------
    Looking at the website. This is continuation of the "Cookie" challenge. So let's have
    look.This time the read page: "Welcome to my cookie search page. Only the admin can use it"! add the cookie is :
    
    auth_name = VzJraUUyU1c3QTZuOG10dSsxMTJqQXpCVTEwS2IxcjNoWStLRlhOM3QzY3ZDbWZ5N05YRVB4UnB2ZEFZYnptRjhVakRTRE5FTHo1RVpsVitxcVkrRHBOOWFSMng2S1djekhlNE8zK3liUjdvb1Ywd1U1ZTBXblVqZGw0RmtwMFE=

    It's a base64 when I decode it, it's still in gibberish. So it's encrypted. Let's see the hint.

    - Hint 1: https://en.wikipedia.org/wiki/Homomorphic_encryption

It's a Wikipedia page for a very interesting encryption method, It's more like an algorithm than an encryption formula. I found this to be the hardest challenge in the web, Reading articles about Homomorphic encryption and looking at other writeups I understand that we do not have to decrypt it to solve it, Homomorphic encryption allows you to perform operations on encrypted text. Also, I noticed that the letters "CBC" are oddly capitalized in the challenge description. So, It's a CBC bitflip. Meaning the encrypted text contains a bit that determines if it's admin or not, so probably something like admin=0 but I don't know it's position so I brute forced it, Here's the code

    from base64 import b64decode
    from base64 import b64encode
    import requests

    def bitFlip( pos, bit, data):
        raw = b64decode(data)

        list1 = list(raw)
        list1[pos] = chr(ord(list1[pos])^bit)
        raw = ''.join(list1)
        return b64encode(raw)

    ck = "UXVDRDhEMmNrbTFCV25jbzdheFBjbHNmOWErZnNJdnY5Nk5pUkVNTkVXYUdRK0FVSk9tTGtRT3h1a0dWSDJrbmNHSUxsRTlNR2FZZFJaZ3RRb09EdngyUnd6L3FlbCtPSmZjbnJUVE5pWnVVUHNDQ1lJdFkzbTI4N29NWWxBRU4="

    for i in range(128):
    for j in range(128):
        c = bitFlip(i, j, ck)
        cookies = {'auth_name': c}
        r = requests.get('http://mercury.picoctf.net:25992/', cookies=cookies)
        if "picoCTF{" in r.text:
        print(r.text)
        break