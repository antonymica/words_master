import itertools
from unidecode import unidecode

def generer_mots_possibles(lettres):
    """Générer toutes les combinaisons possibles à partir des lettres fournies."""
    lettres = unidecode(lettres).upper()
    mots_possibles = set()

    for longueur in range(1, len(lettres) + 1):
        for combinaison in itertools.permutations(lettres, longueur):
            mot = "".join(combinaison)
            mots_possibles.add(mot)

    return mots_possibles

def rechercher_mots_valides(mots_possibles, fichier_mots):
    """Rechercher les mots valides dans le fichier de mots."""
    mots_valides = set()

    try:
        with open(fichier_mots, "r", encoding="utf-8") as f:
            mots_francais = set(unidecode(mot.strip()).upper() for mot in f)
        mots_valides = mots_possibles.intersection(mots_francais)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_mots} est introuvable.")

    return mots_valides

def enregistrer_resultats(mots_valides, nom_fichier):
    """Enregistrer les mots valides dans un fichier .txt."""
    with open(nom_fichier, "w", encoding="utf-8") as f:
        for mot in sorted(mots_valides):
            f.write(mot + "\n")
