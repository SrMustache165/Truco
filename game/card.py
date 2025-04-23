class Card:
    def __init__(self, valor, naipe, peso, imagem_path=None):
        self.valor = valor        # Ex: '4'
        self.naipe = naipe        # Ex: 'paus'
        self.peso = peso          # Peso da carta
        self.imagem_path = imagem_path

    def nome(self):
        return f"{self.valor} de {self.naipe}"

    def __str__(self):
        return self.nome()
