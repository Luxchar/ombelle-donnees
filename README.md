# Ombelle : les données du module Conception et architecture des données

Le dépôt du module **Conception et architecture des données** (Bachelor 3, Ynov Paris, novembre 2026).

**Ombelle** est une place de marché en ligne fictive, un Amazon en version simplifiée : 300 boutiques indépendantes y vendent 20 000 produits (vêtements, livres, vélos, épicerie…) à 50 000 clients. Les deux séances de TD s'appuient sur elle : on la modélise en relationnel en séance 1, on la découpe entre plusieurs bases en séance 2. Au TP, chaque groupe travaille sur son propre sujet.

```
donnees/    le générateur des données (python donnees/generer.py)
cours/      les scripts des séances 1 et 2
sgbd/       un dossier par SGBD : Docker et fiche de démarrage
rendu/      le squelette du dépôt de votre groupe, pour le TP
```

---

## Ce qu'il faut

- **Git** et **Docker** (Docker Desktop sous Windows et macOS) ;
- **Python 3.10 ou plus**, pour générer les données.

```bash
git clone https://github.com/Luxchar/ombelle-donnees.git
cd ombelle-donnees
```

## Séance 1 : le schéma relationnel

```bash
cd sgbd/postgres
docker compose up -d
docker compose exec db psql -U ombelle -d ombelle -f /cours/seance-1/coeur.sql
```

Puis l'exercice : compléter `cours/seance-1/a-vous.sql`, le lancer, et le vérifier.

```bash
docker compose exec db psql -U ombelle -d ombelle -f /cours/seance-1/a-vous.sql
docker compose exec db psql -U ombelle -d ombelle -f /cours/seance-1/verifier.sql
```

## Séance 2 : un exercice, quatre exemples à essayer

L'exercice « Le fichier des retours » : `cours/seance-2/retours.csv`, à ouvrir dans un tableur, ou à charger dans PostgreSQL (base de la séance 1 lancée) :

```bash
cd sgbd/postgres
docker compose exec db psql -U ombelle -d ombelle -f /cours/seance-2/retours.sql
```

Les exemples des quatre familles NoSQL du support, en version complète, à essayer chez vous :

| Fichier | Famille | SGBD |
|---|---|---|
| `cours/seance-2/document.js` | document | MongoDB |
| `cours/seance-2/cle-valeur.redis` | clé-valeur | Redis |
| `cours/seance-2/colonne.cql` | colonne large | Cassandra |
| `cours/seance-2/graphe.cypher` | graphe | Neo4j |

Chacune indique en tête comment la lancer, depuis le dossier `sgbd/` du SGBD concerné.

## Les données d'Ombelle

```bash
python donnees/generer.py
```

Une quinzaine de secondes. L'empreinte affichée à la fin doit être **`8c9008a940a6`** : vous avez alors exactement les mêmes données que tout le monde. Le détail des fichiers est dans [`donnees/README.md`](donnees/README.md).

## Le TP : votre sujet, votre base

Le sujet est sur Moodle. Ce dépôt vous sert de deux façons.

1. **Les fiches des SGBD**, dans `sgbd/` : lancement avec Docker, connexion, chargement, pièges connus. Partez du `docker-compose.yml` de la base que vous choisissez.

   | SGBD | Paradigme | Fiche |
   |---|---|---|
   | PostgreSQL | relationnel | [`sgbd/postgres`](sgbd/postgres/README.md) |
   | PostgreSQL + JSONB | relationnel et document | [`sgbd/postgres-jsonb`](sgbd/postgres-jsonb/README.md) |
   | MongoDB | document | [`sgbd/mongodb`](sgbd/mongodb/README.md) |
   | Redis | clé-valeur | [`sgbd/redis`](sgbd/redis/README.md) |
   | Cassandra | colonne large | [`sgbd/cassandra`](sgbd/cassandra/README.md) |
   | Neo4j | graphe | [`sgbd/neo4j`](sgbd/neo4j/README.md) |
   | DuckDB | colonne analytique | [`sgbd/duckdb`](sgbd/duckdb/README.md) |

   Pour charger vos propres fichiers dans un conteneur : `docker compose cp mon_fichier.csv <service>:/tmp/`, ou un script Python qui se connecte depuis votre machine.

2. **Le squelette de votre dépôt**, dans `rendu/` : copiez son contenu dans le dépôt de votre groupe. Pour le bonus, `donnees/generer.py` est un exemple à suivre pour générer vos données : une graine fixe, des volumes réglables, des fichiers CSV en sortie.

## Récupérer une mise à jour, repartir de zéro

```bash
git pull                    # un fichier a été corrigé
docker compose down -v      # dans un dossier sgbd/… : efface la base, puis docker compose up -d
```

## En cas de souci

| Symptôme | Solution |
|---|---|
| `port is already allocated` | un autre service occupe le port. Chaque fichier `docker-compose.yml` accepte une variable : `PORT_POSTGRES`, `PORT_MONGO`, `PORT_REDIS`, `PORT_CASSANDRA`, `PORT_NEO4J`. Sous PowerShell : `$env:PORT_POSTGRES=5433; docker compose up -d` |
| `python` introuvable sous Windows | essayez `py donnees/generer.py` |
| L'empreinte n'est pas la bonne | vérifiez la version de Python (`python --version`, 3.10 ou plus) et que `generer.py` n'a pas été modifié (`git status`) |
| La machine rame | une seule base lancée à la fois : `docker compose down` dans les autres dossiers |
