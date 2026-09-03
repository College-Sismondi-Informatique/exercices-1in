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
OUTPUT_FILENAME = "compilation.ipynb"
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
    La cellule immédiatement suivante est considérée comme la réponse attendue.

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
                if i + 1 < len(cells):
                    next_cell = cells[i + 1]
                    # La cellule suivante est une réponse seulement si ce n'est pas
                    # elle-même un autre exercice (cas de l'exercice 7 sans cellule de réponse)
                    is_next_exercise = (
                        next_cell.cell_type == "markdown"
                        and re.search(
                            r"!!!\s+note\s+Exercice\s+\d+",
                            next_cell.source,
                            re.IGNORECASE,
                        )
                    )
                    if not is_next_exercise:
                        template = next_cell
                        # On saute la cellule de réponse dans la boucle principale
                        # pour éviter qu'elle ne soit traitée comme un exercice indépendant.
                        i += 1
                exercises.append(
                    {
                        "num": ex_num,
                        "text": ex_text,
                        "template": template,
                    }
                )
        i += 1
    return exercises


def find_student_notebooks(root: Path):
    """
    Retourne un OrderedDict {nom_élève_normalisé: chemin_notebook}.

    Le nom de l'élève est extrait du nom du dossier parent, supposé être
    de la forme :  NOM PRENOM_123456_assignsubmission_file
    """
    students = OrderedDict()
    for nb_path in sorted(root.rglob("*.ipynb")):
        # On ignore l'énoncé et le notebook de sortie potentiel
        if nb_path.name == ENONCE_FILENAME or nb_path.name == OUTPUT_FILENAME:
            continue

        # Extraction du nom d'élève depuis le dossier parent
        parent_name = nb_path.parent.name
        # Supprime la partie _<chiffres>_assignsubmission_file
        name_match = re.match(r"(.+?)_\d+_assignsubmission_file$", parent_name)
        if name_match:
            student_name = name_match.group(1).strip()
        else:
            # Fallback : nom du fichier sans extension
            student_name = nb_path.stem

        students[normalize_name(student_name)] = nb_path
    return students


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
    """Crée une nouvelle cellule nbformat à partir d'une cellule existante."""
    if cell.cell_type == "code":
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

def main(enonce_path: Path = None):
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
    existing_students = find_student_notebooks(ROOT_DIR)
    print(f"[INFO] {len(existing_students)} rendu(s) trouvé(s).")
    if not existing_students:
        print("[ERREUR] Aucun notebook d'élève détecté.")
        return

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
    students_data = OrderedDict()  # {nom: {responses, done, groupe, absent}}
    for student_name, nb_path, groupe in all_students:
        if nb_path:
            print(f"[INFO] Analyse de {student_name} ...")
            nb_student = nbformat.read(str(nb_path), as_version=4)
            student_exercises = parse_exercises(nb_student)

            responses = {}  # num -> cell
            done_flags = {}  # num -> bool

            for ex in student_exercises:
                num = ex["num"]
                resp_cell = ex["template"]  # la cellule après le markdown d'exercice
                responses[num] = resp_cell

                template_cell = templates_by_num.get(num)
                template_src = template_cell.source if template_cell else ""
                resp_src = resp_cell.source if resp_cell else ""
                done_flags[num] = is_done(resp_src, template_src)

            students_data[student_name] = {
                "responses": responses,
                "done": done_flags,
                "groupe": groupe,
                "absent": False,
            }
        else:
            # Élève absent : aucun rendu
            students_data[student_name] = {
                "responses": {},
                "done": {ex["num"]: False for ex in enonce_exercises},
                "groupe": groupe,
                "absent": True,
            }

    # 4. Construire le notebook de sortie
    out_cells = []

    # --- Titre global ---
    out_cells.append(
        nbformat.v4.new_markdown_cell("# Compilation des évaluations")
    )

    # --- Tableau récapitulatif ---
    table_md = "## Tableau récapitulatif de l'avancement\n\n"
    student_items = list(students_data.items())

    for groupe, group in groupby(student_items, key=lambda item: item[1]["groupe"]):
        group_list = list(group)
        if not groupe:
            table_md += "### Sans classe\n\n"
        else:
            table_md += f"### Classe {groupe}\n\n"

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
                sym = SYMBOLE_FAIT if data["done"].get(num, False) else SYMBOLE_PAS_FAIT
                row += f" {sym} |"
            lines.append(row)

        table_md += "\n".join(lines) + "\n\n"

    out_cells.append(
        nbformat.v4.new_markdown_cell(table_md)
    )

    # --- Sections par exercice ---
    for ex in enonce_exercises:
        num = ex["num"]
        # Titre d'exercice
        out_cells.append(
            nbformat.v4.new_markdown_cell(
                f"---\n\n## Exercice {num}\n\n"
                f"**Énoncé**\n\n{ex['text']}"
            )
        )

        for student_name, data in students_data.items():
            out_cells.append(
                nbformat.v4.new_markdown_cell(f"### Réponse de {student_name}")
            )
            resp_cell = data["responses"].get(num)
            if resp_cell:
                out_cells.append(copy_cell(resp_cell))
            else:
                if data.get("absent"):
                    msg = "*Aucun rendu (élève absent).*"
                else:
                    msg = "*Aucune réponse détectée.*"
                out_cells.append(
                    nbformat.v4.new_markdown_cell(msg)
                )

    # 5. Écrire le notebook
    nb_out = nbformat.v4.new_notebook()
    nb_out.cells = out_cells
    output_path = ROOT_DIR / OUTPUT_FILENAME
    nbformat.write(nb_out, str(output_path))
    print(f"[SUCCÈS] Notebook compilé généré : {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compile les notebooks d'évaluation des élèves."
    )
    parser.add_argument(
        "-e", "--enonce",
        type=Path,
        help="Chemin vers le notebook énoncé (défaut : enonce.ipynb dans le dossier courant)",
    )
    args = parser.parse_args()
    main(enonce_path=args.enonce)
