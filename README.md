# Choix de code

Pour plus de facilité et lisibilité, nous avons décidé d'utiliser des classes.
Nous aurions pu améliorer nos class pour la partie base de données, en créant une class mère Database, ainsi nos class DatabasePOSTGRESQL et DatabaseSQLITE auraient pu hériter des fonctions de la class Database
Nous avons repris le squelette du projet 1 qui nous semblait cohérent avec le besoin.

# Pensez à bien utiliser cette commande dans le même terminal que celui que vous utilisez pour exécuter vos fichiers

Si on travaille en environnement virtuel cela est crucial, en effet l'environnement virtuel permet d'avoir une version de python spécifique.
Cela permet d'avoir des librairies compatibles avec cette version de python.
Si on exécute cette commande en dehors ou dans un autre projet, le résultat ne correspondra pas à la version qui sera installée dans notre environnement virtuel

# Algorithmie [1/2]

## Indiquer dans le fichier README.md le nom des trois chaînes/pays qui ont diffusé le plus d’épisodes.

La fonction qui permet de répondre à cela se trouve dans : database_postgresql.py ( count_episodes_by_field )

Les trois chaînes qui ont diffusé le plus d'épisodes sont : - Netflix - Disney+ - Prime Video

Les trois pays qui ont diffusé le plus d'épisodes sont : - EtatsUnis - France - Canada

## Quels sont les 10 mots les plus présents dans les noms des séries ?

Nous avons utilisé un **DISTINCT** pour la recherche des noms de série car une série peut avoir 4 épisodes dans un mois.
Ainsi, nous avons vraiment les séries une fois, et non le nombre de fois qu'il y a d'épisodes.

Les 10 mots les plus présents dans les noms des séries sont : - the(23) - of(7) - (2023)(3) - de(3) - american(3) - les(3) - john(3) - all(2) - and(2) - young(2)
l'affichage des 10 mots les plus présents peut varier suivant la façon dont on récupère la donnée en base, en effet on retrouve plusieurs mots avec le même nombre d'occurences. Néanmoins les premiers sont toujours 'the' avec 23 occurences et 'of' avec 7 occurences.

# Algorithmie [2/2]

## Quelle est la chaîne de TV qui diffuse des épisodes pendant le plus grand nombre de jours consécutifs sur le mois d’Octobre ?

La chaîne de TV qui diffuse des épisodes pendant le plus grand nombre de jours consécutifs sur le mois d'Octobre est TF1 avec 5 jours consécutifs.

# Orchestration

Nous avons un fichier summarize_episodes.py que nous appelons en CLI.
Avec cette commande par exemple : python3 summarize_episodes.py --month 11
Ceci appelle donc notre fichier avec le mois 11 en paramètres.

Ainsi, notre fonction va récupérer le premier et dernier jour du mois ainsi que l'année en cours.
Par la suite, il envoie tout au main.py qui va exécuter l'intégralité du code.

Nous n'avons pas fait un affichage dédié pour cette question, néanmoins vu que le script s'execute de la même manière, voila les résultats pour Novembre 2023 :

209 episodes seront diffusés pendant le mois de 11.

C'est Etats-Unis qui diffusera le plus d'épisodes avec 170 épisodes.

C'est HULU qui diffusera le plus d'episodes avec 21 épisodes.

C'est NBC qui diffusera des épisodes pendant le plus grand nombre \
de jours consécutifs avec 3 de jours consécutifs.
