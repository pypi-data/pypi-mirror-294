import sys
import nmap
import argparse


class TargetInfo:
    def __init__(self, target=None, context=None, ports=None, api_type="gemini", api_key=None, priority_tool="tools/tool_priority.txt", safe_tool="tools/authorized_tools.txt", prompt_version="prompt_webpen_v1"):
        self.target = target if target else "No IP provided"
        self.context = context if context else "No context provided"
        self.ports = ports if ports else "No ports scanned"
        self.api_type = api_type
        self.api_key = api_key
        self.priority_tool = priority_tool
        self.safe_tool = safe_tool
        self.prompt_version = prompt_version

    def __str__(self):
        return (f"Target IP: {self.target}, Context: {self.context}, Ports: {self.ports}, "
                f"API Type: {self.api_type}, API Key: {self.api_key}, Priority Tool: {self.priority_tool}, "
                f"Safe Tool: {self.safe_tool}, Prompt Version: {self.prompt_version}")

    def get_summary(self):
        return f"Target: {self.target}, Context: {self.context}, Ports: {self.ports}"

    def get_api_type(self):
        return self.api_type

    def get_api_key(self):
        return self.api_key

    def get_safe_tool(self):
        return self.safe_tool

    def get_priority_tool(self):
        return self.priority_tool

    def get_prompt(self):
        return self.prompt_version


def run_nmap_scan(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, arguments='-p-')  # Scanne tous les ports

    open_ports = []

    for host in scanner.all_hosts():
        for proto in scanner[host].all_protocols():
            ports = scanner[host][proto].keys()
            for port in ports:
                if scanner[host][proto][port]['state'] == 'open':
                    open_ports.append(port)

    return open_ports


def get_target_info(args=None):
    parser = argparse.ArgumentParser(description="Script pour scanner les ports et obtenir des informations cibles.")
    parser.add_argument('-ip', '--target', help="Adresse IP à scanner")
    parser.add_argument('-c', '--context', default=None, help="Contexte")
    parser.add_argument('-p', '--priority-tool', default="tools/tool_priority.txt", help="Chemin vers le fichier des outils de priorité")
    parser.add_argument('-s', '--safe-tool', default="tools/authorized_tools.txt", help="Chemin vers le fichier des outils autorisés")
    parser.add_argument('-v', '--prompt-version', default="prompt_webpen_v1", help="Version du prompt")
    parser.add_argument('-api', '--api-type', default="gemini", help="Type d'API")
    parser.add_argument('-key', '--api-key', default=None, help="Clé API")
    parser.add_argument('--auto', action='store_true', help="Activer le mode auto pour entrer les valeurs manuellement")

    if args is None:
        args = sys.argv[1:]  # Utilise les arguments de la ligne de commande

    parsed_args = parser.parse_args(args)

    if parsed_args.auto:
        # Demander les informations via input si le mode auto est activé
        while True:
            try:
                target = input("Veuillez entrer l'adresse IP à scanner: ").strip()
                if not target:
                    raise ValueError("Une adresse IP doit être fournie.")
                
                context = input(f"Contexte (laisser vide pour '{parsed_args.context}'): ").strip() or parsed_args.context
                priority_tool = input(f"Chemin vers le fichier des outils de priorité (laisser vide pour '{parsed_args.priority_tool}'): ").strip() or parsed_args.priority_tool
                safe_tool = input(f"Chemin vers le fichier des outils autorisés (laisser vide pour '{parsed_args.safe_tool}'): ").strip() or parsed_args.safe_tool
                prompt_version = input(f"Version du prompt (laisser vide pour '{parsed_args.prompt_version}'): ").strip() or parsed_args.prompt_version
                api_type = input(f"Type d'API (laisser vide pour '{parsed_args.api_type}'): ").strip() or parsed_args.api_type
                api_key = input(f"Clé API (laisser vide pour '{parsed_args.api_key}'): ").strip() or parsed_args.api_key
                
                if not target:
                    print("Erreur: L'adresse IP est requise.")
                    continue

                break
            
            except ValueError as ve:
                print(f"Erreur: {ve}. Veuillez réessayer.")
            
            except KeyboardInterrupt:
                print("\nProgramme interrompu (Ctrl+C).\nAucun rapport final ne sera généré.")
                sys.exit(1)  # Arrêter le programme proprement avec un code de sortie approprié

    else:
        if not parsed_args.target:
            print("Erreur: L'adresse IP est requise. Utilisez -h pour obtenir de l'aide.")
            sys.exit(1)

        target = parsed_args.target
        context = parsed_args.context
        priority_tool = parsed_args.priority_tool
        safe_tool = parsed_args.safe_tool
        prompt_version = parsed_args.prompt_version
        api_type = parsed_args.api_type
        api_key = parsed_args.api_key

    print(f"Running Nmap scan on {target}...")

    open_ports = run_nmap_scan(target)
    ports_info = open_ports if open_ports else "No open ports found"

    return TargetInfo(target, context, ports_info, api_type, api_key, priority_tool, safe_tool, prompt_version)


if __name__ == "__main__":
    target_info = get_target_info()
    print(target_info)
    print(f"Summary: {target_info.get_summary()}")
    print(f"API Type: {target_info.get_api_type()}")
    print(f"API Key: {target_info.get_api_key()}")
    print(f"Safe Tool: {target_info.get_safe_tool()}")
    print(f"Priority Tool: {target_info.get_priority_tool()}")
    print(f"Prompt Version: {target_info.get_prompt()}")
