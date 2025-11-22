# Level01 Write-up

## Introduction

Let's start by launching the program.

## Program Execution

```
********* ADMIN LOGIN PROMPT *********
Enter Username: asdf
verifying username....

nope, incorrect username...
```

The program asks for a username and prints an error message if it's incorrect.

## Reverse Engineering

Let's examine the program's internals:

```assembly
.text:080484D0 ; int __cdecl main(int argc, const char **argv, const char **envp)
.text:080484D0                 public main
.text:080484D0 main            proc near               ; DATA XREF: _start+17↑o
.text:080484D0
.text:080484D0 argc            = dword ptr  8
.text:080484D0 argv            = dword ptr  0Ch
.text:080484D0 envp            = dword ptr  10h
.text:080484D0
.text:080484D0 ; __unwind {
.text:080484D0                 push    ebp
.text:080484D1                 mov     ebp, esp
.text:080484D3                 push    edi
.text:080484D4                 push    ebx
.text:080484D5                 and     esp, 0FFFFFFF0h
.text:080484D8                 sub     esp, 60h
.text:080484DB                 lea     ebx, [esp+1Ch]
.text:080484DF                 mov     eax, 0
.text:080484E4                 mov     edx, 10h
.text:080484E9                 mov     edi, ebx
.text:080484EB                 mov     ecx, edx
.text:080484ED                 rep stosd
.text:080484EF                 mov     dword ptr [esp+5Ch], 0
.text:080484F7                 mov     dword ptr [esp], offset aAdminLoginProm ; "********* ADMIN LOGIN PROMPT *********"
.text:080484FE                 call    _puts
.text:08048503                 mov     eax, offset aEnterUsername ; "Enter Username: "
.text:08048508                 mov     [esp], eax
.text:0804850B                 call    _printf
.text:08048510                 mov     eax, ds:stdin@@GLIBC_2_0
.text:08048515                 mov     [esp+8], eax
.text:08048519                 mov     dword ptr [esp+4], 100h
.text:08048521                 mov     [esp], offset a_user_name
.text:08048528                 call    _fgets
.text:0804852D                 call    verify_user_name
```

## Program Flow

The program:

1. Sets the buffer at `esp + 28` to 0:
```assembly
lea     ebx, [esp+28]
mov     eax, 0
mov     edx, 16
mov     edi, ebx
mov     ecx, edx
rep stosd
```

2. Puts 0 at address `esp+92`:
```assembly
mov     dword ptr [esp+92], 0
```

3. Prints the admin login prompt:
```assembly
mov     dword ptr [esp], offset aAdminLoginProm ; "********* ADMIN LOGIN PROMPT *********"
call    _puts
```

4. Prints "Enter Username:":
```assembly
mov     eax, offset aEnterUsername ; "Enter Username: "
mov     [esp], eax
call    _printf
```

5. Reads 256 bytes from stdin and stores them in the `.bss` buffer `a_user_name`:
```assembly
mov     eax, ds:stdin@@GLIBC_2_0
mov     [esp+8], eax
mov     dword ptr [esp+4], 256
mov     [esp], offset a_user_name
call    _fgets
```

The buffer size:
```assembly
.bss:0804A040                 public a_user_name
.bss:0804A040 a_user_name     db    ? ;               ; DATA XREF: verify_user_name+14↑o
.bss:0804A040                                         ; main+51↑o\
.bss:0804A0A2                 db    ? ;
.bss:0804A0A3                 db    ? ;
.bss:0804A0A3 _bss            ends
```

The buffer size is:
```
gef➤  p/d 0x0804A0A2-0x0804A040
$7 = 98
```

So the `a_user_name` buffer is only 98 bytes in size.

6. Calls `verify_user_name`:
```assembly
call    verify_user_name
```

The `verify_user_name` function:
```assembly
public verify_user_name
verify_user_name proc near
; __unwind {
push    ebp
mov     ebp, esp
push    edi
push    esi
sub     esp, 10h
mov     dword ptr [esp], offset aVerifyingUsern ; "verifying username....\n"
call    _puts
mov     edx, offset a_user_name
mov     eax, offset aDatWil ; "dat_wil"
mov     ecx, 7
mov     esi, edx
mov     edi, eax
repe cmpsb
setnbe  dl
setb    al
mov     ecx, edx
sub     cl, al
mov     eax, ecx
movsx   eax, al
add     esp, 10h
pop     esi
pop     edi
pop     ebp
retn
; } // starts at 8048464
verify_user_name endp
```

The important part is the comparison:
```assembly
mov     edx, offset a_user_name
mov     eax, offset aDatWil ; "dat_wil"
mov     ecx, 7
mov     esi, edx
mov     edi, eax
repe cmpsb
```

This compares 7 bytes from `aDatWil` (like `strncmp`).

So the username is `dat_wil`.

7. After verifying the result of the function call, if it's 0, it continues with `verify_user_pass`:
```assembly
mov     [esp+5Ch], eax
cmp     dword ptr [esp+5Ch], 0
jz      short loc_8048550
```

8. Gets 100 bytes into the buffer at position `esp + 28`:
```assembly
mov     dword ptr [esp], offset aEnterPassword ; "Enter Password: "
call    _puts
mov     eax, ds:stdin@@GLIBC_2_0
mov     [esp+8], eax
mov     dword ptr [esp+4], 64h ; 'd'
lea     eax, [esp+28]
mov     [esp], eax
call    _fgets
lea     eax, [esp+28]
mov     [esp], eax
call    verify_user_pass
```

The `verify_user_pass` function:
```assembly
; __unwind {
push    ebp
mov     ebp, esp
push    edi
push    esi
mov     eax, [ebp+arg_0]
mov     edx, eax
mov     eax, offset aAdmin ; "admin"
mov     ecx, 5
mov     esi, edx
mov     edi, eax
repe cmpsb
setnbe  dl
setb    al
mov     ecx, edx
sub     cl, al
mov     eax, ecx
movsx   eax, al
pop     esi
pop     edi
pop     ebp
retn
; } // st
```

This compares the first 5 bytes with "admin".

So the password is `admin`.

## Vulnerability

The exploit works because in the second `fgets` call, it reads 100 bytes and puts the elements inside the stack buffer, but the stack buffer is actually of size `96 - 28 = 68` bytes. However, because you have a variable at position `mov [esp+92], eax`:

```assembly
mov     eax, ds:stdin@@GLIBC_2_0
mov     [esp+8], eax
mov     dword ptr [esp+4], 100
lea     eax, [esp+28]
mov     [esp], eax
call    _fgets
```

The problem here is copying more elements than the size of the buffer.

## Exploitation

To create a cyclic pattern for the second argument to find the offset:

Found an offset of 80:
```
gef➤  pattern search $eip
[+] Searching for '75616161'/'61616175' with period=4
[+] Found at offset 80 (little-endian search) likely
```

Destination:
```
info variable 
0x0804a040  a_user_name
```

So:
- Input 1 = `dat_wil` + shellcode
- Input 2 = `A * 80` + address

## Flag

```
PwBLgNa8p8MTKW57S7zxVAQCxnCpV8JqTTs9XEBv
```
