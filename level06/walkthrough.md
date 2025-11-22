# Level06 Write-up

## Introduction

The program takes two inputs and makes some hash and compares it with a value. If it's correct, it spawns a new `/bin/bash`.

## Anti-Debugging Protection

The problem is that it checks if the program has some debugger already attached:

```c
if ( ptrace(PTRACE_TRACEME, 0, 1, 0) == -1 )
```

## Solution Approach

The solution is to make a breakpoint just before and jump to the next instruction.

But I prefer the approach that just codes the function and looks at what's expected from the input.

## Finding the Credentials

So I found for the string `jerdos`:
I found the serial: `6232807`

## Flag

```
GbcPDRgsFK77LNnnuh7QyFYA2942Gp8yKj9KrWD8
```
