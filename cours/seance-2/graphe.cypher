// Séance 2 · démo graphe avec Neo4j
//
// Depuis sgbd/neo4j, base lancée (docker compose up -d, une trentaine de secondes) :
//   docker compose exec neo4j cypher-shell -u neo4j -p ombelle2026 -f /cours/seance-2/graphe.cypher
// ou dans l'interface web, http://localhost:7474, requête par requête.
//
// Des nœuds (les choses) reliés par des relations (les liens). Les relations sont
// stockées comme des pointeurs : les suivre ne coûte rien, même sur plusieurs pas.

MATCH (n) DETACH DELETE n;

// 1 · Trois clients, quatre produits, et ce que chacun a acheté
CREATE (lea:Client {id: 1234, prenom: 'Léa'}),
       (tom:Client {id: 777, prenom: 'Tom'}),
       (ines:Client {id: 2222, prenom: 'Inès'}),
       (recueil:Produit {id: 4242, nom: 'Recueil bilingue'}),
       (essai:Produit {id: 3907, nom: 'Essai illustré'}),
       (manuel:Produit {id: 10398, nom: 'Manuel annoté'}),
       (vase:Produit {id: 12, nom: 'Vase Sauge'}),
       (lea)-[:A_ACHETE]->(recueil),
       (lea)-[:A_ACHETE]->(essai),
       (tom)-[:A_ACHETE]->(recueil),
       (tom)-[:A_ACHETE]->(essai),
       (tom)-[:A_ACHETE]->(manuel),
       (ines)-[:A_ACHETE]->(manuel),
       (ines)-[:A_ACHETE]->(vase);

// 2 · « Ceux qui ont acheté ce produit ont aussi acheté » : on suit les flèches
MATCH (:Produit {id: 4242})<-[:A_ACHETE]-(c:Client)-[:A_ACHETE]->(autre:Produit)
WHERE autre.id <> 4242
RETURN autre.nom AS produit, count(DISTINCT c) AS acheteurs_communs
ORDER BY acheteurs_communs DESC;

// 3 · Un pas de plus, sans jointure à écrire : ce qu'ont acheté les clients
//     qui ont un achat en commun avec Léa, et qu'elle n'a pas encore
MATCH (lea:Client {id: 1234})-[:A_ACHETE]->(:Produit)<-[:A_ACHETE]-(voisin:Client)-[:A_ACHETE]->(p:Produit)
WHERE NOT EXISTS { (lea)-[:A_ACHETE]->(p) }
RETURN p.nom AS suggestion, count(*) AS force
ORDER BY force DESC;
