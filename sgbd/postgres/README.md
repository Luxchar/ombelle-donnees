# Fiche PostgreSQL

**Paradigme : relationnel.** Des tables, des clés, des jointures, des transactions ACID.

Ce dossier sert aussi à la séance 1.

---

## Lancer, se connecter

```bash
cd sgbd/postgres
docker compose up -d
docker compose exec db psql -U ombelle -d ombelle
```

| Client graphique (DBeaver, pgAdmin, extension VS Code) | |
|---|---|
| Hôte, port | `localhost`, `5432` |
| Base, utilisateur, mot de passe | `ombelle`, `ombelle`, `ombelle` |

**Sans Docker** : n'importe quel PostgreSQL 14 ou plus convient. Créez la base, puis lancez les fichiers depuis le dossier du dépôt :

```bash
psql -U postgres -c "CREATE DATABASE ombelle"
psql -U postgres -d ombelle -f cours/seance-1/coeur.sql
```

Dans les commandes Docker des supports, remplacez `docker compose exec db psql -U ombelle -d ombelle -f /cours/…` par `psql -U postgres -d ombelle -f cours/…`. Pour charger les données, `COPY … FROM '/donnees/…'` devient `\copy … FROM 'donnees/sortie/…'`, lancé dans `psql` depuis le dossier du dépôt.

Depuis Python :

```bash
pip install "psycopg[binary]"
```

```python
import psycopg
connexion = psycopg.connect("postgresql://ombelle:ombelle@localhost:5432/ombelle", autocommit=True)
print(connexion.execute("SELECT count(*) FROM clients").fetchone())
```

## Charger les données

Dans le conteneur, les fichiers générés sont dans `/donnees`. Une fois vos tables créées :

```sql
COPY clients FROM '/donnees/clients.csv' WITH (FORMAT csv, HEADER true);
```

Si une table n'a pas les mêmes colonnes que le fichier, nommez les colonnes : `COPY produits (id, boutique_id, …) FROM …`, ou passez par une table temporaire.

## Ce qui vous attend

| Situation | Piste |
|---|---|
| `port is already allocated` | un autre PostgreSQL occupe le port. `PORT_POSTGRES=5433 docker compose up -d` (PowerShell : `$env:PORT_POSTGRES=5433; docker compose up -d`) |
| Les tables de la séance 1 gênent | repartir de zéro : `docker compose down -v`, puis `up -d` |
| Une requête lente | `EXPLAIN ANALYZE` devant la requête : un `Seq Scan` sur une grosse table appelle souvent un index |
| Une opération qui touche plusieurs tables, tout ou rien | une transaction (`BEGIN` … `COMMIT`), ou une procédure |

## Documentation

- [COPY](https://www.postgresql.org/docs/16/sql-copy.html)
- [Index](https://www.postgresql.org/docs/16/indexes.html)
- [Transactions](https://www.postgresql.org/docs/16/tutorial-transactions.html)
