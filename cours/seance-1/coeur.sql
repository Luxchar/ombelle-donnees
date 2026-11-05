-- Séance 1 · l'exemple : le cœur de la boutique Ombelle
--
-- Le MPD PostgreSQL issu du MCD du cours (RG1 à RG6).
-- Rejouable : on efface d'abord ce qui existe.
--
--   docker compose exec db psql -U ombelle -d ombelle -f /cours/seance-1/coeur.sql

DROP TABLE IF EXISTS avis, lignes_commande, commandes, produits, boutiques, clients, categories CASCADE;

-- RG5 : un produit appartient à une seule catégorie.
CREATE TABLE categories (
    id    serial PRIMARY KEY,
    nom   text NOT NULL UNIQUE
);

CREATE TABLE produits (
    id            serial PRIMARY KEY,
    categorie_id  integer NOT NULL REFERENCES categories (id),     -- RG5 : (1,1) côté produit
    nom           text NOT NULL,
    prix          numeric(8, 2) NOT NULL CHECK (prix > 0),
    stock         integer NOT NULL DEFAULT 0 CHECK (stock >= 0),
    cree_le       date NOT NULL DEFAULT current_date
);

-- RG1 : un client est identifié par son e-mail.
CREATE TABLE clients (
    id          serial PRIMARY KEY,
    prenom      text NOT NULL,
    nom         text NOT NULL,
    email       text NOT NULL UNIQUE,
    ville       text,
    inscrit_le  timestamp NOT NULL DEFAULT now()
);

-- RG2 : une commande est passée par un seul client.
-- RG3 : une commande est payée, expédiée, livrée ou annulée.
CREATE TABLE commandes (
    id          serial PRIMARY KEY,
    client_id   integer NOT NULL REFERENCES clients (id),
    passee_le   timestamp NOT NULL DEFAULT now(),
    statut      text NOT NULL DEFAULT 'payee'
                CHECK (statut IN ('payee', 'expediee', 'livree', 'annulee'))
);

-- RG4 : une commande contient au moins un produit, en une certaine quantité.
-- RG6 : on garde le prix payé, qui n'est pas forcément le prix du jour.
-- L'association « Contenir » (n,n) devient une table : sa clé est le couple.
CREATE TABLE lignes_commande (
    commande_id    integer NOT NULL REFERENCES commandes (id),
    produit_id     integer NOT NULL REFERENCES produits (id),
    quantite       integer NOT NULL CHECK (quantite > 0),
    prix_unitaire  numeric(8, 2) NOT NULL CHECK (prix_unitaire >= 0),
    PRIMARY KEY (commande_id, produit_id)
);

-- PostgreSQL n'indexe pas les clés étrangères tout seul.
-- lignes_commande (commande_id) est déjà couvert par la clé primaire.
CREATE INDEX ON produits (categorie_id);
CREATE INDEX ON commandes (client_id);
CREATE INDEX ON lignes_commande (produit_id);
