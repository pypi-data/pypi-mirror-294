from .utils import check_root, display_loading_screen, clean_report, maximum_parse# OK
from .session_management import init_sessions # OK
from .target_info import * # OK
from .task_execution import init_tree, task, command, output, analyse, update_tree
from .report_creation import finish, save_artifact, log_analyse
from colorama import Fore

import sys

def main():
    try:
        check_root()
        target_info = get_target_info()
        display_loading_screen()
        clean_report()
        reasoning_session, generation_session, parsing_session, final_session, util_session = init_sessions(target_info)
        task_tree = init_tree(reasoning_session, target_info)
        print(task_tree)
        cmd_output = ""
        while True:
            print("Task selected :")
            task_selected = task(reasoning_session, task_tree, target_info)
            print(task_selected)
            if not task_selected:
                break

            print("Command :")
            cmd = command(generation_session, parsing_session, task_selected, target_info, cmd_output)
            cmd, cmd_output, task_tree = output(cmd, reasoning_session, generation_session,parsing_session, target_info, task_tree, task_selected)
            base_cmd = cmd.split()[0]
            print("Analyse")
            analyse_output = analyse(parsing_session, cmd_output)
            print("Analyse output:")
            print(analyse_output)
            save_artifact(base_cmd, analyse_output, cmd_output)
            log_analyse(cmd, analyse_output)
            print(Fore.CYAN + "Update_tree")
            test_parsed = maximum_parse(util_session,analyse_output)
            task_tree = update_tree(reasoning_session, target_info, task_tree, test_parsed)
            print(Fore.GREEN + task_tree)
            finish(util_session,final_session, task_tree)
            
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgramme interrompu (Ctrl+C).")
        sys.exit(0)

if __name__ == "__main__":
    main()
