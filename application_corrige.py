"""Corrigé du TP : analyse de la fréquentation d'un réseau de transport.

Exercices 3 et 4 : calculer des moyennes fiables et tester les cas limites.
Exercice 5 : refuser un fichier CSV dont une colonne obligatoire manque.

Ce corrigé utilise uniquement la bibliothèque standard de Python (sans Pandas).
"""

import csv
from pathlib import Path


# Contrat de données : ces quatre colonnes doivent exister dans le fichier.
# Les colonnes supplémentaires sont acceptées ; leur ordre n'a pas d'importance.
CHAMPS_OBLIGATOIRES = {"date", "ligne", "arret", "nb_voyageurs"}


def charger_csv(chemin):
    """Charger le CSV ou signaler une erreur si son schéma a changé."""
    with open(chemin, mode="r", encoding="utf-8", newline="") as fichier:
        lecteur = csv.DictReader(fichier)

        # DictReader lit les noms des colonnes dans la première ligne du CSV.
        champs_presents = set(lecteur.fieldnames or [])

        # Différence d'ensembles : colonnes exigées mais absentes du fichier.
        champs_absents = CHAMPS_OBLIGATOIRES - champs_presents
        if champs_absents:
            # Ne pas poursuivre : avec un schéma incorrect, les calculs
            # pourraient produire des résultats vides ou trompeurs.
            raise ValueError(
                "Schéma CSV incompatible ; colonnes absentes : "
                + ", ".join(sorted(champs_absents))
            )

        # Chaque observation est un dictionnaire :
        # {"date": "...", "ligne": "L1", "nb_voyageurs": "120", ...}.
        # Les valeurs lues dans un CSV sont des chaînes de caractères.
        return list(lecteur)


def _mesure_valide(observation):
    """Renvoyer (identifiant_de_ligne, nombre) ou None si la mesure est invalide.

    Cette fonction commune garantit que total et moyenne appliquent
    exactement les mêmes règles de filtrage.
    """
    identifiant = str(observation.get("ligne") or "").strip()
    if not identifiant:
        return None  # Identifiant de ligne absent ou vide.

    try:
        # Exemple : "120" devient l'entier 120 ; "ND" est rejeté.
        nombre = int(observation.get("nb_voyageurs"))
    except (ValueError, TypeError):
        return None  # Valeur absente ou impossible à convertir en entier.

    if nombre < 0:
        return None  # Un nombre de voyageurs négatif n'est pas valide.

    return identifiant, nombre  # Zéro est une valeur valide.


def total_voyageurs(donnees):
    """Additionner les voyageurs des seules observations valides."""
    total = 0
    for observation in donnees:
        mesure = _mesure_valide(observation)
        if mesure is None:
            continue  # Ignorer cette observation et passer à la suivante.

        _, nombre = mesure  # Le total général n'utilise pas l'identifiant.
        total += nombre

    return total


def moyenne_par_ligne(donnees):
    """Calculer la moyenne PAR OBSERVATION de chaque ligne de transport.

    Une ligne sans aucune observation valide n'apparaît pas dans le résultat.
    Si donnees est vide, la fonction renvoie le dictionnaire vide {}.
    """
    sommes = {}   # Exemple : {"L1": 300, "L2": 200}
    comptes = {}  # Exemple : {"L1": 3,   "L2": 2}

    for observation in donnees:
        mesure = _mesure_valide(observation)
        if mesure is None:
            continue  # L'observation n'entre ni dans la somme ni dans le compte.

        identifiant, nombre = mesure

        # get(cle, 0) utilise zéro si cette ligne n'est pas encore présente.
        sommes[identifiant] = sommes.get(identifiant, 0) + nombre
        comptes[identifiant] = comptes.get(identifiant, 0) + 1

    moyennes = {}
    for identifiant in sommes:
        # Chaque clé présente dans sommes a au moins une mesure valide :
        # le dénominateur comptes[identifiant] ne vaut donc jamais zéro.
        moyennes[identifiant] = sommes[identifiant] / comptes[identifiant]

    return moyennes


if __name__ == "__main__":
    # __file__ permet de retrouver donnees.csv à côté de ce script,
    # indépendamment du dossier de travail choisi dans Pyzo ou PyCharm.
    repertoire = Path(__file__).resolve().parent
    donnees = charger_csv(repertoire / "donnees.csv")

    print("Total voyageurs :", total_voyageurs(donnees))
    print("Moyennes par ligne :", moyenne_par_ligne(donnees))
