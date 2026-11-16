"""Étape 6 — L'API JSON (adresse /api/...).

Les mêmes données que les pages, mais en JSON : un autre programme (une
application mobile, un script Python avec requests, le site d'un ami…)
peut les lire sans analyser du HTML. jsonify(objet) transforme un dict ou
une liste Python en réponse JSON.

Essayez dans le navigateur :  http://127.0.0.1:5000/api/profil
ou en Python :
    import requests
    print(requests.get("http://127.0.0.1:5000/api/projets").json())

La première route est écrite : elle sert de modèle.
"""
from flask import Blueprint, jsonify, request, url_for

import db
from a_faire import AFaire
from outils import extraire_resume

api = Blueprint("api", __name__)


@api.route("/profil")
def profil():
    le_profil = db.lire_profil()
    if le_profil is None:
        return jsonify({"erreur": "profil introuvable"}), 404
    return jsonify(le_profil)


@api.route("/projets")
def projets():
    """La liste des projets (dict complets, technologies en liste), filtrée
    par ?techno=... comme la page /projets."""
    # À FAIRE (étape 6)
    raise AFaire(6, "projets")


@api.route("/projets/<slug>")
def projet(slug):
    """Un projet ; inconnu → {"erreur": "projet introuvable"} avec le code 404."""
    # À FAIRE (étape 6)
    raise AFaire(6, "projet")


@api.route("/articles")
def articles():
    """Les articles PUBLIÉS, sans leur contenu complet. Chaque élément :
        {"titre": ..., "slug": ..., "cree_le": ...,
         "resume": extraire_resume(contenu),
         "url": l'adresse COMPLÈTE de la page de l'article}
    """
    # À FAIRE (étape 6)
    # Indice : url_for("pages.article", slug=..., _external=True) donne "http://.../blog/le-slug".
    raise AFaire(6, "articles")


@api.route("/cv")
def cv():
    """Le CV complet : {"profil": ..., "experiences": [...],
    "formations": [...], "competences": {...}}."""
    # À FAIRE (étape 6)
    raise AFaire(6, "cv")
