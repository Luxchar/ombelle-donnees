-- Séance 2 · démo colonne avec Cassandra
--
-- Depuis sgbd/cassandra, base lancée et prête (docker compose ps : healthy) :
--   docker compose exec cassandra cqlsh -f /cours/seance-2/colonne.cql
--
-- Cassandra range les lignes par partition. On ne conçoit pas une table à partir des
-- entités, mais à partir d'une requête : une question, une table.

DROP KEYSPACE IF EXISTS ombelle_demo;
CREATE KEYSPACE ombelle_demo
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE ombelle_demo;

-- 1 · La requête : « les dernières commandes d'un client »
-- La clé de partition (client_id) dit où vivent les lignes.
-- La clé de tri (passee_le) dit dans quel ordre elles sont rangées sur le disque.
CREATE TABLE commandes_par_client (
    client_id    int,
    passee_le    timestamp,
    commande_id  int,
    statut       text,
    total        decimal,
    PRIMARY KEY ((client_id), passee_le, commande_id)
) WITH CLUSTERING ORDER BY (passee_le DESC, commande_id DESC);

INSERT INTO commandes_par_client (client_id, passee_le, commande_id, statut, total)
VALUES (777, '2026-10-13 06:03:57+0000', 192912, 'livree', 56.50);
INSERT INTO commandes_par_client (client_id, passee_le, commande_id, statut, total)
VALUES (777, '2026-09-17 10:48:40+0000', 183294, 'livree', 38.39);
INSERT INTO commandes_par_client (client_id, passee_le, commande_id, statut, total)
VALUES (777, '2026-09-08 00:34:23+0000', 179786, 'livree', 427.80);
INSERT INTO commandes_par_client (client_id, passee_le, commande_id, statut, total)
VALUES (777, '2026-08-12 10:30:38+0000', 172129, 'livree', 111.74);
INSERT INTO commandes_par_client (client_id, passee_le, commande_id, statut, total)
VALUES (1234, '2026-11-10 10:12:00+0000', 200001, 'payee', 155.86);

-- Une seule partition lue, déjà dans l'ordre : c'est la requête pour laquelle la table existe.
SELECT commande_id, passee_le, statut, total FROM commandes_par_client WHERE client_id = 777 LIMIT 3;

-- 2 · Une autre question, une autre table : on duplique au lieu de joindre
-- « Le chiffre d'affaires par catégorie pour un mois » : un compteur par (mois, catégorie),
-- augmenté à chaque commande. Le calcul est fait à l'écriture, pas à la lecture.
CREATE TABLE ca_par_mois (
    mois         text,
    categorie    text,
    ca_centimes  counter,
    PRIMARY KEY ((mois), categorie)
);

UPDATE ca_par_mois SET ca_centimes = ca_centimes + 8598 WHERE mois = '2026-11' AND categorie = 'Livres';
UPDATE ca_par_mois SET ca_centimes = ca_centimes + 3998 WHERE mois = '2026-11' AND categorie = 'Livres';
UPDATE ca_par_mois SET ca_centimes = ca_centimes + 800  WHERE mois = '2026-11' AND categorie = 'Maison';
UPDATE ca_par_mois SET ca_centimes = ca_centimes + 2190 WHERE mois = '2026-11' AND categorie = 'Vêtements';

SELECT categorie, ca_centimes FROM ca_par_mois WHERE mois = '2026-11';

-- 3 · La limite : une question qu'on n'a pas prévue
-- « Toutes les commandes annulées » : statut n'est pas dans la clé, Cassandra refuse
-- (il faudrait lire toutes les partitions). La réponse : une troisième table.
SELECT * FROM commandes_par_client WHERE statut = 'annulee';
