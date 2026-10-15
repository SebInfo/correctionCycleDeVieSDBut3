
"""Tests du corrigé, utilisables depuis Pyzo."""

import unittest
from pathlib import Path
from application_corrige import (
    charger_csv,
    total_voyageurs,
    moyenne_par_ligne
)

BASE = Path(__file__).resolve().parent


class TestFrequentation(unittest.TestCase):

    def setUp(self):
        self.donnees = charger_csv(BASE / "donnees.csv")

    def test_total(self):
        self.assertEqual(total_voyageurs(self.donnees), 560)

    def test_moyennes(self):
        self.assertEqual(
            moyenne_par_ligne(self.donnees),
            {"L1": 100.0, "L2": 100.0, "L3": 60.0}
        )

    def test_liste_vide(self):
        self.assertEqual(moyenne_par_ligne([]), {})

    def test_effectif_negatif(self):
        donnees = [
            {"ligne": "L1", "nb_voyageurs": "80"},
            {"ligne": "L1", "nb_voyageurs": "120"},
            {"ligne": "L1", "nb_voyageurs": "-5"}
        ]
        self.assertEqual(
            moyenne_par_ligne(donnees),
            {"L1": 100.0}
        )

    def test_valeur_nd(self):
        donnees = [
            {"ligne": "L1", "nb_voyageurs": "80"},
            {"ligne": "L1", "nb_voyageurs": "120"},
            {"ligne": "L1", "nb_voyageurs": "ND"}
        ]
        self.assertEqual(
            moyenne_par_ligne(donnees),
            {"L1": 100.0}
        )

    def test_schema_change(self):
        with self.assertRaisesRegex(ValueError, "nb_voyageurs"):
            charger_csv(BASE / "donnees_incident.csv")


if __name__ == "__main__":
    unittest.main(verbosity=2)
