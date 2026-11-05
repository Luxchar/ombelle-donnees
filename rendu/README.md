# <Votre sujet> · groupe <numéro>

<!-- Le squelette du dépôt de votre groupe. Remplacez tout ce qui est entre < >, supprimez ces commentaires. -->

<Prénom Nom>, <Prénom Nom>, <Prénom Nom> · Bachelor 3 · Conception et architecture des données · Ynov Paris, novembre 2026

<Le sujet en deux lignes : de quoi il s'agit, qui s'en sert.>

**Base de données** : <votre SGBD>, parce que <l'argument principal de votre ADR>.

| Fichier | Contenu |
|---|---|
| [`CONCEPTION.md`](CONCEPTION.md) | les règles de gestion, le MCD, le MLD, ce que le schéma ne garantit pas |
| [`docs/adr/`](docs/adr/) | notre choix de base |
| `modele/` | <en bonus : la création de la base (SQL ou ORM), le script de données, les requêtes ; sinon supprimez cette ligne> |
| `app/` | <en bonus : notre petite application ; sinon supprimez cette ligne> |

## En bonus : tout lancer, depuis zéro

<!-- Seulement si vous avez fait le bonus ; sinon supprimez cette partie. -->

```bash
# 1. La base
<docker compose up -d, la commande de votre fiche, ou comment vous l'avez installée>

# 2. Le modèle et les données
<la ou les commandes>

# 3. Les requêtes, l'application
<la commande>
```

## En bonus : nos requêtes et leur résultat

<Pour chacune : la question à laquelle elle répond, puis le résultat obtenu sur vos données (les premières lignes suffisent).>
