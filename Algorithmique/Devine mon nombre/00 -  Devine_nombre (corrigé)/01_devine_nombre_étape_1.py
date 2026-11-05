''' Auteur(s)   : Edoardo Basilico
    Contact     : edu-basilicoe@eduge.ch
    License     : "CC-BY-NC-SA"
    Date        : 18 janvier 2024
    Version     : 0.1
    Description : Exercice devine nombre, étape 1
'''
from random import *

nombre_entier_hasard = randint(1,100)

nombre_entier_choisi = 0

# Boucle de jeu, tant que gagne est faux, le jeu continue.
while nombre_entier_choisi != nb_hasard:
    # Nombre saisie par le joueur ou la joueuse
    nombre_entier_choisi = int(input("Entrez un nombre: "))

    if nb_hasard > nombre_entier_choisi:
        print("Plus grand...")
    elif nb_hasard < nombre_entier_choisi:
        print("Plus petit...")

#Fin de partie
print("C'est gagné !")