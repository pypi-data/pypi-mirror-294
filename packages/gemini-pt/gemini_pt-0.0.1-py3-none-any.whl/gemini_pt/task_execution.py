import sys
import subprocess
from .target_info import TargetInfo
from .utils import create_checkpoint, safety_verification, command_modification
from .ai_config import send_and_print_message

from .install_util import install_package


def init_tree(reasoning_session, target_info):
    """
    Initialise l'arbre de tâches et envoie le message d'initialisation.
    """
    prompt_version = target_info.get_prompt()
    if not prompt_version:
            print("Votre prompt n'as pas été trouvé, veuillez vérifier le fichier .env")
            sys.exit(1)
            
    # Importation dynamique du module de prompt en fonction de la version
    prompt_module = __import__(f"{prompt_version}", fromlist=['Pentestprompt'])
    Pentestprompt = getattr(prompt_module, 'Pentestprompt')
    pt = Pentestprompt()
    checkpoint = create_checkpoint('', target_info)
    return send_and_print_message("init_tree_session",reasoning_session, pt.task_description + checkpoint)


def task(reasoning_session, task_tree, target_info):
    """
    Sélectionne et initialise une tâche à partir des informations sur la cible.
    """

    priority_tool = TargetInfo().get_priority_tool()

    if not priority_tool:
        print('Fichier des outils préférés non trouvé. Pensez à changer le PATH dans le .env')
        sys.exit(1)
    prompt_version = target_info.get_prompt()
    if not prompt_version:
            print("Votre prompt n'as pas été trouvé, veuillez vérifier le fichier .env")
            sys.exit(1)
            
    # Importation dynamique du module de prompt en fonction de la version
    prompt_module = __import__(f"{prompt_version}", fromlist=['Pentestprompt'])
    Pentestprompt = getattr(prompt_module, 'Pentestprompt')
    
    pt = Pentestprompt()
    checkpoint = create_checkpoint(task_tree, target_info)
    return send_and_print_message("task_session", reasoning_session, f"{pt.process_results_task_selection}\n{checkpoint}\n")


def command(generation_session,parsing_session, task, target_info,cmd_before):
    """
    Crée une commande basée sur la tâche et les informations sur la cible.
    Help section à ajouter seulement si la commande fail
    Penser à modifier aussi le prompt
    """
    prompt_version = target_info.get_prompt()
    if not prompt_version:
            print("Votre prompt n'as pas été trouvé, veuillez vérifier le fichier .env")
            sys.exit(1)
            
    # Importation dynamique du module de prompt en fonction de la version
    prompt_module = __import__(f"{prompt_version}", fromlist=['Pentestprompt'])
    Pentestprompt = getattr(prompt_module, 'Pentestprompt')
    pt = Pentestprompt()

    # command=send_and_print_message("command_session",generation_session, f"{pt.todo_to_command}\nTask: {task}\n")
    # result = subprocess.run([command.split()[0], '--help'], capture_output=True, text=True, check=True)
    # help_section=send_and_print_message("help_session",parsing_session,result.stdout)
    
    return send_and_print_message("final_command_session", generation_session, f"{pt.todo_to_command}\nTask: {task}\n{target_info.get_summary()}\n The output of the command before was:\n {cmd_before}")


def output(cmd, reasoning_session, generation_session,parsing_session, target_info, task_tree, task):
    """
    Exécute la commande si elle est autorisée, sinon relance la tâche avec une nouvelle commande.
    """
    print("command before :",cmd)
    if safety_verification(cmd):
        install_package(cmd.split()[0])  # Vérification d'installation du paquet
        command_valid = ["yes", "|"] + [cmd]  # Utilisation de l'app yes pour faire du batch
        cmd=command_modification(cmd)
        print("command after :",cmd)

        input("Entrer cette commande ? :\n" +"`"+cmd+"`")

        result = subprocess.run(" ".join(command_valid), shell=True, capture_output=True, text=True)

        print("Sortie de la commande :")
        print(result.stdout)
        return cmd, result.stdout, task_tree

    print("La commande n'est pas autorisée ou contient des caractères spéciaux. Changement de la tâche")
    new_task = retry_task(reasoning_session, task_tree, task, target_info)
    cmd = command(generation_session,parsing_session, new_task, target_info,cmd)

    return output(cmd, reasoning_session, generation_session,parsing_session, target_info, task_tree, new_task)


def analyse(parsing_session, cmd_output):
    """
    Analyse le résultat de la commande.
    """
    return send_and_print_message("analyse_session", parsing_session, f"The command output is:\n{cmd_output}\nIf the output is empty, please say : The task is not applicable")


def update_tree(reasoning_session, target_info, task_tree, output):
    """
    Met à jour l'arbre des tâches avec les résultats de l'analyse.
    """
    prompt_version = target_info.get_prompt()
    if not prompt_version:
            print("Votre prompt n'as pas été trouvé, veuillez vérifier le fichier .env")
            sys.exit(1)
            
    # Importation dynamique du module de prompt en fonction de la version
    prompt_module = __import__(f"{prompt_version}", fromlist=['Pentestprompt'])
    Pentestprompt = getattr(prompt_module, 'Pentestprompt')
    pt = Pentestprompt()
    checkpoint = create_checkpoint(task_tree, target_info)
    #return send_and_print_message("update_tree_session", reasoning_session, f"{pt.process_results}\nPTT:\n{task_tree}\nTest result: \n\n{output}")
    return send_and_print_message("update_tree_session", reasoning_session, f"{pt.process_results}\n{checkpoint}\nTest result: \n\n{output}")



def retry_task(reasoning_session, task_tree, task, target_info):
    """
    Relance une tâche si la commande précédente a échoué ou n'est pas autorisée.
    """

    priority_tool = TargetInfo().get_priority_tool()

    if not priority_tool:
        print('Fichier des outils préférés non trouvé. Pensez à changer le PATH dans le .env')
        sys.exit(1)
    prompt_version = target_info.get_prompt()
    if not prompt_version:
            print("Votre prompt n'as pas été trouvé, veuillez vérifier le fichier .env")
            sys.exit(1)
            
    # Importation dynamique du module de prompt en fonction de la version
    prompt_module = __import__(f"{prompt_version}", fromlist=['Pentestprompt'])
    Pentestprompt = getattr(prompt_module, 'Pentestprompt')
    pt = Pentestprompt()
    checkpoint = create_checkpoint(task_tree, target_info)
    return send_and_print_message("retry_task_session", reasoning_session, f"{pt.retry_task}\n{checkpoint}\nREFUSED TASK: {task}\n")
