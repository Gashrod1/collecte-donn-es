# Projet Scraping Bordeaux Tourisme

## Étape 1 - Aspect légal
Pour restreindre le risque juridique :
1. **Respect du robots.txt** : Vérifier les interdictions d'indexation.
2. **Limitation de fréquence** : Imposer un délai (ex: 1-2 secondes) entre les requêtes pour éviter le déni de service.
3. **Identification** : Utiliser un User-Agent clair identifiant le bot et un moyen de contact.
4. **Données personnelles** : Ne pas collecter de données personnelles (RGPD).
5. **Usage** : Usage pédagogique uniquement, pas de republication commerciale.

## Structure du projet
* `ingestion_data/` : Contient les fichiers Parquet générés.
* `scripts/` : Contient les scripts Python de scraping.

## Configuration de l'environnement
### Création de virtual env
```bash
python -m venv venv
```
### Activation du virtual env
```bash
source venv/bin/activate
```
ou
```fish
source venv/bin/activate.fish
```
ou
```powershell
venv\Scripts\activate
```
### Installation des dépendances
```bash
pip install -r requirements.txt
```
