# Level02 Write-up

## Introduction

Let's examine the program.

## Security Analysis

```
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   /home/users/level02/level02
```

## Program Execution

```bash
level02@OverRide:~$ ./level02 
===== [ Secure Access System v1.0 ] =====
/***************************************\
|| You must login to access this system. |
\**************************************/
--[ Username: a
--[ Password: a
*****************************************
a does not have access!
```

The program takes two inputs and prints something.

## Reverse Engineering

Let's examine what's inside:

```assembly
.text:0000000000400814 ; int __fastcall main(int argc, const char **argv, const char **envp)
.text:0000000000400814                 public main
.text:0000000000400814 main            proc near               ; DATA XREF: _start+1D↑o
```

The program opens a file in read-only mode:

```assembly
.text:0000000000400898                 mov     edx, offset modes ; "r"
.text:000000000040089D                 mov     eax, offset filename ; "/home/users/level03/.pass"
.text:00000000004008A2                 mov     rsi, rdx        ; modes
.text:00000000004008A5                 mov     rdi, rax        ; filename
.text:00000000004008A8                 call    _fopen
```

And stores the value in `rbp+stream`:

```assembly
.text:00000000004008AD                 mov     [rbp+stream], rax
.text:00000000004008B1                 cmp     [rbp+stream], 0
.text:00000000004008B6                 jnz     short loc_4008E6
```

If it fails, it prints an error:

```assembly
.text:00000000004008B8                 mov     rax, cs:stderr@@GLIBC_2_2_5
.text:00000000004008BF                 mov     rdx, rax
.text:00000000004008C2                 mov     eax, offset aErrorFailedToO ; "ERROR: failed to open password file\n"
.text:00000000004008C7                 mov     rcx, rdx        ; s
.text:00000000004008CA                 mov     edx, 24h ; '$'  ; n
.text:00000000004008CF                 mov     esi, 1          ; size
.text:00000000004008D4                 mov     rdi, rax        ; ptr
.text:00000000004008D7                 call    _fwrite
```

After that, it reads from the stream and puts it into the flag buffer:

```assembly
.text:00000000004008E6 loc_4008E6:                             ; CODE XREF: main+A2↑j
.text:00000000004008E6                 lea     rax, [rbp+flag]
.text:00000000004008ED                 mov     rdx, [rbp+stream]
.text:00000000004008F1                 mov     rcx, rdx        ; stream
.text:00000000004008F4                 mov     edx, 41         ; n
.text:00000000004008F9                 mov     esi, 1          ; size
.text:00000000004008FE                 mov     rdi, rax        ; ptr
.text:0000000000400901                 call    _fread
```

Gets the length of the string:

```assembly
.text:0000000000400906                 mov     [rbp+var_C], eax
.text:0000000000400909                 lea     rax, [rbp+flag]
.text:0000000000400910                 mov     esi, offset reject ; "\n"
.text:0000000000400915                 mov     rdi, rax        ; s
.text:0000000000400918                 call    _strcspn
```

Puts a 0 at the end of the flag:

```assembly
.text:000000000040091D                 mov     [rbp+rax+flag], 0
```

If the length of the string is 41:

```assembly
.text:0000000000400925                 cmp     [rbp+var_C], 41
.text:0000000000400929                 jz      short loc_40097D
```

Otherwise, it writes an error message:

```assembly
.text:000000000040092B                 mov     rax, cs:stderr@@GLIBC_2_2_5
.text:0000000000400932                 mov     rdx, rax
.text:0000000000400935                 mov     eax, offset aErrorFailedToR ; "ERROR: failed to read password file\n"
.text:000000000040093A                 mov     rcx, rdx        ; s
.text:000000000040093D                 mov     edx, 24h ; '$'  ; n
.text:0000000000400942                 mov     esi, 1          ; size
.text:0000000000400947                 mov     rdi, rax        ; ptr
.text:000000000040094A                 call    _fwrite
```

Prints some elements before the input:

```assembly
.text:000000000040097D loc_40097D:                             ; CODE XREF: main+115↑j
.text:000000000040097D                 mov     rax, [rbp+stream]
.text:0000000000400981                 mov     rdi, rax        ; stream
.text:0000000000400984                 call    _fclose
.text:0000000000400989                 mov     edi, offset s   ; "===== [ Secure Access System v1.0 ] ==="...
.text:000000000040098E                 call    _puts
.text:0000000000400993                 mov     edi, offset asc_400C50 ; "/**************************************"...
.text:0000000000400998                 call    _puts
.text:000000000040099D                 mov     edi, offset aYouMustLoginTo ; "| You must login to access this system."...
.text:00000000004009A2                 call    _puts
.text:00000000004009A7                 mov     edi, offset asc_400CB0 ; "\\*************************************"...
.text:00000000004009AC                 call    _puts
.text:00000000004009B1                 mov     eax, offset format ; "--[ Username: "
.text:00000000004009B6                 mov     rdi, rax        ; format
.text:00000000004009B9                 mov     eax, 0
.text:00000000004009BE                 call    _printf
```

Gets 100 bytes from stdin:

```assembly
.text:00000000004009C3                 mov     rax, cs:stdin@@GLIBC_2_2_5
.text:00000000004009CA                 mov     rdx, rax        ; stream
.text:00000000004009CD                 lea     rax, [rbp+input1]
.text:00000000004009D1                 mov     esi, 100 ;      ; n
.text:00000000004009D6                 mov     rdi, rax        ; s
.text:00000000004009D9                 call    _fgets
```

Gets the length of the input:

```assembly
.text:00000000004009DE                 lea     rax, [rbp+input1]
.text:00000000004009E2                 mov     esi, offset reject ; "\n"
.text:00000000004009E7                 mov     rdi, rax        ; s
.text:00000000004009EA                 call    _strcspn
```

And puts `\0` at the end:

```assembly
.text:00000000004009EF                 mov     [rbp+rax+input1], 0
```

Prints password prompt:

```assembly
.text:00000000004009F4                 mov     eax, offset aPassword ; "--[ Password: "
.text:00000000004009F9                 mov     rdi, rax        ; format
.text:00000000004009FC                 mov     eax, 0
.text:0000000000400A01                 call    _printf
```

Gets 100 bytes and puts the result in `rbp+input2`:

```assembly
.text:0000000000400A06                 mov     rax, cs:stdin@@GLIBC_2_2_5
.text:0000000000400A0D                 mov     rdx, rax        ; stream
.text:0000000000400A10                 lea     rax, [rbp+input2]
.text:0000000000400A17                 mov     esi, 64h ; 'd'  ; n
.text:0000000000400A1C                 mov     rdi, rax        ; s
.text:0000000000400A1F                 call    _fgets
```

Gets the length and puts 0 at the end of the string:

```assembly
.text:0000000000400A24                 lea     rax, [rbp+input2]
.text:0000000000400A2B                 mov     esi, offset reject ; "\n"
.text:0000000000400A30                 mov     rdi, rax        ; s
.text:0000000000400A33                 call    _strcspn
.text:0000000000400A38                 mov     [rbp+rax+input2], 0
```

Prints some elements:

```assembly
.text:0000000000400A40                 mov     edi, offset asc_400CF8 ; "***************************************"...
.text:0000000000400A45                 call    _puts
```

Compares the second input2 with the flag, only the first 41 bytes:

```assembly
.text:0000000000400A4A                 lea     rcx, [rbp+input2]
.text:0000000000400A51                 lea     rax, [rbp+flag]
.text:0000000000400A58                 mov     edx, 41         ; n
.text:0000000000400A5D                 mov     rsi, rcx        ; s2
.text:0000000000400A60                 mov     rdi, rax        ; s1
.text:0000000000400A63                 call    _strncmp
.text:0000000000400A68                 test    eax, eax
.text:0000000000400A6A                 jnz     short loc_400A96
```

If correct, it prints input1 and calls `/bin/sh`:

```assembly
.text:0000000000400A6C                 mov     eax, offset aGreetingsS ; "Greetings, %s!\n"
.text:0000000000400A71                 lea     rdx, [rbp+input1]
.text:0000000000400A75                 mov     rsi, rdx
.text:0000000000400A78                 mov     rdi, rax        ; format
.text:0000000000400A7B                 mov     eax, 0
.text:0000000000400A80                 call    _printf
.text:0000000000400A85                 mov     edi, offset command ; "/bin/sh"
.text:0000000000400A8A                 call    _system
.text:0000000000400A8F                 mov     eax, 0
.text:0000000000400A94                 leave
.text:0000000000400A95                 retn
```

If not correct:

```assembly
.text:0000000000400A96
.text:0000000000400A96 loc_400A96:                             ; CODE XREF: main+256↑j
.text:0000000000400A96                 lea     rax, [rbp+input1]
.text:0000000000400A9A                 mov     rdi, rax        ; format
.text:0000000000400A9D                 mov     eax, 0
.text:0000000000400AA2                 call    _printf
.text:0000000000400AA7                 mov     edi, offset aDoesNotHaveAcc ; " does not have access!"
.text:0000000000400AAC                 call    _puts
.text:0000000000400AB1                 mov     edi, 1          ; status
.text:0000000000400AB6                 call    _exit
```

## Vulnerability

The program copies more than 100 elements into a smaller buffer:

```c
char input2[96]; // [rsp+10h] [rbp-110h] BYREF
```

This writes more than 4 bytes beyond the buffer, but that's not the important part here because it only overrides a value that is not important.

The important part is that if the password is incorrect, it gets `rbp+input1` and puts it directly into `printf`:

```assembly
.text:0000000000400A96
.text:0000000000400A96 loc_400A96:                             ; CODE XREF: main+256↑j
.text:0000000000400A96                 lea     rax, [rbp+input1]
.text:0000000000400A9A                 mov     rdi, rax        ; format
.text:0000000000400A9D                 mov     eax, 0
.text:0000000000400AA2                 call    _printf
```

So `input1` is directly put into `printf`, and it's possible to print the stack!

## Exploitation

If I use `%1$p`, it prints the first argument of the stack in hex.

So I just need to know which argument I want.

So `[rbp+flag]`:

```
flag = byte ptr -0A0h or -160
```

Because the stack is 288 bytes of space:

```assembly
.text:0000000000400818                 sub     rsp, 288
```

The argument is at `288 - 160 = 128`.

But because each argument is 8 bytes of space:
```
128 / 8 = 16
```

But the ABI says that you need to use before the register is `16 + 6` registers, so it's `= 22` elements.

So to bypass in local gdb, I use this to modify the address of the string:
```
set {char[20]} $rdi = "/tmp/.pass"
```

The flag is 41 bytes long, so one byte for `\0`, so 40 bytes.

For printing, I use `%p` which prints 8 bytes from the stack, so I need `40 / 8 = 5` prints from the stack.

So each element looks like that:
```
%22 + X $p * 5
```

## Flag

```
Hh74RPnuQ9sa5JAEXgNWCqz7sXGnh5J5M9KfPg3H
```
