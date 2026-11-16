"""Point d'entrée du site. Fichier fourni : vous n'avez rien à y écrire.

    flask --app app init-db           crée les tables (EFFACE tout)
    python remplir.py                 met VOS données dans la base
    flask --app app creer-admin       crée le compte administrateur
    flask --app app run --debug       lance le site sur http://127.0.0.1:5000

create_app() fabrique l'application : elle charge la configuration,
branche la base de données, enregistre les trois groupes de routes
(« blueprints ») et quelques filtres utilisés par les gabarits HTML.
"""
from datetime import date

from flask import Flask, render_template

import db
from a_faire import AFaire
from config import Config
from outils import decouper_paragraphes, duree, extraire_resume, formater_periode


def create_app(config_test=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_test:
        app.config.update(config_test)

    db.init_app(app)

    # Les trois groupes de routes : un fichier chacun.
    from pages import pages
    from admin import admin
    from api import api
    app.register_blueprint(pages)
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(api, url_prefix="/api")

    # Filtres des gabarits :  {{ exp.debut | periode(exp.fin) }}
    @app.template_filter("periode")
    def filtre_periode(debut, fin):
        return formater_periode(debut, fin)

    @app.template_filter("duree")
    def filtre_duree(debut, fin):
        return duree(debut, fin, date.today().strftime("%Y-%m"))

    @app.template_filter("paragraphes")
    def filtre_paragraphes(texte):
        return decouper_paragraphes(texte)

    @app.template_filter("resume")
    def filtre_resume(texte, longueur=160):
        return extraire_resume(texte, longueur)

    # Le profil est utile sur TOUTES les pages (en-tête, pied de page).
    @app.context_processor
    def injecter_profil():
        try:
            return {"moi": db.lire_profil()}
        except Exception:          # base pas encore créée
            return {"moi": None}

    @app.errorhandler(404)
    def page_introuvable(erreur):
        return render_template("404.html"), 404

    # Pendant le développement, une fonction pas encore écrite affiche une
    # page qui le dit (et non une erreur incompréhensible). Pendant les
    # tests, l'exception remonte jusqu'à pytest, qui compte « À FAIRE ».
    if not app.testing:
        @app.errorhandler(AFaire)
        def fonction_a_faire(erreur):
            return render_template("a_faire.html", erreur=erreur), 501

    return app
