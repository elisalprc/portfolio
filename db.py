"""Étape 2 — Accès à la base de données SQLite.

Tout le SQL du site est dans ce fichier, et nulle part ailleurs : les
routes (pages.py, admin.py, api.py) appellent ces fonctions, sans jamais
écrire de requête elles-mêmes.

RÈGLE DE SÉCURITÉ, sans exception : une valeur venue de l'extérieur
(formulaire, URL) n'est JAMAIS collée dans le texte SQL avec + ou un
f-string. On écrit un « ? » et on passe la valeur à part :

    requete("SELECT * FROM projets WHERE slug = ?", (slug,), une=True)

sinon, n'importe quel visiteur peut faire exécuter son propre SQL
(« injection SQL »).

Chaque fonction RENVOIE des dict (ou une liste de dict), jamais des objets
sqlite3 : les pages et l'API JSON les utilisent directement.
"""
import sqlite3
from datetime import datetime

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash

from a_faire import AFaire
from outils import liste_technologies, slugifier


# --------------------------------------------------------------------------
# Fourni : connexion, création des tables, commandes flask
# --------------------------------------------------------------------------
def connexion():
    """La connexion à la base, ouverte une fois par requête HTTP (dans g)."""
    if "bdd" not in g:
        g.bdd = sqlite3.connect(current_app.config["BASE_DE_DONNEES"])
        g.bdd.row_factory = sqlite3.Row      # lignes lisibles par nom de colonne
        g.bdd.execute("PRAGMA foreign_keys = ON")
    return g.bdd


def fermer_connexion(exception=None):
    bdd = g.pop("bdd", None)
    if bdd is not None:
        bdd.close()


def requete(sql, parametres=(), une=False):
    """Exécute un SELECT et renvoie une liste de dict (ou UN dict / None
    si une=True)."""
    curseur = connexion().execute(sql, parametres)
    lignes = curseur.fetchall()
    curseur.close()
    if une:
        return dict(lignes[0]) if lignes else None
    return [dict(ligne) for ligne in lignes]


def executer(sql, parametres=()):
    """Exécute un INSERT / UPDATE / DELETE, l'enregistre (commit), et
    renvoie le curseur : curseur.lastrowid est l'id de la ligne insérée,
    curseur.rowcount le nombre de lignes modifiées."""
    bdd = connexion()
    curseur = bdd.execute(sql, parametres)
    bdd.commit()
    return curseur


def maintenant():
    """Date et heure actuelles, au format « AAAA-MM-JJ HH:MM »."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def init_db():
    with current_app.open_resource("schema.sql") as fichier:
        connexion().executescript(fichier.read().decode("utf-8"))


def creer_admin(identifiant, mot_de_passe):
    executer("DELETE FROM admin")
    executer("INSERT INTO admin (id, identifiant, mot_de_passe_hash) VALUES (1, ?, ?)",
             (identifiant, generate_password_hash(mot_de_passe)))


@click.command("init-db")
def commande_init_db():
    """Efface et recrée toutes les tables."""
    init_db()
    click.echo("Base de données initialisée.")


@click.command("creer-admin")
@click.option("--identifiant", prompt=True)
@click.password_option("--mot-de-passe", prompt="Mot de passe")
def commande_creer_admin(identifiant, mot_de_passe):
    """Crée (ou remplace) le compte administrateur."""
    creer_admin(identifiant, mot_de_passe)
    click.echo(f"Administrateur « {identifiant} » enregistré.")


def init_app(app):
    app.teardown_appcontext(fermer_connexion)
    app.cli.add_command(commande_init_db)
    app.cli.add_command(commande_creer_admin)


# --------------------------------------------------------------------------
# Profil, CV — la première fonction est écrite (modèle)
# --------------------------------------------------------------------------
def lire_profil():
    """Le profil (un dict), ou None si la table est vide."""
    return requete("SELECT * FROM profil WHERE id = 1", une=True)


def lister_experiences(categorie):
    """Les expériences de la catégorie "pro" ou "formation", les plus
    récentes d'abord (tri sur la colonne debut, décroissant)."""
    # À FAIRE (étape 2)
    # Indice : Modèle : lire_profil(). Ici « WHERE categorie = ? ORDER BY ... DESC » et (categorie,).
    raise AFaire(2, "lister_experiences")


def competences_par_categorie():
    """Les compétences regroupées par catégorie :

        {"Langages": [{"nom": "Python", "niveau": 4}, ...], "Outils": [...]}

    Les catégories dans l'ordre alphabétique ; dans chaque catégorie, le
    niveau décroissant, puis le nom (ordre alphabétique) à niveau égal.
    Chaque compétence ne contient que les clés "nom" et "niveau".
    """
    # À FAIRE (étape 2)
    # Indice : Une seule requête, triée « ORDER BY categorie, niveau DESC, nom » ; puis une boucle
    #          qui range chaque ligne dans le dict (créez la liste quand la catégorie est nouvelle).
    raise AFaire(2, "competences_par_categorie")


# --------------------------------------------------------------------------
# Projets
# --------------------------------------------------------------------------
def lister_projets(limite=None, techno=None):
    """Les projets, les plus récents d'abord (colonne date décroissante,
    puis id décroissant).

    Dans chaque dict, la clé "technologies" est remplacée par une LISTE
    (utilisez liste_technologies).
    Si `techno` est donnée, on ne garde que les projets qui l'utilisent,
    sans tenir compte des majuscules ("flask" trouve "Flask").
    Si `limite` est donnée, on renvoie au plus `limite` projets (APRÈS le
    filtre).
    """
    # À FAIRE (étape 2)
    # Indice : Le filtre et la limite se font en Python, après la requête :
    #          t.lower() == techno.lower() ; puis projets[:limite].
    raise AFaire(2, "lister_projets")


def projet_par_slug(slug):
    """Le projet dont le slug est donné (technologies en liste), ou None."""
    # À FAIRE (étape 2)
    raise AFaire(2, "projet_par_slug")


def toutes_technologies():
    """Toutes les technologies citées par au moins un projet, sans doublon
    (en ignorant les majuscules : on garde la première écriture rencontrée),
    triées par ordre alphabétique sans tenir compte des majuscules."""
    # À FAIRE (étape 2)
    # Indice : Réutilisez lister_projets(). sorted(liste, key=str.lower) trie sans tenir compte des majuscules.
    raise AFaire(2, "toutes_technologies")


# --------------------------------------------------------------------------
# Articles du blog
# --------------------------------------------------------------------------
def compter_articles(publies_seulement=True):
    """Nombre d'articles (seulement les publiés, ou tous)."""
    # À FAIRE (étape 2)
    # Indice : « SELECT COUNT(*) AS n FROM articles » renvoie une ligne ; ajoutez « WHERE publie = 1 » si besoin.
    raise AFaire(2, "compter_articles")


def lister_articles(publies_seulement=True, limite=None, decalage=0):
    """Les articles, du plus récent au plus ancien (cree_le décroissant,
    puis id décroissant). Avec `limite`, au plus `limite` articles à partir
    du rang `decalage` (pour la pagination)."""
    # À FAIRE (étape 2)
    # Indice : SQL : « ... ORDER BY ... LIMIT ? OFFSET ? ». Construisez la requête morceau par morceau,
    #          comme dans compter_articles, et la liste des paramètres en parallèle.
    raise AFaire(2, "lister_articles")


def article_par_slug(slug, publies_seulement=True):
    """L'article dont le slug est donné, ou None. Un brouillon n'est
    renvoyé que si publies_seulement vaut False."""
    # À FAIRE (étape 2)
    raise AFaire(2, "article_par_slug")


def article_par_id(id_article):
    """L'article (publié ou non) dont l'id est donné, ou None."""
    # À FAIRE (étape 2)
    raise AFaire(2, "article_par_id")


def slug_disponible(titre):
    """Un slug pour `titre` qu'aucun article n'utilise encore :
    slugifier(titre), sinon le même suivi de -2, puis -3, etc."""
    # À FAIRE (étape 2)
    # Indice : Une boucle while : tant qu'une ligne a ce slug, essayez le suivant.
    raise AFaire(2, "slug_disponible")


def creer_article(titre, contenu, publie):
    """Insère un article (cree_le = maintenant(), slug = slug_disponible)
    et renvoie son id. `publie` est un booléen : stockez 1 ou 0."""
    # À FAIRE (étape 2)
    # Indice : executer(...) renvoie un curseur ; curseur.lastrowid est l'id créé.
    raise AFaire(2, "creer_article")


def modifier_article(id_article, titre, contenu, publie):
    """Met à jour titre, contenu, publie et modifie_le (= maintenant()).
    Le slug ne change PAS : les liens déjà partagés restent valides.
    Renvoie True si l'article existait, False sinon."""
    # À FAIRE (étape 2)
    # Indice : curseur.rowcount vaut le nombre de lignes modifiées par l'UPDATE.
    raise AFaire(2, "modifier_article")


def supprimer_article(id_article):
    """Supprime l'article. Renvoie True s'il existait, False sinon."""
    # À FAIRE (étape 2)
    raise AFaire(2, "supprimer_article")


# --------------------------------------------------------------------------
# Messages reçus par le formulaire de contact
# --------------------------------------------------------------------------
def ajouter_message(nom, email, sujet, contenu):
    """Enregistre un message (recu_le = maintenant(), lu = 0) ; renvoie son id."""
    # À FAIRE (étape 2)
    raise AFaire(2, "ajouter_message")


def lister_messages():
    """Tous les messages, les non lus d'abord, puis du plus récent au plus
    ancien (recu_le décroissant, puis id décroissant)."""
    # À FAIRE (étape 2)
    # Indice : « ORDER BY lu, ... » : 0 (non lu) passe avant 1 (lu).
    raise AFaire(2, "lister_messages")


def marquer_lu(id_message):
    """Marque le message comme lu. Renvoie True s'il existait."""
    # À FAIRE (étape 2)
    raise AFaire(2, "marquer_lu")


def compter_messages_non_lus():
    """Nombre de messages dont lu vaut 0."""
    # À FAIRE (étape 2)
    raise AFaire(2, "compter_messages_non_lus")
