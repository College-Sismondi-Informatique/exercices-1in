# Compiler Évaluations — Documentation

Ce script Python compile les notebooks Jupyter rendus par les élèves en un (ou plusieurs) notebook récapitulatif, facilitant la correction et le suivi de l'avancement.

---

## Structure attendue

Placez le script dans un dossier contenant :

```
.
├── compiler_evaluations.py
├── enonce.ipynb                     # Énoncé de référence (optionnel si --enonce)
├── *.csv                            # Export Moodle des participants (optionnel)
└── <Dossier_Moodle>_123456_assignsubmission_file/
    └── <notebook_élève>.ipynb
```

Le nom du dossier parent des devoirs (`<Dossier_Moodle>`) sera utilisé pour nommer les fichiers de sortie.

---

## Modes de fonctionnement

### Mode normal (par défaut)

Génère :
- **Un fichier récapitulatif global** (`compilation_<dossier>.ipynb`) contenant uniquement les tableaux de suivi par classe.
- **Un fichier par classe** (`compilation_<dossier>_1IN.DOxx.ipynb`) contenant le tableau de suivi **et** les réponses détaillées de chaque élève.

Usage :

```bash
python compiler_evaluations.py
```

### Mode light (`--light` ou `-l`)

Génère uniquement le fichier récapitulatif global, sans les réponses détaillées. Idéal pour un aperçu rapide ou lorsque les fichiers complets sont trop lourds.

Usage :

```bash
python compiler_evaluations.py --light
```

---

## Options

| Option | Description |
|--------|-------------|
| `-e`, `--enonce <chemin>` | Spécifie un chemin personnalisé pour le fichier énoncé (défaut : `enonce.ipynb` dans le dossier courant). |
| `-l`, `--light` | Active le mode light (tableaux uniquement, pas de réponses détaillées). |

### Exemples combinés

```bash
# Mode normal avec énoncé externe
python compiler_evaluations.py --enonce /chemin/vers/mon_enonce.ipynb

# Mode light avec énoncé externe
python compiler_evaluations.py --light --enonce /chemin/vers/mon_enonce.ipynb
```

---

## Fonctionnalités automatiques

### Tri par classe
Si un fichier CSV exporté depuis Moodle est présent dans le dossier, le script :
- Trie les élèves par groupe (`1IN.DO06`, `1IN.DO07`, etc.).
- Affiche les absents (présents dans le CSV mais sans rendu) avec toutes les cases "❌".
- Ignore les personnes sans groupe (enseignants, observateurs, etc.).

### Indicateurs du tableau récapitulatif
Pour chaque exercice, le tableau affiche :
- Le nombre d'exécutions de la cellule en **vert** si l'exercice est fait, **rouge** sinon.
- `(absent)` à côté du nom de l'élève si aucun rendu n'a été déposé.

### Tableau anonymisé (exemple en HTML)

En complément du tableau principal, un **tableau anonymisé en HTML** est disponible dans le notebook. Il reprend les mêmes indicateurs sans divulguer les noms des élèves :

```html
<table border="1" cellpadding="4" cellspacing="0" style="border-collapse:collapse;font-family:sans-serif">
  <tr style="background-color:#f0f0f0">
    <th>Élève</th><th>Ex 1</th><th>Ex 2</th><th>Ex 3</th>
  </tr>
  <tr>
    <td>Élève 1</td><td style="color:#2ecc71;font-weight:bold;text-align:center">3</td>
    <td style="color:#e74c3c;font-weight:bold;text-align:center">0</td>
    <td style="color:#2ecc71;font-weight:bold;text-align:center">5</td>
  </tr>
  <tr>
    <td>Élève 2</td><td style="color:#2ecc71;font-weight:bold;text-align:center">2</td>
    <td style="color:#2ecc71;font-weight:bold;text-align:center">4</td>
    <td style="color:#e74c3c;font-weight:bold;text-align:center">0</td>
  </tr>
  <tr>
    <td>Élève 3</td><td style="color:#e74c3c;font-weight:bold;text-align:center">0</td>
    <td style="color:#e74c3c;font-weight:bold;text-align:center">0</td>
    <td style="color:#e74c3c;font-weight:bold;text-align:center">0</td>
  </tr>
</table>
```

> **Vert** = exercice réalisé | **Rouge** = exercice non réalisé | Chiffre = nombre d'exécutions de la cellule

### Allègement des fichiers
Les notebooks générés ne conservent que le **code source** des cellules. Les outputs (graphiques, tableaux, images) sont volontairement ignorés pour réduire la taille des fichiers.

---

## Fichiers générés

### Mode normal
```
compilation_Sis-VN-1IN-Rendu_Leçon_1a-255321.ipynb                 # Récap global (light)
compilation_Sis-VN-1IN-Rendu_Leçon_1a-255321_1IN.DO06.ipynb        # Récap + réponses DO06
compilation_Sis-VN-1IN-Rendu_Leçon_1a-255321_1IN.DO07.ipynb        # Récap + réponses DO07
compilation_Sis-VN-1IN-Rendu_Leçon_1a-255321_1IN.DO08.ipynb        # Récap + réponses DO08
...
```

### Mode light
```
compilation_Sis-VN-1IN-Rendu_Leçon_1a-255321.ipynb                 # Récap global uniquement
```

---

## Dépendances

- Python 3
- `nbformat` (installable via `pip install nbformat`)

---

## Note sur les énoncés

Le script repère les exercices grâce au motif `!!! note Exercice <num>` dans les cellules Markdown de l'énoncé. La cellule de réponse attendue est la première cellule `code` ou `raw` qui suit chaque énoncé.
