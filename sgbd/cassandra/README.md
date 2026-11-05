# Fiche Cassandra

**Paradigme : colonne large.** Des tables rangées par partition, réparties sur plusieurs machines, qui encaissent des écritures massives. Pas de jointure : on conçoit **une table par requête**, et on accepte de dupliquer.

---

## Lancer, se connecter

Cassandra demande environ 2 Go de mémoire libre et une à deux minutes de démarrage.

```bash
cd sgbd/cassandra
docker compose up -d
docker compose ps                  # attendez « healthy »
docker compose exec cassandra cqlsh
```

Depuis Python :

```bash
pip install cassandra-driver
```

```python
from cassandra.cluster import Cluster
session = Cluster(["127.0.0.1"]).connect()
print(session.execute("SELECT release_version FROM system.local").one())
```

Si l'installation du pilote échoue sous Windows : essayez `pip install scylla-driver` (même interface), ou travaillez depuis WSL.

## Charger les données

`cqlsh` sait charger un CSV dont les colonnes correspondent à la table :

```sql
COPY ombelle.ma_table (col1, col2, col3) FROM '/donnees/mon_fichier.csv' WITH HEADER = true;
```

Mais vos tables auront la forme de vos requêtes, pas celle des fichiers (Cassandra ne fait pas de jointure). Le chemin le plus court : **préparer avec Python ou DuckDB des CSV qui ont la forme de vos tables**, puis les charger avec `COPY FROM`. Ou insérer depuis Python avec une requête préparée et `execute_concurrent_with_args`.

## Ce qui vous attend

| Situation | Piste |
|---|---|
| `ALLOW FILTERING` | Cassandra vous prévient qu'elle va tout lire. C'est le signe qu'il manque une table |
| Pas de `GROUP BY` libre, pas de jointure | calculer à l'écriture : compteurs (`counter`), tables pré-agrégées |
| Clé de partition | choisissez-la pour que chaque requête lise **une seule** partition, de taille raisonnable |
| Une opération tout ou rien | pas de transaction sur plusieurs partitions. `IF` (transaction légère) ne protège qu'une ligne ; un `BATCH` est atomique mais ne vérifie rien. Que garantissez-vous vraiment ? |

## Documentation

- [Modéliser pour Cassandra](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/index.html)
- [CQL](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/index.html)
- [COPY dans cqlsh](https://cassandra.apache.org/doc/latest/cassandra/managing/tools/cqlsh.html)
