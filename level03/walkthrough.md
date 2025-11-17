level02@OverRide:~$ su level03
Password: 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   /home/users/level03/level03


so the program have
partiel protection of the got
have the canary enable
BUT have the stack executable
and no have aslr 



so here the only possibility is to use ROP so gadget !


 ./level03 
***********************************
*               level03         **
***********************************
Password:a

Invalid Password


is juste put a input and write is not valide


info function :
0x08048617  get_unum
0x0804864f  prog_timeout
0x08048660  decrypt
0x08048747  test
0x0804885a  main


is have multiple function   