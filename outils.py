"""Étape 1 — Fonctions utilitaires « pures ».

Aucune de ces fonctions ne touche au web ni à la base de données : elles
reçoivent des valeurs et RENVOIENT un résultat (elles n'affichent rien).
On les teste donc sans lancer le site :

    python -m pytest tests/test_etape1_outils.py

Les deux premières fonctions sont écrites : elles servent de modèle.
"""
import math
import unicodedata

from a_faire import AFaire

MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin",
        "juil.", "août", "sept.", "oct.", "nov.", "déc."]


# --------------------------------------------------------------------------
# Écrites pour vous (modèles)
# --------------------------------------------------------------------------
def temps_de_lecture(texte, mots_par_minute=200):
    """Nombre de minutes pour lire `texte`, arrondi au-dessus, au moins 1.

    >>> temps_de_lecture("un deux trois")
    1
    >>> temps_de_lecture("mot " * 401)
    3
    """
    nb_mots = len(texte.split())
    return max(1, math.ceil(nb_mots / mots_par_minute))


def liste_technologies(chaine):
    """Découpe « Python, Flask ,  SQLite, » en ["Python", "Flask", "SQLite"].

    Les espaces autour des noms et les morceaux vides sont retirés.
    """
    return [morceau.strip() for morceau in chaine.split(",") if morceau.strip()]


# --------------------------------------------------------------------------
# À écrire
# --------------------------------------------------------------------------
def slugifier(titre):
    """Transforme un titre en « slug », le morceau d'URL qui l'identifie.

    >>> slugifier("Mon Premier Article !")
    'mon-premier-article'
    >>> slugifier("  Été 2026 : bilan & perspectives ")
    'ete-2026-bilan-perspectives'
    >>> slugifier("???")
    'sans-titre'

    Règles : minuscules ; accents retirés ; toute suite de caractères qui
    ne sont ni des lettres ni des chiffres devient UN seul tiret ; pas de
    tiret au début ni à la fin ; « sans-titre » si rien ne reste.
    """
    # À FAIRE (étape 1)
    # Indice : Pour retirer les accents :
    #              sans_accents = unicodedata.normalize("NFKD", titre).encode("ascii", "ignore").decode()
    #          Parcourez ensuite les caractères : c.isalnum() dit si c est une lettre ou un chiffre.
    raise AFaire(1, "slugifier")


def email_valide(email):
    """Vérification SIMPLE d'une adresse électronique.

    Valide si : aucun espace ; exactement un « @ » ; au moins un caractère
    avant le « @ » ; après le « @ », un point qui n'est ni le premier ni
    le dernier caractère.

    >>> email_valide("camille.martin@exemple.fr")
    True
    >>> email_valide("camille@exemple")
    False
    """
    # À FAIRE (étape 1)
    # Indice : email.count("@"), email.split("@"), partie.startswith("."), partie.endswith(".")
    raise AFaire(1, "email_valide")


def valider_contact(formulaire):
    """Vérifie le formulaire de contact ; renvoie un dict {champ: message}.

    `formulaire` se comporte comme un dict (clés "nom", "email", "sujet",
    "message") ; une clé peut manquer. Les espaces au début et à la fin des
    valeurs ne comptent pas. Règles, et messages EXACTS attendus :

      nom     obligatoire, 2 à 100 caractères
              "Indiquez votre nom (2 à 100 caractères)."
      email   doit être valide (email_valide)
              "Adresse électronique invalide."
      sujet   facultatif, 150 caractères au plus
              "Le sujet ne doit pas dépasser 150 caractères."
      message obligatoire, 10 à 2000 caractères
              "Le message doit faire entre 10 et 2000 caractères."

    Un dict VIDE signifie : tout est correct.
    """
    # À FAIRE (étape 1)
    # Indice : valeur = formulaire.get("nom", "").strip()  puis un if par règle.
    raise AFaire(1, "valider_contact")


def formater_periode(debut, fin):
    """Met en forme une période « AAAA-MM » → texte lisible.

    >>> formater_periode("2023-09", "2025-06")
    'sept. 2023 – juin 2025'
    >>> formater_periode("2025-09", None)
    "sept. 2025 – aujourd'hui"

    Le tiret est le caractère « – » (tiret demi-cadratin), entouré
    d'espaces. Utilisez la liste MOIS.
    """
    # À FAIRE (étape 1)
    # Indice : "2023-09".split("-") donne ["2023", "09"] ; int("09") vaut 9 ; MOIS[8] est "sept.".
    #          Écrivez une petite fonction locale qui formate UNE date, et appelez-la deux fois.
    raise AFaire(1, "formater_periode")


def duree(debut, fin, aujourdhui):
    """Durée d'une période, en texte : "8 mois", "1 an", "2 ans 3 mois".

    `debut` et `fin` sont au format « AAAA-MM » ; `fin` vaut None pour une
    période en cours, on prend alors `aujourdhui` (même format). Le mois de
    début et le mois de fin comptent tous les deux :

    >>> duree("2025-01", "2025-01", "2026-11")
    '1 mois'
    >>> duree("2024-09", "2025-08", "2026-11")
    '1 an'
    >>> duree("2023-09", None, "2026-11")
    '3 ans 3 mois'
    """
    # À FAIRE (étape 1)
    # Indice : Comptez tout en mois : (annee_fin - annee_debut) * 12 + (mois_fin - mois_debut) + 1,
    #          puis // 12 et % 12. Attention au singulier « an » et à « mois » (invariable).
    raise AFaire(1, "duree")


def decouper_paragraphes(texte):
    """Découpe un texte en paragraphes (séparés par au moins une ligne vide).

    Dans un paragraphe, les retours à la ligne deviennent des espaces.
    Les paragraphes vides disparaissent.

    >>> decouper_paragraphes("Bonjour\\ntout le monde.\\n\\n\\nSecond.\\n")
    ['Bonjour tout le monde.', 'Second.']
    """
    # À FAIRE (étape 1)
    # Indice : Une ligne vide est une ligne dont line.strip() == "". Accumulez les lignes du
    #          paragraphe courant dans une liste ; à chaque ligne vide, fermez le paragraphe.
    raise AFaire(1, "decouper_paragraphes")


def extraire_resume(texte, longueur=160):
    """Début du texte, pour les listes d'articles.

    Si le texte (espaces multiples et retours à la ligne réduits à un seul
    espace) tient en `longueur` caractères, il est renvoyé tel quel. Sinon
    on garde les mots ENTIERS qui tiennent dans `longueur` caractères et on
    ajoute « … » (un seul caractère).

    >>> extraire_resume("Un texte court.")
    'Un texte court.'
    >>> extraire_resume("un deux trois quatre", 12)
    'un deux…'
    """
    # À FAIRE (étape 1)
    # Indice : " ".join(texte.split()) normalise les espaces. Ajoutez ensuite les mots un à un
    #          tant que la longueur reste <= longueur.
    raise AFaire(1, "extraire_resume")


def paginer(nb_elements, page, par_page):
    """Calcule la pagination d'une liste de `nb_elements` éléments.

    Renvoie un dict :
      "page"       la page affichée, ramenée entre 1 et nb_pages ;
      "nb_pages"   au moins 1 (une liste vide a une page, vide) ;
      "decalage"   le nombre d'éléments à sauter (OFFSET en SQL) ;
      "precedente" le numéro de la page précédente, ou None ;
      "suivante"   le numéro de la page suivante, ou None.

    >>> paginer(12, 2, 5)
    {'page': 2, 'nb_pages': 3, 'decalage': 5, 'precedente': 1, 'suivante': 3}
    """
    # À FAIRE (étape 1)
    # Indice : nb_pages = math.ceil(nb_elements / par_page), mais jamais moins de 1.
    #          min() et max() ramènent la page dans l'intervalle.
    raise AFaire(1, "paginer")
