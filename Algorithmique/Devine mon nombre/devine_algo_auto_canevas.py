from random import randint

print("Bienvenue dans le jeu du nombre mystere. Voilà, j'ai choisi un nombre entre 1 et 100, à toi de jouer!")

nombre_mystere = randint(1, 100)
nombre = 0
minimum = ....
maximum = ...


while nombre != nombre_mystere:
    nombre = ....
    
    if nombre == nombre_mystere:
        print("C'est gagné !")
    elif nombre < nombre_mystere:
        print("Plus grand...")
        ....
    elif nombre > nombre_mystere:
        print("Plus petit...")
        ...

