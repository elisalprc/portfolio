"""Étape 3 — pages publiques (pages.py). On « visite » le site avec un client
de test : client.get("/cv") renvoie la réponse, sans lancer de serveur."""


def page(client, url, code=200):
    reponse = client.get(url)
    assert reponse.status_code == code, f"{url} : code {reponse.status_code} au lieu de {code}"
    return reponse.get_data(as_text=True)


def test_accueil_fourni(client):
    html = page(client, "/")
    assert "Alex Dupont" in html
    assert "Projet Trois" in html and "Projet Quatre" not in html   # 3 projets au plus
    assert "Article 7" in html and "Article 4" not in html          # 3 articles au plus


def test_cv(client):
    html = page(client, "/cv")
    for texte in ["Job étudiant", "Stage été", "Cycle ingénieur", "Baccalauréat",
                  "juin 2024 – août 2024", "Python", "Langues"]:
        assert texte in html, f"{texte!r} absent de la page /cv"
    assert html.index("Job étudiant") < html.index("Stage été")


def test_projets(client):
    html = page(client, "/projets")
    for titre in ["Projet Un", "Projet Deux", "Projet Trois", "Projet Quatre"]:
        assert titre in html
    assert "SQLite" in html and "Pandas" in html


def test_projets_filtre(client):
    html = page(client, "/projets?techno=flask")
    assert "Projet Un" in html and "Projet Quatre" in html
    assert "Projet Deux" not in html and "Projet Trois" not in html


def test_projets_filtre_vide(client):
    assert "Aucun projet" in page(client, "/projets?techno=Cobol")


def test_projet(client):
    html = page(client, "/projets/projet-un")
    assert "Projet Un" in html and "Description un." in html and "Suite." in html
    assert "https://github.com/alex/un" in html


def test_projet_inconnu(client):
    assert "Page introuvable" in page(client, "/projets/inconnu", 404)


def test_blog_page1(client):
    html = page(client, "/blog")
    for i in (7, 6, 5, 4, 3):
        assert f"Article {i}" in html
    assert "Article 2" not in html
    assert "Brouillon secret" not in html
    assert "Page 1 / 2" in html


def test_blog_page2(client):
    html = page(client, "/blog?page=2")
    assert "Article 2" in html and "Article 1" in html and "Article 3" not in html
    assert "Page 2 / 2" in html


def test_blog_page_incorrecte(client):
    assert "Page 1 / 2" in page(client, "/blog?page=abc")
    assert "Page 2 / 2" in page(client, "/blog?page=50")


def test_article(client):
    html = page(client, "/blog/article-3")
    assert "Article 3" in html and "Second paragraphe." in html
    assert "1 min de lecture" in html


def test_article_brouillon_ou_inconnu(client):
    page(client, "/blog/brouillon-secret", 404)
    page(client, "/blog/inconnu", 404)
