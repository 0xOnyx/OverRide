# Level00 Write-up

## Introduction

Let's start by logging in and examining the first program.

## Program Execution

```bash
level00@OverRide:~$ ./level00
***********************************
* 	     -Level00 -		  *
***********************************
Password:1

Invalid Password!
```

The program asks for a password and prints "Invalid Password!" if it's incorrect.

## Reverse Engineering

Let's decompile the program to see what's inside:

```assembly
.text:08048494                 push    ebp
.text:08048495                 mov     ebp, esp
.text:08048497                 and     esp, 0FFFFFFF0h
.text:0804849A                 sub     esp, 32
.text:0804849D                 mov     dword ptr [esp], offset asc_80485F0 ; "***********************************"
.text:080484A4                 call    _puts
.text:080484A9                 mov     dword ptr [esp], offset aLevel00 ; "* \t     -Level00 -\t\t  *"
.text:080484B0                 call    _puts
.text:080484B5                 mov     dword ptr [esp], offset asc_80485F0 ; "***********************************"
.text:080484BC                 call    _puts
.text:080484C1                 mov     eax, offset aPassword ; "Password:"
.text:080484C6                 mov     [esp], eax
.text:080484C9                 call    _printf
.text:080484CE                 mov     eax, offset aD  ; "%d"
.text:080484D3                 lea     edx, [esp+28]
.text:080484D7                 mov     [esp+4], edx
.text:080484DB                 mov     [esp], eax
.text:080484DE                 call    ___isoc99_scanf
.text:080484E3                 mov     eax, [esp+28]
.text:080484E7                 cmp     eax, 5276
.text:080484EC                 jnz     short loc_804850D
.text:080484EE                 mov     dword ptr [esp], offset aAuthenticated ; "\nAuthenticated!"
.text:080484F5                 call    _puts
.text:080484FA                 mov     dword ptr [esp], offset aBinSh ; "/bin/sh"
.text:08048501                 call    _system
.text:08048506                 mov     eax, 0
.text:0804850B                 jmp     short locret_804851E
```

## Analysis

The program reads a number from stdin using `scanf` and stores the value on the stack:

```assembly
.text:080484CE                 mov     eax, offset aD  ; "%d"
.text:080484D3                 lea     edx, [esp+28]
.text:080484D7                 mov     [esp+4], edx
.text:080484DB                 mov     [esp], eax
.text:080484DE                 call    ___isoc99_scanf
```

After that, it compares this value with `5276`. If they match, it launches a shell with `/bin/sh`.

## Solution

The password is `5276`. Entering this value will authenticate and spawn a shell.

## Flag

```
uSq2ehEGT6c9S24zbshexZQBXUGrncxn5sD5QfGL
```
