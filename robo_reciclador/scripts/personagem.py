"""
Personagem (Robô jogável) com gráficos aprimorados.
"""

import math
import pygame
from scripts.objeto_jogo import ObjetoJogo
from scripts.constantes import *


class Personagem(ObjetoJogo):
    """
    Robô controlável.
    - Movimento em 8 direções (WASD / setas)
    - Inventário de um único item
    """

    VELOCIDADE_BASE = 4.8

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 52, 56)
        self.velocidade = self.VELOCIDADE_BASE
        self.inventario = None          # Residuo ou None
        self.direcao_x = 0.0
        self.direcao_y = 0.0
        self.anim_timer = 0.0
        self.olhando_direita = True
        self.pecas = 0                  # peças de upgrade acumuladas
        self.nivel_upgrade = 0          # nível visual (0 a MAX)

    def coletar_peca(self) -> None:
        """Acumula uma peça e aplica melhoria de velocidade."""
        self.pecas += 1
        self.nivel_upgrade = min(self.pecas, MAX_PECAS_BONUS)
        bonus = min(self.pecas, MAX_PECAS_BONUS) * BONUS_VELOCIDADE_POR_PECA
        self.velocidade = self.VELOCIDADE_BASE + bonus

    def processar_input(self, teclas) -> None:
        self.direcao_x = 0.0
        self.direcao_y = 0.0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.direcao_x = -1
            self.olhando_direita = False
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.direcao_x = 1
            self.olhando_direita = True

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.direcao_y = -1
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.direcao_y = 1

        # Normalização diagonal
        if self.direcao_x != 0 and self.direcao_y != 0:
            fator = 1 / math.sqrt(2)
            self.direcao_x *= fator
            self.direcao_y *= fator

    def atualizar(self, limites, dt: float) -> None:
        self.x += self.direcao_x * self.velocidade
        self.y += self.direcao_y * self.velocidade

        esq, topo, dir_, baixo = limites
        self.x = max(esq, min(self.x, dir_ - self.largura))
        self.y = max(topo, min(self.y, baixo - self.altura))
        self.atualizar_rect()

        # Animação contínua
        self.anim_timer += dt * 8

    def coletar(self, residuo) -> bool:
        if self.inventario is None and residuo.ativo:
            self.inventario = residuo
            residuo.ativo = False
            return True
        return False

    def depositar(self):
        item = self.inventario
        self.inventario = None
        return item

    def tem_item(self) -> bool:
        return self.inventario is not None

    def desenhar(self, superficie: pygame.Surface) -> None:
        # Sombra
        sombra = pygame.Surface((self.largura + 8, 14), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 70), sombra.get_rect())
        superficie.blit(sombra, (self.rect.x - 4, self.rect.bottom - 6))

        # Corpo principal (fica mais dourado conforme upgrades)
        nivel = self.nivel_upgrade
        if nivel >= 6:
            cor_corpo = (90, 80, 40)
            cor_borda = (180, 150, 40)
        elif nivel >= 3:
            cor_corpo = (70, 75, 90)
            cor_borda = (100, 110, 80)
        else:
            cor_corpo = (55, 70, 95)
            cor_borda = (30, 45, 70)

        corpo = pygame.Rect(self.rect.x + 4, self.rect.y + 12, 44, 36)
        pygame.draw.rect(superficie, cor_corpo, corpo, border_radius=10)
        pygame.draw.rect(superficie, cor_borda, corpo, 3, border_radius=10)

        # Detalhe de painel frontal
        painel = pygame.Rect(self.rect.x + 10, self.rect.y + 20, 32, 18)
        pygame.draw.rect(superficie, (40, 55, 80), painel, border_radius=4)

        # Luzes de upgrade no painel (quantas peças tiver, até 4)
        for i in range(min(nivel, 4)):
            lx = self.rect.x + 14 + i * 8
            ly = self.rect.y + 26
            pygame.draw.circle(superficie, (255, 220, 50), (lx, ly), 3)
            pygame.draw.circle(superficie, (255, 255, 180), (lx, ly), 1)

        # Olhos (com brilho) — ficam mais intensos com upgrades
        olho_y = self.rect.y + 28
        offset_x = 6 if self.olhando_direita else -6
        cor_olho = (255, 230, 80) if nivel >= 5 else CIANO
        # Olho esquerdo
        pygame.draw.circle(superficie, cor_olho, (self.rect.x + 18 + offset_x // 2, olho_y), 7)
        pygame.draw.circle(superficie, (20, 40, 60), (self.rect.x + 18 + offset_x // 2, olho_y), 7, 2)
        pygame.draw.circle(superficie, BRANCO, (self.rect.x + 16 + offset_x // 2, olho_y - 2), 2)
        # Olho direito
        pygame.draw.circle(superficie, cor_olho, (self.rect.x + 34 + offset_x // 2, olho_y), 7)
        pygame.draw.circle(superficie, (20, 40, 60), (self.rect.x + 34 + offset_x // 2, olho_y), 7, 2)
        pygame.draw.circle(superficie, BRANCO, (self.rect.x + 32 + offset_x // 2, olho_y - 2), 2)

        # Cabeça / capacete
        cabeca = pygame.Rect(self.rect.x + 8, self.rect.y + 2, 36, 18)
        pygame.draw.rect(superficie, (70, 90, 120), cabeca, border_radius=8)
        pygame.draw.rect(superficie, (40, 55, 80), cabeca, 2, border_radius=8)

        # Antena animada (fica dourada com muitos upgrades)
        antena_x = self.rect.centerx
        antena_y = self.rect.y + 2
        balanco = math.sin(self.anim_timer) * 3
        cor_antena = (255, 200, 50) if nivel >= 4 else CINZA_CLARO
        pygame.draw.line(superficie, cor_antena,
                         (antena_x, antena_y),
                         (antena_x + balanco, antena_y - 14), 3)
        pygame.draw.circle(superficie, VERMELHO if nivel < 4 else (255, 180, 30),
                           (int(antena_x + balanco), int(antena_y - 16)), 5)
        pygame.draw.circle(superficie, (255, 120, 120),
                           (int(antena_x + balanco - 1), int(antena_y - 17)), 2)

        # Rodas / esteiras laterais
        for dx in (-2, self.largura - 10):
            pygame.draw.rect(superficie, (40, 40, 50),
                             (self.rect.x + dx, self.rect.bottom - 12, 12, 10),
                             border_radius=3)
            pygame.draw.circle(superficie, (80, 80, 90),
                               (self.rect.x + dx + 6, self.rect.bottom - 7), 3)

        # Indicador de inventário (bolha acima)
        if self.inventario is not None:
            cor = CORES_MATERIAL[self.inventario.tipo]
            bx = self.rect.centerx - 14
            by = self.rect.y - 32
            pygame.draw.rect(superficie, (30, 30, 40), (bx - 2, by - 2, 32, 24), border_radius=6)
            pygame.draw.rect(superficie, cor, (bx, by, 28, 20), border_radius=5)
            pygame.draw.rect(superficie, BRANCO, (bx, by, 28, 20), 1, border_radius=5)
            pygame.draw.polygon(superficie, (30, 30, 40),
                                [(self.rect.centerx - 5, by + 22),
                                 (self.rect.centerx + 5, by + 22),
                                 (self.rect.centerx, by + 28)])
