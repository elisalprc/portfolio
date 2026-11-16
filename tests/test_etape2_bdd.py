"""Étape 2 — fonctions de db.py (sur la base de test de conftest.py)."""
import db


def test_lire_profil_fourni(app):
    assert db.lire_profil()["nom"] == "Alex Dupont"


def test_lister_experiences(app):
    pro = db.lister_experiences("pro")
    assert [e["titre"] for e in pro] == ["Job étudiant", "Stage été"]
    assert pro[0]["fin"] is None
    assert [e["titre"] for e in db.lister_experiences("formation")] == \
        ["Cycle ingénieur", "Baccalauréat"]
    assert db.lister_experiences("autre") == []


def test_competences_par_categorie(app):
    assert db.competences_par_categorie() == {
        "Langages": [{"nom": "Python", "niveau": 4}, {"nom": "C", "niveau": 3},
                     {"nom": "Java", "niveau": 3}],
        "Langues": [{"nom": "Anglais", "niveau": 4}],
        "Outils": [{"nom": "Git", "niveau": 3}],
    }
    assert list(db.competences_par_categorie()) == ["Langages", "Langues", "Outils"]


def test_lister_projets_ordre_et_technologies(app):
    projets = db.lister_projets()
    assert [p["slug"] for p in projets] == ["projet-trois", "projet-un", "projet-deux",
                                           "projet-quatre"]
    assert projets[1]["technologies"] == ["Python", "Flask"]
    assert projets[3]["technologies"] == ["Flask", "SQLite"]


def test_lister_projets_limite(app):
    assert [p["slug"] for p in db.lister_projets(limite=2)] == ["projet-trois", "projet-un"]


def test_lister_projets_filtre_sans_majuscules(app):
    assert [p["slug"] for p in db.lister_projets(techno="PYTHON")] == ["projet-un", "projet-deux"]
    assert [p["slug"] for p in db.lister_projets(techno="flask", limite=1)] == ["projet-un"]
    assert db.lister_projets(techno="Rust") == []


def test_projet_par_slug(app):
    projet = db.projet_par_slug("projet-quatre")
    assert projet["titre"] == "Projet Quatre"
    assert projet["technologies"] == ["Flask", "SQLite"]
    assert projet["lien_demo"] == "https://demo.exemple.fr"
    assert db.projet_par_slug("inconnu") is None


def test_projet_par_slug_injection(app):
    assert db.projet_par_slug("' OR '1'='1") is None


def test_toutes_technologies(app):
    assert db.toutes_technologies() == ["C", "Flask", "Pandas", "Python", "SQLite"]


def test_compter_articles(app):
    assert db.compter_articles() == 7
    assert db.compter_articles(publies_seulement=False) == 8


def test_lister_articles(app):
    articles = db.lister_articles()
    assert len(articles) == 7
    assert articles[0]["slug"] == "article-7"
    assert "brouillon-secret" not in [a["slug"] for a in articles]
    tous = db.lister_articles(publies_seulement=False)
    assert [a["slug"] for a in tous[:2]] == ["brouillon-secret", "article-7"]


def test_lister_articles_limite_decalage(app):
    assert [a["slug"] for a in db.lister_articles(limite=2)] == ["article-7", "article-6"]
    assert [a["slug"] for a in db.lister_articles(limite=5, decalage=5)] == \
        ["article-2", "article-1"]


def test_article_par_slug(app):
    assert db.article_par_slug("article-3")["titre"] == "Article 3"
    assert db.article_par_slug("brouillon-secret") is None
    assert db.article_par_slug("brouillon-secret", publies_seulement=False)["publie"] == 0
    assert db.article_par_slug("inconnu") is None


def test_article_par_id(app):
    brouillon = db.article_par_slug("brouillon-secret", publies_seulement=False)
    assert db.article_par_id(brouillon["id"])["titre"] == "Brouillon secret"
    assert db.article_par_id(9999) is None


def test_slug_disponible(app):
    assert db.slug_disponible("Un titre neuf") == "un-titre-neuf"
    assert db.slug_disponible("Article 3") == "article-3-2"


def test_creer_article(app):
    id_article = db.creer_article("Nouvel article", "Du contenu.", True)
    article = db.article_par_id(id_article)
    assert article["slug"] == "nouvel-article"
    assert article["publie"] == 1
    assert len(article["cree_le"]) == 16          # « AAAA-MM-JJ HH:MM »
    assert article["modifie_le"] is None
    assert db.compter_articles() == 8


def test_creer_article_slug_en_double(app):
    premier = db.creer_article("Même titre", "a", False)
    second = db.creer_article("Même titre", "b", False)
    troisieme = db.creer_article("Même titre", "c", False)
    assert [db.article_par_id(i)["slug"] for i in (premier, second, troisieme)] == \
        ["meme-titre", "meme-titre-2", "meme-titre-3"]
    assert db.article_par_id(premier)["publie"] == 0


def test_modifier_article(app):
    article = db.article_par_slug("article-1")
    assert db.modifier_article(article["id"], "Titre changé", "Nouveau contenu.", False)
    apres = db.article_par_id(article["id"])
    assert apres["titre"] == "Titre changé"
    assert apres["contenu"] == "Nouveau contenu."
    assert apres["publie"] == 0
    assert apres["slug"] == "article-1"            # le slug ne change pas
    assert apres["modifie_le"] is not None
    assert not db.modifier_article(9999, "x", "y", True)


def test_supprimer_article(app):
    article = db.article_par_slug("article-1")
    assert db.supprimer_article(article["id"])
    assert db.article_par_id(article["id"]) is None
    assert not db.supprimer_article(article["id"])


def test_messages(app):
    assert db.compter_messages_non_lus() == 1
    id_message = db.ajouter_message("Zoé", "zoe@exemple.fr", "", "Un troisième message.")
    assert db.compter_messages_non_lus() == 2
    messages = db.lister_messages()
    assert [m["nom"] for m in messages] == ["Zoé", "Eve", "Bob"]
    assert messages[0]["lu"] == 0 and messages[0]["id"] == id_message
    assert db.marquer_lu(id_message)
    assert db.compter_messages_non_lus() == 1
    assert [m["nom"] for m in db.lister_messages()] == ["Eve", "Zoé", "Bob"]
    assert not db.marquer_lu(9999)
