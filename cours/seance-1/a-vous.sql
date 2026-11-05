-- Séance 1 · À vous : les boutiques et les avis
--
-- Complétez les ___ à partir de votre MLD, puis lancez le fichier après coeur.sql :
--
--   docker compose exec db psql -U ombelle -d ombelle -f /cours/seance-1/a-vous.sql
--   docker compose exec db psql -U ombelle -d ombelle -f /cours/seance-1/verifier.sql
--
-- Pour recommencer : relancez coeur.sql, puis ce fichier.

-- RG7 : une boutique a un nom, unique sur la plateforme, une ville et une date d'ouverture.
CREATE TABLE boutiques (
    id          serial PRIMARY KEY,
    nom         text NOT NULL ___,
    ville       text NOT NULL,
    ouverte_le  date NOT NULL
);

-- RG8 : un produit est vendu par une seule boutique ; une boutique vend de 0 à n produits.
ALTER TABLE produits ADD COLUMN boutique_id integer NOT NULL REFERENCES ___ (id);

-- RG9  : un client donne au plus un avis par produit.
-- RG10 : la note va de 1 à 5.
-- RG11 : le commentaire est facultatif ; la date de publication est obligatoire.
CREATE TABLE avis (
    client_id    integer NOT NULL REFERENCES ___ (id),
    produit_id   integer NOT NULL REFERENCES ___ (id),
    note         smallint NOT NULL CHECK (___),
    commentaire  text,
    publie_le    timestamp NOT NULL DEFAULT now(),
    PRIMARY KEY (___)
);

-- Les clés étrangères qui ne sont pas déjà en tête d'une clé primaire.
CREATE INDEX ON produits (___);
CREATE INDEX ON avis (___);
