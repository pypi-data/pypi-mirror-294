import os
import sys
import time
from itertools import permutations
import datetime
from colorama import Fore
from .target_info import TargetInfo
from .ai_config import send_and_print_message

def check_root():
    if os.geteuid() != 0:
        print("Ce script doit être exécuté avec des privilèges root.")
        sys.exit(1)

def display_loading_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    pentest_ai_ascii = """
      \_/
     (* *)      _|Pentest AI
    __)#(__      |Loading...
   ( )...( )(_)
   || |_| ||//
>==() | | ()/
    _(___)_
   [-]   [-]
   
    v0.0.1 by Elouan TEISSERE SII 2024
    """

    print(pentest_ai_ascii)
    print("Loading...")

    for i in range(3):
        print("." * (i + 1))
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(pentest_ai_ascii)
        print("Loading...")

    print("Initialization complete!")

# Call the display_loading_screen function at the start of your script

def clean_report():
    my_path = 'outputs/'
    for root, dirs, files in os.walk(my_path):
        for file_name in files:
            if file_name.endswith('.txt') or file_name.endswith('.md') or file_name.endswith('.pdf'):
                file_path = os.path.join(root, file_name)
                os.remove(file_path)
                print(f"Removed: {file_path}")
                
def safety_verification(cmd):
    special_chars = ['[', ';', '|', ']']  # Caractères spéciaux interdits

    file_path = TargetInfo().get_safe_tool()

    if not file_path:
        print('Le programme ne peut pas vérifier la commande, changez le PATH de authorized tools dans le .env')
        sys.exit(1)

    # Lire les commandes autorisées
    with open(file_path, 'r') as file:
        authorized_commands = file.read().splitlines()

    # Extraire la commande de base (sans arguments)
    base_cmd = cmd.split()[0]

    # Vérifier si la commande est autorisée et ne contient pas de caractères spéciaux
    is_safe = base_cmd in authorized_commands and not any(char in cmd for char in special_chars)

    # Log de la commande
    log_command(cmd, is_safe)

    return is_safe

def command_modification(cmd):
    # Fonction pour générer toutes les permutations possibles des options conflictuelles
    def generate_permutations(options):
        return ['-' + ''.join(p) for p in permutations(options)]
    
    # Liste des permutations de 'qweds'
    conflicting_permutations = generate_permutations('qweds')

    if cmd.startswith('dirb '):
        # Ajouter l'option -S pour dirb
        if '-S' not in cmd:
            cmd += ' -S'
    
    elif cmd.startswith('gobuster '):
        # Ajouter l'option -q pour gobuster
        if '-q' not in cmd:
            cmd += ' -q'
    
    elif cmd.startswith('uniscan '):
        # Ajouter l'option -qweds pour uniscan
        if not any(opt in cmd for opt in conflicting_permutations):
            cmd += ' -qweds'
    
    return cmd


def log_command(cmd, is_safe):
    """ Log la commande avec le résultat WORK/DON'T WORK dans un fichier de log. """
    # Génération du chemin vers le fichier de log
    log_file_path = "logs/command_history.log"
    
    # Création des répertoires si nécessaire
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Génération du message de log avec WORK ou DON'T WORK
    status = "WORK" if is_safe else "DON'T WORK"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_message = f"{timestamp} - Command: {cmd} - Status: {status}\n"
    print(log_message)
    # Écriture dans le fichier de log
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message)
        
    
def create_checkpoint(task_tree, target_info):
    return f"PTT: {task_tree}, Target: {target_info.get_summary()}" # Le checkpoint sert à ce que l'IA ne perde pas le contexte global

def maximum_parse(util_session, cmd_output):
    """
    Parse la sortie de la commande pour obtenir le maximum de données.
    """
    print(Fore.CYAN + "Parsing...")
    parsed=send_and_print_message("util_session", util_session, "You will need to parse the test result to a maximum. The aim is to reduce the number of token as the test result will be used in another LLM. Here is the text that you need to parse :\n"+cmd_output)
    return parsed