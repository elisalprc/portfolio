"""Étape 5 — L'espace d'administration (adresse /admin/...).

Vous seul(e) devez pouvoir écrire un article ou lire vos messages.
Principe :
  1. /admin/connexion vérifie l'identifiant et le mot de passe ;
  2. s'ils sont bons, on écrit session["admin"] = identifiant. Flask range
     la session dans un cookie SIGNÉ avec la clé secrète : le visiteur peut
     le lire mais pas le falsifier ;
  3. chaque route protégée porte le décorateur @login_requis (fourni), qui
     renvoie vers /admin/connexion si session ne contient pas "admin".

Les routes qui MODIFIENT quelque chose n'acceptent que POST : un simple
lien (GET) ne doit jamais pouvoir supprimer un article.
"""
from functools import wraps

from flask import (Blueprint, abort, flash, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash

import db
from a_faire import AFaire

admin = Blueprint("admin", __name__)


# --------------------------------------------------------------------------
# Fourni
# --------------------------------------------------------------------------
def login_requis(vue):
    """Décorateur : la route n'est accessible qu'une fois connecté.

    Un décorateur est une fonction qui reçoit une fonction et en renvoie
    une autre, qui « l'enveloppe ». Écrire @login_requis au-dessus d'une
    route revient à écrire  route = login_requis(route).
    """
    @wraps(vue)
    def vue_protegee(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.connexion", suivant=request.path))
        return vue(*args, **kwargs)
    return vue_protegee


@admin.route("/deconnexion", methods=["POST"])
def deconnexion():
    session.clear()
    flash("Vous êtes déconnecté(e).", "info")
    return redirect(url_for("pages.accueil"))


@admin.route("/messages")
@login_requis
def messages():
    return render_template("admin/messages.html", messages=db.lister_messages())


# --------------------------------------------------------------------------
# À écrire
# --------------------------------------------------------------------------
def verifier_admin(identifiant, mot_de_passe):
    """True si le couple identifiant / mot de passe est celui de la table
    admin. Le mot de passe stocké est un HACHAGE : on ne le compare pas
    avec ==, on appelle check_password_hash(hachage, mot_de_passe)."""
    # À FAIRE (étape 5)
    # Indice : db.requete(...) renvoie None si la table admin est vide : renvoyez alors False.
    raise AFaire(5, "verifier_admin")


@admin.route("/connexion", methods=["GET", "POST"])
def connexion():
    """Gabarit admin/connexion.html (aucune variable).

    POST, champs "identifiant" et "mot_de_passe" :
      - corrects : session["admin"] = identifiant, flash("Bienvenue !", "succes"),
        puis redirect vers l'adresse request.args["suivant"] si elle est donnée
        ET commence par "/admin/", sinon vers le tableau de bord ;
      - incorrects : flash("Identifiant ou mot de passe incorrect.", "erreur")
        et le formulaire à nouveau, avec le code 401.
    """
    # À FAIRE (étape 5)
    # Indice : Vérifier que "suivant" commence par "/admin/" empêche un lien piégé de vous
    #          renvoyer, après connexion, vers un autre site (« open redirect »).
    raise AFaire(5, "connexion")


@admin.route("/")
@login_requis
def tableau():
    """Gabarit admin/tableau.html ; variables : nb_publies, nb_brouillons,
    nb_non_lus (trois entiers)."""
    # À FAIRE (étape 5)
    # Indice : Brouillons = tous les articles moins les publiés.
    raise AFaire(5, "tableau")


@admin.route("/articles")
@login_requis
def articles():
    """Gabarit admin/articles.html ; variable : articles (TOUS, brouillons compris)."""
    # À FAIRE (étape 5)
    raise AFaire(5, "articles")


def lire_formulaire_article(formulaire):
    """Lit le formulaire d'article ; renvoie (valeurs, erreurs).

    valeurs = {"titre": ..., "contenu": ... (sans espaces autour),
               "publie": True si la case "publie" est cochée}
    erreurs : "titre" → "Le titre est obligatoire." si vide ;
              "contenu" → "Le contenu est obligatoire." si vide.
    Une case à cocher non cochée n'est PAS envoyée par le navigateur.
    """
    # À FAIRE (étape 5)
    raise AFaire(5, "lire_formulaire_article")


@admin.route("/articles/nouveau", methods=["GET", "POST"])
@login_requis
def nouvel_article():
    """Gabarit admin/article_form.html ; variables : valeurs, erreurs,
    article (None ici : c'est une création).

    GET : formulaire vide. POST : lire_formulaire_article ; erreurs → même
    gabarit, code 400 ; sinon creer_article, flash("Article créé.", "succes"),
    redirect vers la liste des articles d'administration.
    """
    # À FAIRE (étape 5)
    raise AFaire(5, "nouvel_article")


@admin.route("/articles/<int:id_article>/modifier", methods=["GET", "POST"])
@login_requis
def modifier_article(id_article):
    """Même gabarit que nouvel_article, avec article = l'article modifié.
    Article inconnu → 404. GET : le formulaire pré-rempli (valeurs = titre,
    contenu, publie de l'article). POST : comme nouvel_article, mais
    modifier_article et flash("Article modifié.", "succes")."""
    # À FAIRE (étape 5)
    # Indice : <int:id_article> dans l'URL : Flask convertit en entier et donne 404 si ce n'en est pas un.
    raise AFaire(5, "modifier_article")


@admin.route("/articles/<int:id_article>/supprimer", methods=["POST"])
@login_requis
def supprimer_article(id_article):
    """POST seulement. Article inconnu → 404 ; sinon supprimer_article,
    flash("Article supprimé.", "succes"), redirect vers la liste."""
    # À FAIRE (étape 5)
    raise AFaire(5, "supprimer_article")


@admin.route("/messages/<int:id_message>/lu", methods=["POST"])
@login_requis
def message_lu(id_message):
    """POST seulement. Message inconnu → 404 ; sinon marquer_lu puis
    redirect vers la liste des messages (pas de flash)."""
    # À FAIRE (étape 5)
    raise AFaire(5, "message_lu")
