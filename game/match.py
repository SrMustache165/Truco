import time
import logging
from game.deck import Deck

class Match:
    def __init__(self, jogador, parceiro, inimigo1, inimigo2, deck: Deck, debug=False):
        self.jogador = jogador
        self.parceiro = parceiro
        self.inimigo1 = inimigo1
        self.inimigo2 = inimigo2

        self.jogadores = [jogador, inimigo1, parceiro, inimigo2]
        self.deck = deck

        self.pontos_time_1 = 0
        self.pontos_time_2 = 0
        self.vitorias_parciais = {"time1": 0, "time2": 0}
        self.jogadas_rodada = []
        self.vez_do_jogador = jogador

        self.debug = debug
        if self.debug:
            logging.basicConfig(
                filename='debug.log',
                level=logging.DEBUG,
                format='%(asctime)s [%(levelname)s] %(message)s'
            )

    def log(self, mensagem):
        if self.debug:
            print(mensagem)
            logging.debug(mensagem)

    def iniciar_rodada(self):
        self.deck = Deck()
        for p in self.jogadores:
            p.receber_cartas(self.deck.distribuir(3))
        self.jogadas_rodada.clear()
        self.vitorias_parciais = {"time1": 0, "time2": 0}
        self.vez_do_jogador = self.jogador

        if self.debug:
            self.log("\n=== NOVA RODADA ===")
            for p in self.jogadores:
                cartas = [str(c) for c in p.mao]
                self.log(f"{p.nome}: {cartas}")

    def jogar_carta(self, jogador, carta):
        jogador.remover_carta(carta)
        self.jogadas_rodada.append((jogador, carta))
        self.log(f"{jogador.nome} jogou: {carta}")

    def proximo_jogador(self):
        idx = self.jogadores.index(self.vez_do_jogador)
        prox = self.jogadores[(idx + 1) % len(self.jogadores)]
        self.vez_do_jogador = prox
        return prox

    def rodada_terminada(self):
        return len(self.jogadas_rodada) == 4

    def verificar_vencedor_jogada(self):
        vencedor, carta = max(self.jogadas_rodada, key=lambda x: x[1].peso)
        self.log(f"🃏 Vencedor da jogada: {vencedor.nome} com {carta}")
        return vencedor

    def registrar_vitoria_subrodada(self, vencedor):
        if vencedor in (self.jogador, self.parceiro):
            self.vitorias_parciais["time1"] += 1
        else:
            self.vitorias_parciais["time2"] += 1
        self.jogadas_rodada.clear()

        self.log(f"Sub-rodada vencida por: {'Time 1' if vencedor in (self.jogador, self.parceiro) else 'Time 2'}")
        self.log(f"Parciais → Time1: {self.vitorias_parciais['time1']} | Time2: {self.vitorias_parciais['time2']}")

    def mao_terminada(self):
        return self.vitorias_parciais["time1"] == 2 or self.vitorias_parciais["time2"] == 2

    def vencedor_mao(self):
        return "time1" if self.vitorias_parciais["time1"] == 2 else "time2"

    def registrar_ponto(self, dupla: str):
        if dupla == "time1":
            self.pontos_time_1 += 1
        else:
            self.pontos_time_2 += 1
        self.log(f"PONTO PARA {'Time 1 (Você/Parceiro)' if dupla == 'time1' else 'Time 2 (Inimigos)'}")
        self.log(f"PLACAR ATUAL — Time1: {self.pontos_time_1} | Time2: {self.pontos_time_2}")

    def partida_terminada(self):
        return self.pontos_time_1 >= 12 or self.pontos_time_2 >= 12

    def vencedor_partida(self):
        vencedor = "Você e Parceiro" if self.pontos_time_1 >= 12 else "Dupla Inimiga"
        self.log(f"🏆 Fim da Partida - Vencedor: {vencedor}")
        return vencedor

    def tempo_ia(self, funcao_escolha, *args):
        inicio = time.time()
        resultado = funcao_escolha(*args)
        fim = time.time()
        tempo = fim - inicio
        self.log(f"⏱️ IA decidiu em {tempo:.2f} segundos.")
        return resultado
