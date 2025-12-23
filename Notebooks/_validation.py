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
from js import document, Reflect

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
            (<label><input type="checkbox" name="option" value="A"> A) Réponse A</label><br>)
            defined in the user namespace (top-level).
        :param **kwargs: passed to parent constructor.
        """
        for key in ids_and_values.keys(): # for list typing of potential single answer
            if not isinstance(ids_and_values[key], list):
                ids_and_values[key] = [ids_and_values[key]]
        super().__init__(ids_and_values.keys(), ids_and_values.values(), **kwargs)

    def compute_result(self, id: str, precomputed_data: Any) -> Any:
        form = document.getElementById(id)
        inputs = form.querySelectorAll('input[type="checkbox"]')

        rep =[item.value for item in inputs if item.checked]
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
            
            
#####  Réponses exos
# Divers
test_a_42 = ValidateVariables({"a": 42})
continuer_si_10 = LitLaConsigne()

# Notebook 1IN - 5a
test_quiz1 = ValidateQuiz({"quiz1": ["C"]})
