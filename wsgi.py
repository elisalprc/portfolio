"""Point d'entrée pour l'hébergeur (étape 7 — déploiement).

Sur votre machine, on lance le site avec  flask --app app run --debug
(serveur de développement). Un hébergeur, lui, utilise un serveur « WSGI »
qui cherche une variable nommée `application` : la voici.
"""
from app import create_app

application = create_app()
