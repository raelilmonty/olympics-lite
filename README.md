# Olympics Lite

Ce projet est un exemple d’application Python permettant de voir diverses
informations sur les Jeux Olympiques de Paris 2024.

Certaines données de la base de données viennent du dépôt
https://github.com/22Ranjan15/Paris-2024-Olympic_Dashboard

Il comprend 4 manières d’accéder aux données :

- une interface web dans `olympics/api.py`.
- une interface en ligne de commande dans `olympics/__main__.py`,
- une bibliothèque pour afficher des résultats dans le terminal dans `olympics/cli.py`,
- une bibliothèque bas-niveau pour accéder à la base de données dans `olympics/db.py`,

Cette application est écrite à des fins éducatives, et ne suit pas toutes les
bonnes pratiques du développement d’applications en Python.

## Comment l’installer

1. Forkez le dépôt.

2. Clonez votre fork.

   `git clone git@github.com:YourNickName/olympics-lite.git`

3. Allez dans votre dépôt cloné.

   `cd olympics-lite`

4. Créez un environnement virtuel appelé `venv`.

   `python -m venv venv`

5. Activez votre environnement virtuel.

6. Installez les dépendances du projet.

   `pip install -e .`


## Comment l’utiliser

Pour utiliser l’application, veillez bien à être à la
racine du dépôt que vous avez cloné et à activer l’environnement virtuel.

### Pour utiliser l’API web

`fastapi dev olympics`

Vous avez alors accès à l’adresse `http://127.0.0.1:8000` et aux différentes
routes de l’application.

Une documentation automatique, avec une interface de test, est disponible à
l’adresse `http://127.0.0.1:8000/docs`.

Vous pouvez arrêter le serveur avec `Ctrl+C`.

### Pour utiliser la CLI

`python -m olympics --help`

Différentes commandes s’offrent à vous. Pour afficher le top 5 des médailles
individuelles, vous pouvez par exemple lancer :

`python -m olympics individual --top=5`

### Pour utiliser la bibliothèque

`python`

Dans l’interpréteur Python :

```python
>>> from olympics import cli
>>> help(cli)
```

Différentes fonctions sont disponibles. Pour afficher le top 3 des pays pour
les médailles collectives, vous pouvez par exemple lancer :

```python
>>> cli.top_collective(top=3)
```

Pour quitter l’interpréteur, utilisez `exit()`.

### Pour utiliser les fonctions bas-niveau de la base de données

`python`

Dans l’interpréteur Python :

```python
>>> from olympics import db
>>> help(db)
```

Différentes fonctions sont possibles. Pour récupérer une liste de tous les
athlètes et afficher les informations du premier, vous pouvez par exemple
lancer :

```python
>>> athletes = db.get_athletes()
>>> dict(athletes[0])
{'id': 1, 'name': 'Artur ALEKSANYAN', 'gender': 'male', 'country_id': 8}
```

Vous pouvez également lancer des requêtes SQL de cette manière :

```python
>>> cursor = db.get_connection().cursor()
>>> athletes = cursor.execute('SELECT id, name FROM athlete LIMIT 5').fetchall()
>>> dict(athletes[0])
{'id': 1, 'name': 'Artur ALEKSANYAN'}
```

Le schéma de la base de données est dans `database/model.sql`.

Pour quitter l’interpréteur, utilisez `exit()`.


## Idées d’améliorations

### Vérifiez la qualité du code

Mettez en place un outil de vérification de la qualité du code : installez,
configurez et utilisez `ruff`. Mettez en place dans votre dépôt Git des
méthodes pour s’assurer que le code suit toujours ces bonnes pratiques.

### Utilisez un ORM

Utilisez [SQLAlchemy](https://www.sqlalchemy.org/) à la place du module
`sqlite3`. Inspirez-vous des bonnes pratiques données dans les documentations
de FastAPI et de SQLAlchemy a ce sujet.

### Refactorisez le code de `db.py`

Avec ou sans SQLAlchemy, il est possible d’éviter les nombreuses répétitions de
code dans le fichiers `db.py`. Ne serait-ce pas l’occasion d’utiliser des
décorateurs pour rendre cela moins verbeux et plus élégant ?

### Ajoutez de nouvelles fonctionnalités

L’interface en ligne de commande est limitée. Proposez donc de nouvelles
fonctionnalités, en privilégiant bien sûr l’utilité et l’intelligence à la
quantité.

### Générez une documentation simple

En utilisant [Sphinx](https://www.sphinx-doc.org/), générez une documentation
simple. Pas la peine d’écrire des pavés de texte, une petite introduction et
une documentation automatique de l’API Python sont largement suffisantes.
