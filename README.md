[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-html.svg)](https://forthebadge.com)

# Scripts

Lors de l'éxécution récupère les informations d'un livre, d'une catégorie entière,\
ou de tout les produits du site à partir de l'URL fournie.

P2_01_book.py :\
\
Génère un fichier CSV pour l'URL du livre en paramètre.

P2_02_category.py :\
\
Génère un fichier CSV avec tous les livres/infos associés\
pour l'URL de la catégorie en paramètre.

P2_03_all_books.py:\
\
Génère deux dossiers 'Export_CSV' et 'Book_images' comprenant respectivement :
- Les fichiers CSV de chaque catégorie.
- Les images au format .JPG de chaque livre.

### Informations complémentaires

Nécéssite les packages requests, BeautifoulSoup, urllib

Utiliser le fichier 'requirements.txt' lors de l'initialisation de l'environement virtuel\
(cf. Lancements des scripts)

## Création de l'environnement virtuel

Depuis l'emplacement du script, dans un terminal de command:\
\
python3 -m venv venv\
\
cd /venv/Scripts/\
\
activate

## Lancement des scripts
\
cd ../..\
\
pip install -r requirements.txt\
\
python3 Nom_Du_Script
