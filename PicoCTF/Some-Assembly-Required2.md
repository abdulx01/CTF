#                       Some Assembly Required 2 : (Web CTF)

## What is Wat and Wasm?
**WebAssembly has the code in a binary format called WASM. You can also get the text format in WebAssembly and it is called WAT (WebAssembly Text format). As a developer you are not supposed to write code in WebAssembly, instead, you have to compile high-level languages like C, C++ and Rust to WebAssembly.**

## Analysis Code 
**Something I found a './aD8SvhyVkb' in JavaScript file, but it's give me a file that contains Assembly code then I decomile: with ```wasm-decompile``` it give assembly code**

**No luck!**
__Just look at below source code of assembly file here youcan see:__ 

```wat
(data (i32.const 1024) "xakgK\5cNs><m:i1>1991:nkjl<ii1j0n=mm09;<i:u\00\00")

```

**I found decode assembly data decode with python on internet**

```Python
>>> s=[chr(ord(j)^8) for j in "xakgK\5cNs><m:i1>1991:nkjl<ii1j0n=mm09;<i:u\00\00"]
>>> print(s)
```