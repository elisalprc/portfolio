"""Étape 1 — fonctions de outils.py (aucune base, aucun serveur)."""
from outils import (decouper_paragraphes, duree, email_valide, extraire_resume,
                    formater_periode, liste_technologies, paginer, slugifier,
                    temps_de_lecture, valider_contact)


# Fonctions fournies : ces tests passent dès le départ.
def test_temps_de_lecture():
    assert temps_de_lecture("") == 1
    assert temps_de_lecture("mot " * 200) == 1
    assert temps_de_lecture("mot " * 201) == 2


def test_liste_technologies():
    assert liste_technologies("Python, Flask ,  SQLite,") == ["Python", "Flask", "SQLite"]
    assert liste_technologies("") == []


# --- slugifier -------------------------------------------------------------
def test_slugifier_simple():
    assert slugifier("Mon Premier Article") == "mon-premier-article"


def test_slugifier_ponctuation_et_espaces():
    assert slugifier("  Bonjour,   le monde !! ") == "bonjour-le-monde"
    assert slugifier("C++ & Python") == "c-python"


def test_slugifier_accents():
    assert slugifier("Été 2026 : bilan") == "ete-2026-bilan"
    assert slugifier("Ça, c'est noël") == "ca-c-est-noel"


def test_slugifier_vide():
    assert slugifier("") == "sans-titre"
    assert slugifier("?!") == "sans-titre"


# --- email_valide / valider_contact ------------------------------------------
def test_email_valide_oui():
    assert email_valide("a@b.fr")
    assert email_valide("camille.martin@etu.exemple.fr")


def test_email_valide_non():
    for adresse in ["", "camille", "@exemple.fr", "camille@exemple", "camille@@exemple.fr",
                    "camille@.fr", "camille@exemple.", "camille martin@exemple.fr"]:
        assert not email_valide(adresse), f"{adresse!r} ne devrait pas être valide"


FORMULAIRE_OK = {"nom": "Bob", "email": "bob@exemple.fr", "sujet": "", "message": "Bonjour, ça va ?"}


def test_valider_contact_correct():
    assert valider_contact(FORMULAIRE_OK) == {}


def test_valider_contact_sujet_absent():
    formulaire = dict(FORMULAIRE_OK)
    del formulaire["sujet"]
    assert valider_contact(formulaire) == {}


def test_valider_contact_tout_faux():
    erreurs = valider_contact({"nom": " B ", "email": "bob", "sujet": "x" * 151,
                               "message": "Court"})
    assert erreurs == {
        "nom": "Indiquez votre nom (2 à 100 caractères).",
        "email": "Adresse électronique invalide.",
        "sujet": "Le sujet ne doit pas dépasser 150 caractères.",
        "message": "Le message doit faire entre 10 et 2000 caractères.",
    }


def test_valider_contact_espaces_ignores():
    formulaire = dict(FORMULAIRE_OK, message="   court      ")
    assert list(valider_contact(formulaire)) == ["message"]


def test_valider_contact_limites():
    assert valider_contact(dict(FORMULAIRE_OK, nom="x" * 100, message="m" * 2000)) == {}
    assert "nom" in valider_contact(dict(FORMULAIRE_OK, nom="x" * 101))
    assert "message" in valider_contact(dict(FORMULAIRE_OK, message="m" * 2001))


# --- formater_periode / duree ------------------------------------------------
def test_formater_periode():
    assert formater_periode("2023-09", "2025-06") == "sept. 2023 – juin 2025"
    assert formater_periode("2024-01", "2024-12") == "janv. 2024 – déc. 2024"


def test_formater_periode_en_cours():
    assert formater_periode("2025-09", None) == "sept. 2025 – aujourd'hui"


def test_duree_mois():
    assert duree("2025-01", "2025-01", "2026-11") == "1 mois"
    assert duree("2024-06", "2024-08", "2026-11") == "3 mois"


def test_duree_ans():
    assert duree("2024-09", "2025-08", "2026-11") == "1 an"
    assert duree("2021-09", "2024-08", "2026-11") == "3 ans"
    assert duree("2024-11", "2025-12", "2026-11") == "1 an 2 mois"


def test_duree_en_cours():
    assert duree("2023-09", None, "2026-11") == "3 ans 3 mois"


# --- decouper_paragraphes / extraire_resume -----------------------------------
def test_decouper_paragraphes():
    texte = "Bonjour\ntout le monde.\n\n\nSecond.\n"
    assert decouper_paragraphes(texte) == ["Bonjour tout le monde.", "Second."]


def test_decouper_paragraphes_lignes_blanches():
    assert decouper_paragraphes("  \n\nUn\n   \nDeux  \n  trois\n\n") == ["Un", "Deux trois"]
    assert decouper_paragraphes("") == []


def test_extraire_resume_court():
    assert extraire_resume("Un texte   court.\n") == "Un texte court."


def test_extraire_resume_coupe_entre_les_mots():
    assert extraire_resume("un deux trois quatre", 12) == "un deux…"
    assert extraire_resume("un deux trois quatre", 13) == "un deux trois…"
    assert extraire_resume("mot " * 100) == ("mot " * 40).strip() + "…"


# --- paginer --------------------------------------------------------------------
def test_paginer_milieu():
    assert paginer(12, 2, 5) == {"page": 2, "nb_pages": 3, "decalage": 5,
                                 "precedente": 1, "suivante": 3}


def test_paginer_bords():
    assert paginer(12, 1, 5)["precedente"] is None
    assert paginer(12, 3, 5)["suivante"] is None
    assert paginer(10, 2, 5)["nb_pages"] == 2


def test_paginer_page_hors_limites():
    assert paginer(12, 99, 5)["page"] == 3
    assert paginer(12, -4, 5)["page"] == 1
    assert paginer(12, 99, 5)["decalage"] == 10


def test_paginer_liste_vide():
    assert paginer(0, 1, 5) == {"page": 1, "nb_pages": 1, "decalage": 0,
                                "precedente": None, "suivante": None}
