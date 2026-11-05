# Fiche PostgreSQL + JSONB

**Paradigme : relationnel, avec des documents dedans.** La question qu'il pose : *et si on n'ajoutait aucune base ?* PostgreSQL sait stocker et indexer du JSON. Jusqu'où ça suffit-il ?

---

## Lancer, se connecter

C'est la même base que PostgreSQL : utilisez le dossier `sgbd/postgres`.

```bash
cd sgbd/postgres
docker compose down -v      # repartir d'une base vide si la séance 1 a laissé des tables
docker compose up -d
docker compose exec db psql -U ombelle -d ombelle
```

Connexion depuis Python et client graphique : voir [la fiche PostgreSQL](../postgres/README.md).

## Quand s'en servir

Pour une partie des données dont la forme varie d'une ligne à l'autre (des attributs différents selon le type), à côté de tables classiques pour le reste. Ce que vous y perdez : rien ne garantit la forme ni le type de ce qu'il y a dans le `jsonb`.

## Charger un fichier JSON lines

Exemple avec `produits.jsonl` d'Ombelle, où chaque ligne est un objet JSON. On les charge d'abord bruts, puis on les range :

```sql
CREATE TEMP TABLE brut (doc jsonb);

-- Le format csv avec des séparateurs improbables : chaque ligne arrive entière, sans retouche.
COPY brut FROM '/donnees/produits.jsonl' WITH (FORMAT csv, QUOTE e'\x01', DELIMITER e'\x02');

SELECT doc->>'nom', doc->'attributs' FROM brut LIMIT 3;
```

À vous ensuite : `INSERT INTO produits (…) SELECT (doc->>'id')::int, …, doc->'attributs' FROM brut;`

## Ce qui vous attend

| Situation | Piste |
|---|---|
| Lire un attribut | `attributs->>'marque'` renvoie du texte, `attributs->'pages'` du JSON |
| Chercher dans les attributs | `WHERE attributs @> '{"electrique": true}'` |
| C'est lent | un index GIN : `CREATE INDEX ON produits USING gin (attributs jsonb_path_ops);` |
| Un attribut doit être un nombre | `(attributs->>'pages')::int` : rien ne garantit qu'il l'est, c'est le prix de la souplesse |

## Documentation

- [Les types JSON](https://www.postgresql.org/docs/16/datatype-json.html)
- [Fonctions et opérateurs JSON](https://www.postgresql.org/docs/16/functions-json.html)
- [Index GIN](https://www.postgresql.org/docs/16/gin.html)
