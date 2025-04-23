# game/match.py
from game.deck import Deck

class Match:
    def __init__(self, jogador, parceiro, inimigo1, inimigo2, deck: Deck):
        # Referências aos jogadores
        self.jogador   = jogador
        self.parceiro  = parceiro
        self.inimigo1  = inimigo1
        self.inimigo2  = inimigo2

        # Ordem fixa: Você → Inimigo1 → Parceiro → Inimigo2
        self.jogadores = [jogador, inimigo1, parceiro, inimigo2]

        self.deck = deck
        # Pontos de partida (meta: 12)
        self.pontos_time_1 = 0  # Você + Parceiro
        self.pontos_time_2 = 0  # Inimigos

        # Contador de sub-rodadas vencidas (melhor de 3)
        self.vitorias_parciais = {"time1": 0, "time2": 0}

        # Estado da sub-rodada
        self.jogadas_rodada = []      # lista de tuplas (Player, Card)
        self.vez_do_jogador = jogador # quem começa a sub-rodada

    def iniciar_rodada(self):
        """Reinicia baralho e distribui 3 cartas a cada um, zera sub-rodada."""
        self.deck = Deck()
        for p in self.jogadores:
            p.receber_cartas(self.deck.distribuir(3))
        self.jogadas_rodada.clear()
        self.vitorias_parciais = {"time1": 0, "time2": 0}
        self.vez_do_jogador = self.jogador

    def jogar_carta(self, jogador, carta):
        """Remove carta da mão e registra a jogada na sub-rodada."""
        jogador.remover_carta(carta)
        self.jogadas_rodada.append((jogador, carta))

    def proximo_jogador(self):
        """Define e retorna quem joga a seguir na ordem fixa."""
        idx = self.jogadores.index(self.vez_do_jogador)
        prox = self.jogadores[(idx + 1) % len(self.jogadores)]
        self.vez_do_jogador = prox
        return prox

    def rodada_terminada(self):
        """True quando 4 cartas já foram jogadas nesta sub-rodada."""
        return len(self.jogadas_rodada) == 4

    def verificar_vencedor_jogada(self):
        """Compara as 4 cartas da sub-rodada e devolve o Player vencedor."""
        vencedor, _ = max(self.jogadas_rodada, key=lambda x: x[1].peso)
        return vencedor

    def registrar_vitoria_subrodada(self, vencedor):
        """Conta a vitória da sub-rodada para o time apropriado e limpa a mesa."""
        if vencedor in (self.jogador, self.parceiro):
            self.vitorias_parciais["time1"] += 1
        else:
            self.vitorias_parciais["time2"] += 1
        # limpa para próxima sub-rodada
        self.jogadas_rodada.clear()

    def mao_terminada(self):
        """True quando um time já ganhou 2 sub-rodadas (melhor de 3)."""
        return (self.vitorias_parciais["time1"] == 2 or
                self.vitorias_parciais["time2"] == 2)

    def vencedor_mao(self):
        """Retorna 'time1' ou 'time2' conforme quem ganhou as 2 sub-rodadas."""
        return "time1" if self.vitorias_parciais["time1"] == 2 else "time2"

    def registrar_ponto(self, dupla: str):
        """Soma 1 ponto de rodada à dupla vencedora."""
        if dupla == "time1":
            self.pontos_time_1 += 1
        else:
            self.pontos_time_2 += 1

    def partida_terminada(self):
        """True quando algum time atinge 12 pontos."""
        return (self.pontos_time_1 >= 12 or
                self.pontos_time_2 >= 12)

    def vencedor_partida(self):
        """Retorna string com o nome da dupla vencedora da partida."""
        if self.pontos_time_1 >= 12:
            return "Você e Parceiro"
        return "Dupla Inimiga"
