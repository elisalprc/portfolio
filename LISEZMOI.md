# Mon portfolio — kit de départ

Le sujet complet est dans `Projet_Portfolio.pdf`. Démarrage rapide, dans un
terminal ouvert **dans ce dossier** (Python 3.10 ou plus récent) :

```
python -m venv .venv
.venv\Scripts\activate              (macOS, Linux : source .venv/bin/activate)
pip install -r requirements.txt
flask --app app init-db
python remplir.py
flask --app app creer-admin
flask --app app run --debug         puis ouvrir http://127.0.0.1:5000
```

Dans un second terminal :

```
python -m pytest
```

Objectif : **88 passed**. Les fonctions à écrire contiennent
`raise AFaire(...)` ; cherchez « À FAIRE » dans `outils.py`, `schema.sql`,
`db.py`, `pages.py`, `admin.py` et `api.py`.

Ne modifiez pas `tests/`, `a_faire.py` ni `app.py`. Le dossier `instance/`
(base de données, clé secrète) ne doit jamais être publié : il est exclu
par `.gitignore`.
