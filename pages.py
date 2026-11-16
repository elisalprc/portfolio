"""Étapes 3 et 4 — Les pages publiques du portfolio.

Une route = une URL + une fonction qui RENVOIE la réponse. Ici, presque
toujours : render_template("gabarit.html", variable=valeur, ...).
Le gabarit (dossier templates/) est fourni : il attend des variables
précises, listées en tête de chaque fichier HTML et dans le sujet.

La route accueil() est écrite : elle sert de modèle.
"""
from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)

import db
from a_faire import AFaire
from outils import paginer, temps_de_lecture, valider_contact

pages = Blueprint("pages", __name__)


@pages.route("/")
def accueil():
    return render_template(
        "accueil.html",
        projets=db.lister_projets(limite=3),
        articles=db.lister_articles(limite=3),
    )


@pages.route("/cv")
def cv():
    """Gabarit cv.html ; variables : experiences (catégorie "pro"),
    formations (catégorie "formation"), competences (le dict de
    competences_par_categorie)."""
    # À FAIRE (étape 3)
    raise AFaire(3, "cv")


@pages.route("/projets")
def projets():
    """Gabarit projets.html ; variables : projets, technologies (toutes,
    pour les boutons de filtre), techno (le filtre choisi, ou None).
    Le filtre arrive dans l'URL :  /projets?techno=Flask"""
    # À FAIRE (étape 3)
    # Indice : request.args.get("techno") renvoie la valeur, ou None si elle est absente.
    raise AFaire(3, "projets")


@pages.route("/projets/<slug>")
def projet(slug):
    """Gabarit projet.html ; variable : projet. Projet inconnu → 404."""
    # À FAIRE (étape 3)
    # Indice : abort(404) interrompt la fonction et renvoie la page « introuvable ».
    raise AFaire(3, "projet")


@pages.route("/blog")
def blog():
    """Gabarit blog.html ; variables : articles (ceux de la page), pagination
    (le dict de paginer). Seuls les articles PUBLIÉS apparaissent ; le nombre
    par page est current_app.config["ARTICLES_PAR_PAGE"]. La page arrive dans
    l'URL :  /blog?page=2  (page 1 si absente ou pas un nombre)."""
    # À FAIRE (étape 3)
    # Indice : request.args.get("page", 1, type=int) convertit en entier, et renvoie 1 en cas d'échec.
    #          Ordre : compter_articles() → paginer(...) → lister_articles(limite=..., decalage=...).
    raise AFaire(3, "blog")


@pages.route("/blog/<slug>")
def article(slug):
    """Gabarit article.html ; variables : article, minutes (temps de lecture).
    Article inconnu OU brouillon → 404."""
    # À FAIRE (étape 3)
    raise AFaire(3, "article")


@pages.route("/contact", methods=["GET", "POST"])
def contact():
    """Gabarit contact.html ; variables : erreurs (dict) et valeurs (ce que
    le visiteur a déjà tapé, pour ne pas lui faire tout retaper).

    GET  : formulaire vide (erreurs = {}, valeurs = {}).
    POST : valider_contact(request.form)
           - erreurs → on réaffiche le formulaire, avec le code HTTP 400 ;
           - sinon   → ajouter_message(...) avec les valeurs SANS les espaces
             autour, flash("Merci, votre message a bien été envoyé.", "succes"),
             puis redirect vers la page de contact (GET).
    Anti-robot : le formulaire contient un champ caché « site_web » qu'un
    humain ne voit pas. S'il est rempli, faites comme si tout allait bien
    (même flash, même redirection) mais N'ENREGISTREZ RIEN.
    """
    # À FAIRE (étape 4)
    # Indice : Une réponse avec un code : return render_template(...), 400
    #          Le motif « POST → redirect → GET » évite qu'un F5 renvoie le formulaire une 2e fois.
    raise AFaire(4, "contact")
