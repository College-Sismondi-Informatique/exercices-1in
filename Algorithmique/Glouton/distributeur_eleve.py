from distributeur import nombre_billets, billet_suivant

for _ in range(nombre_billets):
    billet = billet_suivant()
    print(billet)
