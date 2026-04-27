''' Auteur(s) : Mathieu Schiess
    Contact   : edu-schiessma@eduge.ch
    License   : "CC-BY-NC-SA"
    Description : Ce programme est une version "humain contre ordinateur" du
                  jeu du nombre mystère.
                  L'ordinateur choisit un nombre au hasard entre 1 et 100 et
                  indique, chaque fois que l'utilisateur propose un nombre, si la
                  proposition est trop grande ou trop petite.
                  Le jeu s'arrête quand l'utilisteur donne le bon nombre, dans ce
                  cas le nombre total d'essais est affiché.
    Date: 07 février 2024
'''

from random import randint

nombre = randint(1,100)

print("Bienvenue dans le jeu du nombre mystère")
print("Voilà, j'ai choisi un nombre entre 1 et 100, à toi de jouer!")

proposition = 0
nb_tentatives = 0

while proposition != nombre :
    proposition = int(input("Quelle est ta proposition : "))
    nb_tentatives = nb_tentatives + 1    
    if proposition > nombre:
        print("trop grand")
    elif proposition < nombre:
        print("trop petit")

print("Bravo vous avez deviné après ", nb_tentatives, " coups")