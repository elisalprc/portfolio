"""Configuration du site. Fichier fourni : vous n'avez rien à y écrire.

Les valeurs sensibles ne sont JAMAIS écrites dans le code (qui finit sur
GitHub) :
  - la clé secrète, qui signe le cookie de session, est lue dans la
    variable d'environnement SECRET_KEY ; à défaut, elle est tirée au
    hasard une fois pour toutes et rangée dans instance/cle_secrete.txt ;
  - le mot de passe administrateur n'est stocké que sous forme de
    « hachage » dans la base (commande flask creer-admin).
Le dossier instance/ est exclu de git (voir .gitignore).
"""
import os
import secrets
from pathlib import Path

DOSSIER_PROJET = Path(__file__).resolve().parent
DOSSIER_INSTANCE = DOSSIER_PROJET / "instance"


def cle_secrete():
    if os.environ.get("SECRET_KEY"):
        return os.environ["SECRET_KEY"]
    fichier = DOSSIER_INSTANCE / "cle_secrete.txt"
    if not fichier.exists():
        DOSSIER_INSTANCE.mkdir(exist_ok=True)
        fichier.write_text(secrets.token_hex(32), encoding="utf-8")
    return fichier.read_text(encoding="utf-8").strip()


class Config:
    SECRET_KEY = cle_secrete()
    BASE_DE_DONNEES = os.environ.get(
        "PORTFOLIO_BDD", str(DOSSIER_INSTANCE / "portfolio.db"))
    ARTICLES_PAR_PAGE = 5
    # Le cookie de session n'est pas envoyé par un formulaire posté depuis
    # un autre site : protection simple contre les attaques CSRF.
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
