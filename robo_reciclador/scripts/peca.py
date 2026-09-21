"""
Peça de Upgrade: cai junto com os resíduos e melhora o robô ao ser coletada.
"""

import math
import pygame
from scripts.objeto_jogo import ObjetoJogo
from scripts.constantes import *


class Peca(ObjetoJogo):
    """
    Item especial que cai na esteira.
    Coletado automaticamente (não ocupa inventário).
    Acumula e melhora o robô.
    """

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 28, 28)
        self.velocidade_y = 0.0
        self.tempo_vida = 0.0
        self.rotacao = 0.0

    def atualizar(self, dt: float) -> None:
        self.y += self.velocidade_y
        self.rotacao += dt * 90
        self.tempo_vida += dt
        self.atualizar_rect()

        if self.y > ALTURA_TELA + 20:
            self.ativo = False

    def desenhar(self, superficie: pygame.Surface) -> None:
        if not self.ativo:
            return

        # Brilho pulsante
        pulso = 0.6 + 0.4 * math.sin(self.tempo_vida * 6)
        tamanho = int(14 + 3 * pulso)

        # Aura externa
        aura = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(aura, (255, 215, 0, int(60 * pulso)), (20, 20), 18)
        superficie.blit(aura, (self.rect.centerx - 20, self.rect.centery - 20))

        # Corpo da peça (engrenagem / chip dourado)
        cx, cy = self.rect.center
        pygame.draw.circle(superficie, (255, 200, 50), (cx, cy), tamanho)
        pygame.draw.circle(superficie, (255, 240, 150), (cx, cy), tamanho - 4)
        pygame.draw.circle(superficie, (180, 120, 20), (cx, cy), tamanho, 2)

        # Detalhe interno (cruz / chip)
        pygame.draw.rect(superficie, (180, 120, 20), (cx - 6, cy - 2, 12, 4))
        pygame.draw.rect(superficie, (180, 120, 20), (cx - 2, cy - 6, 4, 12))
        pygame.draw.circle(superficie, (255, 255, 200), (cx, cy), 3)
