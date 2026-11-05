# Fiche Neo4j

**Paradigme : graphe.** Des nœuds reliés par des relations. Suivre une relation ne coûte presque rien, même sur plusieurs pas : c'est le terrain des recommandations, des réseaux, de la détection de fraude.

---

## Lancer, se connecter

```bash
cd sgbd/neo4j
docker compose up -d                 # une trentaine de secondes
```

Interface web : <http://localhost:7474>, utilisateur `neo4j`, mot de passe `ombelle2026`.

En ligne de commande :

```bash
docker compose exec neo4j cypher-shell -u neo4j -p ombelle2026
```

Depuis Python :

```bash
pip install neo4j
```

```python
from neo4j import GraphDatabase
pilote = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "ombelle2026"))
enregistrements, _, _ = pilote.execute_query("MATCH (n) RETURN count(n) AS n")
print(enregistrements[0]["n"])
```

## Charger les données

Les fichiers sont dans le dossier d'import de Neo4j. **Créez d'abord une contrainte d'unicité par type de nœud** : sans elle, chaque relation créée parcourt tous les nœuds.

```cypher
CREATE CONSTRAINT client_id IF NOT EXISTS FOR (c:Client) REQUIRE c.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM 'file:///clients.csv' AS l
CALL {
    WITH l
    CREATE (:Client {id: toInteger(l.id), prenom: l.prenom, ville: l.ville})
} IN TRANSACTIONS OF 10000 ROWS;
```

Dans l'interface web, préfixez une requête `IN TRANSACTIONS` par `:auto`. Dans `cypher-shell`, rien à ajouter.

## Ce qui vous attend

| Situation | Piste |
|---|---|
| Tout arrive en texte | `toInteger`, `toFloat`, `datetime(replace(l.passee_le, ' ', 'T'))` |
| Nœud ou propriété ? | ce qu'on traverse (client, produit, commande, boutique) est un nœud ; ce qu'on affiche est une propriété |
| Une requête lente | `PROFILE` devant la requête : `AllNodesScan` veut dire qu'il manque une contrainte ou un index |
| Les gros totaux (un chiffre d'affaires) | possible, mais regardez combien de nœuds il faut parcourir pour un simple total |

## Documentation

- [LOAD CSV](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/)
- [Modéliser un graphe](https://neo4j.com/docs/getting-started/data-modeling/)
- [Pilote Python](https://neo4j.com/docs/python-manual/current/)
