import sys
from .target_info import TargetInfo
from .ai_config import create_chat_session, send_and_print_message

# Récupérer la version du prompt depuis .env

def init_sessions(target_info):
    api_key = target_info.get_api_key()
    if not api_key:
        print('Votre clé API n\'est pas définie.')
        sys.exit(1)
    prompt_version = target_info.get_prompt()
    
    if not prompt_version:
            print("Votre prompt n'as pas été trouvé, veuillez vérifier le fichier .env")
            sys.exit(1)
    # Importation dynamique du module de prompt en fonction de la version
    prompt_module = __import__(f".{prompt_version}", fromlist=['Pentestprompt'])
    Pentestprompt = getattr(prompt_module, 'Pentestprompt')
    
    pt = Pentestprompt()
    sessions = [create_chat_session(api_key) for _ in range(5)]
    reasoning_session, generation_session, parsing_session, final_session, util_session = sessions

    # Initialisation des sessions
    task_tree=send_and_print_message("init_session_reason",reasoning_session, pt.reasoning_session_init)
    send_and_print_message("init_session_gen", generation_session, pt.generation_session_init)
    send_and_print_message("init_session_parse", parsing_session, pt.input_parsing_init)
    send_and_print_message("init_session_final", final_session, pt.final_report_init)

    return reasoning_session, generation_session, parsing_session, final_session, util_session
