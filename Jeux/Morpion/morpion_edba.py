''' Auteur(s)   : Enseignants informatique Collège Sismondi
    Contact     : edu-basilicoe@eduge.ch
    License     : "CC-BY-NC-SA"
    Date        : 09 mars 2025
    Version     : 1.0
                  - Reste à tracer le trait de la victoire. 
    Description : Dessine un morpion et gère les dessins X et O dans les bonnes cases.
    
          case_1|case_2|case_3
          --------------------
          case_4|case_5|case_6
          --------------------        
          case_7|case_8|case_9
 
'''

from tkinter import Tk, Canvas, Button, Label

# Variables pour suivre l'état des cases
case_1 = " "
case_2 = " "
case_3 = " "
case_4 = " "
case_5 = " "
case_6 = " "
case_7 = " "
case_8 = " "
case_9 = " "

joueur_actuel = "X"
nb_coup_joue = 0
jeu_termine = False

# Création de la fenêtre et du canevas
fenetre = Tk()
fenetre.title("Morpion")
canvas = Canvas(fenetre, width=300, height=300)
canvas.pack()

label_info = Label(fenetre, text="Joueur-se X, à toi de jouer !", font=("Arial", 14))
label_info.pack()


# Dessiner la grille
canvas.create_line(100, 0, 100, 300, width=5)
canvas.create_line(200, 0, 200, 300, width=5)
canvas.create_line(0, 100, 300, 100, width=5)
canvas.create_line(0, 200, 300, 200, width=5)

def dessine(joueur, x, y):
    global nb_coup_joue
    
    padding = 30
    nb_coup_joue = nb_coup_joue + 1
    if joueur == "X":
        canvas.create_line(x+padding, y+padding, x+100-padding, y+100-padding, width=5, fill="blue")
        canvas.create_line(x+100-padding, y+padding, x+padding, y+100-padding, width=5, fill="blue")
    else:
        canvas.create_oval(x+padding, y+padding, x+100-padding, y+100-padding, width=5, outline="red")

def verifier_victoire(joueur):
    #global case_1, case_2, case_3, case_4, case_5, case_6, case_7, case_8, case_9
    combinaison = joueur + joueur + joueur
    if case_1 + case_2 + case_3 == combinaison or \
       case_4 + case_5 + case_6 == combinaison or \
       case_7 + case_8 + case_9 == combinaison or \
       case_1 + case_4 + case_7 == combinaison or \
       case_2 + case_5 + case_8 == combinaison or \
       case_3 + case_6 + case_9 == combinaison or \
       case_1 + case_5 + case_9 == combinaison or \
       case_3 + case_5 + case_7 == combinaison :
        return True
    else:
        return False


# Fonction pour détecter la case cliquée et jouer
def clic(event):
    global nb_coup_joue, joueur_actuel, jeu_termine, case_1, case_2, case_3, case_4, case_5, case_6, case_7, case_8, case_9

    if jeu_termine:
        return  # Arrêter si le jeu est terminé
    
    x = event.x
    y = event.y
    colonne = x // 100
    ligne = y // 100
    case_numero = ligne * 3 + colonne + 1

    if case_numero == 1 and case_1 == " ":
        case_1 = joueur_actuel
        dessine(joueur_actuel, 0, 0)
    elif case_numero == 2 and case_2 == " ":
        case_2 = joueur_actuel
        dessine(joueur_actuel, 100, 0)
    elif case_numero == 3 and case_3 == " ":
        case_3 = joueur_actuel
        dessine(joueur_actuel, 200, 0)
    elif case_numero == 4 and case_4 == " ":
        case_4 = joueur_actuel
        dessine(joueur_actuel, 0, 100)
    elif case_numero == 5 and case_5 == " ":
        case_5 = joueur_actuel
        dessine(joueur_actuel, 100, 100)
    elif case_numero == 6 and case_6 == " ":
        case_6 = joueur_actuel
        dessine(joueur_actuel, 200, 100)
    elif case_numero == 7 and case_7 == " ":
        case_7 = joueur_actuel
        dessine(joueur_actuel, 0, 200)
    elif case_numero == 8 and case_8 == " ":
        case_8 = joueur_actuel
        dessine(joueur_actuel, 100, 200)
    elif case_numero == 9 and case_9 == " ":
        case_9 = joueur_actuel
        dessine(joueur_actuel, 200, 200)
    else:
        return  # La case est déjà occupée


    jeu_termine = verifier_victoire(joueur_actuel)
    
    if jeu_termine:
        label_info.config(text=f"🎉 {joueur_actuel} a gagné ! 🎉")
        
        return # Arrêter si le jeu est terminé
    else:
        if nb_coup_joue == 9:
            label_info.config(text=f"Match nul !")
            jeu_termine = True
            return

        # Changer de joueur
        if joueur_actuel == "X":
            joueur_actuel = "O"
        else:
            joueur_actuel = "X"
        label_info.config(text=f"Joueur-se {joueur_actuel}, à toi de jouer !")

# Lier le clic à la fonction
# On lie l'évenement clic gauche (Button-1) à l'appel de la fonction clic
canvas.bind("<Button-1>", clic)

# Lancer la boucle de la fenêtre
fenetre.mainloop()

