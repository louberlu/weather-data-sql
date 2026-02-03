# Weather Data SQL
Ce projet est un cas d'étude présenté par Natacha Njongwa Yepnga.

## Résumé
Une entreprise dans le secteur du tourisme souhaite automatiser la collecte de données météo pour ses différentes destinations. Ces données sont collectées via l'API publique OpenWeather. Les données collectées sont nettoyées, normalisées et stockées dans une base SQL. L'objectif est d'optimiser leurs recommandations aux clients. 

## Architecture du pipeline

```text
OpenWeather API
      ↓
Extraction (JSON)
      ↓
Transformation / Normalisation
      ↓
Base de données PostgreSQL
```

## Technologies utilisées
- Langage : Python
- Bibliothèques : requests
- Base de données relationnelles : PostgreSQL

## Structure du projet
La structure du projet est organisée comme suit :
```src/api        → appels API
src/processing → transformations
src/database   → schéma et insertion SQL
src/main.py    → orchestration du pipeline
```

## Instructions d'exécution
Les instructions d’exécution seront précisées une fois le pipeline finalisé.
```git clone ...
cp .env.example .env
pip install -r requirements.txt
python src/main.py
```

## Modèle de données
Cette partie sera complétée après l'exploration des données via le notebook.