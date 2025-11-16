level02@localhost's password: 

RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   /home/users/level02/level02
level02@OverRide:~$ ./level02 
===== [ Secure Access System v1.0 ] =====
/***************************************\
| You must login to access this system. |
\**************************************/
--[ Username: a
--[ Password: a
*****************************************
a does not have access!



so the programme take two input and print some thing

let's show wat's is inside


.text:0000000000400814 ; int __fastcall main(int argc, const char **argv, const char **envp)
.text:0000000000400814                 public main
.text:0000000000400814 main            proc near               ; DATA XREF: _start+1D↑o
.text:0000000000400814
.text:0000000000400814 var_120         = qword ptr -120h
.text:0000000000400814 var_114         = dword ptr -114h
.text:0000000000400814 input2          = byte ptr -110h
.text:0000000000400814 anonymous_0     = dword ptr -0B0h
.text:0000000000400814 flag            = byte ptr -0A0h
.text:0000000000400814 input1          = byte ptr -70h
.text:0000000000400814 anonymous_1     = dword ptr -10h
.text:0000000000400814 var_C           = dword ptr -0Ch
.text:0000000000400814 stream          = qword ptr -8
.text:0000000000400814
.text:0000000000400814 ; __unwind {
.text:0000000000400814                 push    rbp
.text:0000000000400815                 mov     rbp, rsp
.text:0000000000400818                 sub     rsp, 288
.text:000000000040081F                 mov     [rbp+var_114], edi
.text:0000000000400825                 mov     [rbp+var_120], rsi
.text:000000000040082C                 lea     rdx, [rbp+input1]
.text:0000000000400830                 mov     eax, 0
.text:0000000000400835                 mov     ecx, 0Ch
.text:000000000040083A                 mov     rdi, rdx
.text:000000000040083D                 rep stosq
.text:0000000000400840                 mov     rdx, rdi
.text:0000000000400843                 mov     [rdx], eax
.text:0000000000400845                 add     rdx, 4
.text:0000000000400849                 lea     rdx, [rbp+flag]
.text:0000000000400850                 mov     eax, 0
.text:0000000000400855                 mov     ecx, 5
.text:000000000040085A                 mov     rdi, rdx
.text:000000000040085D                 rep stosq
.text:0000000000400860                 mov     rdx, rdi
.text:0000000000400863                 mov     [rdx], al
.text:0000000000400865                 add     rdx, 1
.text:0000000000400869                 lea     rdx, [rbp+input2]
.text:0000000000400870                 mov     eax, 0
.text:0000000000400875                 mov     ecx, 0Ch
.text:000000000040087A                 mov     rdi, rdx
.text:000000000040087D                 rep stosq
.text:0000000000400880                 mov     rdx, rdi
.text:0000000000400883                 mov     [rdx], eax
.text:0000000000400885                 add     rdx, 4
.text:0000000000400889                 mov     [rbp+stream], 0
.text:0000000000400891                 mov     [rbp+var_C], 0
.text:0000000000400898                 mov     edx, offset modes ; "r"
.text:000000000040089D                 mov     eax, offset filename ; "/home/users/level03/.pass"
.text:00000000004008A2                 mov     rsi, rdx        ; modes
.text:00000000004008A5                 mov     rdi, rax        ; filename
.text:00000000004008A8                 call    _fopen
.text:00000000004008AD                 mov     [rbp+stream], rax
.text:00000000004008B1                 cmp     [rbp+stream], 0
.text:00000000004008B6                 jnz     short loc_4008E6
.text:00000000004008B8                 mov     rax, cs:stderr@@GLIBC_2_2_5
.text:00000000004008BF                 mov     rdx, rax
.text:00000000004008C2                 mov     eax, offset aErrorFailedToO ; "ERROR: failed to open password file\n"
.text:00000000004008C7                 mov     rcx, rdx        ; s
.text:00000000004008CA                 mov     edx, 24h ; '$'  ; n
.text:00000000004008CF                 mov     esi, 1          ; size
.text:00000000004008D4                 mov     rdi, rax        ; ptr
.text:00000000004008D7                 call    _fwrite
.text:00000000004008DC                 mov     edi, 1          ; status
.text:00000000004008E1                 call    _exit
.text:00000000004008E6 ; ---------------------------------------------------------------------------
.text:00000000004008E6
.text:00000000004008E6 loc_4008E6:                             ; CODE XREF: main+A2↑j
.text:00000000004008E6                 lea     rax, [rbp+flag]
.text:00000000004008ED                 mov     rdx, [rbp+stream]
.text:00000000004008F1                 mov     rcx, rdx        ; stream
.text:00000000004008F4                 mov     edx, 41         ; n
.text:00000000004008F9                 mov     esi, 1          ; size
.text:00000000004008FE                 mov     rdi, rax        ; ptr
.text:0000000000400901                 call    _fread
.text:0000000000400906                 mov     [rbp+var_C], eax
.text:0000000000400909                 lea     rax, [rbp+flag]
.text:0000000000400910                 mov     esi, offset reject ; "\n"
.text:0000000000400915                 mov     rdi, rax        ; s
.text:0000000000400918                 call    _strcspn
.text:000000000040091D                 mov     [rbp+rax+flag], 0
.text:0000000000400925                 cmp     [rbp+var_C], 41
.text:0000000000400929                 jz      short loc_40097D
.text:000000000040092B                 mov     rax, cs:stderr@@GLIBC_2_2_5
.text:0000000000400932                 mov     rdx, rax
.text:0000000000400935                 mov     eax, offset aErrorFailedToR ; "ERROR: failed to read password file\n"
.text:000000000040093A                 mov     rcx, rdx        ; s
.text:000000000040093D                 mov     edx, 24h ; '$'  ; n
.text:0000000000400942                 mov     esi, 1          ; size
.text:0000000000400947                 mov     rdi, rax        ; ptr
.text:000000000040094A                 call    _fwrite
.text:000000000040094F                 mov     rax, cs:stderr@@GLIBC_2_2_5
.text:0000000000400956                 mov     rdx, rax
.text:0000000000400959                 mov     eax, offset aErrorFailedToR ; "ERROR: failed to read password file\n"
.text:000000000040095E                 mov     rcx, rdx        ; s
.text:0000000000400961                 mov     edx, 24h ; '$'  ; n
.text:0000000000400966                 mov     esi, 1          ; size
.text:000000000040096B                 mov     rdi, rax        ; ptr
.text:000000000040096E                 call    _fwrite
.text:0000000000400973                 mov     edi, 1          ; status
.text:0000000000400978                 call    _exit
.text:000000000040097D ; ---------------------------------------------------------------------------
.text:000000000040097D
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
.text:00000000004009C3                 mov     rax, cs:stdin@@GLIBC_2_2_5
.text:00000000004009CA                 mov     rdx, rax        ; stream
.text:00000000004009CD                 lea     rax, [rbp+input1]
.text:00000000004009D1                 mov     esi, 64h ; 'd'  ; n
.text:00000000004009D6                 mov     rdi, rax        ; s
.text:00000000004009D9                 call    _fgets
.text:00000000004009DE                 lea     rax, [rbp+input1]
.text:00000000004009E2                 mov     esi, offset reject ; "\n"
.text:00000000004009E7                 mov     rdi, rax        ; s
.text:00000000004009EA                 call    _strcspn
.text:00000000004009EF                 mov     [rbp+rax+input1], 0
.text:00000000004009F4                 mov     eax, offset aPassword ; "--[ Password: "
.text:00000000004009F9                 mov     rdi, rax        ; format
.text:00000000004009FC                 mov     eax, 0
.text:0000000000400A01                 call    _printf
.text:0000000000400A06                 mov     rax, cs:stdin@@GLIBC_2_2_5
.text:0000000000400A0D                 mov     rdx, rax        ; stream
.text:0000000000400A10                 lea     rax, [rbp+input2]
.text:0000000000400A17                 mov     esi, 64h ; 'd'  ; n
.text:0000000000400A1C                 mov     rdi, rax        ; s
.text:0000000000400A1F                 call    _fgets
.text:0000000000400A24                 lea     rax, [rbp+input2]
.text:0000000000400A2B                 mov     esi, offset reject ; "\n"
.text:0000000000400A30                 mov     rdi, rax        ; s
.text:0000000000400A33                 call    _strcspn
.text:0000000000400A38                 mov     [rbp+rax+input2], 0
.text:0000000000400A40                 mov     edi, offset asc_400CF8 ; "***************************************"...
.text:0000000000400A45                 call    _puts
.text:0000000000400A4A                 lea     rcx, [rbp+input2]
.text:0000000000400A51                 lea     rax, [rbp+flag]
.text:0000000000400A58                 mov     edx, 41         ; n
.text:0000000000400A5D                 mov     rsi, rcx        ; s2
.text:0000000000400A60                 mov     rdi, rax        ; s1
.text:0000000000400A63                 call    _strncmp
.text:0000000000400A68                 test    eax, eax
.text:0000000000400A6A                 jnz     short loc_400A96
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
.text:0000000000400A96 ; ---------------------------------------------------------------------------
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
.text:0000000000400AB6 ; } // starts at 400814
.text:0000000000400AB6 main            endp
.text:0000000000400AB6




so this code juste open the file in read only 

.text:0000000000400880                 mov     rdx, rdi
.text:0000000000400883                 mov     [rdx], eax
.text:0000000000400885                 add     rdx, 4
.text:0000000000400889                 mov     [rbp+stream], 0
.text:0000000000400891                 mov     [rbp+var_C], 0
.text:0000000000400898                 mov     edx, offset modes ; "r"
.text:000000000040089D                 mov     eax, offset filename ; "/home/users/level03/.pass"
.text:00000000004008A2                 mov     rsi, rdx        ; modes
.text:00000000004008A5                 mov     rdi, rax        ; filename
.text:00000000004008A8                 call    _fopen



and store the value inside the rbp+stream

.text:00000000004008AD                 mov     [rbp+stream], rax
.text:00000000004008B1                 cmp     [rbp+stream], 0
.text:00000000004008B6                 jnz     short loc_4008E6



IS juste print a error 
.text:00000000004008B8                 mov     rax, cs:stderr@@GLIBC_2_2_5
.text:00000000004008BF                 mov     rdx, rax
.text:00000000004008C2                 mov     eax, offset aErrorFailedToO ; "ERROR: failed to open password file\n"
.text:00000000004008C7                 mov     rcx, rdx        ; s
.text:00000000004008CA                 mov     edx, 24h ; '$'  ; n
.text:00000000004008CF                 mov     esi, 1          ; size
.text:00000000004008D4                 mov     rdi, rax        ; ptr
.text:00000000004008D7                 call    _fwrite





after is read from the stream and put to the flag buffer

.text:00000000004008E6 loc_4008E6:                             ; CODE XREF: main+A2↑j
.text:00000000004008E6                 lea     rax, [rbp+flag]
.text:00000000004008ED                 mov     rdx, [rbp+stream]

.text:00000000004008F1                 mov     rcx, rdx        ; stream
.text:00000000004008F4                 mov     edx, 41         ; n
.text:00000000004008F9                 mov     esi, 1          ; size
.text:00000000004008FE                 mov     rdi, rax        ; ptr
.text:0000000000400901                 call    _fread





size_t strspn(const char *s, const char *accept);
so is get the len of the str

.text:0000000000400906                 mov     [rbp+var_C], eax
.text:0000000000400909                 lea     rax, [rbp+flag]

.text:0000000000400910                 mov     esi, offset reject ; "\n"
.text:0000000000400915                 mov     rdi, rax        ; s
.text:0000000000400918                 call    _strcspn


put a 0 inside the len of the end of flag 
.text:000000000040091D                 mov     [rbp+rax+flag], 0

if the len of the len of the str is 41
.text:0000000000400925                 cmp     [rbp+var_C], 41
.text:0000000000400929                 jz      short loc_40097D



write erreor message is false
.text:000000000040092B                 mov     rax, cs:stderr@@GLIBC_2_2_5
.text:0000000000400932                 mov     rdx, rax
.text:0000000000400935                 mov     eax, offset aErrorFailedToR ; "ERROR: failed to read password file\n"
.text:000000000040093A                 mov     rcx, rdx        ; s
.text:000000000040093D                 mov     edx, 24h ; '$'  ; n
.text:0000000000400942                 mov     esi, 1          ; size
.text:0000000000400947                 mov     rdi, rax        ; ptr
.text:000000000040094A                 call    _fwrite
.text:000000000040094F                 mov     rax, cs:stderr@@GLIBC_2_2_5
.text:0000000000400956                 mov     rdx, rax
.text:0000000000400959                 mov     eax, offset aErrorFailedToR ; "ERROR: failed to read password file\n"
.text:000000000040095E                 mov     rcx, rdx        ; s
.text:0000000000400961                 mov     edx, 24h ; '$'  ; n
.text:0000000000400966                 mov     esi, 1          ; size
.text:000000000040096B                 mov     rdi, rax        ; ptr
.text:000000000040096E                 call    _fwrite
.text:0000000000400973                 mov     edi, 1          ; status
.text:0000000000400978                 call    _exit






print some element before the input
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



get from stdin 100octet 

.text:00000000004009C3                 mov     rax, cs:stdin@@GLIBC_2_2_5
.text:00000000004009CA                 mov     rdx, rax        ; stream
.text:00000000004009CD                 lea     rax, [rbp+input1]
.text:00000000004009D1                 mov     esi, 100 ;      ; n
.text:00000000004009D6                 mov     rdi, rax        ; s
.text:00000000004009D9                 call    _fgets



get the len of the input 

.text:00000000004009DE                 lea     rax, [rbp+input1]
.text:00000000004009E2                 mov     esi, offset reject ; "\n"
.text:00000000004009E7                 mov     rdi, rax        ; s
.text:00000000004009EA                 call    _strcspn

and put end of the len \0
.text:00000000004009EF                 mov     [rbp+rax+input1], 0


print some element password
.text:00000000004009F4                 mov     eax, offset aPassword ; "--[ Password: "
.text:00000000004009F9                 mov     rdi, rax        ; format
.text:00000000004009FC                 mov     eax, 0
.text:0000000000400A01                 call    _printf



get 100 octet from the len and put the result inside the rbp+input2

.text:0000000000400A06                 mov     rax, cs:stdin@@GLIBC_2_2_5
.text:0000000000400A0D                 mov     rdx, rax        ; stream
.text:0000000000400A10                 lea     rax, [rbp+input2]
.text:0000000000400A17                 mov     esi, 64h ; 'd'  ; n
.text:0000000000400A1C                 mov     rdi, rax        ; s
.text:0000000000400A1F                 call    _fgets




get the len and put the value 0 of the end of the string

.text:0000000000400A24                 lea     rax, [rbp+input2]
.text:0000000000400A2B                 mov     esi, offset reject ; "\n"
.text:0000000000400A30                 mov     rdi, rax        ; s
.text:0000000000400A33                 call    _strcspn
.text:0000000000400A38                 mov     [rbp+rax+input2], 0




print some element

.text:0000000000400A40                 mov     edi, offset asc_400CF8 ; "***************************************"...
.text:0000000000400A45                 call    _puts




compare after the second input2 with the flag only the first 41 octet

.text:0000000000400A4A                 lea     rcx, [rbp+input2]
.text:0000000000400A51                 lea     rax, [rbp+flag]
.text:0000000000400A58                 mov     edx, 41         ; n
.text:0000000000400A5D                 mov     rsi, rcx        ; s2
.text:0000000000400A60                 mov     rdi, rax        ; s1
.text:0000000000400A63                 call    _strncmp


.text:0000000000400A68                 test    eax, eax
.text:0000000000400A6A                 jnz     short loc_400A96


if is corret is printing input1 and call /bin/sh


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
.text:0000000000400A96 ; ---------------------------------------------------------------------------



if not correct 

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
.text:0000000000400AB6 ; } // starts at 400814
.text:0000000000400AB6 main            endp
.text:0000000000400AB6


so how to exploit this binary 



ok because is copy more than 100 elment inside a buffer more little 
  char input2[96]; // [rsp+10h] [rbp-110h] BYREF


is write more than 4 octet up 



but is not the point important here because is only override a value than is not important


but the important part here is if is not correct is get the rbp+input and put directly to printf


.text:0000000000400A96
.text:0000000000400A96 loc_400A96:                             ; CODE XREF: main+256↑j
.text:0000000000400A96                 lea     rax, [rbp+input1]
.text:0000000000400A9A                 mov     rdi, rax        ; format
.text:0000000000400A9D                 mov     eax, 0
.text:0000000000400AA2                 call    _printf
.text:0000000000400AA7                 mov     edi, offset aDoesNotHaveAcc ; " does 


so the input1 is directly put inside printf and  is possible to print the stack !


so if i huse %1$p is print the frist argument of the stack in hex

so i juste need to know wat the argument i want 

so [rbp+flag]

flag= byte ptr -0A0h or -160


so because the stack is 288 of 288 octet of space
.text:0000000000400818                 sub     rsp, 288


the argument is on 288 - 160 =  128     


but because eache argument is 8 elment of space 
128 / 8 = 16