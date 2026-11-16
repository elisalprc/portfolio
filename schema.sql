-- Schéma de la base SQLite du portfolio.
-- Exécuté par la commande :  flask --app app init-db
-- ATTENTION : init-db EFFACE toutes les tables puis les recrée.

DROP TABLE IF EXISTS profil;
DROP TABLE IF EXISTS experiences;
DROP TABLE IF EXISTS competences;
DROP TABLE IF EXISTS projets;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS admin;

-- Une seule ligne : vous.
CREATE TABLE profil (
    id        INTEGER PRIMARY KEY CHECK (id = 1),
    nom       TEXT NOT NULL,
    titre     TEXT NOT NULL,      -- « Étudiant ingénieur en génie électrique »
    bio       TEXT NOT NULL,
    email     TEXT NOT NULL,
    ville     TEXT,
    github    TEXT,               -- URL complète, ou NULL
    linkedin  TEXT
);

-- Expériences professionnelles ET formations (colonne categorie).
CREATE TABLE experiences (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    categorie     TEXT NOT NULL CHECK (categorie IN ('pro', 'formation')),
    titre         TEXT NOT NULL,  -- « Stage développeur », « Licence 3 »
    organisation  TEXT NOT NULL,
    lieu          TEXT,
    debut         TEXT NOT NULL,  -- « AAAA-MM »
    fin           TEXT,           -- « AAAA-MM », ou NULL si en cours
    description   TEXT NOT NULL DEFAULT ''
);

CREATE TABLE competences (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nom        TEXT NOT NULL,
    categorie  TEXT NOT NULL,     -- « Langages », « Outils », « Langues »…
    niveau     INTEGER NOT NULL CHECK (niveau BETWEEN 1 AND 5)
);

CREATE TABLE projets (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    titre         TEXT NOT NULL,
    slug          TEXT NOT NULL UNIQUE,
    resume        TEXT NOT NULL,  -- une phrase, affichée sur les cartes
    description   TEXT NOT NULL,  -- texte complet, paragraphes séparés par une ligne vide
    technologies  TEXT NOT NULL DEFAULT '',  -- « Python, Flask, SQLite »
    lien_code     TEXT,
    lien_demo     TEXT,
    date          TEXT NOT NULL   -- « AAAA-MM »
);

-- À FAIRE (étape 2) : écrivez ici les deux CREATE TABLE.
-- Indice : Table articles : id (clé auto-incrémentée), titre, slug (unique), contenu,
--          publie (entier 0 ou 1, 0 par défaut), cree_le (texte, obligatoire), modifie_le (texte, facultatif).

CREATE TABLE articles (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    titre         TEXT NOT NULL,
    slug          TEXT NOT NULL UNIQUE,
    contenu        TEXT NOT NULL,  -- une phrase, affichée sur les cartes
    description   TEXT NOT NULL,  -- texte complet, paragraphes séparés par une ligne vide
    publie        INTEGER NOT NULL CHECK (publie BETWEEN 0 AND 1) DEFAULT 0,
    cree_le       TEXT NOT NULL,   -- « AAAA-MM »
    modifie_le    TEXT   -- « AAAA-MM »
); 

--          Table messages : id, nom, email, sujet (facultatif), contenu, recu_le (texte, obligatoire),
--          lu (entier 0 ou 1, 0 par défaut).  Modèle : la table projets ci-dessus.

CREATE TABLE messages (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nom         TEXT NOT NULL,
    email          TEXT NOT NULL,
    sujet        TEXT, --facultatif donc on retire le NOT NULL
    recu_le   TEXT NOT NULL,  -- AAAA-MM
    lu        INTEGER NOT NULL CHECK (lu BETWEEN 0 AND 1) DEFAULT 0
); 


-- Le compte administrateur (une ligne). Le mot de passe n'est jamais
-- stocké en clair : seulement son hachage (werkzeug.security).
CREATE TABLE admin (
    id                  INTEGER PRIMARY KEY CHECK (id = 1),
    identifiant         TEXT NOT NULL,
    mot_de_passe_hash   TEXT NOT NULL
);
