# Jogo de Truco com IA

Este é um projeto de **Jogo de Truco** desenvolvido em **Python**, com **Tkinter** para a interface gráfica e **Inteligência Artificial (IA)** para controlar os adversários. O objetivo é proporcionar uma experiência interativa de jogo de Truco com a possibilidade de jogar contra adversários controlados por IA.

## Funcionalidades

- **Regras Reais de Truco:** Jogo baseado nas regras clássicas do Truco, onde dois times competem até 12 pontos.
- **IA para os Adversários:** O jogo conta com 2 adversários controlados por IA, e um parceiro tambem controlado por IA, cada um com um comportamento estratégico para tentar vencer jogo.
- **Interface Gráfica com Tkinter:** A interface foi construída usando o Tkinter, proporcionando uma experiência visual simples e intuitiva.
- **Simulação de Rodadas:** Cada rodada consiste em cada jogador jogando uma carta e, com base na maior carta, o vencedor é determinado.

## Como Jogar

1. Execute o código Python (`main.py`).
2. O jogo começa automaticamente com a distribuição das cartas.
3. O jogador deve escolher uma carta para jogar a cada rodada. Os adversários controlados por IA também jogam suas cartas.
4. Após todas as cartas serem jogadas, o vencedor da rodada é determinado, e a pontuação dos times é atualizada.
5. O jogo segue até que um time consiga acumular 12 pontos.

## Pré-requisitos

- Python 3.6 ou superior
- Tkinter (geralmente já incluído nas distribuições padrão do Python)

## Instalação

Clone o repositório para a sua máquina local:

```bash
git clone https://github.com/seu-usuario/truco-ia.git
cd truco-ia
