# OverRide
This project is the exploitation of (elf-like) binary


qemu-system-x86_64 -boot d -cdrom ./override.iso -m 2048 -enable-kvm \
-net nic -net user,hostfwd=tcp::8888-:4242


ssh utilisateur@localhost -p 8888


#uesful links 
https://dogbolt.org/

https://shell-storm.org/shellcode/index.html


