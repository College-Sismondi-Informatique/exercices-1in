# Librairie pour problème de rendu de monnaie
# VN - 04.26
# from distributeur import nombre_billets, billet_suivant

billets = [1000, 200, 100, 50, 20, 10]
iterBillets = iter(billets)
nombre_billets = len(billets)

def billet_suivant():
    return next(iterBillets)
