class Player:
    def __init__(self, nome, is_humano=False):
        self.nome = nome
        self.is_humano = is_humano
        self.mao = []
        self.cartas_jogadas = []
        self.time = None  # Será definido na partida

    def receber_cartas(self, cartas):
        self.mao = cartas
        self.cartas_jogadas = []

    def remover_carta(self, carta):
        if carta in self.mao:
            self.mao.remove(carta)
            self.cartas_jogadas.append(carta)

    def escolher_carta(self):
        """
        Retorna a carta escolhida.
        - Se for humano, a escolha vem da interface (não usada aqui).
        - Se for IA, retorna a carta de menor peso (lógica simples).
        """
        if self.is_humano:
            # Humano escolhe via UI, então aqui não é usado.
            return None
        # IA básica: joga a carta de menor peso
        return min(self.mao, key=lambda c: c.peso) if self.mao else None
