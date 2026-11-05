# Fiche DuckDB

**Paradigme : colonne analytique (OLAP).** Une base embarquée, sans serveur : un fichier sur le disque, ouvert par votre programme. Elle range les données par colonne, ce qui rend les agrégats sur des millions de lignes très rapides. C'est le cousin « analyse » de SQLite.

---

## Lancer, se connecter

Pas de Docker : DuckDB s'installe comme une bibliothèque.

```bash
pip install duckdb
```

```python
import duckdb
con = duckdb.connect("ombelle.duckdb")       # le fichier est créé s'il n'existe pas
print(con.execute("SELECT 42").fetchone())
```

Pour explorer à la main : le client en ligne de commande (`duckdb ombelle.duckdb`, voir duckdb.org) ou DBeaver.

## Charger les données

DuckDB lit les CSV et le JSON directement :

```sql
CREATE TABLE commandes AS SELECT * FROM read_csv('../../donnees/sortie/commandes.csv');
```

Pour `produits.jsonl`, regardez ce que donne `read_json_auto` sur la colonne `attributs`, puis comparez avec une lecture où vous imposez le type :

```sql
SELECT id, attributs
FROM read_json('../../donnees/sortie/produits.jsonl',
               columns = {id: 'INTEGER', nom: 'VARCHAR', attributs: 'JSON'});
```

La différence entre les deux dit beaucoup de ce que DuckDB devine, et de ce qu'il faut lui imposer.

## Ce qui vous attend

| Situation | Piste |
|---|---|
| `Could not set lock on file` | un seul programme peut écrire dans le fichier : fermez le client avant de lancer le script |
| Les petites écritures | elles marchent, mais ce n'est pas le terrain de DuckDB : mesurez, et dites pourquoi |
| Plusieurs utilisateurs en même temps | DuckDB vit dans un seul processus : c'est une base d'analyse, pas la base d'un site |

## Documentation

- [Lire des CSV](https://duckdb.org/docs/stable/data/csv/overview)
- [Lire du JSON](https://duckdb.org/docs/stable/data/json/overview)
- [API Python](https://duckdb.org/docs/stable/clients/python/overview)
