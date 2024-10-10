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
                dictionnaire_fichier_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(dictionnaire_fichier.filename))
                dictionnaire_fichier.save(dictionnaire_fichier_path)

                lettres = request.form.get("lettres", "").strip()
                if lettres:
                    # Générer les mots possibles à partir des lettres saisies
                    mots_possibles = generer_mots_possibles(lettres)

                    # Rechercher les mots valides dans le dictionnaire
                    mots_valides = rechercher_mots_valides(mots_possibles, dictionnaire_fichier_path)

                    if not mots_valides:
                        message = "Aucun mot valide trouvé."

    return render_template("index.html", mots_valides=mots_valides, message=message)

@app.route("/download")
def download():
    # Logique pour télécharger les résultats si nécessaire
    return send_file("resultats_mots.txt", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
