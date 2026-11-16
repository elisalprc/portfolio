"""Étape 6 — API JSON (api.py)."""


def json(client, url, code=200):
    reponse = client.get(url)
    assert reponse.status_code == code, f"{url} : code {reponse.status_code} au lieu de {code}"
    assert reponse.is_json, f"{url} doit renvoyer du JSON (jsonify)"
    return reponse.get_json()


def test_profil_fourni(client):
    assert json(client, "/api/profil")["nom"] == "Alex Dupont"


def test_projets(client):
    projets = json(client, "/api/projets")
    assert [p["slug"] for p in projets] == ["projet-trois", "projet-un", "projet-deux",
                                           "projet-quatre"]
    assert projets[1]["technologies"] == ["Python", "Flask"]


def test_projets_filtre(client):
    assert [p["slug"] for p in json(client, "/api/projets?techno=flask")] == \
        ["projet-un", "projet-quatre"]


def test_projet(client):
    assert json(client, "/api/projets/projet-deux")["titre"] == "Projet Deux"
    assert json(client, "/api/projets/inconnu", 404) == {"erreur": "projet introuvable"}


def test_articles(client):
    articles = json(client, "/api/articles")
    assert len(articles) == 7
    premier = articles[0]
    assert set(premier) == {"titre", "slug", "cree_le", "resume", "url"}
    assert premier["slug"] == "article-7"
    assert premier["url"] == "http://portfolio.test/blog/article-7"
    assert premier["resume"] == "Contenu de l'article 7. Second paragraphe."


def test_cv(client):
    cv = json(client, "/api/cv")
    assert set(cv) == {"profil", "experiences", "formations", "competences"}
    assert cv["profil"]["nom"] == "Alex Dupont"
    assert [e["titre"] for e in cv["formations"]] == ["Cycle ingénieur", "Baccalauréat"]
    assert cv["competences"]["Outils"] == [{"nom": "Git", "niveau": 3}]
