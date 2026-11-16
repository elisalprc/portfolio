"""Remplit la base avec le contenu du portfolio : À PERSONNALISER.

Les données ci-dessous sont celles d'une personne FICTIVE, Camille Martin.
Remplacez-les par les vôtres (votre CV, vos vrais projets), puis :

    flask --app app init-db       # recrée des tables vides
    python remplir.py             # les remplit

Ce script efface le contenu des tables avant de les remplir : vous pouvez
le relancer autant de fois que vous voulez. Il n'efface PAS le compte
administrateur.

Fichier fourni, mais c'est VOTRE contenu : modifiez-le librement.
"""
import sqlite3

from config import Config

PROFIL = {
    "nom": "Camille Martin",
    "titre": "Étudiante ingénieure — développement logiciel",
    "bio": "Je termine ma deuxième année d'école d'ingénieurs. J'aime les "
           "programmes simples qui rendent service, et je cherche un stage "
           "de quatre mois en développement Python à partir de juin.",
    "email": "camille.martin@exemple.fr",
    "ville": "Strasbourg",
    "github": "https://github.com/exemple",
    "linkedin": None,
}

# (categorie, titre, organisation, lieu, debut, fin, description)
EXPERIENCES = [
    ("pro", "Stage d'été — assistante informatique", "Mairie de Sélestat",
     "Sélestat", "2025-07", "2025-08",
     "Inventaire du parc informatique, script Python de suivi des prêts de matériel."),
    ("pro", "Animatrice de colonie de vacances", "Ligue de l'enseignement",
     "Vosges", "2024-07", "2024-08", "Encadrement d'enfants de 8 à 12 ans."),
    ("formation", "Cycle ingénieur", "INSA Strasbourg", "Strasbourg",
     "2024-09", None, "Cours de programmation Python, C et C++."),
    ("formation", "Baccalauréat général", "Lycée Kléber", "Strasbourg",
     "2021-09", "2024-06", "Spécialités mathématiques et NSI, mention bien."),
]

# (nom, categorie, niveau de 1 à 5)
COMPETENCES = [
    ("Python", "Langages", 4), ("C", "Langages", 3), ("SQL", "Langages", 2),
    ("Git", "Outils", 3), ("Flask", "Outils", 3), ("Linux", "Outils", 2),
    ("Anglais", "Langues", 4), ("Allemand", "Langues", 2),
]

# (titre, slug, resume, description, technologies, lien_code, lien_demo, date)
PROJETS = [
    ("Mon portfolio", "mon-portfolio",
     "Ce site : un portfolio écrit en Python avec Flask et SQLite.",
     "Le site que vous lisez. Le serveur est écrit en Python avec Flask ; "
     "les données sont rangées dans une base SQLite.\n\n"
     "Il comporte un blog, un formulaire de contact, un espace "
     "d'administration protégé par mot de passe et une API JSON.",
     "Python, Flask, SQLite, HTML", "https://github.com/exemple/portfolio", None, "2026-12"),
    ("Gestion d'une bibliothèque", "gestion-bibliotheque",
     "Un programme en console pour gérer les prêts de livres d'une association.",
     "Les livres et les adhérents sont enregistrés dans des fichiers CSV.\n\n"
     "Le programme signale les retards et produit des statistiques.",
     "Python, CSV", None, None, "2026-03"),
    ("Analyse des ventes d'une boulangerie", "ventes-boulangerie",
     "Tableaux et graphiques des ventes sur un an, avec Pandas et Matplotlib.",
     "Projet du module Python : nettoyage des données, ventes par jour de la "
     "semaine et par saison, prévision simple.",
     "Python, Pandas, Matplotlib", None, None, "2026-05"),
    ("Jeu du serpent", "jeu-serpent",
     "Le moteur d'un jeu du serpent en C, avec une interface graphique raylib.",
     "Projet du module C : grille allouée dynamiquement, scores sauvegardés "
     "dans un fichier.",
     "C, raylib", None, None, "2025-12"),
]

# (titre, slug, contenu, publie, cree_le)
ARTICLES = [
    ("Pourquoi un portfolio ?", "pourquoi-un-portfolio",
     "Un CV tient sur une page. Un portfolio montre ce que l'on sait faire.\n\n"
     "Dans cet article, j'explique comment j'ai conçu ce site, et pourquoi "
     "j'ai choisi d'écrire moi-même le serveur plutôt que d'utiliser un "
     "générateur de site tout prêt.", 1, "2026-10-20 18:30"),
    ("Ce que j'ai appris sur SQL", "appris-sur-sql",
     "SELECT, INSERT, UPDATE, DELETE : quatre mots suffisent pour commencer.\n\n"
     "Le plus important : ne jamais coller une valeur dans une requête, "
     "toujours utiliser des paramètres.", 1, "2026-10-27 09:15"),
    ("Brouillon : mon stage", "brouillon-stage",
     "Article pas encore terminé.", 0, "2026-11-02 10:00"),
]


def remplir(chemin_bdd):
    bdd = sqlite3.connect(chemin_bdd)
    for table in ("profil", "experiences", "competences", "projets"):
        bdd.execute(f"DELETE FROM {table}")
    bdd.execute(
        "INSERT INTO profil (id, nom, titre, bio, email, ville, github, linkedin) "
        "VALUES (1, :nom, :titre, :bio, :email, :ville, :github, :linkedin)", PROFIL)
    bdd.executemany(
        "INSERT INTO experiences (categorie, titre, organisation, lieu, debut, fin, description) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)", EXPERIENCES)
    bdd.executemany("INSERT INTO competences (nom, categorie, niveau) VALUES (?, ?, ?)",
                    COMPETENCES)
    bdd.executemany(
        "INSERT INTO projets (titre, slug, resume, description, technologies, lien_code, "
        "lien_demo, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", PROJETS)
    try:
        bdd.execute("DELETE FROM articles")
        bdd.executemany(
            "INSERT INTO articles (titre, slug, contenu, publie, cree_le) VALUES (?, ?, ?, ?, ?)",
            ARTICLES)
    except sqlite3.OperationalError:
        print("Table articles absente (étape 2, schema.sql) : articles non insérés.")
    bdd.commit()
    bdd.close()


if __name__ == "__main__":
    remplir(Config.BASE_DE_DONNEES)
    print(f"Base remplie : {Config.BASE_DE_DONNEES}")
