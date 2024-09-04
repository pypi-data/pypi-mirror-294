import subprocess
import sys

def install_package(package_name):
    # Vérifie si la commande est disponible
    command_result = subprocess.run(['which', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if command_result.returncode == 0:
        print(f"La commande '{package_name}' est disponible sur le système.")
    else:
        # Si la commande n'est pas trouvée, on vérifie si c'est un paquet installé
        try:
            package_result = subprocess.run(['dpkg-query', '-W', '-f=${Status}', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if b"install ok installed" in package_result.stdout:
                print(f"Le paquet '{package_name}' est installé.")
            else:
                print(f"Le paquet '{package_name}' n'est pas installé.")
                try:
                    subprocess.run(['sudo', 'apt-get', 'install', '-y', package_name], check=True)
                    print(f"{package_name} a été installé avec succès.")
                except subprocess.CalledProcessError:
                    print(f"Erreur lors de l'installation de {package_name}.")
                    sys.exit(1)
        except subprocess.CalledProcessError:
            print(f"Le paquet ou la commande '{package_name}' n'est ni installé ni disponible.")    
            
if __name__ == "__main__":
    install_package("sl")
    install_package("ls")
