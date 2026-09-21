"""
EcoSort 2D: Operação Reciclagem — ponto de entrada.
"""

import pygame
import sys
from scripts.cenas import (Menu, Partida, Pausa, FaseCompleta, GameOver,
                           Vitoria, Ranking, Dialogo)
from scripts.constantes import LARGURA_TELA, ALTURA_TELA, FPS, TITULO


def main():
    pygame.init()
    pygame.display.set_caption(TITULO)
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    relogio = pygame.time.Clock()

    ranking = []
    cenas = {
        "menu": Menu(tela),
        "dialogo": Dialogo(tela),
        "partida": Partida(tela, ranking),
        "pausa": Pausa(tela),
        "fase_completa": FaseCompleta(tela),
        "game_over": GameOver(tela),
        "vitoria": Vitoria(tela),
        "ranking": Ranking(tela, ranking),
    }
    cena_atual = "menu"

    while True:
        dt = relogio.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            cenas[cena_atual].processar_evento(evento)

        novo_estado = cenas[cena_atual].atualizar(dt)

        if novo_estado != cena_atual:
            if novo_estado == "partida":
                if cena_atual in ("menu", "dialogo", "game_over", "vitoria"):
                    cenas["partida"] = Partida(tela, ranking)
                elif cena_atual == "fase_completa":
                    if getattr(cenas["fase_completa"], "precisa_reiniciar_fase", False):
                        cenas["partida"]._iniciar_fase()
                        cenas["fase_completa"].precisa_reiniciar_fase = False
            cena_atual = novo_estado

        pygame.display.flip()


if __name__ == "__main__":
    main()
