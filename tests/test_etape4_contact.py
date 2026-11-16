"""Étape 4 — formulaire de contact (route contact de pages.py)."""
import db

MESSAGE_OK = {"nom": "  Zoé  ", "email": "zoe@exemple.fr", "sujet": "Stage",
              "message": "Bonjour, je vous écris au sujet d'un stage."}


def test_contact_get(client):
    reponse = client.get("/contact")
    assert reponse.status_code == 200
    assert 'name="email"' in reponse.get_data(as_text=True)


def test_contact_post_correct(client):
    reponse = client.post("/contact", data=MESSAGE_OK)
    assert reponse.status_code == 302, "après un envoi réussi, il faut rediriger"
    assert reponse.headers["Location"].endswith("/contact")
    dernier = db.lister_messages()[0]
    assert dernier["nom"] == "Zoé"                 # espaces retirés
    assert dernier["sujet"] == "Stage"
    assert dernier["lu"] == 0


def test_contact_message_flash(client):
    reponse = client.post("/contact", data=MESSAGE_OK, follow_redirects=True)
    assert "Merci, votre message a bien été envoyé." in reponse.get_data(as_text=True)


def test_contact_post_incorrect(client):
    avant = len(db.lister_messages())
    reponse = client.post("/contact", data=dict(MESSAGE_OK, email="pas-une-adresse"))
    assert reponse.status_code == 400
    html = reponse.get_data(as_text=True)
    assert "Adresse électronique invalide." in html
    assert "Bonjour, je vous écris" in html, "le message tapé doit être réaffiché"
    assert len(db.lister_messages()) == avant


def test_contact_robot(client):
    avant = len(db.lister_messages())
    reponse = client.post("/contact", data=dict(MESSAGE_OK, site_web="http://spam.example"),
                          follow_redirects=True)
    assert "Merci, votre message a bien été envoyé." in reponse.get_data(as_text=True)
    assert len(db.lister_messages()) == avant, "un robot ne doit rien enregistrer"


def test_contact_html_echappe(client):
    """Jinja échappe le HTML : un <script> tapé par un visiteur s'affiche
    comme du texte, il ne s'exécute pas."""
    reponse = client.post("/contact", data=dict(MESSAGE_OK, nom="<script>x</script>", email="?"))
    html = reponse.get_data(as_text=True)
    assert "<script>x</script>" not in html
    assert "&lt;script&gt;" in html
