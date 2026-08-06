from random import randint

proposition = -1
minimum = 1
maximum = 128
tentatives = 0

nombre_mystere = randint(1, maximum)

print("Bienvenue dans le jeu du nombre mystere. Voilà, j'ai choisi un nombre entre 1 et ", maximum,", à toi de jouer!")


while proposition !=  nombre_mystere:
    
    proposition = (maximum+minimum)//2
    print("Ma proposition est", proposition)
    
    if proposition == nombre_mystere:
        print("C'est gagné !")
    elif proposition < nombre_mystere:
        print("Plus grand...")
        minimum = proposition
    elif proposition > nombre_mystere:
        print("Plus petit...")
        maximum = proposition

    tentatives = tentatives + 1


print("tentatives : ", tentatives)