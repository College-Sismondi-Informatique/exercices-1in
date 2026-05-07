from distributeur import nombre_billets, billet_suivant

somme = 3870
somme_restante = somme

for _ in range(nombre_billets):
    billet = billet_suivant()
    while somme_restante >= billet:
        print(billet)
        somme_restante = somme_restante-billet
        
