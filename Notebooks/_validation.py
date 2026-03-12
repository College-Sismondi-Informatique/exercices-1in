from basthon.autoeval import (
    Validate,
    ValidateVariables,
    ValidateFunction,
    ValidateFunctionPretty,
    validationclass,
    ValidateSequences,
)
from typing import Any
import time
import sys

# Essayer d'importer les objets JS, sinon fournir des valeurs None
try:
    from js import document, Reflect, Jupyter  # type: ignore
except Exception:
    document = None
    Reflect = None
    Jupyter = None

codes_dict = {}
lastCode = ""


def store_all_cells_content():
    global codes_dict
    if Jupyter is None or not hasattr(Jupyter, "notebook"):
        return
    for i, cell in enumerate(Jupyter.notebook.get_cells()):
        # protection si l'API est différente
        cm = getattr(cell, "code_mirror", None)
        if cm is not None and hasattr(cm, "getValue"):
            codes_dict[i] = cm.getValue()


def store_cell_content():
    global codes_dict
    if Jupyter is None or not hasattr(Jupyter, "notebook"):
        return
    idx = Jupyter.notebook.get_selected_index()
    cell = Jupyter.notebook.get_selected_cell()
    cm = getattr(cell, "code_mirror", None)
    if cm is not None and hasattr(cm, "getValue"):
        codes_dict[idx] = cm.getValue()


def restore_all_cells_content():
    if Jupyter is None or not hasattr(Jupyter, "notebook"):
        return
    for i, cell in enumerate(Jupyter.notebook.get_cells()):
        if i in codes_dict:
            cm = getattr(cell, "code_mirror", None)
            if cm is not None and hasattr(cm, "setValue"):
                cm.setValue(codes_dict[i])


##### Classes custom
@validationclass
class LitLaConsigne:
    def __init__(self):
        super().__init__()
        self._start = time.time()

    def __call__(self):
        # au moins 10 secondes (ajusté pour test rapide)
        if time.time() - self._start > 10:
            print("Bravo, tu as pris le temps de lire la consigne !")
            return True
        else:
            print("As-tu vraiment pris le temps de lire la consigne ?", file=sys.stderr)
            return False


@validationclass
class ValidateQuiz(ValidateSequences[str, Any]):
    """A class to validate html form checkbox quiz."""

    def __init__(self, ids_and_values: dict[str, Any] | str, **kwargs):
        # Si on reçoit un str, on récupère les bonnes réponses depuis le DOM
        if isinstance(ids_and_values, str):
            if document is None:
                ids_and_values = {ids_and_values: []}
            else:
                el = document.getElementById(ids_and_values)
                if el is None:
                    ids_and_values = {ids_and_values: []}
                else:
                    inputs = el.querySelectorAll('input[type="checkbox"]')
                    rep = [item.name for item in inputs if getattr(item, "value", None) == "correct"]
                    ids_and_values = {ids_and_values: rep}

        # Forcer la liste pour chaque valeur
        for k in list(ids_and_values.keys()):
            if not isinstance(ids_and_values[k], list):
                ids_and_values[k] = [ids_and_values[k]]

        # ValidateSequences attend des itérables parallèles : on lui passe lists
        keys = list(ids_and_values.keys())
        values = [ids_and_values[k] for k in keys]
        super().__init__(keys, values, **kwargs)

    def compute_result(self, id: str, precomputed_data: Any) -> Any:
        if document is None:
            return []
        el = document.getElementById(id)
        if el is None:
            return []
        inputs = el.querySelectorAll('input[type="checkbox"]')
        rep = [item.name for item in inputs if getattr(item, "checked", False)]
        return rep

    def handle_failure(self, name: str, target: Any, value: Any) -> bool:
        print("Mauvaise(s) réponse(s), essaie encore.", file=sys.stderr)
        return False

    def handle_exception(self, exc: Exception, name: str, target: Any) -> bool:
        print(f"Erreur Il y a un problème avec : '{name}'", file=sys.stderr)
        return False

    def handle_full_success(self):
        print("👏 Bravo, bonne(s) réponse(s) !")


@validationclass
class ValidateTextInput(ValidateSequences[str, str]):
    """A class to validate html text inputs."""

    def __init__(self, ids_and_values: dict[str, str] | str, **kwargs):
        if isinstance(ids_and_values, str):
            if document is None:
                ids_and_values = {ids_and_values: []}
            else:
                el = document.getElementById(ids_and_values)
                if el is None:
                    ids_and_values = {ids_and_values: []}
                else:
                    inputs = el.querySelectorAll('input[type="text"]')
                    ids_and_values = {ids_and_values: [i.id for i in inputs]}

        for k in list(ids_and_values.keys()):
            if not isinstance(ids_and_values[k], list):
                ids_and_values[k] = [ids_and_values[k]]

        keys = list(ids_and_values.keys())
        values = [ids_and_values[k] for k in keys]
        super().__init__(keys, values, **kwargs)

    def compute_result(self, id: str, precomputed_data: Any) -> Any:
        if document is None:
            return []
        el = document.getElementById(id)
        if el is None:
            return []
        inputs = el.querySelectorAll('input[type="text"]')
        return [getattr(i, "value", "") for i in inputs]

    def handle_failure(self, name: str, target: Any, value: Any) -> bool:
        print("Mauvaise(s) réponse(s), essaie encore.", file=sys.stderr)
        return False

    def handle_exception(self, exc: Exception, name: str, target: Any) -> bool:
        print(f"Erreur Il y a un problème avec : '{name}'", file=sys.stderr)
        return False

    def handle_full_success(self):
        print("👏 Bravo, bonne(s) réponse(s) !")


def remove_shortcuts():
    keep_shortcut = {
        "jupyter-notebook:run-cell",
        "jupyter-notebook:run-cell-and-select-next",
        "jupyter-notebook:save-notebook",
        "jupyter-notebook:select-previous-cell",
        "jupyter-notebook:select-next-cell",
        "jupyter-notebook:enter-edit-mode",
    }

    if Jupyter is None or not hasattr(Jupyter, "keyboard_manager"):
        return

    km = Jupyter.keyboard_manager

    # Command mode shortcuts
    cmd_shortcuts = getattr(km, "command_shortcuts", None)
    if cmd_shortcuts is not None and hasattr(cmd_shortcuts, "_shortcuts"):
        try:
            items = cmd_shortcuts._shortcuts.to_py()
        except Exception:
            try:
                items = dict(cmd_shortcuts._shortcuts)
            except Exception:
                items = {}
        for k, v in list(items.items()):
            if (v not in keep_shortcut) or len(k) == 1:
                if isinstance(v, dict):
                    for k1 in v:
                        try:
                            cmd_shortcuts.remove_shortcut(f"{k},{k1}")
                        except Exception:
                            pass
                else:
                    try:
                        cmd_shortcuts.remove_shortcut(k)
                    except Exception:
                        pass

    # Edit mode shortcuts
    edit_shortcuts = getattr(km, "edit_shortcuts", None)
    if edit_shortcuts is not None and hasattr(edit_shortcuts, "_shortcuts"):
        try:
            items = edit_shortcuts._shortcuts.to_py()
        except Exception:
            try:
                items = dict(edit_shortcuts._shortcuts)
            except Exception:
                items = {}
        for k, v in list(items.items()):
            if (v not in keep_shortcut) or len(k) == 1:
                if isinstance(v, dict):
                    for k1 in v:
                        try:
                            edit_shortcuts.remove_shortcut(f"{k},{k1}")
                        except Exception:
                            pass
                else:
                    try:
                        edit_shortcuts.remove_shortcut(k)
                    except Exception:
                        pass


# Appel sûr de la suppression des shortcuts
try:
    remove_shortcuts()
except Exception:
    # Ne pas planter si l'API n'est pas présente
    pass


#####  Réponses exos (exemples et tests)
# test_a_42 = ValidateVariables({"a": 42})
# continuer_si_10 = LitLaConsigne()
# test_quiz_exemple = ValidateQuiz({"quiz1": ["C"], "quiz2": ["A","B"]})
# test_quiz_exemple_2 = ValidateQuiz("quiz1")
# test_text_input_1 = ValidateTextInput({"question1.1": "42"})
# test_text_input_2 = ValidateTextInput("question1.1")

# Notebook 5a
test_5a_3 = ValidateVariables({"A": 121})
test_5a_4a = ValidateVariables({"x": 70})
test_5b_6b = ValidateVariables({"k": 10})
