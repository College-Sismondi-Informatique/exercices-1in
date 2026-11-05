''' Auteur(s)   : Edoardo Basilico
    Contact     : edu-basilicoe@eduge.ch
    License     : "CC-BY-NC-SA"
    Date        : 18 janvier 2024
    Version     : 0.1
    Description : Exercice devine nombre complet
'''
from random import *

# Variable qui indique si le joueur-se veut rejouer.
rejouer = True

while rejouer:
    # Nombre entier au hasard compris entre 1 et 100
    nb_hasard = randint(1,100)

    #Initialisation de la variable qui contiendra le nombre tapé au clavier
    nombre_entier_choisi = 0

    # Compteur de tentative 
    compteur = 1

    # On boucle tant que le nombre n'est pas trouvé ou que le nombre de tentative
    # n'a pas dépassé 10.
    while nombre_entier_choisi != nb_hasard and compteur <= 10:
        
        print("Tentative n°", compteur, end=". ")
        
        nombre_entier_choisi = int(input("Entrez un nombre: "))

        # On vérifie si le nombre est bien compris entre 1 et 100
        if nombre_entier_choisi < 1 or nombre_entier_choisi > 100:
                print("Votre nombre n'est pas compris entre 1 et 100 !")
        else:
            compteur = compteur + 1
            # On indique si le nombre est trop grand ou trop petit
            if nb_hasard > nombre_entier_choisi:
                print("Plus grand...")
            elif nb_hasard < nombre_entier_choisi:
                print("Plus petit...")
            # On affiche le message de milieu de partie (option 2.D)
            if compteur == 5:
                print("ATTENTION: Il vous reste encore 5 tentatives.")                

    #Fin de partie
    if nombre_entier_choisi != nb_hasard:
        print("Vous avez joué 10 fois sans trouver... ")
        print("La réponse était", nb_hasard, ".")
    else:
        print("Vous avez gagné en", compteur, "coup(s)...")
    
    # On demande si le joueur-se veut rejouer.
    reponse = input("Voulez-vous rejouer ? [O/N]:")
    rejouer = (reponse == 'O' or reponse == 'o')
