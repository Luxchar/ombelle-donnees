#!/usr/bin/env python3
"""Génère les données de la boutique Ombelle.

Ombelle est une place de marché en ligne fictive : 300 boutiques indépendantes
y vendent 20 000 produits à 50 000 clients. Les données s'arrêtent au
31 octobre 2026.

Aucune dépendance : Python 3.10 ou plus suffit.

    python generer.py

Les fichiers sont écrits dans le dossier sortie/. La graine est fixe : tout le
monde obtient exactement les mêmes données, et donc les mêmes résultats aux
vérifications du cours. Le script affiche une empreinte à la fin : comparez-la
à celle du README.
"""

import bisect
import csv
import hashlib
import json
import os
import random
import unicodedata
from datetime import date, datetime, timedelta

GRAINE = 2026
SORTIE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sortie")

N_BOUTIQUES = 300
N_PRODUITS = 20_000
N_CLIENTS = 50_000
N_COMMANDES = 200_000
N_AVIS = 80_000
N_PANIERS = 5_000

DEBUT = datetime(2025, 1, 1)
FIN = datetime(2026, 10, 31, 23, 59, 59)

# Les cas du TP : ces identifiants sont cités dans le sujet.
PRODUIT_VEDETTE = 4242      # la fiche produit, le panier, les recommandations
CLIENT_PANIER = 1234        # le panier qui devient une commande
CLIENT_BLOQUE = 2222        # le panier qui contient un produit épuisé
CLIENT_FIDELE = 777         # l'historique des commandes

rng = random.Random(GRAINE)


# ---------------------------------------------------------------------------
# Les listes de mots
# ---------------------------------------------------------------------------

PRENOMS = (
    "Léa Emma Chloé Manon Inès Jade Louise Alice Lina Rose Anna Mila Ambre Julia "
    "Zoé Lou Sarah Nina Camille Eva Lucas Hugo Louis Gabriel Arthur Jules Adam "
    "Raphaël Nathan Léo Ethan Paul Noah Sacha Tom Malo Yanis Nolan Amir Rayan "
    "Karim Mehdi Sofiane Aya Yasmine Fatou Moussa Ibrahim Kenza Wassim"
).split()

NOMS = (
    "Martin Bernard Dubois Thomas Robert Richard Petit Durand Leroy Moreau Simon "
    "Laurent Lefebvre Michel Garcia David Bertrand Roux Vincent Fournier Morel "
    "Girard André Mercier Dupont Lambert Bonnet François Martinez Legrand Garnier "
    "Faure Rousseau Blanc Guerin Muller Henry Roussel Nicolas Perrin Morin Mathieu "
    "Clement Gauthier Diallo Benali Nguyen Traoré Haddad Kone"
).split()

VILLES = [
    ("Paris", 30), ("Lyon", 9), ("Marseille", 8), ("Toulouse", 7), ("Nantes", 6),
    ("Bordeaux", 6), ("Lille", 6), ("Rennes", 5), ("Strasbourg", 5),
    ("Montpellier", 5), ("Nice", 4), ("Grenoble", 3), ("Dijon", 2), ("Brest", 2),
    ("Tours", 2), ("Rouen", 2), ("Nanterre", 2), ("Angers", 2), ("Clermont-Ferrand", 2),
    ("Limoges", 1),
]

MOTS_BOUTIQUE_1 = "Atelier Maison Comptoir Fabrique Boutique Galerie Cabane Repaire Studio Échoppe".split()
MOTS_BOUTIQUE_2 = (
    "Lune Sauge Hibou Marelle Baobab Cerise Ondine Lichen Corail Brindille Mistral "
    "Pivoine Bruyère Écume Ardoise Noisette Grenade Zéphyr Caramel Basalte Tilleul "
    "Ocre Azur Nacre Cobalt"
).split()

COMMENTAIRES = {
    1: ["Très déçu.", "Produit arrivé abîmé.", "Ne correspond pas à la description.", "À éviter."],
    2: ["Bof.", "Qualité moyenne pour le prix.", "Livraison très lente.", "Pas convaincu."],
    3: ["Correct, sans plus.", "Fait le travail.", "Conforme, mais un peu cher.", "Moyen."],
    4: ["Bon produit.", "Satisfait, je recommande.", "Bonne qualité, livraison rapide.", "Très bien."],
    5: ["Parfait !", "Excellent, je rachèterai.", "Superbe qualité.", "Rien à redire, merci la boutique."],
}


def attributs_vetements():
    return {
        "taille": rng.choice(["XS", "S", "M", "L", "XL", "XXL"]),
        "couleur": rng.choice(["noir", "blanc", "bleu", "vert", "écru", "rouge", "gris"]),
        "matiere": rng.choice(["coton bio", "laine", "lin", "polyester recyclé", "chanvre"]),
    }


def attributs_livres():
    return {
        "auteur": f"{rng.choice(PRENOMS)} {rng.choice(NOMS)}",
        "editeur": rng.choice(["Éditions du Lichen", "Marelle", "Le Baobab", "Pivoine", "Ardoise"]),
        "pages": rng.randint(80, 900),
        "langue": rng.choice(["français"] * 6 + ["anglais", "espagnol"]),
    }


def attributs_maison():
    return {
        "matiere": rng.choice(["chêne", "céramique", "verre", "lin", "métal", "rotin"]),
        "couleur": rng.choice(["naturel", "blanc", "noir", "terracotta", "sauge"]),
        "dimensions_cm": [rng.randint(10, 120), rng.randint(10, 120), rng.randint(2, 80)],
    }


def attributs_electronique():
    connectique = ["USB-C", "Bluetooth", "Wi-Fi", "jack 3,5 mm", "HDMI"]
    n = rng.randint(1, 3)
    choisies = []
    while len(choisies) < n:
        c = rng.choice(connectique)
        if c not in choisies:
            choisies.append(c)
    return {
        "marque": rng.choice(["Voltaïc", "Nébula", "Kestrel", "Ondine Audio", "Pixelis"]),
        "garantie_mois": rng.choice([12, 24, 24, 36]),
        "puissance_w": rng.choice([5, 10, 20, 45, 65, 100]),
        "connectique": choisies,
    }


def attributs_velo():
    electrique = rng.random() < 0.4
    a = {
        "type": rng.choice(["ville", "route", "VTT", "gravel", "cargo"]),
        "taille_cadre": rng.choice(["S", "M", "L", "XL"]),
        "vitesses": rng.choice([1, 3, 7, 8, 11, 12]),
        "electrique": electrique,
    }
    if electrique:
        a["autonomie_km"] = rng.choice([40, 60, 80, 100, 120])
    return a


def attributs_beaute():
    return {
        "contenance_ml": rng.choice([15, 30, 50, 100, 200, 250]),
        "type_peau": rng.choice(["tous types", "sèche", "grasse", "sensible", "mixte"]),
        "bio": rng.random() < 0.6,
    }


def attributs_jeux():
    jmin = rng.randint(1, 3)
    return {
        "age_min": rng.choice([3, 6, 8, 10, 12, 14]),
        "joueurs_min": jmin,
        "joueurs_max": jmin + rng.randint(1, 6),
        "duree_min": rng.choice([10, 20, 30, 45, 60, 90, 120]),
    }


def attributs_epicerie():
    return {
        "poids_g": rng.choice([100, 125, 250, 500, 750, 1000]),
        "origine": rng.choice(["France", "Italie", "Espagne", "Maroc", "Pérou", "Vietnam"]),
        "bio": rng.random() < 0.5,
        "dlc_jours": rng.choice([7, 30, 90, 180, 365, 730]),
    }


# id, nom, prix min, prix max, noms, adjectifs, attributs
CATEGORIES = [
    (1, "Vêtements", 12, 140,
     "Pull Chemise Robe Veste Tee-shirt Pantalon Écharpe Bonnet Gilet Jupe".split(),
     "Lune Sauge Mistral Corail Brume Ardoise Noisette Écume".split(), attributs_vetements),
    (2, "Livres", 6, 45,
     "Roman Essai Recueil Album Guide Carnet Atlas Manuel".split(),
     "illustré poche relié collector annoté bilingue".split(), attributs_livres),
    (3, "Maison", 8, 320,
     "Lampe Vase Tapis Coussin Étagère Plaid Miroir Bougie Tabouret Panier".split(),
     "Bruyère Tilleul Basalte Ocre Nacre Rotin Grenade Sauge".split(), attributs_maison),
    (4, "Électronique", 15, 650,
     "Enceinte Casque Chargeur Lampe Station Clavier Souris Écran Batterie Radio".split(),
     "Nomade Studio Pro Mini Max Air Zen Flux".split(), attributs_electronique),
    (5, "Vélo", 25, 2400,
     "Vélo Casque Antivol Sacoche Pompe Éclairage Selle Panier Garde-boue".split(),
     "Urbain Gravel Cargo Sprint Rando Évasion Azur Cobalt".split(), attributs_velo),
    (6, "Beauté", 5, 90,
     "Savon Crème Huile Baume Sérum Shampoing Masque Gommage".split(),
     "Amande Karité Lavande Argile Rose Calendula Néroli Avoine".split(), attributs_beaute),
    (7, "Jeux", 8, 120,
     "Puzzle Jeu Casse-tête Coffret Cartes Dés Plateau Escape".split(),
     "Hibou Baobab Marelle Zéphyr Pirate Galaxie Château Dragon".split(), attributs_jeux),
    (8, "Épicerie", 3, 45,
     "Thé Café Miel Chocolat Confiture Huile Épices Biscuits Pâtes Riz".split(),
     "fumé doux corsé épicé vanillé noir blanc fruité".split(), attributs_epicerie),
]


def sans_accents(texte):
    texte = unicodedata.normalize("NFD", texte)
    return "".join(c for c in texte if unicodedata.category(c) != "Mn").lower().replace(" ", "")


def date_entre(a, b):
    secondes = int((b - a).total_seconds())
    return a + timedelta(seconds=rng.randint(0, secondes))


def prix_rond(x):
    centimes = rng.choice([0, 50, 90, 99])
    return round(int(x) + centimes / 100, 2)


def poids_saison(d):
    """Plus de commandes en novembre-décembre, et une activité qui grandit."""
    saison = {11: 1.6, 12: 1.9, 1: 0.9, 7: 0.8, 8: 0.7}.get(d.month, 1.0)
    croissance = 0.7 + 0.6 * (d - DEBUT).days / (FIN - DEBUT).days
    return saison * croissance


# ---------------------------------------------------------------------------
# Génération
# ---------------------------------------------------------------------------

def generer():
    os.makedirs(SORTIE, exist_ok=True)

    # Catégories
    categories = [{"id": c[0], "nom": c[1]} for c in CATEGORIES]
    par_id_cat = {c[0]: c for c in CATEGORIES}

    # Boutiques
    boutiques = []
    noms_vus = set()
    for i in range(1, N_BOUTIQUES + 1):
        while True:
            nom = f"{rng.choice(MOTS_BOUTIQUE_1)} {rng.choice(MOTS_BOUTIQUE_2)}"
            if nom not in noms_vus:
                break
            nom = f"{nom} {rng.randint(2, 9)}"
            if nom not in noms_vus:
                break
        noms_vus.add(nom)
        boutiques.append({
            "id": i,
            "nom": nom,
            "ville": rng.choices([v for v, _ in VILLES], [p for _, p in VILLES])[0],
            "specialite_id": rng.randint(1, 8),
            "ouverte_le": date_entre(datetime(2018, 1, 1), datetime(2024, 12, 31)).date(),
        })

    # Produits
    produits = []
    produits_par_cat = {c[0]: [] for c in CATEGORIES}
    for i in range(1, N_PRODUITS + 1):
        b = boutiques[rng.randint(0, N_BOUTIQUES - 1)]
        cat_id = b["specialite_id"] if rng.random() < 0.8 else rng.randint(1, 8)
        _, _, pmin, pmax, mots, adjs, gen_attr = par_id_cat[cat_id]
        stock = 0 if rng.random() < 0.03 else rng.randint(1, 200)
        ouverte = datetime.combine(b["ouverte_le"], datetime.min.time())
        produits.append({
            "id": i,
            "boutique_id": b["id"],
            "categorie_id": cat_id,
            "nom": f"{rng.choice(mots)} {rng.choice(adjs)}",
            "prix": prix_rond(pmin + (pmax - pmin) * rng.random() ** 2),
            "stock": stock,
            "cree_le": date_entre(max(ouverte, datetime(2022, 1, 1)), datetime(2026, 9, 30)).date(),
            "attributs": gen_attr(),
            "qualite": 2.8 + 2.0 * rng.random(),       # cachée : sert aux notes des avis
        })
        produits_par_cat[cat_id].append(i)

    # Popularité : quelques produits très demandés, une longue traîne.
    rangs = list(range(1, N_PRODUITS + 1))
    rng.shuffle(rangs)
    j = rangs.index(20)                          # le produit vedette prend le rang 20
    rangs[j] = rangs[PRODUIT_VEDETTE - 1]
    rangs[PRODUIT_VEDETTE - 1] = 20
    poids = [1 / (r ** 0.9) for r in rangs]
    cumul = []
    total = 0.0
    for p in poids:
        total += p
        cumul.append(total)
    ids_produits = list(range(1, N_PRODUITS + 1))

    def produit_populaire():
        return rng.choices(ids_produits, cum_weights=cumul)[0]

    # Chaque produit a trois compagnons : ce qu'on achète souvent avec lui.
    compagnons = {}
    for p in produits:
        liste = produits_par_cat[p["categorie_id"]]
        compagnons[p["id"]] = [liste[rng.randint(0, len(liste) - 1)] for _ in range(3)]

    # Clients
    clients = []
    for i in range(1, N_CLIENTS + 1):
        prenom = rng.choice(PRENOMS)
        nom = rng.choice(NOMS)
        clients.append({
            "id": i,
            "prenom": prenom,
            "nom": nom,
            "email": f"{sans_accents(prenom)}.{sans_accents(nom)}.{i}@exemple.fr",
            "ville": rng.choices([v for v, _ in VILLES], [p for _, p in VILLES])[0],
            "inscrit_le": date_entre(datetime(2022, 6, 1), datetime(2026, 9, 30)),
        })

    # Activité des clients : quelques gros acheteurs.
    activite = [min(rng.paretovariate(1.6), 20.0) for _ in range(N_CLIENTS)]
    activite[CLIENT_FIDELE - 1] = 16.0

    # Les dates d'abord, triées : les numéros de commande suivent le temps.
    dates = []
    while len(dates) < N_COMMANDES:
        d = date_entre(DEBUT, FIN)
        if rng.random() * 2.2 < poids_saison(d):
            dates.append(d)
    dates.sort()

    # À une date donnée, seuls les clients déjà inscrits peuvent commander.
    ordre = sorted(range(N_CLIENTS), key=lambda k: clients[k]["inscrit_le"])
    inscriptions = [clients[k]["inscrit_le"] for k in ordre]
    cumul_inscrits = []
    total = 0.0
    for k in ordre:
        total += activite[k]
        cumul_inscrits.append(total)

    # Commandes et lignes
    commandes = []
    lignes = []
    achats = []          # (client_id, produit_id, date) des commandes livrées, pour les avis
    for i, d in enumerate(dates, start=1):
        n_inscrits = bisect.bisect_right(inscriptions, d)
        x = rng.random() * cumul_inscrits[n_inscrits - 1]
        client = clients[ordre[bisect.bisect_left(cumul_inscrits, x)]]
        age = (FIN - d).days
        if age < 3:
            statut = "payee"
        elif age < 10:
            statut = rng.choice(["payee", "expediee", "expediee"])
        else:
            statut = "livree"
        if rng.random() < 0.05:
            statut = "annulee"
        commandes.append({"id": i, "client_id": client["id"], "passee_le": d, "statut": statut})

        n = rng.choices([1, 2, 3, 4, 5], [45, 28, 15, 8, 4])[0]
        dans_commande = []
        while len(dans_commande) < n:
            if dans_commande and rng.random() < 0.45:
                base = dans_commande[rng.randint(0, len(dans_commande) - 1)]
                p_id = compagnons[base][rng.randint(0, 2)]
            else:
                p_id = produit_populaire()
            if p_id in dans_commande:
                continue
            dans_commande.append(p_id)
            prix_actuel = produits[p_id - 1]["prix"]
            facteur = rng.choice([1.0] * 7 + [0.9, 0.85, 1.1])
            lignes.append({
                "commande_id": i,
                "produit_id": p_id,
                "quantite": rng.choices([1, 2, 3], [80, 15, 5])[0],
                "prix_unitaire": round(prix_actuel * facteur, 2),
            })
            if statut == "livree":
                achats.append((client["id"], p_id, d))

    # Avis : seuls les acheteurs notent, une fois par produit.
    avis = []
    deja = set()
    while len(avis) < N_AVIS:
        c_id, p_id, d = achats[rng.randint(0, len(achats) - 1)]
        if (c_id, p_id) in deja:
            continue
        deja.add((c_id, p_id))
        q = produits[p_id - 1]["qualite"]
        note = max(1, min(5, round(q + rng.uniform(-1.6, 1.6))))
        publie = d + timedelta(days=rng.randint(3, 40), seconds=rng.randint(0, 86_399))
        avis.append({
            "id": len(avis) + 1,
            "produit_id": p_id,
            "client_id": c_id,
            "note": note,
            "commentaire": rng.choice(COMMENTAIRES[note]),
            "publie_le": min(publie, FIN),
        })

    # Paniers en cours
    paniers = []
    clients_panier = set()
    while len(clients_panier) < N_PANIERS:
        c_id = rng.randint(1, N_CLIENTS)
        if c_id in (CLIENT_PANIER, CLIENT_BLOQUE):
            continue
        clients_panier.add(c_id)
    for c_id in sorted(clients_panier):
        contenu = []
        for _ in range(rng.choices([1, 2, 3, 4, 5], [35, 30, 18, 10, 7])[0]):
            p_id = produit_populaire()
            if p_id not in contenu:
                contenu.append(p_id)
        for p_id in contenu:
            paniers.append({
                "client_id": c_id,
                "produit_id": p_id,
                "quantite": rng.choices([1, 2, 3], [80, 15, 5])[0],
                "ajoute_le": date_entre(datetime(2026, 10, 1), FIN),
            })

    # Les deux paniers du TP, posés à la main.
    en_stock = [p["id"] for p in produits if p["stock"] >= 20 and p["id"] != PRODUIT_VEDETTE]
    epuises = [p["id"] for p in produits if p["stock"] == 0]
    for p_id, q in ((en_stock[10], 1), (en_stock[400], 2), (en_stock[3000], 1)):
        paniers.append({"client_id": CLIENT_PANIER, "produit_id": p_id, "quantite": q,
                        "ajoute_le": datetime(2026, 10, 30, 18, 12, 0)})
    for p_id, q in ((en_stock[50], 1), (epuises[5], 1)):
        paniers.append({"client_id": CLIENT_BLOQUE, "produit_id": p_id, "quantite": q,
                        "ajoute_le": datetime(2026, 10, 31, 9, 40, 0)})
    paniers.sort(key=lambda l: (l["client_id"], l["produit_id"]))

    return categories, boutiques, produits, clients, commandes, lignes, avis, paniers


# ---------------------------------------------------------------------------
# Écriture
# ---------------------------------------------------------------------------

def texte(v):
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(v, date):
        return v.isoformat()
    return v


def ecrire_csv(nom, colonnes, lignes):
    chemin = os.path.join(SORTIE, nom)
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(colonnes)
        for l in lignes:
            w.writerow([texte(l[c]) for c in colonnes])
    return chemin


def ecrire_jsonl(nom, objets):
    chemin = os.path.join(SORTIE, nom)
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        for o in objets:
            f.write(json.dumps({k: texte(v) for k, v in o.items()}, ensure_ascii=False) + "\n")
    return chemin


def main():
    categories, boutiques, produits, clients, commandes, lignes, avis, paniers = generer()

    fichiers = [
        ecrire_csv("categories.csv", ["id", "nom"], categories),
        ecrire_csv("boutiques.csv", ["id", "nom", "ville", "ouverte_le"], boutiques),
        ecrire_csv("produits.csv",
                   ["id", "boutique_id", "categorie_id", "nom", "prix", "stock", "cree_le"], produits),
        ecrire_csv("attributs_produits.csv", ["produit_id", "cle", "valeur"],
                   [{"produit_id": p["id"], "cle": k,
                     "valeur": json.dumps(v, ensure_ascii=False) if isinstance(v, (list, bool)) else v}
                    for p in produits for k, v in p["attributs"].items()]),
        ecrire_jsonl("produits.jsonl",
                     [{k: p[k] for k in ("id", "boutique_id", "categorie_id", "nom", "prix",
                                         "stock", "cree_le", "attributs")} for p in produits]),
        ecrire_csv("clients.csv", ["id", "prenom", "nom", "email", "ville", "inscrit_le"], clients),
        ecrire_csv("commandes.csv", ["id", "client_id", "passee_le", "statut"], commandes),
        ecrire_csv("lignes_commande.csv",
                   ["commande_id", "produit_id", "quantite", "prix_unitaire"], lignes),
        ecrire_csv("avis.csv",
                   ["id", "produit_id", "client_id", "note", "commentaire", "publie_le"], avis),
        ecrire_csv("paniers.csv", ["client_id", "produit_id", "quantite", "ajoute_le"], paniers),
    ]

    empreinte = hashlib.sha256()
    for chemin in fichiers:
        with open(chemin, "rb") as f:
            empreinte.update(f.read())

    annulees = {c["id"] for c in commandes if c["statut"] == "annulee"}
    ca = sum(l["quantite"] * l["prix_unitaire"] for l in lignes if l["commande_id"] not in annulees)

    print(f"Données écrites dans {SORTIE}")
    print(f"  {len(boutiques):>7} boutiques")
    print(f"  {len(produits):>7} produits")
    print(f"  {len(clients):>7} clients")
    print(f"  {len(commandes):>7} commandes")
    print(f"  {len(lignes):>7} lignes de commande")
    print(f"  {len(avis):>7} avis")
    print(f"  {len(paniers):>7} lignes de panier")
    print(f"  chiffre d'affaires hors annulations : {ca:,.2f} €".replace(",", " "))
    print(f"  empreinte : {empreinte.hexdigest()[:12]}")


if __name__ == "__main__":
    main()
