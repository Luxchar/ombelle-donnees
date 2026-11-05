-- Séance 1 · vérification de l'exercice « À vous »
--
-- Essaie des écritures que votre schéma doit accepter, et d'autres qu'il doit refuser.
-- Tout est annulé à la fin : votre base reste vide.
--
--   docker compose exec db psql -U ombelle -d ombelle -f /cours/seance-1/verifier.sql
--
-- Objectif : 12 tests réussis sur 12.

\set QUIET on
\pset footer off
BEGIN;

CREATE TEMP TABLE resultats (num int, test text, ok boolean);

-- Lance une requête et note si elle a réussi ou échoué comme prévu.
-- Un refus ne compte que si la table ou la colonne testée existe (p_requis).
CREATE FUNCTION pg_temp.tester(p_num int, p_test text, p_requis boolean, p_sql text, p_doit_reussir boolean)
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    v_reussi boolean := false;
BEGIN
    IF NOT p_requis THEN
        INSERT INTO resultats VALUES (p_num, p_test, false);
        RETURN;
    END IF;
    BEGIN
        EXECUTE p_sql;
        v_reussi := true;
        -- Une écriture qui aurait dû être refusée est annulée : elle ne fausse pas les tests suivants.
        IF NOT p_doit_reussir THEN
            RAISE EXCEPTION USING ERRCODE = 'P0099';
        END IF;
    EXCEPTION
        WHEN SQLSTATE 'P0099' THEN NULL;
        WHEN others THEN v_reussi := false;
    END;
    INSERT INTO resultats VALUES (p_num, p_test, v_reussi = p_doit_reussir);
END;
$$;

-- Vrai si la colonne existe.
CREATE FUNCTION pg_temp.colonne(p_table text, p_colonne text)
RETURNS boolean
LANGUAGE sql
AS $$
    SELECT EXISTS (SELECT 1 FROM pg_attribute
                   WHERE attrelid = to_regclass(p_table) AND attname = p_colonne AND NOT attisdropped);
$$;

-- Vrai si la table a un index dont la première colonne est celle-ci.
CREATE FUNCTION pg_temp.indexee(p_table text, p_colonne text)
RETURNS boolean
LANGUAGE sql
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM pg_index i
        JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = i.indkey[0]
        WHERE i.indrelid = to_regclass(p_table)
          AND a.attname = p_colonne
    );
$$;

-- Le décor : une catégorie et deux clients.
DO $$
BEGIN
    INSERT INTO categories (id, nom) VALUES (900001, 'Catégorie de test');
    INSERT INTO clients (id, prenom, nom, email)
    VALUES (900001, 'Ada', 'Test', 'ada@test.fr'), (900002, 'Alan', 'Test', 'alan@test.fr');
EXCEPTION WHEN others THEN
    RAISE NOTICE 'Le décor ne se met pas en place : avez-vous lancé coeur.sql ? (%)', SQLERRM;
END;
$$;

DO $do$
BEGIN
    PERFORM pg_temp.tester(1, 'Une boutique se crée', pg_temp.colonne('boutiques', 'nom'),
        $q$INSERT INTO boutiques (id, nom, ville, ouverte_le) VALUES (900001, 'Atelier Test', 'Paris', '2024-01-01')$q$, true);
    PERFORM pg_temp.tester(2, 'RG7  : deux boutiques ne portent pas le même nom', pg_temp.colonne('boutiques', 'nom'),
        $q$INSERT INTO boutiques (id, nom, ville, ouverte_le) VALUES (900002, 'Atelier Test', 'Lyon', '2024-01-01')$q$, false);
    PERFORM pg_temp.tester(3, 'Un produit se crée dans une boutique', pg_temp.colonne('produits', 'boutique_id'),
        $q$INSERT INTO produits (id, boutique_id, categorie_id, nom, prix) VALUES (900001, 900001, 900001, 'Lampe test', 10), (900004, 900001, 900001, 'Vase test', 12)$q$, true);
    PERFORM pg_temp.tester(4, 'RG8  : un produit sans boutique est refusé', pg_temp.colonne('produits', 'boutique_id'),
        $q$INSERT INTO produits (id, boutique_id, categorie_id, nom, prix) VALUES (900002, NULL, 900001, 'Orphelin', 10)$q$, false);
    PERFORM pg_temp.tester(5, 'RG8  : un produit d''une boutique inconnue est refusé', pg_temp.colonne('produits', 'boutique_id'),
        $q$INSERT INTO produits (id, boutique_id, categorie_id, nom, prix) VALUES (900003, 999999, 900001, 'Fantôme', 10)$q$, false);
    PERFORM pg_temp.tester(6, 'Un avis se crée', pg_temp.colonne('avis', 'note'),
        $q$INSERT INTO avis (client_id, produit_id, note, commentaire) VALUES (900001, 900001, 4, 'Très bien.')$q$, true);
    PERFORM pg_temp.tester(7, 'RG9  : un client ne note qu''une fois le même produit', pg_temp.colonne('avis', 'note'),
        $q$INSERT INTO avis (client_id, produit_id, note) VALUES (900001, 900001, 2)$q$, false);
    PERFORM pg_temp.tester(8, 'RG10 : une note de 6 est refusée', pg_temp.colonne('avis', 'note'),
        $q$INSERT INTO avis (client_id, produit_id, note) VALUES (900002, 900001, 6)$q$, false);
    PERFORM pg_temp.tester(9, 'RG10 : une note de 0 est refusée', pg_temp.colonne('avis', 'note'),
        $q$INSERT INTO avis (client_id, produit_id, note) VALUES (900002, 900001, 0)$q$, false);
    PERFORM pg_temp.tester(10, 'RG11 : un autre client note ce produit, sans commentaire', pg_temp.colonne('avis', 'note'),
        $q$INSERT INTO avis (client_id, produit_id, note) VALUES (900002, 900001, 5)$q$, true);
    PERFORM pg_temp.tester(11, 'RG9  : un client peut noter plusieurs produits', pg_temp.colonne('avis', 'note'),
        $q$INSERT INTO avis (client_id, produit_id, note) VALUES (900001, 900004, 3)$q$, true);
END;
$do$;

INSERT INTO resultats
VALUES (12, 'Les clés étrangères produits.boutique_id et avis.produit_id sont indexées',
        pg_temp.indexee('produits', 'boutique_id') AND pg_temp.indexee('avis', 'produit_id'));

\set QUIET off
SELECT num AS "n°", CASE WHEN ok THEN 'OK' ELSE 'KO' END AS "résultat", test
FROM resultats ORDER BY num;

SELECT count(*) FILTER (WHERE ok) || ' tests réussis sur ' || count(*) AS bilan FROM resultats;

ROLLBACK;
