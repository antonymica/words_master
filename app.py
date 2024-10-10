from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
from backend import generer_mots_possibles, rechercher_mots_valides, enregistrer_resultats

app = Flask(__name__)

# Dossier pour stocker les fichiers téléchargés
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Créer le dossier s'il n'existe pas
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    mots_valides = []
    message = ""

    if request.method == "POST":
        # Vérifie si un fichier a été téléchargé
        if 'dictionnaire' in request.files:
            dictionnaire_fichier = request.files['dictionnaire']
            if dictionnaire_fichier.filename == '':
                message = "Aucun fichier sélectionné."
            else:
                # Enregistrer le fichier dictionnaire téléchargé
                dictionnaire_fichier_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(dictionnaire_fichier.filename))
                dictionnaire_fichier.save(dictionnaire_fichier_path)

                # Récupérer les lettres saisies dans le formulaire
                lettres = request.form.get("lettres", "").strip()
                if lettres:
                    # Générer les mots possibles à partir des lettres saisies
                    mots_possibles = generer_mots_possibles(lettres)

                    # Rechercher les mots valides dans le dictionnaire téléchargé
                    mots_valides = rechercher_mots_valides(mots_possibles, dictionnaire_fichier_path)

                    if not mots_valides:
                        message = "Aucun mot valide trouvé."
                    else:
                        # Enregistrer les mots valides dans un fichier
                        nom_fichier = "resultats_mots.txt"
                        enregistrer_resultats(mots_valides, nom_fichier)

    return render_template("index.html", mots_valides=mots_valides, message=message)

@app.route("/download")
def download():
    file_path = "resultats_mots.txt"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Erreur : Le fichier n'existe pas sur le serveur.", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
