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
Voici le MLD produit :

Weather(**weather_id**, main, description, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, clouds, rain, snow, observation_time, sunrise, sunset, *location_id*)

Location (**location_id**, country_name, city, country_code, timezone, lat, lon)

Voici le dictionnaire de données :
| Intitulé           | Description                                   | Type      | Taille | Observation                                  |
|--------------------|-----------------------------------------------|-----------|--------|----------------------------------------------|
| weather_id         | Identifiant                                   | SERIAL    |        | Obl., unique                                 |
| main               | Conditions météorologiques                    | VARCHAR   | 20     | Obl., Rain, Snow, Clouds, etc.               |
| description        | Condition météo au sein du groupe             | VARCHAR   |        | Obl.                                         |
| temp               | Température                                   | FLOAT     |        | Obl., unité = Kelvin                         |
| feels_like         | Température ressentie                         | FLOAT     |        | Obl.                                         |
| temp_min           | Température minimale à ce moment              | FLOAT     |        | Obl.                                         |
| temp_max           | Température maximale à ce moment              | FLOAT     |        | Obl.                                         |
| pressure           | Pression atmosphérique                        | FLOAT     |        | Obl., unité = hPa                            |
| humidity           | Pourcentage de l’humidité                     | FLOAT     |        | Obl.                                         |
| visibility         | Visibilité                                    | FLOAT     |        | Optionnel, unité = mètre, 10 km max          |
| wind_speed         | Vitesse du vent                               | FLOAT     |        | Obl.                                         |
| clouds             | Couverture nuageuse (%)                       | FLOAT     |        | Obl.                                         |
| rain               | Précipitations                                | FLOAT     |        | Optionnel, unité = mm/h                      |
| snow               | Précipitations                                | FLOAT     |        | Optionnel, unité = mm/h                      |
| observation_time   | Date au moment du calcul                      | TIMESTAMP |        | Obl.                                         |
| sunrise            | Heure du lever du soleil                      | TIMESTAMP |        | Obl.                                         |
| sunset             | Heure du coucher du soleil                    | TIMESTAMP |        | Obl.                                         |
| location_id        | Identifiant de la localisation                | SERIAL    |        | Obl., unique                                 |
| country_name       | Pays                                          | VARCHAR   | 100    | Obl.                                         |
| city               | Ville                                         | VARCHAR   | 100    | Obl.                                         |
| country_code       | Code du pays                                  | VARCHAR   | 2      | Obl.                                         |
| timezone           | Fuseau horaire (offset UTC en secondes)       | INTEGER   |        | Obl.                                         |
| lat                | Latitude                                      | FLOAT     |        | Obl.                                         |
| lon                | Longitude                                     | FLOAT     |        | Obl.                                         |

