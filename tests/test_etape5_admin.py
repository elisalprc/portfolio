"""Étape 5 — administration (admin.py)."""
import db
from admin import lire_formulaire_article, verifier_admin
from conftest import IDENTIFIANT_TEST, MOT_DE_PASSE_TEST


def test_verifier_admin(app):
    assert verifier_admin(IDENTIFIANT_TEST, MOT_DE_PASSE_TEST)
    assert not verifier_admin(IDENTIFIANT_TEST, "mauvais")
    assert not verifier_admin("autre", MOT_DE_PASSE_TEST)


def test_verifier_admin_sans_compte(app):
    db.executer("DELETE FROM admin")
    assert not verifier_admin(IDENTIFIANT_TEST, MOT_DE_PASSE_TEST)


def test_mot_de_passe_jamais_en_clair(app):
    compte = db.requete("SELECT * FROM admin", une=True)
    assert MOT_DE_PASSE_TEST not in compte["mot_de_passe_hash"]


def test_pages_protegees(client):
    for url in ["/admin/", "/admin/articles", "/admin/articles/nouveau", "/admin/messages",
                "/admin/articles/1/modifier"]:
        reponse = client.get(url)
        assert reponse.status_code == 302, f"{url} doit être protégée"
        assert "/admin/connexion" in reponse.headers["Location"]


def test_connexion_correcte(client):
    reponse = client.post("/admin/connexion", data={"identifiant": IDENTIFIANT_TEST,
                                                    "mot_de_passe": MOT_DE_PASSE_TEST})
    assert reponse.status_code == 302
    assert reponse.headers["Location"].endswith("/admin/")
    with client.session_transaction() as session:
        assert session["admin"] == IDENTIFIANT_TEST
    assert client.get("/admin/").status_code == 200


def test_connexion_incorrecte(client):
    reponse = client.post("/admin/connexion", data={"identifiant": IDENTIFIANT_TEST,
                                                    "mot_de_passe": "faux"})
    assert reponse.status_code == 401
    assert "Identifiant ou mot de passe incorrect." in reponse.get_data(as_text=True)
    with client.session_transaction() as session:
        assert "admin" not in session


def test_connexion_suivant(client):
    donnees = {"identifiant": IDENTIFIANT_TEST, "mot_de_passe": MOT_DE_PASSE_TEST}
    reponse = client.post("/admin/connexion?suivant=/admin/messages", data=donnees)
    assert reponse.headers["Location"].endswith("/admin/messages")


def test_connexion_suivant_autre_site(client):
    donnees = {"identifiant": IDENTIFIANT_TEST, "mot_de_passe": MOT_DE_PASSE_TEST}
    reponse = client.post("/admin/connexion?suivant=https://pirate.example/", data=donnees)
    assert "pirate" not in reponse.headers["Location"]


def test_deconnexion_fournie(client_admin):
    client_admin.post("/admin/deconnexion")
    assert client_admin.get("/admin/").status_code == 302


def test_tableau(client_admin):
    reponse = client_admin.get("/admin/")
    assert reponse.status_code == 200
    html = reponse.get_data(as_text=True)
    assert "<strong>7</strong> articles publiés" in html
    assert "<strong>1</strong> brouillon" in html
    assert "<strong>1</strong> message non lu" in html


def test_liste_articles_avec_brouillons(client_admin):
    html = client_admin.get("/admin/articles").get_data(as_text=True)
    assert "Brouillon secret" in html and "Article 1" in html


def test_lire_formulaire_article():
    assert lire_formulaire_article({"titre": " T ", "contenu": " C ", "publie": "on"}) == \
        ({"titre": "T", "contenu": "C", "publie": True}, {})
    valeurs, erreurs = lire_formulaire_article({"titre": "  ", "contenu": ""})
    assert valeurs["publie"] is False
    assert erreurs == {"titre": "Le titre est obligatoire.",
                       "contenu": "Le contenu est obligatoire."}


def test_nouvel_article(client_admin):
    assert client_admin.get("/admin/articles/nouveau").status_code == 200
    reponse = client_admin.post("/admin/articles/nouveau",
                                data={"titre": "Mon stage", "contenu": "C'était bien.",
                                      "publie": "on"})
    assert reponse.status_code == 302
    assert reponse.headers["Location"].endswith("/admin/articles")
    article = db.article_par_slug("mon-stage")
    assert article is not None and article["contenu"] == "C'était bien."


def test_nouvel_article_incorrect(client_admin):
    reponse = client_admin.post("/admin/articles/nouveau", data={"titre": "", "contenu": "x"})
    assert reponse.status_code == 400
    assert "Le titre est obligatoire." in reponse.get_data(as_text=True)
    assert db.compter_articles(publies_seulement=False) == 8


def test_modifier_article(client_admin):
    article = db.article_par_slug("article-2")
    url = f"/admin/articles/{article['id']}/modifier"
    assert "Contenu de l&#39;article 2." in client_admin.get(url).get_data(as_text=True)
    reponse = client_admin.post(url, data={"titre": "Article deux", "contenu": "Neuf."})
    assert reponse.status_code == 302
    apres = db.article_par_id(article["id"])
    assert apres["titre"] == "Article deux" and apres["publie"] == 0


def test_modifier_article_incorrect_ou_inconnu(client_admin):
    article = db.article_par_slug("article-2")
    url = f"/admin/articles/{article['id']}/modifier"
    assert client_admin.post(url, data={"titre": "x", "contenu": " "}).status_code == 400
    assert db.article_par_id(article["id"])["titre"] == "Article 2"
    assert client_admin.get("/admin/articles/9999/modifier").status_code == 404


def test_supprimer_article(client_admin):
    article = db.article_par_slug("article-2")
    url = f"/admin/articles/{article['id']}/supprimer"
    assert client_admin.get(url).status_code == 405, "la suppression doit refuser GET"
    assert client_admin.post(url).status_code == 302
    assert db.article_par_id(article["id"]) is None
    assert client_admin.post(url).status_code == 404


def test_messages(client_admin):
    html = client_admin.get("/admin/messages").get_data(as_text=True)
    assert html.index("Eve") < html.index("Bob")
    eve = db.lister_messages()[0]
    reponse = client_admin.post(f"/admin/messages/{eve['id']}/lu")
    assert reponse.status_code == 302
    assert db.compter_messages_non_lus() == 0
    assert client_admin.post("/admin/messages/9999/lu").status_code == 404
