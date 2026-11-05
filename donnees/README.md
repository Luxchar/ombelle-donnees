# Les données d'Ombelle

```bash
python donnees/generer.py
```

Le script n'a besoin d'aucune bibliothèque. Il écrit une dizaine de fichiers dans `donnees/sortie/` (environ 40 Mo) et affiche à la fin une empreinte : **`8c9008a940a6`**. Si vous avez la même, vos données sont identiques à celles de tout le monde.

Les données s'arrêtent au **31 octobre 2026 à minuit**.

---

## Les fichiers

| Fichier | Lignes | Colonnes |
|---|---|---|
| `categories.csv` | 8 | `id`, `nom` |
| `boutiques.csv` | 300 | `id`, `nom`, `ville`, `ouverte_le` |
| `produits.csv` | 20 000 | `id`, `boutique_id`, `categorie_id`, `nom`, `prix`, `stock`, `cree_le` |
| `attributs_produits.csv` | 73 332 | `produit_id`, `cle`, `valeur` |
| `produits.jsonl` | 20 000 | un objet JSON par ligne : les colonnes de `produits.csv`, plus `attributs` |
| `clients.csv` | 50 000 | `id`, `prenom`, `nom`, `email`, `ville`, `inscrit_le` |
| `commandes.csv` | 200 000 | `id`, `client_id`, `passee_le`, `statut` |
| `lignes_commande.csv` | 395 762 | `commande_id`, `produit_id`, `quantite`, `prix_unitaire` |
| `avis.csv` | 80 000 | `id`, `produit_id`, `client_id`, `note`, `commentaire`, `publie_le` |
| `paniers.csv` | 11 185 | `client_id`, `produit_id`, `quantite`, `ajoute_le` |

Les mêmes attributs existent sous deux formes : `attributs_produits.csv` (une ligne par attribut, pour un modèle relationnel) et `produits.jsonl` (un objet par produit). Prenez celle qui convient à votre modèle.

## Ce qu'il faut savoir

- **Les attributs dépendent de la catégorie.** Un livre a un auteur et un nombre de pages ; un vélo a un type, une taille de cadre, et une autonomie s'il est électrique ; une enceinte a une liste de connectiques.
- **Le prix payé n'est pas toujours le prix du jour.** `lignes_commande.prix_unitaire` est le prix au moment de l'achat (promotion, ancien tarif) ; `produits.prix` est le prix actuel.
- **Le statut d'une commande** vaut `payee`, `expediee`, `livree` ou `annulee`. Le chiffre d'affaires ne compte pas les commandes annulées.
- **Seuls les acheteurs laissent un avis**, au plus un par produit.
- **Les numéros de commande suivent le temps** : plus le numéro est grand, plus la commande est récente.
- Dates au format `AAAA-MM-JJ` ou `AAAA-MM-JJ HH:MM:SS`, séparateur `,`, encodage UTF-8.

## Les identifiants cités dans le cours

| Identifiant | Rôle |
|---|---|
| Produit **4242** | la fiche produit, le panier, les recommandations |
| Client **1234** | un panier de trois produits, qui deviendra une commande |
| Client **2222** | un panier qui contient un produit épuisé |
| Client **777** | un client fidèle, pour l'historique des commandes |
