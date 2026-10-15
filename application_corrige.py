"""Corrigé de l'application de fréquentation. Bibliothèque standard seule."""
import csv
from collections import defaultdict
from pathlib import Path

CHAMPS_OBLIGATOIRES = {"date", "ligne", "arret", "nb_voyageurs"}


def charger_csv(chemin):
    """Charge un CSV et rejette explicitement un schéma inattendu."""
    with open(chemin, mode="r", encoding="utf-8", newline="") as fichier:
        lecteur = csv.DictReader(fichier)
        champs = set(lecteur.fieldnames or [])
        absents = CHAMPS_OBLIGATOIRES - champs
        if absents:
            raise ValueError(
                "Schéma CSV incompatible ; colonnes absentes : "
                + ", ".join(sorted(absents))
            )
        return list(lecteur)


def total_voyageurs(donnees):
    """Total des voyageurs sur des enregistrements valides."""
    return sum(int(ligne["nb_voyageurs"]) for ligne in donnees)


def moyenne_par_ligne(donnees):
    """Moyenne des effectifs par ligne ; ignore les observations invalides."""
    sommes = defaultdict(int)
    nombres = defaultdict(int)
    for observation in donnees:
        identifiant = (observation.get("ligne") or "").strip()
        if not identifiant:
            continue
        try:
            valeur = int(observation.get("nb_voyageurs"))
        except (ValueError, TypeError):
            continue
        if valeur < 0:
            continue
        sommes[identifiant] += valeur
        nombres[identifiant] += 1
    return {ligne: sommes[ligne] / nombres[ligne] for ligne in sommes}


if __name__ == "__main__":
    chemin = Path(__file__).resolve().parent / "donnees.csv"
    lignes = charger_csv(chemin)
    print("Total voyageurs :", total_voyageurs(lignes))
    print("Moyennes par ligne :", moyenne_par_ligne(lignes))
