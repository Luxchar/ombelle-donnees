// Séance 2 · démo document avec MongoDB
//
// Depuis sgbd/mongodb, base lancée (docker compose up -d) :
//   docker compose exec mongo mongosh --quiet --file /cours/seance-2/document.js
//
// Un document, c'est un objet JSON. Les documents d'une même collection n'ont pas
// besoin d'avoir la même forme, et un document peut en contenir d'autres.

db = db.getSiblingDB("ombelle_demo");
db.dropDatabase();

print("\n== 1 · Trois produits, trois formes : aucun schéma imposé");
db.produits.insertMany([
  {
    _id: 4242, nom: "Recueil bilingue", prix: 42.99, stock: 156, categorie: "Livres",
    boutique: { id: 240, nom: "Cabane Basalte 9", ville: "Lille" },
    attributs: { auteur: "Léa Michel", editeur: "Marelle", pages: 697, langue: "français" }
  },
  {
    _id: 1504, nom: "Vélo Rando", prix: 1131.00, stock: 11, categorie: "Vélo",
    boutique: { id: 146, nom: "Galerie Caramel 6", ville: "Lyon" },
    attributs: { type: "route", taille_cadre: "S", vitesses: 12, electrique: true, autonomie_km: 60 }
  },
  {
    _id: 2962, nom: "Enceinte Mini", prix: 108.00, stock: 149, categorie: "Électronique",
    boutique: { id: 54, nom: "Échoppe Azur", ville: "Lyon" },
    attributs: { marque: "Ondine Audio", garantie_mois: 36, puissance_w: 5, connectique: ["USB-C", "Bluetooth"] }
  }
]);
printjson(db.produits.findOne({ _id: 4242 }));

print("\n== 2 · Chercher dans les attributs, quels qu'ils soient");
printjson(db.produits.find({ "attributs.electrique": true }, { nom: 1, prix: 1 }).toArray());
printjson(db.produits.find({ "attributs.connectique": "Bluetooth" }, { nom: 1 }).toArray());
db.produits.createIndex({ "attributs.marque": 1 });

print("\n== 3 · Une commande : les lignes sont imbriquées, avec le nom et le prix du jour recopiés");
db.commandes.insertOne({
  _id: 200001, client_id: 1234, passee_le: new Date("2026-11-10T10:12:00Z"), statut: "payee",
  lignes: [
    { produit_id: 12,   nom: "Vase Sauge",       quantite: 1, prix_unitaire: 8.00 },
    { produit_id: 439,  nom: "Manuel annoté",    quantite: 2, prix_unitaire: 19.99 },
    { produit_id: 3403, nom: "Pantalon Écume",   quantite: 1, prix_unitaire: 21.90 },
    { produit_id: 4242, nom: "Recueil bilingue", quantite: 2, prix_unitaire: 42.99 }
  ],
  total: 155.86
});
// Toute la commande en une seule lecture, sans jointure.
printjson(db.commandes.findOne({ _id: 200001 }));

print("\n== 4 · Le prix de l'imbrication : la boutique 240 change de nom");
// Son nom est recopié dans chacun de ses produits : il faut tous les mettre à jour.
// Ici un seul document ; dans Ombelle, la boutique 240 vend 62 produits.
printjson(db.produits.updateMany({ "boutique.id": 240 }, { $set: { "boutique.nom": "Cabane Basalte" } }));

print("\n== 5 · La question qu'on n'a pas prévue : qui a acheté le produit 4242 ?");
// Possible, mais sans index sur lignes.produit_id, MongoDB lit toutes les commandes.
printjson(db.commandes.find({ "lignes.produit_id": 4242 }, { client_id: 1 }).toArray());
db.commandes.createIndex({ "lignes.produit_id": 1 });
