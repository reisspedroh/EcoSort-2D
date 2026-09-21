"""
Botão de Parada de Emergência — item especial que congela a esteira.
"""

import math
import pygame
from scripts.objeto_jogo import ObjetoJogo
from scripts.constantes import *


class ParadaEmergencia(ObjetoJogo):
    """
    Item especial que cai na esteira.
    Ao ser coletado, paralisa todas as esteiras por DURACAO_PARADA_EMERGENCIA segundos.
    """

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 30, 30)
        self.velocidade_y = 0.0
        self.tempo_vida = 0.0

    def atualizar(self, dt: float) -> None:
        self.y += self.velocidade_y
        self.tempo_vida += dt
        self.atualizar_rect()
        if self.y > ALTURA_TELA + 20:
            self.ativo = False

    def desenhar(self, superficie: pygame.Surface) -> None:
        if not self.ativo:
            return

        pulso = 0.7 + 0.3 * math.sin(self.tempo_vida * 8)
        cx, cy = self.rect.center

        # Aura vermelha
        aura = pygame.Surface((44, 44), pygame.SRCALPHA)
        pygame.draw.circle(aura, (230, 60, 70, int(80 * pulso)), (22, 22), 20)
        superficie.blit(aura, (cx - 22, cy - 22))

        # Botão circular
        pygame.draw.circle(superficie, VERMELHO, (cx, cy), 14)
        pygame.draw.circle(superficie, (180, 30, 40), (cx, cy), 14, 2)
        pygame.draw.circle(superficie, BRANCO, (cx, cy), 8, 2)

        # Ícone de stop (quadrado)
        pygame.draw.rect(superficie, BRANCO, (cx - 5, cy - 5, 10, 10))
