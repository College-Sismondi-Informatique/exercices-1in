''' Auteur(s)   : Edoardo Basilico
    Contact     : edu-basilicoe@eduge.ch
    License     : "CC-BY-NC-SA"
    Date        : 18 janvier 2024
    Version     : 0.1
    Description : Exercice devine nombre, étape 2C
                  Ajoutez un compteur qui compte le nombre de tentatives.
                  À la fin de la partie, le programme affiche ce nombre. 
'''
from random import *

nb_hasard = randint(1,100)

nombre_entier_choisi = 0

# Compteur de tentative 
compteur = 0

while nombre_entier_choisi != nb_hasard and compteur < 10:
    compteur = compteur + 1
    print("Tentative n°", compteur,end=". ")
    
    nombre_entier_choisi = int(input("Entrez un nombre: "))
    if nombre_entier_choisi < 1 or nombre_entier_choisi > 100:
            print("Votre nombre n'est pas compris entre 1 et 100 !")
    else:
        if nb_hasard > nombre_entier_choisi:
            print("Plus grand...")
        elif nb_hasard < nombre_entier_choisi:
            print("Plus petit...")
        # Ajout option D
        if compteur == 5:
            print("ATTENTION: Il vous reste encore 5 tentatives.")
                

#Fin de partie
if nombre_entier_choisi != nb_hasard:
    print("Vous avez joué 10 fois sans trouver... ")
    print("La réponse était", nb_hasard, ".")
else:
    print("Vous avez gagné en", compteur, "coup(s)...")