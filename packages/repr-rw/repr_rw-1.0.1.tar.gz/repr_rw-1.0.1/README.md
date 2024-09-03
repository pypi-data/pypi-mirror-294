# ReprRW

## FRANÇAIS

Cette bibliothèque écrit la représentation d'objets Python dans un fichier
texte et lit le fichier pour recréer les objets. Une représentation d'objet
est une chaîne de caractères renvoyée par la fonction `repr`.

### Contenu

La fonction `write_reprs` écrit la représentation d'objets Python dans un
fichier texte. Chaque ligne du fichier est une représentation d'objet. Si le
fichier spécifié existe déjà, cette fonction l'écrase.

La fonction `read_reprs` lit les fichiers texte qui contiennent des
représentations d'objet Python dans le but de recréer ces objets. Chaque ligne
doit être une représentation d'objet. Les lignes vides sont ignorées.

Consultez la documentation des fonctions et les démos dans le dépôt de code pour
plus d'informations.

### Démos

Le script `demo_write.py` montre comment utiliser la fonction `write_reprs`. Il
faut l'exécuter en premier, car il produit un fichier dont `demo_read.py` a
besoin.

```
python demos/demo_write.py
```

Le script `demo_read.py` montre comment utiliser la fonction `read_reprs`. Il
faut l'exécuter après `demo_write.py`, car il ne fonctionne pas sans le fichier
produit par cet autre script.

```
python demos/demo_read.py
```

## ENGLISH

This library writes Python object representations in a text file and reads the
file to recreate the objects. An object representation is a string returned by
function `repr`.

### Content

Function `write_reprs` writes the representation of Python objects in a text
file. Each line in the file is an object representation. If the specified file
already exists, this function overwrites it.

Function `read_reprs` reads text files that contain the representation of
Python objetcs in order to recreate those objects. Each line must be an object
representation. Empty lines are ignored.

Consult the functions' documentation and the demos in the code repository for
the complete information.

### Demos

Script `demo_write.py` shows how to use function `write_reprs`. It must be
executed first because it makes a file that `demo_read.py` needs.

```
python demos/demo_write.py
```

Script `demo_read.py` shows how to use function `read_reprs`. It must be
executed after `demo_write.py` because it cannont work withoud the file made by
that other script.

```
python demos/demo_read.py
```
