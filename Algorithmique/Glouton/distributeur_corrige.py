from distributeur import nombre_billets, billet_suivant

somme = 3870

for _ in range(nombre_billets):
    billet = billet_suivant()
    while somme >= billet:
        print(billet)
        somme = somme-billet
        
