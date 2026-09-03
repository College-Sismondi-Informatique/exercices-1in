#!/usr/bin/env python3
"""
Compile les notebooks d'évaluation des élèves en un seul notebook.

Le script s'appuie sur un notebook "énoncé" pour identifier les exercices
et détecter si les élèves ont répondu ou non.

Structure du dossier attendue :
    .
    ├── enonce.ipynb              (ou chemin fourni via --enonce)
    ├── compiler_evaluations.py
    ├── *.csv                     (optionnel : liste des participants Moodle)
    └── <dossier_moodle_élève>_123456_assignsubmission_file/
        └── <notebook_élève>.ipynb

Le notebook généré contient :
    1. Un tableau récapitulatif (fait / pas fait) par élève et par exercice.
    2. Pour chaque exercice : l'énoncé, puis les réponses de chaque élève.

Usage :
    python compiler_evaluations.py
    python compiler_evaluations.py --enonce /chemin/vers/mon_enonce.ipynb
    python compiler_evaluations.py --light
    python compiler_evaluations.py --light --enonce /chemin/vers/mon_enonce.ipynb
"""

import os
import re
import csv
import argparse
from pathlib import Path
from itertools import groupby
from collections import OrderedDict
import nbformat

# ============================================================================
# CONFIGURATION
# ============================================================================
ENONCE_FILENAME = "enonce.ipynb"
# Dossier racine contenant les rendus (défaut : dossier courant du script)
ROOT_DIR = Path(__file__).parent.resolve()
# Symboles pour le tableau récapitulatif
SYMBOLE_FAIT = "✅"
SYMBOLE_PAS_FAIT = "❌"
# Pattern pour détecter automatiquement le fichier CSV des participants
CSV_PATTERN = "*.csv"


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def sanitize_table_cell(text: str) -> str:
    """Échappe les caractères problématiques pour une cellule de tableau markdown."""
    return text.replace("|", "\\|").replace("\n", " ")


def normalize_name(name: str) -> str:
    """Normalise un nom pour la comparaison (majuscules, espaces uniques)."""
    return " ".join(name.strip().split()).upper()


def is_done(response_src: str, template_src: str = "") -> bool:
    """
    Détermine si une réponse est considérée comme 'faite'.
    Renvoie False si la cellule est vide, ne contient que des points de suspension,
    ou est strictement identique à la cellule modèle de l'énoncé.
    """
    if response_src is None:
        return False

    cleaned = response_src.strip()
    if not cleaned:
        return False

    # Seulement des points de suspension / espaces / retours à la ligne
    if re.fullmatch(r"[.\s]+", cleaned):
        return False

    # Strictement identique au modèle de l'énoncé (on ignore les espaces de fin)
    if cleaned == template_src.strip():
        return False

    return True


def parse_exercises(nb):
    """
    Parse un notebook et extrait la liste des exercices détectés.

    Un exercice est repéré par une cellule markdown contenant
    '!!! note Exercice <num>'.
    Les cellules markdown suivantes sont sautées (consignes) jusqu'à trouver
    la première cellule code ou raw, considérée comme la réponse attendue.

    Retourne une liste de dicts : [{num, text, template_cell}, ...]
    """
    exercises = []
    cells = list(nb.cells)
    i = 0
    while i < len(cells):
        cell = cells[i]
        if cell.cell_type == "markdown":
            match = re.search(
                r"!!!\s+note\s+Exercice\s+(\d+)", cell.source, re.IGNORECASE
            )
            if match:
                ex_num = int(match.group(1))
                ex_text = cell.source
                template = None
                j = i + 1
                while j < len(cells):
                    next_cell = cells[j]
                    # Si on tombe sur un autre exercice, on s'arrête
                    if next_cell.cell_type == "markdown" and re.search(
                        r"!!!\s+note\s+Exercice\s+\d+",
                        next_cell.source,
                        re.IGNORECASE,
                    ):
                        break
                    # La réponse attendue est la première cellule code ou raw
                    if next_cell.cell_type in ("code", "raw"):
                        template = next_cell
                        i = j  # On saute toutes les cellules intermédiaires
                        break
                    j += 1
                exercises.append(
                    {
                        "num": ex_num,
                        "text": ex_text,
                        "template": template,
                    }
                )
        i += 1
    return exercises


def find_student_notebooks(root: Path, output_filename: str = "compilation.ipynb"):
    """
    Retourne un tuple (OrderedDict {nom_élève_normalisé: chemin_notebook}, dossier_des_devoirs).

    Le nom de l'élève est extrait du nom du dossier parent, supposé être
    de la forme :  NOM PRENOM_123456_assignsubmission_file
    """
    students = OrderedDict()
    homework_dir = None
    for nb_path in sorted(root.rglob("*.ipynb")):
        # On ignore l'énoncé et le notebook de sortie potentiel
        if nb_path.name == ENONCE_FILENAME or nb_path.name == output_filename:
            continue

        # Extraction du nom d'élève depuis le dossier parent
        parent_name = nb_path.parent.name
        # Supprime la partie _<chiffres>_assignsubmission_file
        name_match = re.match(r"(.+?)_\d+_assignsubmission_file$", parent_name)
        if name_match:
            student_name = name_match.group(1).strip()
            if homework_dir is None:
                homework_dir = nb_path.parent.parent.name
        else:
            # Fallback : nom du fichier sans extension
            student_name = nb_path.stem

        students[normalize_name(student_name)] = nb_path
    return students, homework_dir


def load_participants(csv_path: Path):
    """
    Charge le CSV Moodle des participants.
    Retourne un dict {nom_normalisé: {prenom, nom, groupe}}.
    """
    participants = {}
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        # Nettoyer le BOM potentiel sur les noms de colonnes
        if reader.fieldnames:
            reader.fieldnames = [
                name.lstrip("\ufeff").strip() for name in reader.fieldnames
            ]
        for row in reader:
            prenom = row.get("Prénom", "").strip()
            nom = row.get("Nom de famille", "").strip()
            groupe = row.get("Groupes", "").strip()
            if not prenom or not nom:
                continue
            # La clé suit le même format que les dossiers Moodle : NOM PRENOM
            name_key = normalize_name(f"{nom} {prenom}")
            participants[name_key] = {
                "prenom": prenom,
                "nom": nom,
                "groupe": groupe,
            }
    return participants


def build_student_list(existing_students: OrderedDict, participants: dict):
    """
    Construit la liste finale des élèves.
    Retourne une liste de tuples : (nom_affichage, chemin_notebook, groupe)
    Triée par groupe puis par nom.
    """
    if not participants:
        # Comportement original : uniquement les rendus trouvés, triés par nom
        items = [(name, path, "") for name, path in existing_students.items()]
        items.sort(key=lambda x: x[0])
        return items

    combined = []
    matched_existing = set()

    for name_key, info in participants.items():
        if not info["groupe"]:
            continue
        path = existing_students.get(name_key)
        combined.append((name_key, path, info["groupe"]))
        if path:
            matched_existing.add(name_key)

    # Ajouter les rendus supplémentaires non listés dans le CSV
    for name, path in existing_students.items():
        if name not in matched_existing:
            combined.append((name, path, ""))

    # Tri par groupe (vide en dernier) puis par nom
    combined.sort(key=lambda x: (x[2] if x[2] else "ZZZ", x[0]))
    return combined


def copy_cell(cell):
    """Crée une nouvelle cellule nbformat à partir d'une cellule existante.
    
    Les outputs sont volontairement ignorés pour alléger le notebook compilé."""
    if cell.cell_type == "code":
        # new_code_cell ne copie que la source : outputs et execution_count sont vidés
        return nbformat.v4.new_code_cell(cell.source)
    elif cell.cell_type == "raw":
        return nbformat.v4.new_raw_cell(cell.source)
    elif cell.cell_type == "markdown":
        return nbformat.v4.new_markdown_cell(cell.source)
    else:
        return nbformat.v4.new_markdown_cell(str(cell.source))


# ============================================================================
# LOGIQUE PRINCIPALE
# ============================================================================

def main(enonce_path: Path = None, light_mode: bool = False):
    if enonce_path is None:
        enonce_path = ROOT_DIR / ENONCE_FILENAME
    else:
        enonce_path = Path(enonce_path).resolve()

    if not enonce_path.exists():
        print(f"[ERREUR] Énoncé introuvable : {enonce_path}")
        return

    # 1. Charger l'énoncé et identifier les exercices
    print(f"[INFO] Chargement de l'énoncé : {enonce_path}")
    nb_enonce = nbformat.read(str(enonce_path), as_version=4)
    enonce_exercises = parse_exercises(nb_enonce)
    if not enonce_exercises:
        print("[ERREUR] Aucun exercice détecté dans l'énoncé.")
        return

    print(f"[INFO] {len(enonce_exercises)} exercice(s) détecté(s) : "
          f"{[ex['num'] for ex in enonce_exercises]}")

    # Index rapide par numéro d'exercice pour les templates
    templates_by_num = {ex["num"]: ex["template"] for ex in enonce_exercises}

    # 2. Découvrir les notebooks élèves
    existing_students, homework_dir = find_student_notebooks(ROOT_DIR)
    print(f"[INFO] {len(existing_students)} rendu(s) trouvé(s).")
    if not existing_students:
        print("[ERREUR] Aucun notebook d'élève détecté.")
        return

    # Nom du fichier de sortie basé sur le dossier contenant les devoirs
    if homework_dir:
        clean_name = homework_dir.replace(" ", "_").replace("/", "_").replace("\\", "_")
        output_filename = f"compilation_{clean_name}.ipynb"
    else:
        output_filename = f"compilation_{ROOT_DIR.name.replace(' ', '_')}.ipynb"

    # 2b. Charger participants CSV si présent
    csv_files = sorted(ROOT_DIR.glob(CSV_PATTERN))
    participants = None
    if csv_files:
        print(f"[INFO] Fichier CSV détecté : {csv_files[0].name}")
        participants = load_participants(csv_files[0])
        print(
            f"[INFO] {len(participants)} participant(s) chargé(s) depuis {csv_files[0].name}"
        )
        if participants:
            first = next(iter(participants.items()))
            print(f"[DEBUG] Exemple de participant lu : {first[0]} → groupe {first[1]['groupe']}")
        else:
            print("[AVERTISSEMENT] Aucun participant valide trouvé dans le CSV (vérifiez l'encodage ou les colonnes).")
    else:
        print("[INFO] Aucun fichier CSV trouvé, mode sans participant activé.")

    all_students = build_student_list(existing_students, participants)
    absents = [s for s in all_students if s[1] is None]
    print(f"[INFO] {len(all_students)} élève(s) au total ({len(absents)} absent(s) + {len(all_students) - len(absents)} rendu(s)).")

    # 3. Parser chaque notebook élève
    students_data = OrderedDict()  # {nom: {responses, done, exec_counts, groupe, absent}}
    for student_name, nb_path, groupe in all_students:
        if nb_path:
            print(f"[INFO] Analyse de {student_name} ...")
            nb_student = nbformat.read(str(nb_path), as_version=4)
            student_exercises = parse_exercises(nb_student)

            responses = {}       # num -> cell
            done_flags = {}      # num -> bool
            exec_counts = {}     # num -> int | None

            for ex in student_exercises:
                num = ex["num"]
                resp_cell = ex["template"]  # la cellule après l'énoncé (code/raw)
                responses[num] = resp_cell

                if resp_cell is None:
                    done_flags[num] = False
                    exec_counts[num] = None
                elif resp_cell.cell_type == "code":
                    # Validation textuelle (différence avec l'énoncé)
                    template_cell = templates_by_num.get(num)
                    template_src = template_cell.source if template_cell else ""
                    resp_src = resp_cell.source
                    done_flags[num] = is_done(resp_src, template_src)
                    exec_counts[num] = resp_cell.execution_count
                else:
                    # Fallback markdown/raw : comparaison textuelle
                    template_cell = templates_by_num.get(num)
                    template_src = template_cell.source if template_cell else ""
                    resp_src = resp_cell.source
                    done_flags[num] = is_done(resp_src, template_src)
                    exec_counts[num] = None

            students_data[student_name] = {
                "responses": responses,
                "done": done_flags,
                "exec_counts": exec_counts,
                "groupe": groupe,
                "absent": False,
            }
        else:
            # Élève absent : aucun rendu
            students_data[student_name] = {
                "responses": {},
                "done": {ex["num"]: False for ex in enonce_exercises},
                "exec_counts": {ex["num"]: None for ex in enonce_exercises},
                "groupe": groupe,
                "absent": True,
            }

    # 4. Construire les notebooks de sortie
    #    Mode normal : récap global + 1 notebook par classe
    #    Mode light  : seulement les tableaux récap (pas les réponses détaillées)
    def build_recap_table(student_items, subgroup_title=None):
        """Construit le markdown du tableau récapitulatif pour un sous-ensemble d'élèves."""
        md = "## Tableau récapitulatif de l'avancement\n\n"
        if subgroup_title:
            md += f"**{subgroup_title}**\n\n"

        grouped = sorted(student_items, key=lambda item: (item[1]["groupe"] if item[1]["groupe"] else "ZZZ", item[0]))
        for groupe, group in groupby(grouped, key=lambda item: item[1]["groupe"]):
            group_list = list(group)
            if not groupe:
                md += "### Sans classe\n\n"
            else:
                md += f"### Classe {groupe}\n\n"

            header = "| Élève |"
            separator = "|-------|"
            for ex in enonce_exercises:
                header += f" Ex {ex['num']} |"
                separator += "-------|"
            lines = [header, separator]

            for student_name, data in group_list:
                display_name = student_name
                if data.get("absent"):
                    display_name += " *(absent)*"
                row = f"| {sanitize_table_cell(display_name)} |"
                for ex in enonce_exercises:
                    num = ex["num"]
                    done = data["done"].get(num, False)
                    sym = SYMBOLE_FAIT if done else SYMBOLE_PAS_FAIT
                    exec_count = data["exec_counts"].get(num)
                    color = "green" if done else "red"
                    if exec_count is None:
                        exec_count = 0
                    cell_content = f'<span style="font-weight: bold;color:{color}">{exec_count}</span>'
                    row += f" {cell_content} |"
                lines.append(row)

            md += "\n".join(lines) + "\n\n"
        return md

    def build_notebook(student_items, title_suffix="", light=False):
        """Construit un notebook complet ou light pour un sous-ensemble d'élèves."""
        cells = []

        # Titre
        titre = "# Compilation des évaluations"
        if title_suffix:
            titre += f" - {title_suffix}"
        cells.append(nbformat.v4.new_markdown_cell(titre))

        # Tableau récapitulatif
        cells.append(
            nbformat.v4.new_markdown_cell(
                build_recap_table(student_items, subgroup_title=title_suffix)
            )
        )

        if not light:
            # Sections par exercice avec réponses détaillées
            for ex in enonce_exercises:
                num = ex["num"]
                cells.append(
                    nbformat.v4.new_markdown_cell(
                        f"---\n\n## Exercice {num}\n\n"
                        f"**Énoncé**\n\n{ex['text']}"
                    )
                )
                for student_name, data in student_items:
                    cells.append(
                        nbformat.v4.new_markdown_cell(f"### Réponse de {student_name}")
                    )
                    resp_cell = data["responses"].get(num)
                    if resp_cell:
                        cells.append(copy_cell(resp_cell))
                    else:
                        if data.get("absent"):
                            msg = "*Aucun rendu (élève absent).*"
                        else:
                            msg = "*Aucune réponse détectée.*"
                        cells.append(nbformat.v4.new_markdown_cell(msg))
        else:
            # Note light : on rappelle que les réponses sont dans les notebooks par élève
            cells.append(
                nbformat.v4.new_markdown_cell(
                    "---\n\n*Ce notebook est en mode light. "
                    "Les réponses détaillées ne sont pas incluses pour alléger le fichier. "
                    "Elles sont disponibles dans les notebooks individuels des élèves.*"
                )
            )

        nb = nbformat.v4.new_notebook()
        nb.cells = cells
        return nb

    # Grouper les élèves par classe
    student_items = list(students_data.items())
    grouped_by_class = {}
    for groupe, group in groupby(
        sorted(student_items, key=lambda item: (item[1]["groupe"] if item[1]["groupe"] else "ZZZ", item[0])),
        key=lambda item: item[1]["groupe"],
    ):
        grouped_by_class[groupe] = list(group)

    # Nom de base du fichier
    base_name = homework_dir.replace(" ", "_").replace("/", "_").replace("\\", "_") if homework_dir else ROOT_DIR.name.replace(" ", "_")

    if light_mode:
        # Mode light : fichiers _LIGHT avec tableaux uniquement
        # 1. Notebook global light
        global_light_path = ROOT_DIR / f"compilation_{base_name}.ipynb"
        nb_global = build_notebook(student_items, title_suffix="Toutes classes", light=True)
        nbformat.write(nb_global, str(global_light_path))
        print(f"[SUCCÈS] Récap light global généré : {global_light_path}")

    else:
        # Mode normal :
        # 1. Notebook global light (tableau récap uniquement)
        global_path = ROOT_DIR / f"compilation_{base_name}.ipynb"
        nb_global = build_notebook(student_items, title_suffix="Toutes classes", light=True)
        nbformat.write(nb_global, str(global_path))
        print(f"[SUCCÈS] Notebook global récap généré : {global_path}")

        # 2. Un notebook complet (tableaux + réponses) par classe
        for groupe, items in grouped_by_class.items():
            suffix = groupe if groupe else "Sans_classe"
            class_path = ROOT_DIR / f"compilation_{base_name}_{suffix}.ipynb"
            nb_class = build_notebook(items, title_suffix=suffix, light=False)
            nbformat.write(nb_class, str(class_path))
            print(f"[SUCCÈS] Notebook classe {suffix} généré : {class_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compile les notebooks d'évaluation des élèves."
    )
    parser.add_argument(
        "-e", "--enonce",
        type=Path,
        help="Chemin vers le notebook énoncé (défaut : enonce.ipynb dans le dossier courant)",
    )
    parser.add_argument(
        "-l", "--light",
        action="store_true",
        help="Mode light : génère seulement les tableaux récapitulatifs (pas de réponses détaillées)",
    )
    args = parser.parse_args()
    main(enonce_path=args.enonce, light_mode=args.light)
