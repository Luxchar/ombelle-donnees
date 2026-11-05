# Fiche Redis

**Paradigme : clé-valeur, en mémoire.** On lit et on écrit par la clé, en une fraction de milliseconde. Redis ne cherche jamais dans les valeurs : tout le modèle est dans le nom des clés et le choix des structures (chaîne, hash, liste, set, sorted set).

---

## Lancer, se connecter

```bash
cd sgbd/redis
docker compose up -d
docker compose exec redis redis-cli
```

Client graphique : Redis Insight (gratuit), sur `localhost:6379`.

Depuis Python :

```bash
pip install redis
```

```python
import redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r.set("bonjour", "Ombelle")
print(r.get("bonjour"))
```

## Charger les données

Redis n'importe pas de CSV. On écrit un script Python qui lit les fichiers et envoie les écritures **par paquets**, sinon chaque écriture attend sa réponse :

```python
import csv
pipe = r.pipeline(transaction=False)
with open("../../donnees/sortie/produits.csv", encoding="utf-8") as f:
    for i, ligne in enumerate(csv.DictReader(f), start=1):
        pipe.hset(f"produit:{ligne['id']}", mapping=ligne)
        if i % 10_000 == 0:
            pipe.execute()
pipe.execute()
```

Ne chargez pas tout « au cas où » : chargez ce dont vos requêtes ont besoin, sous la forme dont elles ont besoin. Pour le reporting ou les recommandations, ça veut dire **calculer à l'avance** pendant le chargement.

## Ce qui vous attend

| Situation | Piste |
|---|---|
| « Tous les … qui … » | impossible directement : un index que vous tenez à jour vous-même (un set, un sorted set) |
| La mémoire | tout est en RAM : `INFO memory`, ligne `used_memory_human` |
| `KEYS *` | bloque le serveur sur une grosse base : `SCAN` à la place |
| Une opération tout ou rien | `MULTI` … `EXEC` regroupe, mais **n'annule rien** si une règle métier échoue. Voir `WATCH`, ou un script Lua (`EVAL`) qui vérifie puis écrit |

## Documentation

- [Les types de données](https://redis.io/docs/latest/develop/data-types/)
- [Transactions](https://redis.io/docs/latest/develop/interact/transactions/)
- [Scripts Lua](https://redis.io/docs/latest/develop/interact/programmability/eval-intro/)
- [redis-py](https://redis.readthedocs.io/)
