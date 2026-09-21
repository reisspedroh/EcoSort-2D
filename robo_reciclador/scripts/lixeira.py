"""
Lixeira (zona de descarte) com gráficos aprimorados.
"""

import pygame
from scripts.objeto_jogo import ObjetoJogo
from scripts.constantes import *


class Lixeira(ObjetoJogo):
    """
    Zona de descarte.
    Valida se o tipo de resíduo depositado corresponde à sua categoria.
    """

    def __init__(self, x: float, y: float, tipo: TipoMaterial):
        super().__init__(x, y, 78, 100)
        self.tipo = tipo
        self.cor = CORES_MATERIAL[tipo]
        self.acertos = 0
        self.erros = 0
        self.pulse = 0.0

    def validar_deposito(self, residuo) -> tuple:
        """
        Retorna (sucesso: bool, pontos: int)
        """
        if residuo is None:
            return False, 0

        if residuo.tipo == self.tipo:
            self.acertos += 1
            self.pulse = 0.4
            return True, 10
        else:
            self.erros += 1
            self.pulse = 0.4
            return False, -5

    def atualizar(self, dt: float) -> None:
        if self.pulse > 0:
            self.pulse -= dt

    def desenhar(self, superficie: pygame.Surface) -> None:
        # Sombra
        sombra = pygame.Surface((self.largura + 10, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 80), sombra.get_rect())
        superficie.blit(sombra, (self.rect.x - 5, self.rect.bottom - 8))

        # Corpo da lixeira
        corpo = self.rect.copy()
        pygame.draw.rect(superficie, self.cor, corpo, border_radius=8)

        # Borda com feedback de pulse
        borda_cor = BRANCO if self.pulse > 0 else PRETO
        espessura = 4 if self.pulse > 0 else 3
        pygame.draw.rect(superficie, borda_cor, corpo, espessura, border_radius=8)

        # Tampa
        tampa = pygame.Rect(self.rect.x - 5, self.rect.y - 10, self.largura + 10, 16)
        pygame.draw.rect(superficie, (25, 25, 30), tampa, border_radius=5)
        pygame.draw.rect(superficie, (60, 60, 70), tampa, 2, border_radius=5)

        # Abertura (boca da lixeira)
        abertura = pygame.Rect(self.rect.x + 16, self.rect.y + 12, self.largura - 32, 22)
        pygame.draw.rect(superficie, (20, 20, 25), abertura, border_radius=4)

        # Faixa decorativa
        pygame.draw.rect(superficie, (0, 0, 0, 40),
                         (self.rect.x + 8, self.rect.y + 45, self.largura - 16, 6))

        # Label do tipo
        fonte = pygame.font.SysFont("Arial", 15, bold=True)
        nome = NOMES_MATERIAL[self.tipo]
        texto = fonte.render(nome, True, BRANCO)
        # Fundo do texto
        fundo = texto.get_rect(center=(self.rect.centerx, self.rect.bottom - 22))
        pygame.draw.rect(superficie, (0, 0, 0, 120), fundo.inflate(10, 4), border_radius=4)
        superficie.blit(texto, fundo)
