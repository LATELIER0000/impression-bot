# Fichier : test_conversion.py
import os
import subprocess
import shutil
import pathlib

# --- On définit les dossiers ici aussi ---
CONVERTED_FOLDER = os.path.join(os.getcwd(), 'uploads', 'converted')

# --- On copie-colle la fonction de débogage EXACTE d'en haut ---
def convert_to_pdf(source_path):
    filename = os.path.basename(source_path)
    pdf_path = os.path.join(CONVERTED_FOLDER, f"{os.path.splitext(filename)[0]}.pdf")
    if os.path.splitext(filename)[1].lower() == '.pdf':
        shutil.copy(source_path, pdf_path)
        return pdf_path
        
    lo_command = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
    if not os.path.exists(lo_command):
        print(f"ERREUR CRITIQUE: LibreOffice introuvable: {lo_command}")
        return None
    
    user_profile_path = os.path.join(os.getcwd(), 'lo_profile')
    user_profile_url = pathlib.Path(user_profile_path).as_uri()

    try:
        print(f"--- DÉBUT DE LA CONVERSION DÉBOGAGE pour '{filename}' ---")
        command = [
            lo_command,
            f'-env:UserInstallation={user_profile_url}',
            '--headless',
            '--convert-to', 'pdf:writer_pdf_Export',
            '--outdir', CONVERTED_FOLDER,
            source_path
        ]
        
        result = subprocess.run(
            command, 
            timeout=120, 
            capture_output=True,
            text=True
        )

        print("--- Sortie Standard (stdout) de LibreOffice ---")
        print(result.stdout if result.stdout else "Aucune sortie standard.")
        print("-----------------------------------------------")
        
        print("--- Sortie d'Erreur (stderr) de LibreOffice ---")
        print(result.stderr if result.stderr else "Aucune sortie d'erreur.")
        print("-----------------------------------------------")

        if result.returncode != 0:
            print(f"ERREUR : LibreOffice a quitté avec un code d'erreur : {result.returncode}")
            return None

        if os.path.exists(user_profile_path):
            shutil.rmtree(user_profile_path)
            
        if os.path.exists(pdf_path):
             print(f"--- FIN CONVERSION DÉBOGAGE : Fichier PDF créé. ---")
             return pdf_path
        else:
             print(f"--- FIN CONVERSION DÉBOGAGE : Le fichier PDF n'a PAS été créé. ---")
             return None
        
    except Exception as e:
        print(f"ERREUR FATALE durant la conversion de {filename}: {e}")
        if os.path.exists(user_profile_path):
            shutil.rmtree(user_profile_path)
        return None

# --- POINT D'ENTRÉE DU TEST ---
if __name__ == "__main__":
    # --- À MODIFIER : Mettez le chemin complet vers votre fichier de test ---
    # Par exemple, un .docx, un .png, un .xlsx qui pose problème.
    # Assurez-vous que ce fichier existe !
    fichier_a_tester = r"C:\Users\Wawa\Desktop\PrintServer\uploads\TEST.docx" 
    
    print(f"Lancement du test de conversion pour : {fichier_a_tester}")
    if os.path.exists(fichier_a_tester):
        resultat = convert_to_pdf(fichier_a_tester)
        if resultat:
            print(f"\nSUCCÈS ! Le fichier a été créé ici : {resultat}")
        else:
            print(f"\nÉCHEC ! La conversion a échoué. Vérifiez les logs ci-dessus.")
    else:
        print(f"\nERREUR DE TEST : Le fichier '{fichier_a_tester}' n'existe pas. Veuillez corriger le chemin.")
