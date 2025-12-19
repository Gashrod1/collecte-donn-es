# Documentation du Projet : Collecte de Données pour la Prédiction de Trafic (Rocade Bordelaise)

Ce document détaille le processus de mise en place du pipeline d'ingestion de données, réalisé dans le cadre de l'atelier de constitution du jeu de données d'entraînement.

## Contexte
L'objectif est de créer un modèle prédictif de trafic sur la rocade bordelaise. Pour cela, nous avons identifié plusieurs facteurs influents (trafic, météo, calendrier scolaire, jours fériés) et mis en place un script pour automatiser la récupération de ces données.

## Étape 1 & 2 : Analyse et Sources (Réalisé en amont)
Un brainstorming a permis d'identifier les facteurs clés et leurs sources de données respectives (Open Data).
*   **Facteurs directs** : Trafic routier, accidents, travaux, météo.
*   **Facteurs contextuels** : Événements, vacances scolaires, jours fériés.

## Étape 3 : Ingestion des Données (Réalisation Technique)

J'ai développé un script Python `scripts/ingest_data.py` qui automatise la collecte et le stockage des données.

### 1. Sources de Données Connectées
Le script se connecte aux API Open Data suivantes :

| Donnée | Source | URL API utilisée |
| :--- | :--- | :--- |
| **Trafic Temps Réel** | Bordeaux Métropole | `opendata.bordeaux-metropole.fr` (Dataset: `ci_trafi_l`) |
| **Calendrier Scolaire** | Éducation Nationale | `data.education.gouv.fr` (Dataset: `fr-en-calendrier-scolaire`) |
| **Jours Fériés** | Data.gouv.fr | `data.gouv.fr` (Dataset: Jours fériés en France) |
| **Météo (Historique)** | Météo France / OpenDataSoft | `public.opendatasoft.com` (Station: BORDEAUX-MERIGNAC) |

### 2. Fonctionnement du Script (`scripts/ingest_data.py`)

Le script suit les étapes suivantes pour chaque source de données :

1.  **Requête HTTP** : Il effectue une requête `GET` sur l'URL de l'API pour récupérer les données brutes (généralement au format CSV).
2.  **Lecture et Parsing** :
    *   Il utilise la librairie `pandas` pour lire le contenu CSV.
    *   Il gère automatiquement les séparateurs (point-virgule `;` ou virgule `,`) pour s'adapter aux différents formats des fournisseurs.
3.  **Stockage (Format Parquet)** :
    *   Les données sont converties en DataFrames pandas.
    *   Elles sont sauvegardées dans le dossier `ingestion_data/` au format **Parquet**.
    *   Le format Parquet a été choisi car il est optimisé pour le stockage de gros volumes de données et très performant pour la lecture ultérieure (compression, typage des colonnes).
4.  **Nommage des Fichiers** :
    *   Les fichiers sont nommés dynamiquement en incluant la date d'exécution pour permettre l'historisation.
    *   Format : `{type_donnee}_{AAAAMMJJ}.parquet` (ex: `traffic_20251219.parquet`).

### 3. Utilisation

Pour lancer l'ingestion des données, exécutez la commande suivante depuis la racine du projet :

```bash
python scripts/ingest_data.py
```

### 4. Fichiers Générés

Après l'exécution du script, les fichiers suivants sont disponibles dans le dossier `ingestion_data/` :

*   `traffic_YYYYMMDD.parquet` : Données de trafic (vitesse, débit, taux d'occupation sur les tronçons).
*   `school_holidays_YYYYMMDD.parquet` : Calendrier des vacances scolaires par zone.
*   `public_holidays_YYYYMMDD.parquet` : Liste des jours fériés passés et à venir.
*   `weather_YYYYMMDD.parquet` : Relevés météorologiques (température, précipitations, vent) de la station Bordeaux-Mérignac.

---
*Généré par GitHub Copilot le 19 Décembre 2025.*
