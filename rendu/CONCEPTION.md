# La conception

<!-- Étapes 1, 2 et 4 du TP. Remplacez tout ce qui est entre < >, supprimez ces commentaires. -->

## 1. Les règles de gestion

<!-- 8 à 12 règles, numérotées. Chacune dit un « au plus », un « au moins », un « toujours » ou un « facultatif ». -->

> **RG1.** …
> **RG2.** …

Les questions que nous nous sommes posées, et la réponse retenue :

| Question | Réponse | Ce que ça change dans le MCD |
|---|---|---|
| <Une catégorie peut-elle être vide ?> | <Oui : une catégorie se crée avant ses produits> | <0,n côté catégorie> |

## 2. Le MCD

<!-- En Mermaid, comme dans le cours, ou une image exportée (Looping, draw.io) dans docs/. -->

```mermaid
flowchart LR
    A["<b>ENTITÉ A</b><br>id<br>…"]
    R(["Association"])
    B["<b>ENTITÉ B</b><br>id<br>…"]
    A ---|"0,n"| R
    R ---|"1,1"| B
```

| Cardinalité | Règle |
|---|---|
| <un A … 0 à n B> | <RG2> |

## 3. Le MLD, dans <votre SGBD>

<!-- Le MCD traduit dans la base choisie dans votre ADR. En relationnel : les tables, clé primaire soulignée, clé étrangère précédée de #. En NoSQL : vos collections, clés, tables ou nœuds, avec un exemple de chacun. Avec plusieurs bases : une partie par base, et quelle donnée va où. -->

- A (<u>id</u>, …)
- …

| Association du MCD | Dans la base | Pourquoi |
|---|---|---|
| <Association, entre A et B> | <une clé étrangère #a_id dans B ; ou : les B imbriqués dans A> | <règle de passage : 1,1 côté B ; ou : on lit toujours A avec ses B> |

Ce que nous recopions exprès, et qui tient la copie à jour : <rien, ou la donnée et qui la met à jour>.

## 4. Ce que le schéma ne garantit pas

| Règle | Pourquoi le schéma ne suffit pas | Où nous la garantissons |
|---|---|---|
| <RG… : au moins un …> | | <une transaction, un trigger, le code> |

## 5. En bonus : la base créée, et les requêtes

<!-- Seulement si vous avez fait le bonus ; sinon supprimez cette partie. -->

<Comment la base est créée (SQL, schéma d'un ORM, script), et l'écart avec le MLD s'il y en a un.>

| Question de l'application | Requête (fichier dans `modele/`) |
|---|---|
| <la question 1> | |
| <la question 2> | |
| <la question 3> | |
