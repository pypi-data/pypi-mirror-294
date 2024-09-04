import sys
import datetime
import markdown2
import pdfkit
import os
from .ai_config import send_and_print_message

def finish(reasoning_session, final_session, task_tree):
    end_task = send_and_print_message(
        "finish_session", reasoning_session,
        "If every task is 'completed' or non applicable, answer with FINISH. Answer with YES and nothing else if you understood. Here is the task tree :" + task_tree
    )

    print("Task tree:", task_tree)
    print(end_task)

    if "FINISH" in end_task:
        print('Programme fini avec succès, compte rendus des fonctions disponible dans /outputs')
        
        # Vérifier l'existence des répertoires nécessaires
        os.makedirs("outputs/parsed", exist_ok=True)
        
        try:
            final_report(final_session)
            markdown_to_pdf("outputs/parsed/final_report.md", "outputs/parsed/final_report.pdf")
            sys.exit(0)
        except FileNotFoundError as e:
            print(f"Erreur : {e}. Impossible de générer le rapport final.")
        except Exception as e:
            print(f"Erreur inattendue lors de la génération du rapport final : {e}")

def final_report(final_session):
    log_path = 'outputs/analysis_log.txt'

    # Vérifier si le fichier existe avant de tenter de le lire
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Le fichier {log_path} n'existe pas.")
    
    # Assurer que le répertoire pour le rapport final existe
    os.makedirs("outputs/parsed", exist_ok=True)

    with open(log_path, 'r') as f:
        content = f.read()
        parsed_report = send_and_print_message("final_report_session", final_session, content)
        
        with open("outputs/parsed/final_report.md", "w") as file:
            file.write(parsed_report)

def markdown_to_pdf(markdown_file, output_pdf):
    try:
        # Lire le fichier Markdown
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        # Convertir le Markdown en HTML
        html_text = markdown2.markdown(markdown_text)
        
        # Ajouter un style CSS classique avec un fond blanc, texte noir et un pied de page
        html_text = f"""
        <html>
        <head>
        <style>
            body {{
                background-color: #FFFFFF;
                color: #000000;
                font-family: 'Arial', sans-serif;
                margin: 20px;
                padding-bottom: 40px; /* Assure l'espace pour le pied de page */
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #333333;
                font-family: 'Arial', sans-serif;
            }}
            a {{
                color: #1a0dab;
                text-decoration: none;
            }}
            p {{
                margin: 0 0 1em;
            }}
            pre {{
                background-color: #f4f4f4;
                border: 1px solid #ddd;
                padding: 10px;
                overflow: auto;
            }}
            .footer {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #f1f1f1;
                color: #333333;
                text-align: center;
                font-size: 0.8em;
                padding: 10px;
                border-top: 1px solid #ddd;
            }}
        </style>
        </head>
        <body>
        {html_text}
        <div class="footer">
            Pentest_AI Elouan TEISSERE SII
        </div>
        </body>
        </html>
        """
        
        # Convertir le HTML en PDF
        pdfkit.from_string(html_text, output_pdf)
        print(f"Conversion réussie : {output_pdf}")

    except FileNotFoundError as e:
        print(f"Erreur : Le fichier Markdown {markdown_file} n'existe pas.")
    except Exception as e:
        print(f"Erreur lors de la conversion en PDF : {e}")

def log_analyse(cmd, cmd_output):
    """ Log the command and its analysis to a file. """
    os.makedirs("outputs", exist_ok=True)
    
    with open("outputs/analysis_log.txt", "a") as log_file:
        log_file.write(f"Command: {cmd}\n")
        log_file.write(f"Output:\n{cmd_output}\n")
        log_file.write("="*40 + "\n")

def save_artifact(task_name, output_content, cmd_output):
    """Enregistre l'artefact dans des fichiers distincts pour le contenu traité et brut."""
    # Génération du timestamp pour le nom de fichier
    timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    
    # Création des noms de fichiers pour les deux types d'artefacts
    filename = f"{task_name}_{timestamp}.txt"
    parsed_path = os.path.join("outputs", "parsed", filename)
    raw_output_path = os.path.join("outputs", "raw_output", filename)
    
    # Création des répertoires si nécessaire
    os.makedirs(os.path.dirname(parsed_path), exist_ok=True)
    os.makedirs(os.path.dirname(raw_output_path), exist_ok=True)

    # Enregistrement du contenu traité
    with open(parsed_path, "w") as file:
        file.write(output_content)
    print(f"Artefact enregistré dans : {parsed_path}")

    # Enregistrement du contenu brut
    with open(raw_output_path, "w") as file:
        file.write(cmd_output)
    print(f"Artefact enregistré dans : {raw_output_path}")

    return filename
