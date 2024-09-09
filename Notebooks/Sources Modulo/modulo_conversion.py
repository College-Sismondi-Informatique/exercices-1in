import nbformat as nbf
import re
import os

def md_to_notebook(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Création du notebook avec des métadonnées spécifiques
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.12"
        }
    }

    cells = []
    code_block = False
    image_block = False
    question_block = False
    exercice_block = False
    code_lines = []
    exercise_nb = 1
    skip_first_block = True  # Pour ignorer le premier bloc

    image_base_url = "https://raw.githubusercontent.com/edunumsec2/book/master/src/appr/prog1/"

    for line in lines:
        # Ignorer le premier bloc qui commence par (prog1.repeter)=
        if skip_first_block:
            if line.strip().startswith('(prog1.'):
                continue
            else:
                skip_first_block = False
        
        # Gestion des blocs de code
        if line.startswith('```{codeplay}'):
            code_block = True
            turtle_block = False
            code_lines = []
            continue
        elif line.startswith('```') and code_block:
            if turtle_block and not 'done()' in code_lines:
                code_lines.append('\ndone()')
            cells.append(nbf.v4.new_code_cell('\n'.join(code_lines)))
            code_block = False
            continue

        if code_block:
            # Ignorer la ligne qui commence par :file:
            if not line.startswith(':file:'):
                code_lines.append(line.rstrip())
            if 'from turtle' in line:
                turtle_block = True
            continue
        
        

        # Gestion des blocs d'images en Markdown existants
        if re.match(r'!\[.*\]\(.*\)', line):
            line = re.sub(r'!\[(.*?)\]\((.*?)\)', 
                          lambda m: f"![{m.group(1)}]({image_base_url}{m.group(2)})", 
                          line)
            cells.append(nbf.v4.new_markdown_cell(line))
            continue

        # Gestion des blocs d'images spécifiques au format du fichier
        if line.startswith('```{image}'):
            image_block = True
            image_match = re.search(r'\{image\}\s*(.+)', line)
            if image_match:
                image_name = image_match.group(1).strip().split(':')[0] 
                image_url = f"{image_base_url}{image_name}"
                markdown_image = f'<img src="{image_url}" alt="{image_name}" width="200"/>'
                cells.append(nbf.v4.new_markdown_cell(markdown_image))
            continue
                
        if image_block :
            if line.startswith('```'):
                image_block = False
                cells.append(nbf.v4.new_markdown_cell('\n \n'))
            continue
        
        # Gestion des blocs de questions
        if line.startswith('```{question}'):
            question_block = True
            question_lines = []
            item = 'A'
            continue
            
        elif question_block:
            
            if line.startswith('```'):
                question_block = False
                question_text = "\n".join(question_lines)

                # Ajouter la question en markdown avec les options A), B), etc.
                markdown_question = f"```\n{question_text}\n```"
                cells.append(nbf.v4.new_markdown_cell('<h3 style="color:chocolate;background-color:papayawhip;" > <i class="fa fa-question" aria-hidden="true"> </i> &nbsp; Quizz </h3> \n \n'+ markdown_question))

                # Ajouter le bloc de réponse
                cells.append(nbf.v4.new_raw_cell("Réponse : "))
                
                # Ajouter la correction --> à discuter si corrigé ou ici
#                 cells.append(nbf.v4.new_markdown_cell("""<details>
# <summary style="border-left:3px solid #3c763d; border-radius:2pt; width:100%; color:#3c763d; padding:6px; background-color: #dff0d8"> 
# Réponse
# </summary>  
# 
# <div style="border-left:3px solid #3c763d; border-radius:2pt; color:#3c763d; padding:6px; background-color: #eff0e8">"""+good_answer+"""
# </div>
# </details>
#                 """))
            else:
                # Numérotation des options avec des lettres
                if line.startswith('{'):
                    answer = re.sub(r'\{(f|v)\}`', item + ') ', line.strip())[:-1]                    
                    if '{v}' in line:
                        good_answer = answer
                    item = chr(ord(item)+1)
                else:
                    answer = line.strip()
                question_lines.append(answer)
                
            continue

        if line.startswith('```{exercise}'):
            exercice_block = True
            cells.append(nbf.v4.new_markdown_cell('<h3 style="color:teal;background-color:azure;" > <i class="fa fa-pencil" aria-hidden="true"> </i> &nbsp; Exercice ' + str(exercise_nb) + ' </h3>'))
            exercise_nb += 1
            continue
        if line.startswith('```') and exercice_block:
            exercice_block = False
            continue
        
        
        # Gestion des en-têtes et du texte général
        if line.startswith('#'):
            cells.append(nbf.v4.new_markdown_cell(line))
        elif line.strip() == "":
            if cells and isinstance(cells[-1], nbf.NotebookNode):
                cells[-1].source += "\n"
        else:
            if cells and isinstance(cells[-1], nbf.NotebookNode) and cells[-1].cell_type == "markdown":
                cells[-1].source += line
            else:
                cells.append(nbf.v4.new_markdown_cell(line))
                
        
        

    nb.cells = cells
    cells.append(nbf.v4.new_markdown_cell("""---

#### Remarque générale

Ce document est une adaptation d'un ressource pédagogique tiré du catalogue modulo https://modulo-info.ch/. Il est sous license Creative Commons [BY-NC-SA](https://creativecommons.org/licenses/?lang=fr)
![Licence Creative Commons](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)

    """))

    # Nom du fichier de sortie identique au fichier Markdown, mais avec extension .ipynb
    ipynb_file = os.path.splitext(md_file)[0] + '.ipynb'

    with open(ipynb_file, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

l = os.listdir()
# Utilisation
for md_file in l:
    if md_file[-3:] == '.md':
        md_to_notebook(md_file)
