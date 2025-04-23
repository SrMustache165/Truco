import tkinter as tk
from ui.game_ui import TrucoApp
import sys

class TelaInicial(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bem-vindo ao Truco!")
        self.geometry("1820x1024")
        self.configure(bg="#228B22")  # Verde escuro

        self._criar_widgets()

    def _criar_widgets(self):
        titulo = tk.Label(self, text="🎴 Bem-vindo ao Truco com IA 🎴", font=("Arial", 22, "bold"), fg="white", bg="#228B22")
        titulo.pack(pady=40)

        btn_novo_jogo = tk.Button(self, text="Novo Jogo", font=("Arial", 16), width=20, command=self._iniciar_jogo)
        btn_novo_jogo.pack(pady=10)

        btn_sair = tk.Button(self, text="Sair", font=("Arial", 16), width=20, command=self.quit)
        btn_sair.pack(pady=10)

    def _iniciar_jogo(self):
        self.destroy()  # Fecha a tela inicial
        jogo = TrucoApp()  # Inicia o jogo
        jogo.mainloop()
