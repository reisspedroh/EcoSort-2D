"""
Resíduo coletável com gráficos aprimorados e ícones distintos.
"""

import math
import pygame
from scripts.objeto_jogo import ObjetoJogo
from scripts.constantes import *


class Residuo(ObjetoJogo):
    """
    Objeto coletável.
    Contém o tipo de material e renderização visual correspondente.
    """

    def __init__(self, x: float, y: float, tipo: TipoMaterial):
        super().__init__(x, y, 36, 36)
        self.tipo = tipo
        self.cor = CORES_MATERIAL[tipo]
        self.velocidade_y = 0.0
        self.rotacao = 0.0
        self.tempo_vida = 0.0

    def atualizar(self, dt: float) -> None:
        self.y += self.velocidade_y
        self.rotacao += dt * 40          # leve rotação
        self.tempo_vida += dt
        self.atualizar_rect()

        if self.y > ALTURA_TELA + 30:
            self.ativo = False

    def desenhar(self, superficie: pygame.Surface) -> None:
        if not self.ativo:
            return

        # Sombra
        sombra = pygame.Surface((self.largura + 6, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 60), sombra.get_rect())
        superficie.blit(sombra, (self.rect.x - 3, self.rect.bottom - 4))

        # Corpo principal com leve brilho
        pygame.draw.rect(superficie, self.cor, self.rect, border_radius=8)
        # Borda mais escura
        cor_borda = tuple(max(0, c - 50) for c in self.cor)
        pygame.draw.rect(superficie, cor_borda, self.rect, 2, border_radius=8)

        # Brilho superior
        brilho = pygame.Surface((self.largura - 8, 10), pygame.SRCALPHA)
        pygame.draw.rect(brilho, (255, 255, 255, 50), brilho.get_rect(), border_radius=4)
        superficie.blit(brilho, (self.rect.x + 4, self.rect.y + 4))

        # Ícone específico por tipo
        cx, cy = self.rect.center
        self._desenhar_icone(superficie, cx, cy)

    def _desenhar_icone(self, superficie: pygame.Surface, cx: int, cy: int) -> None:
        if self.tipo == TipoMaterial.PLASTICO:
            # Garrafa estilizada
            pygame.draw.rect(superficie, BRANCO, (cx - 5, cy - 10, 10, 16), 2, border_radius=2)
            pygame.draw.rect(superficie, BRANCO, (cx - 3, cy - 14, 6, 5), 2)

        elif self.tipo == TipoMaterial.PAPEL:
            # Folhas
            pygame.draw.line(superficie, BRANCO, (cx - 9, cy - 7), (cx + 9, cy - 7), 2)
            pygame.draw.line(superficie, BRANCO, (cx - 9, cy), (cx + 9, cy), 2)
            pygame.draw.line(superficie, BRANCO, (cx - 9, cy + 7), (cx + 9, cy + 7), 2)
            pygame.draw.line(superficie, BRANCO, (cx - 9, cy - 7), (cx - 9, cy + 7), 2)

        elif self.tipo == TipoMaterial.VIDRO:
            # Taça / triângulo
            pontos = [(cx, cy - 11), (cx - 9, cy + 9), (cx + 9, cy + 9)]
            pygame.draw.polygon(superficie, BRANCO, pontos, 2)

        elif self.tipo == TipoMaterial.METAL:
            # Lata
            pygame.draw.rect(superficie, BRANCO, (cx - 8, cy - 8, 16, 16), 2, border_radius=2)
            pygame.draw.line(superficie, BRANCO, (cx - 8, cy - 3), (cx + 8, cy - 3), 2)
            pygame.draw.line(superficie, BRANCO, (cx - 8, cy + 3), (cx + 8, cy + 3), 2)

        elif self.tipo == TipoMaterial.ORGANICO:
            # Folha / elipse
            pygame.draw.ellipse(superficie, BRANCO, (cx - 9, cy - 7, 18, 14), 2)
            pygame.draw.line(superficie, BRANCO, (cx, cy - 7), (cx, cy + 7), 2)

        elif self.tipo == TipoMaterial.PERIGOSO:
            # Pilha / raio de perigo
            pygame.draw.rect(superficie, BRANCO, (cx - 6, cy - 8, 12, 16), 2, border_radius=2)
            pygame.draw.line(superficie, BRANCO, (cx - 3, cy - 4), (cx + 3, cy), 2)
            pygame.draw.line(superficie, BRANCO, (cx + 3, cy), (cx - 3, cy + 4), 2)
