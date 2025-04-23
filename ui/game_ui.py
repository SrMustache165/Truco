# ui/game_ui.py
import tkinter as tk
from tkinter import messagebox
from game.deck   import Deck
from game.player import Player
from game.match  import Match
import random

class TrucoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Truco com IA – V2.1")
        self.geometry("1820x1024")

        # Configura 4 jogadores
        self.jogador   = Player("Você", is_humano=True)
        self.parceiro  = Player("Parceiro")
        self.inimigo1  = Player("Inimigo 1")
        self.inimigo2  = Player("Inimigo 2")

        # Inicia partida
        self.match = Match(self.jogador, self.parceiro,
                           self.inimigo1, self.inimigo2, Deck())
        
        # Ativa o modo debug para ver logs no console e no arquivo
        self.match.debug = True
        
        self.match.iniciar_rodada()

        # Logando cartas iniciais
        for p in self.match.jogadores:
            mao = [str(c) for c in p.mao]
            self.match.log(f"{p.nome} recebeu: {mao}")

        # Monta UI
        self._criar_widgets()
        self._atualizar_interface()

    def _criar_widgets(self):
        # Placar
        self.score_label = tk.Label(self, text="", font=("Arial", 16))
        self.score_label.pack(pady=10)

        # Mesa: nomes e cartas
        nomes = ["Você", "Inimigo 1", "Parceiro", "Inimigo 2"]
        self.frame_mesa = tk.Frame(self)
        self.frame_mesa.pack(pady=5)
        for nome in nomes:
            tk.Label(self.frame_mesa, text=nome, font=("Arial", 12))\
              .pack(side=tk.LEFT, padx=40)

        self.frame_cartas = tk.Frame(self)
        self.frame_cartas.pack(pady=5)

        # Mão do jogador
        tk.Label(self, text="Suas cartas:", font=("Arial", 14)).pack(pady=5)
        self.frame_mao = tk.Frame(self)
        self.frame_mao.pack(pady=10)

        # Label de espera/turno
        self.label_espera = tk.Label(self, text="", font=("Arial", 20, "italic"), fg="gray")
        self.label_espera.place_forget()

    def _limpar_mesa(self):
        for w in self.frame_cartas.winfo_children():
            w.destroy()

    def _atualizar_mesa(self):
        self._limpar_mesa()
        # Exibe apenas as jogadas atuais da sub-rodada
        for jogador, carta in self.match.jogadas_rodada:
            img = tk.PhotoImage(file=carta.imagem_path)
            lbl = tk.Label(self.frame_cartas, image=img)
            lbl.image = img
            lbl.pack(side=tk.LEFT, padx=40)

    def _atualizar_interface(self):
        # Atualiza placar
        t1, t2 = self.match.pontos_time_1, self.match.pontos_time_2
        self.score_label.config(
            text=f"Placar — Você/Parceiro: {t1}   Inimigos: {t2}"
        )

        # Atualiza sua mão (botões)
        for w in self.frame_mao.winfo_children():
            w.destroy()
        for carta in self.jogador.mao:
            img = tk.PhotoImage(file=carta.imagem_path)
            btn = tk.Button(self.frame_mao, image=img,
                            command=lambda c=carta: self._acao_jogar(c))
            btn.image = img
            btn.pack(side=tk.LEFT, padx=8)

    def animar_espera(self, texto, duracao):
        """Mostra um '...' animado no centro por duracao segundos."""
        self.label_espera.config(text=texto)
        self.label_espera.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.update()
        passos = int(duracao * 2)
        for i in range(passos):
            self.label_espera.config(text=f"{texto}{'.'*(i%4)}")
            self.update()
            self.after(500)
        self.label_espera.place_forget()

    def _acao_jogar(self, carta):
        # 1) Você joga 1 carta
        self.match.jogar_carta(self.jogador, carta)
        self._atualizar_mesa()
        self._atualizar_interface()
        

        # 2) Os 3 IAs jogam **exatamente 1 carta cada** (com animação)
        for ia in [self.inimigo1, self.parceiro, self.inimigo2]:
            tempo = random.randint(3, 10)
            self.animar_espera(f"{ia.nome} está pensando", tempo)
            escolha = min(ia.mao, key=lambda c: c.peso)
            self.match.jogar_carta(ia, escolha)
            self._atualizar_mesa()
            self.update()

        # 3) Encerrar sub-rodada
        vencedor = self.match.verificar_vencedor_jogada()
        self.match.registrar_vitoria_subrodada(vencedor)
        messagebox.showinfo("Sub-Rodada", f"{vencedor.nome} venceu esta jogada!")

        # 4) Se ganhou 2 sub-rodadas (melhor de 3), fecha a rodada
        if self.match.mao_terminada():
            dupla = self.match.vencedor_mao()
            # registra 1 ponto
            self.match.registrar_ponto(dupla)
            nome_dupla = "Você/Parceiro" if dupla=="time1" else "Inimigos"
            messagebox.showinfo("Rodada Completa", f"{nome_dupla} ganharam a rodada!")

            # 5) Fim de partida?
            if self.match.partida_terminada():
                champ = self.match.vencedor_partida()
                messagebox.showinfo("Fim da Partida", f"🏆 {champ} venceu o jogo!")
                return self.destroy()

            # 6) Nova rodada
            self.match.iniciar_rodada()

        # 7) Atualiza UI para a próxima sub-rodada ou rodada
        self._atualizar_mesa()
        self._atualizar_interface()


if __name__ == "__main__":
    TrucoApp().mainloop()
