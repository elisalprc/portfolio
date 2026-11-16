"""Préparation commune à tous les tests. Fichier fourni : ne pas modifier.

Chaque test reçoit une base NEUVE, dans un dossier temporaire, remplie avec
les données ci-dessous (et non avec les vôtres : vos données de remplir.py
ne sont jamais touchées par les tests).

    python -m pytest                    tous les tests
    python -m pytest tests/test_etape1_outils.py
    python -m pytest -k slugifier       seulement les tests dont le nom contient « slugifier »
    python -m pytest -x                 s'arrêter au premier échec
"""
import sqlite3
from collections import defaultdict

import pytest

import db
from a_faire import AFaire
from app import create_app

IDENTIFIANT_TEST = "admin"
MOT_DE_PASSE_TEST = "motdepasse-test"

PROFIL = (1, "Alex Dupont", "Étudiant ingénieur", "Première ligne.\n\nDeuxième paragraphe.",
          "alex@exemple.fr", "Strasbourg", "https://github.com/alex", None)

EXPERIENCES = [
    ("pro", "Stage été", "Entreprise A", "Colmar", "2024-06", "2024-08", "Un stage."),
    ("pro", "Job étudiant", "Entreprise B", None, "2025-07", None, ""),
    ("formation", "Cycle ingénieur", "INSA", "Strasbourg", "2024-09", None, ""),
    ("formation", "Baccalauréat", "Lycée", "Metz", "2021-09", "2024-06", "Mention bien."),
]

COMPETENCES = [
    ("Python", "Langages", 4), ("Java", "Langages", 3), ("C", "Langages", 3),
    ("Git", "Outils", 3), ("Anglais", "Langues", 4),
]

# (titre, slug, resume, description, technologies, lien_code, lien_demo, date)
PROJETS = [
    ("Projet Un", "projet-un", "Résumé un.", "Description un.\n\nSuite.", "Python, Flask",
     "https://github.com/alex/un", None, "2026-01"),
    ("Projet Deux", "projet-deux", "Résumé deux.", "Description deux.", "python, Pandas",
     None, None, "2025-06"),
    ("Projet Trois", "projet-trois", "Résumé trois.", "Description trois.", "C",
     None, None, "2026-01"),
    ("Projet Quatre", "projet-quatre", "Résumé quatre.", "Description quatre.",
     "Flask , SQLite,", None, "https://demo.exemple.fr", "2024-01"),
]

# 7 articles publiés (a1 le plus ancien ... a7 le plus récent) + 1 brouillon
ARTICLES = [(f"Article {i}", f"article-{i}", f"Contenu de l'article {i}.\n\nSecond paragraphe.",
             1, f"2026-0{i}-15 10:00") for i in range(1, 8)]
ARTICLES.append(("Brouillon secret", "brouillon-secret", "Pas encore publié.", 0,
                 "2026-09-01 10:00"))

MESSAGES = [
    ("Bob", "bob@exemple.fr", "Bonjour", "Un premier message.", "2026-10-01 08:00", 1),
    ("Eve", "eve@exemple.fr", None, "Un second message.", "2026-10-02 09:00", 0),
]


def remplir_base_de_test():
    bdd = db.connexion()
    bdd.execute("INSERT INTO profil VALUES (?, ?, ?, ?, ?, ?, ?, ?)", PROFIL)
    bdd.executemany("INSERT INTO experiences (categorie, titre, organisation, lieu, debut, fin, "
                    "description) VALUES (?, ?, ?, ?, ?, ?, ?)", EXPERIENCES)
    bdd.executemany("INSERT INTO competences (nom, categorie, niveau) VALUES (?, ?, ?)",
                    COMPETENCES)
    bdd.executemany("INSERT INTO projets (titre, slug, resume, description, technologies, "
                    "lien_code, lien_demo, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", PROJETS)
    try:
        bdd.executemany("INSERT INTO articles (titre, slug, contenu, publie, cree_le) "
                        "VALUES (?, ?, ?, ?, ?)", ARTICLES)
        bdd.executemany("INSERT INTO messages (nom, email, sujet, contenu, recu_le, lu) "
                        "VALUES (?, ?, ?, ?, ?, ?)", MESSAGES)
    except sqlite3.OperationalError as erreur:
        if "no such table" in str(erreur):     # tables pas encore écrites
            raise AFaire(2, "schema.sql") from erreur
        raise
    bdd.commit()
    db.creer_admin(IDENTIFIANT_TEST, MOT_DE_PASSE_TEST)


@pytest.fixture
def app(tmp_path):
    application = create_app({
        "TESTING": True,
        "SECRET_KEY": "cle-de-test",
        "BASE_DE_DONNEES": str(tmp_path / "test.db"),
        "SERVER_NAME": "portfolio.test",
    })
    with application.app_context():
        db.init_db()
        remplir_base_de_test()
        yield application


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def client_admin(app):
    """Un client déjà connecté en administrateur (sans passer par la page de
    connexion : les tests de l'étape 5 ne dépendent pas tous d'elle)."""
    c = app.test_client()
    with c.session_transaction() as session:
        session["admin"] = IDENTIFIANT_TEST
    return c


# --------------------------------------------------------------------------
# « À FAIRE » plutôt que « ÉCHEC », et bilan par étape
# --------------------------------------------------------------------------
_bilan = defaultdict(lambda: {"reussis": 0, "a_faire": 0, "echecs": 0})


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultat = yield
    rapport = resultat.get_result()
    if call.excinfo is not None and call.excinfo.errisinstance(AFaire):
        rapport.outcome = "skipped"
        rapport.longrepr = (str(item.path), item.location[1] or 0,
                            f"[À FAIRE] {call.excinfo.value}")
        rapport.a_faire = True


def pytest_runtest_logreport(report):
    etape = report.nodeid.split("test_etape")[1][0] if "test_etape" in report.nodeid else "?"
    if getattr(report, "a_faire", False):
        _bilan[etape]["a_faire"] += 1
    elif report.when == "call" and report.passed:
        _bilan[etape]["reussis"] += 1
    elif report.failed:
        _bilan[etape]["echecs"] += 1


def pytest_terminal_summary(terminalreporter):
    if not _bilan:
        return
    noms = {"1": "outils", "2": "base de données", "3": "pages publiques",
            "4": "contact", "5": "administration", "6": "API JSON"}
    ecrire = terminalreporter.write_line
    ecrire("")
    ecrire("Bilan par étape                réussis   à faire   échecs")
    for etape in sorted(_bilan):
        b = _bilan[etape]
        ecrire(f"  Étape {etape} — {noms.get(etape, ''):<20}{b['reussis']:>7}"
               f"{b['a_faire']:>10}{b['echecs']:>9}")
    ecrire("  (« à faire » : la fonction contient encore raise AFaire)")
