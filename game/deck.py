import random
from .card import Card

class Deck:
    def __init__(self):
        self.cartas = self._criar_baralho()
        random.shuffle(self.cartas)

    def _criar_baralho(self):
        pesos = {'4': 1, '5': 2, '6': 3, '7': 4,
                 'Q': 5, 'J': 6, 'K': 7, 'A': 8,
                 '2': 9, '3': 10}
        naipes = ['paus', 'copas', 'espadas', 'ouros']
        cartas = []

        for valor, peso in pesos.items():
            for naipe in naipes:
                img_path = f"assets/cards/{valor}_de_{naipe}.png"
                cartas.append(Card(valor, naipe, peso, img_path))
        return cartas

    def distribuir(self, qtd=3):
        return [self.cartas.pop() for _ in range(qtd)]
