# Erreurs à corriger dans `WeatherPipeline.py`

## 1. Problèmes de base
- La méthode appelée dans `__init__` est `self.init_connextion()`, mais la méthode définie est `def init_connexion(self):`.
- Dans `init_connexion`, `create_engine(url_BDD)` utilise une variable globale non définie. Il faut `create_engine(self.url_BDD)`.
- Plusieurs méthodes utilisent des attributs de classe sans le préfixe `self.` : `engine`, `locations`, `weathers`, `base`, `url_BDD`, `metadata_obj`, etc.

## 2. Problèmes dans `collecte`
- `requests.get(self.url_meteo, params=p_weather_city)` est correct. Vérifie que `self.url_meteo` est bien défini.
- `conf.json` est créé en mode "x"; si le fichier existe déjà, la création échoue. Pour être sûr, il faut soit vérifier l’existence, soit utiliser "w".

## 3. Méthode `villeId`
- Elle doit faire une requête ciblée vers `location_id` et non `SELECT *`.
- La version actuelle utilise `select(text("SELECT * FROM locations WHERE city = :city")).params(city=city)`, ce qui marche mais n’est pas idiomatique SQLAlchemy.
- Mieux :
  - `select(self.locations.c.location_id).where(self.locations.c.city == city)`
  - puis `result.fetchone()`
- Si la ville n’existe pas, retourner `None` plutôt que rien.

## 4. Logique de `depot_sql`
- `self.villeId(city)` est appelée deux fois pour la même ville. Il faut stocker le résultat une fois :
  - `loc_id = self.villeId(city)`
  - si `loc_id is None`: insérer la ville puis recalculer `loc_id`
- Cela évite une requête SQL inutile par ligne.

## 5. Problèmes de performance potentiels
- Ne pas lire toute la table `locations` avec `select(self.locations)` + `fetchall()`.
- Utiliser toujours un filtre `WHERE city = :city` ou, idéalement, `WHERE city = :city AND country_code = :country_code`.
- Si des noms de ville sont ambigus, `city` seul peut ramener la mauvaise ligne.

## 6. Pistes de correction
- Corriger le nom de la méthode et l’appel `self.init_connexion()`.
- Remplacer `create_engine(url_BDD)` par `create_engine(self.url_BDD)`.
- Modifier `villeId` pour utiliser `self.locations.c.location_id` et un `where` explicite.
- Simplifier le flux de `depot_sql` en réutilisant `loc_id`.
- Si tu gères les insertions par lots plus tard, tu peux aussi remplacer les insertions ligne par ligne par un `bulk insert`.

## 7. Notes pour demain sans connexion
- Tu n’as pas besoin de la base pour corriger la logique et la syntaxe dans le code.
- Tu peux faire ces corrections localement puis tester une fois la connexion disponible.
- Concentre-toi d’abord sur :
  1. appel et nom de la méthode `init_connexion`
  2. utilisation de `self.url_BDD`
  3. requête ciblée dans `villeId`
  4. suppression de la double recherche dans `depot_sql`
