# Level03 Write-up

## Introduction

```bash
level02@OverRide:~$ su level03
Password: 
```

## Security Analysis

```
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   /home/users/level03/level03
```

So the program has:
- Partial protection of the GOT
- Canary enabled
- **BUT** has the stack executable
- No ASLR

So here the only possibility is to use ROP (Return-Oriented Programming) gadgets!

## Program Execution

```bash
./level03 
***********************************
*               level03         **
***********************************
Password:a

Invalid Password
```

It just takes an input and writes "Invalid Password" if it's not valid.

## Function Analysis

```
info function :
0x08048617  get_unum
0x0804864f  prog_timeout
0x08048660  decrypt
0x08048747  test
0x0804885a  main
```

It has multiple functions.

## Main Function

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  time_t v3; // eax
  int savedregs; // [esp+20h] [ebp+0h] BYREF

  v3 = time(0);
  srand(v3);
  puts("***********************************");
  puts("*\t\tlevel03\t\t**");
  puts("***********************************");
  printf("Password:");
  __isoc99_scanf("%d", &savedregs);
  test(savedregs, 322424845);
  return 0;
}
```

## Test Function

```c
int __cdecl test(int a1, int a2)
{
  int result; // eax
  char v3; // al

  switch ( a2 - a1 )
  {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
    case 9:
    case 16:
    case 17:
    case 18:
    case 19:
    case 20:
    case 21:
      result = decrypt(a2 - a1);
      break;
    default:
      v3 = rand();
      result = decrypt(v3);
      break;
  }
  return result;
}
```

## Decrypt Function

Let's see what's inside `decrypt`:

```c
int __cdecl decrypt(char a1)
{
  unsigned int i; // [esp+20h] [ebp-28h]
  unsigned int v3; // [esp+24h] [ebp-24h]
  _DWORD v4[7]; // [esp+2Bh] [ebp-1Dh] BYREF

  *(_DWORD *)((char *)&v4[4] + 1) = __readgsdword(0x14u);
  strcpy((char *)v4, "Q}|u`sfg~sf{}|a3");
  v3 = strlen((const char *)v4);
  for ( i = 0; i < v3; ++i )
    *((_BYTE *)v4 + i) ^= a1;
  if ( !strcmp((const char *)v4, "Congratulations!") )
    return system("/bin/sh");
  else
    return puts("\nInvalid Password");
}
```

## Analysis

Actually, if you pass a value between `322424845` to `322424845 - 21`, it uses the value of the comparison between 1 to 21.

Otherwise, it uses a random value.

So it's only possible to pass these 21 possibilities, and that's okay.

## Solution

Found the value: `322424827`

## Flag

```
kgv3tkEb9h2mLkRsPkXRfc2mHbjMxQzvb2FrgKkf
```
