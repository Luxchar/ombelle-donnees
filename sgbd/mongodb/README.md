# Fiche MongoDB

**Paradigme : document.** Des objets JSON rangés dans des collections, sans schéma imposé. On peut imbriquer : une commande peut contenir ses lignes.

---

## Lancer, se connecter

```bash
cd sgbd/mongodb
docker compose up -d
docker compose ps                 # attendez « healthy » : le replica set est prêt
docker compose exec mongo mongosh ombelle
```

Avec MongoDB Compass : `mongodb://localhost:27017/?directConnection=true`

Depuis Python :

```bash
pip install pymongo
```

```python
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/?directConnection=true")
db = client.ombelle
print(db.produits.count_documents({}))
```

## Charger les données

`mongoimport` est dans le conteneur, les fichiers dans `/donnees` :

```bash
docker compose exec mongo mongoimport --db ombelle --collection produits_brut --file /donnees/produits.jsonl
docker compose exec mongo mongoimport --db ombelle --collection clients_brut --type csv --headerline --file /donnees/clients.csv
```

C'est un import **brut** : un document par ligne de fichier. Votre modèle sera sans doute différent (une commande qui contient ses lignes, un produit qui contient le nom de sa boutique…). Deux chemins :

- remodeler dans MongoDB, avec une agrégation qui se termine par `$merge` ou `$out` ;
- écrire un petit script Python qui lit les CSV, construit vos documents, et les insère par lots (`insert_many` de 5 000 documents).

## Ce qui vous attend

| Situation | Piste |
|---|---|
| Les dates importées depuis un CSV sont du texte | les convertir : `$dateFromString`, ou `datetime.fromisoformat` en Python |
| Imbriquer ou référencer ? | imbriquer ce qu'on lit toujours ensemble et qui ne grandit pas sans fin ; référencer le reste |
| Une requête lente | `.explain("executionStats")` : `COLLSCAN` veut dire « toute la collection a été lue » |
| Une opération qui touche plusieurs documents, tout ou rien | une transaction, possible ici grâce au replica set : `with client.start_session() as s, s.start_transaction(): …` (passez `session=s` à chaque opération) |

## Documentation

- [Modéliser des données](https://www.mongodb.com/docs/manual/data-modeling/)
- [Agrégation](https://www.mongodb.com/docs/manual/aggregation/)
- [Transactions](https://www.mongodb.com/docs/manual/core/transactions/)
- [PyMongo](https://pymongo.readthedocs.io/)
