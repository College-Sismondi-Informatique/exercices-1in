''' Auteur(s)   : Edoardo Basilico
    Contact     : edu-basilicoe@eduge.ch
    License     : "CC-BY-NC-SA"
    Date        : 18 janvier 2024
    Version     : 0.1
    Description : Exercice devine nombre, étape 2A
                  Est-ce que le nombre saisi est compris entre 1 et 100.
                  Si ce n’est pas le cas demander à l’utilisateur·trice de
                  saisir à nouveau un nombre.
'''
from random import *

nb_hasard = randint(1,100)

nombre_entier_choisi = 0


while nombre_entier_choisi != nb_hasard:

    nombre_entier_choisi = int(input("Entrez un nombre: "))
    
    # On test si le nombre est compris entre 1 et 100
    if nombre_entier_choisi < 1 or nombre_entier_choisi > 100:
            print("Votre nombre n'est pas compris entre 1 et 100 !")
    else:
        if nb_hasard > nombre_entier_choisi:
            print("Plus grand...")
        elif nb_hasard < nombre_entier_choisi:
            print("Plus petit...")

#Fin de partie
print("C'est gagné !")