from basthon.autoeval import (
    Validate,
    ValidateVariables,
    ValidateFunction,
    ValidateFunctionPretty,
    validationclass,
    ValidateSequences
)
from typing import Any
import time
import sys
from js import document, Reflect, Jupyter

##### Classes custom
@validationclass
class LitLaConsigne:
    def __init__(self):
        super().__init__()
        self._start = time.time()

    def __call__(self):
        # au moins 5 minutes se sont écoulées
        if time.time() - self._start > 10:
            print("Bravo, tu as pris le temps de lire la consigne !")
            return True
        else:
            print("As-tu vraiment pris le temps de lire la consigne ?", file=sys.stderr)
            return False

@validationclass
class ValidateQuiz(ValidateSequences[str, Any]):
    """A class to validate html form checkbox quiz. """

    def __init__(self, ids_and_values: dict[str, Any], **kwargs):
        """
        :param ids_and_values: a dict with quiz Ids (<form id="">)as key
            and list of correct answers values as values to test against checked answers
            (<label><input type="checkbox" name="C" value="correct"> C) Réponse C</label><br>)
            defined in the user namespace (top-level).
        :param ids_and_values: alternatively, a simple str with the id. Answer will then be searched in the source page
        :param **kwargs: passed to parent constructor.
        """
        if isinstance(ids_and_values, str): # If no answer is specified, find correct answer in HTML "value" parameter
            inputs = document.getElementById(ids_and_values).querySelectorAll('input[type="checkbox"]')
            rep =[item.name for item in inputs if item.value=="correct"]
            ids_and_values = {ids_and_values:rep}
            
        for key in ids_and_values.keys():  # force list typing of potential single answer            
            if not isinstance(ids_and_values[key], list):
                ids_and_values[key] = [ids_and_values[key]]
        super().__init__(ids_and_values.keys(), ids_and_values.values(), **kwargs)

    def compute_result(self, id: str, precomputed_data: Any) -> Any:
        # Return list of names of checked items
        inputs = document.getElementById(id).querySelectorAll('input[type="checkbox"]')
        rep =[item.name for item in inputs if item.checked]
        return rep

    def handle_failure(self, name: str, target: Any, value: Any) -> bool:
        print(
            f"Mauvaise(s) réponse(s), essaie encore.",
            file=sys.stderr,
        )
        return False

    def handle_exception(self, exc: Exception, name: str, target: Any) -> bool:
        print(
            f"Erreur Il y a un problème avec : '{name}'",
            file=sys.stderr,
        )
        return False

    def handle_full_success(self):
        print("👏 Bravo, bonne(s) réponse(s) !")

@validationclass
class ValidateTextInput(ValidateSequences[str, str]): # TODO : Refactor ValidateTextInput and ValidateQuiz in one ValidateForm to check every input and signal error
    """A class to validate html form checkbox quiz. """

    def __init__(self, ids_and_values: dict[str, str], **kwargs):
        """
        :param ids_and_values: a dict with input Ids (<form id="">)as key
            and correct answer as values to test against checked answers
            (<label>Ma réponse : <input type="text" id="12" value=""></label><br>)
            defined in the user namespace (top-level).
        :param ids_and_values: alternatively, a simple str with the id. Answer will then be searched in the source page
        :param **kwargs: passed to parent constructor.
        """
        if isinstance(ids_and_values, str): # If no answer is specified, find correct answer in HTML "value" parameter
            inputs = document.getElementById(ids_and_values).querySelectorAll('input[type="text"]')
            ids_and_values = {ids_and_values:[i.id for i in inputs]}
        super().__init__(ids_and_values.keys(), ids_and_values.values(), **kwargs)

    def compute_result(self, id: str, precomputed_data: Any) -> Any:
        # Return value of input field
        inputs = document.getElementById(id).querySelectorAll('input[type="text"]')
        return [i.value for i in inputs] 

    def handle_failure(self, name: str, target: Any, value: Any) -> bool:
        print(
            f"Mauvaise(s) réponse(s), essaie encore.",
            file=sys.stderr,
        )
        return False

    def handle_exception(self, exc: Exception, name: str, target: Any) -> bool:
        print(
            f"Erreur Il y a un problème avec : '{name}'",
            file=sys.stderr,
        )
        return False

    def handle_full_success(self):
        print("👏 Bravo, bonne(s) réponse(s) !")


def remove_shortcuts():
    keep_shortcut = ["jupyter-notebook:run-cell",
                     "jupyter-notebook:run-cell-and-select-next",
                     "jupyter-notebook:save-notebook",
                     "jupyter-notebook:select-previous-cell",
                     "jupyter-notebook:select-next-cell",
                     "jupyter-notebook:enter-edit-mode"]
    

    for k,v in Jupyter.keyboard_manager.command_shortcuts._shortcuts.to_py().items():
        if v not in keep_shortcut or len(k) == 1:
            if isinstance(v,dict):
                for k1 in v:
                    Jupyter.keyboard_manager.command_shortcuts.remove_shortcut(f"{k},{k1}")
            else:
                Jupyter.keyboard_manager.command_shortcuts.remove_shortcut(k)
                
    for k,v in Jupyter.keyboard_manager.edit_shortcuts._shortcuts.to_py().items():
        if v not in keep_shortcut or len(k) == 1:
            if isinstance(v, dict):
                for k1 in v:
                    Jupyter.keyboard_manager.edit_shortcuts.remove_shortcut(f"{k},{k1}")
            else:
                Jupyter.keyboard_manager.edit_shortcuts.remove_shortcut(k)
                
remove_shortcuts()
                        
            
#####  Réponses exos
### Exemples
# test_a_42 = ValidateVariables({"a": 42})
# continuer_si_10 = LitLaConsigne()
# test_quiz_exemple = ValidateQuiz({"quiz1": ["C"], "quiz2": ["A","B"]})
# test_quiz_exemple_2 = ValidateQuiz("quiz1") # same but with answer in source page
# test_text_input_1 = ValidateTextInput({"question1.1": "42"})
# test_text_input_2 = ValidateTextInput("question1.1") # same but with answer in source page


# Notebook 5a
test_5a_3 = ValidateVariables({"A": 121})
test_5a_4a = ValidateVariables({"x": 70})
test_5b_6b = ValidateVariables({"k": 10})