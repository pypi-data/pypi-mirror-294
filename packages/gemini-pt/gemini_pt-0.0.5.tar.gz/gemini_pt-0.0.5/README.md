> Pour l'instant c'est plutôt aléatoire donc si vous avez des idées pour gérer les prompts c'est cool, j'utilise le prompt v6 pour l'instant c'est le mieux mais je vais bientôt faire une session spécialisée pour les outils difficiles.
> Idéalement utilisez une vm kali comme ça vous aurez la plupart des outils
> Si vous voulez changer et utiliser une autre API d'IA, changez le fichier ai_config dans config.


# Pentest AI Automation Script 

## Description 

Ce projet est un script Python automatisant les tâches de pentest à l'aide d'IA. Il utilise des API pour interagir avec des modèles de langage avancés pour effectuer des tâches comme la sélection d'outils, la génération de commandes, l'exécution de ces commandes, et l'analyse des résultats. Le script est conçu pour optimiser le processus de pentest, en particulier pour les tâches répétitives et l'analyse des résultats.

## Prérequis 

### Logiciels 

- **Kali linux** de préférence mais une distribution **Debian** fonctionnera aussi.
  
- **Python 3.8+**
 
- **pip**  - Pour installer les dépendances Python
 
- **Api Gemini/Openai**
### Python Libraries 

Installez les dépendances avec pip:


```bash
pip install -r requirements.txt
```

### Fichiers nécessaires 
 
- `config/tools/authorized_tools.txt` : Liste des outils autorisés pour les tests de sécurité.
 
- `config/tools/tool_priority.txt` : Liste des outils préférés pour certaines tâches. (Déprécié, vous pouvez changer le code en commentaire dans la fonction command)

## Configuration 
Utilisez le mode --auto ou alors mettez au moins les paramètres -ip, -c et -key

```bash
options:
  -h, --help            show this help message and exit
  -ip TARGET, --target TARGET
                        Adresse IP à scanner
  -c CONTEXT, --context CONTEXT
                        Contexte
  -p PRIORITY_TOOL, --priority-tool PRIORITY_TOOL
                        Chemin vers le fichier des outils de priorité
  -s SAFE_TOOL, --safe-tool SAFE_TOOL
                        Chemin vers le fichier des outils autorisés
  -v PROMPT_VERSION, --prompt-version PROMPT_VERSION
                        Version du prompt
  -api API_TYPE, --api-type API_TYPE
                        Type d'API
  -key API_KEY, --api-key API_KEY
                        Clé API
  --auto                Activer le mode auto pour entrer les valeurs manuellement
```

## Utilisation 

### Lancement du script 

Pour lancer le script, exécutez la commande suivante :


```bash
sudo python main.py
```
- Il faut idéalement avoir les droits administrateur pour certaines commandes
### Fonctionnalités principales 
 
- **Initialisation**  : Le script démarre avec un écran de chargement et une initialisation des sessions IA.
 
- **Saisie des informations cible**  : Vous serez invité à entrer l'adresse IP cible et/ou le contexte du test.
 
- **Arbre des tâches**  : Le script crée un arbre des tâches basé sur les informations fournies et le modèle IA.
 
- **Sélection et exécution des tâches**  : Le script sélectionne la tâche appropriée, génère la commande correspondante, et l'exécute tout en vérifiant la sécurité.
 
- **Analyse et rapport**  : Le résultat de chaque commande est analysé et sauvegardé, et un rapport final est généré en format Markdown et PDF.

### Interruption du script 
Vous pouvez interrompre le script à tout moment avec `Ctrl+C`. Un rapport final sera généré automatiquement.
## Structure du Projet 
 
- **`config/`**  : Contient les fichiers de configuration pour les sessions IA.
 
- **`prompts/`**  : Fichiers de prompt utilisés pour communiquer avec l'IA.
 
- **`tasks/`**  : Scripts et fichiers relatifs aux tâches spécifiques comme la création de rapports, la vérification des installations, etc.
 
- **`outputs/`**  : Dossier où sont stockés les fichiers de sortie, y compris les rapports d'analyse.

- **`logs/`**  : Dossier où sont stockés les logs de commandes et de prompts.


## Limitations 
 
- Le script est conçu pour être utilisé dans un environnement contrôlé avec des outils spécifiques listés dans `authorized_tools.txt`.

- Il nécessite une clé API valide pour interagir avec les services d'IA.

- L'IA peut halluciner ou rester dans des analyses de surface.

## Contributeur 
 
- **Elouan TEISSERE**  - Créateur du projet
