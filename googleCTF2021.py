"""
Let's decode into charcter- 

In source code We see Password like:

const checkPassword = () => {
  const v = document.getElementById("password").value;
  const p = Array.from(v).map(a => 0xCafe + a.charCodeAt(0));

     if(p[0] === 52037 &&
     p[6] === 52081 &&
     p[5] === 52063 &&
     p[1] === 52077 &&
     p[9] === 52077 &&
     p[10] === 52080 &&
     p[4] === 52046 &&
     p[3] === 52066 &&
     p[8] === 52085 &&
     p[7] === 52081 &&
     p[2] === 52077 &&
     p[11] === 52066)

If you decode you won't get right password because you have you change this into right way.
 p[0] === 52037
 p[1] === 52077
 p[2] === 52077
 p[3] === 52066
 p[4] === 52046
 p[5] === 52063
 p[6] === 52081
 p[7] === 52081
 p[8] === 52085
 p[9] === 52077
 p[10] === 52080
 p[11] === 52066

Here is 'OxCafe(=51966)' is added to the character code of each character of the password, and its checked
 whether it becomes a certain value.
 
 You can pull it reverse and convert it to character.
"""

arr = [52037,
52077,
52077,
52066,
52046,
52063,
52081,
52081,
52085,
52077,
52080,
52066]

for v in arr:
    print(chr(v - 0xCafe), end="")
    #Her you go! 