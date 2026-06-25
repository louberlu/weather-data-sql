# Journal - Weather Data SQL

## Semaine 1 (2026/02/02 → 2026/02/08)

### Jour 1 - 2026/02/03

#### Tâches faites :
- Rédaction du README minimal
- Définition de la méthodologie et de la structure du projet

#### Tâches à faire :
- Connexion API
- Inspection des données
- Décider des champs à conserver
- Schéma SQL brouillon

#### Notes / obstacles :
Faire un document, qui explique les outils utilisés, comme un cheat sheet, ou un tuto. Et à la fin du projet ne pas oublier de partager sur linkedIn.

### Jour 2 - 2026/02/04
#### Tâches faites
- Connexion API
- Inspection des données
- Décider des champs à conserver
- Schéma SQL brouillon

#### Tâches à faire
- Définir les tables
- Choisir les types
- Gérer les clés (primary / foreign)
- Penser évolutivité minimale

#### Notes / obstacles :
Il faudra répondre implicitement à : 
“À quel rythme ces données arrivent-elles ?” Une semaine ? Un mois ? Faire un compromis entre efficacité et capacité.

### Jour 3 - 2026/02/05
#### Tâches faites
- Définition des entités (Weather, Location)
- Choix des champs et des types
- Identification des clés primaires et étrangères
- Production du dictionnaire de données et du MLD

#### Tâches à faire
- Finaliser le schéma relationnel
- Rédiger le fichier schema.sql
- Compléter la section “Modèle de données” dans le README
- Définir l’évolutivité minimale (fréquence de collecte)
- Valider la fin de l’étape 2

### Jour 4 - 2026/02/06
#### Tâches faites
- Finaliser le schéma relationnel

#### Tâches à faire
- Rédiger le fichier schema.sql
- Compléter la section “Modèle de données” dans le README
- Définir l’évolutivité minimale (fréquence de collecte)
- Valider la fin de l’étape 2

### Jour 5 - 2026/02/07
#### Tâches faites
- Rédiger le fichier schema.sql
- Compléter la section “Modèle de données” dans le README

#### Tâches à faire
- Définir l’évolutivité minimale (fréquence de collecte)
- Valider la fin de l’étape 2

#### Notes / obstacles :
Il faudra rajouter une section à l'avenir dans les projets, c'est Problème et Contexte. 

### Jour 6 - 2026/02/20
#### Tâches faites
- Définir l’évolutivité minimale (fréquence de collecte)

#### Tâches à faire
- Créer les fonctions de collecte de données
- Réfléchir à la transformation des données

### Jour 7 - 2026/02/27
#### Tâches faites
- Créer la fonction de collecte dans le notebook

#### Tâches à faire
- Améliorer les performances de cette fonction
- Créer une pipeline de collecte de fichier json pour chaque heure (airflow)
- Tester la pipeline

#### Notes / obstacles :
- Lorsque l'on va passer à la création de fichier python, penser à créer un fichier qui contiendra les variables d'environnement. Ce fichier ne devra pas être uploader sur gitHub pour des raisons de sécurité. Y mettre l'API ainsi que les données de configuration de la BDD.

### Jour 8 - 2026/06/18
#### Tâches faites
- Explorer comment récupérer les fichiers JSON pour les déposer la base de données SQL

#### Tâches à faire


#### Notes / obstacles :
- Penser à aller les commentaires dans le documents "Schema SQL.docx"

### Jour 9 - 2026/06/19
#### Tâches faites
- Explorer l'utilisation de sqlalchimy

#### Tâches à faire
- Créer la base de données depuis python (le notebook)
- Insérer à la main les données récupérées du fichier JSON
- Créer une fonction qui va automatiser cette insertion

#### Notes / obstacles :

### Jour 10 - 2026/06/19
#### Tâches faites
- Créer les tables à partir du notebook en utilisant SQLAlchimy

#### Tâches à faire
- Gérer les exceptions
- Faire des insertions
- Semi-automatiser les insertions

#### Notes / obstacles :
- Il faudra regarder des tutoriels sur SQLAlchimy pour des possibilités d'amélioration de son utilisation
- Ne pas s'attarder sur les détails car le projet peut-être améliorer à des dates ultérieures

### Jour 11 - 2026/06/23
#### Tâches faites
- Gérer les exceptions
- Faire des insertions
- Création de la fonction transformer

#### Tâches à faire
- Faire plusieurs insertions
- Créer la fonction de dépôt
- Ajouter d'autres automatisations

#### Notes / obstacles :
- Il y a une différence entre la fonction begin et connect, est que la première gère les commit avec with

### Jour 12 - 2026/06/25
#### Tâches faites
- Faire plusieurs insertions
- Créer la fonction de dépôt
- Créer la classe WeatherPipeline

#### Tâches à faire
- Optimiser la classe WeatherPipeline
- Tester la méthode villeId dans le notebook.
- Rajouter la docstring
- Tester chaque méthode de la classe
- Tester la pipeline complète

#### Notes / obstacles :
