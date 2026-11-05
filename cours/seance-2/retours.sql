-- Séance 2 · À vous : le fichier des retours
--
-- Charge retours.csv tel quel dans une table plate, retours_export, pour l'observer.
-- Ne dépend d'aucune autre table : fonctionne sur la base de la séance 1, ou sur une base vide.
-- Rejouable. Depuis sgbd/postgres, base lancée :
--
--   docker compose exec db psql -U ombelle -d ombelle -f /cours/seance-2/retours.sql
--
-- Vous pouvez aussi ouvrir retours.csv dans un tableur : c'est le même fichier.

\pset footer off

DROP TABLE IF EXISTS retours_export;

CREATE TABLE retours_export (
    commande_id    integer,
    produit_id     integer,
    produit_nom    text,
    client_email   text,
    demande_le     date,
    quantite       integer,
    motif_code     text,
    motif_libelle  text
);

\copy retours_export FROM '/cours/seance-2/retours.csv' WITH (FORMAT csv, HEADER true)

\echo '== Le fichier, trié par client'
SELECT * FROM retours_export ORDER BY client_email, commande_id, produit_id;

\echo '== Combien de fois chaque information est recopiée'
SELECT 'client_email' AS colonne, count(*) AS lignes, count(DISTINCT client_email) AS valeurs_differentes FROM retours_export
UNION ALL
SELECT 'produit_nom', count(*), count(DISTINCT produit_nom) FROM retours_export
UNION ALL
SELECT 'motif_libelle', count(*), count(DISTINCT motif_libelle) FROM retours_export;

\echo '== À vous : écrivez ici la requête qui trouve l''incohérence déjà présente dans le fichier'
