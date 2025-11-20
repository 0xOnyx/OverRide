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

