"""
Componentes de interface (Texto, Botão, HUD).
"""

import pygame
from scripts.constantes import *


class Texto:
    def __init__(self, tela, texto: str, x: int, y: int, cor, tamanho: int, centralizado=False):
        self.tela = tela
        self.texto = texto
        self.posicao = (x, y)
        self.cor = cor
        self.tamanho = tamanho
        self.centralizado = centralizado
        self.fonte = pygame.font.SysFont("Arial", tamanho, bold=True)
        self._render()

    def _render(self):
        self.imagem = self.fonte.render(self.texto, True, self.cor)
        if self.centralizado:
            self.rect = self.imagem.get_rect(center=self.posicao)
        else:
            self.rect = self.imagem.get_rect(topleft=self.posicao)

    def desenhar(self):
        self.tela.blit(self.imagem, self.rect)

    def atualizar_texto(self, novo: str):
        self.texto = novo
        self._render()


class Botao:
    def __init__(self, tela, texto: str, x: int, y: int, largura: int, altura: int,
                 cor_fundo=AZUL, cor_texto=BRANCO, cor_hover=AZUL_ESCURO):
        self.tela = tela
        self.texto_str = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.cor_hover = cor_hover
        self.fonte = pygame.font.SysFont("Arial", 26, bold=True)
        self._clicado = False

    def desenhar(self):
        mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)
        cor = self.cor_hover if hover else self.cor_fundo
        sombra = self.rect.move(3, 4)
        pygame.draw.rect(self.tela, (0, 0, 0, 100), sombra, border_radius=10)
        pygame.draw.rect(self.tela, cor, self.rect, border_radius=10)
        pygame.draw.rect(self.tela, BRANCO, self.rect, 2, border_radius=10)
        img = self.fonte.render(self.texto_str, True, self.cor_texto)
        self.tela.blit(img, img.get_rect(center=self.rect.center))

    def get_click(self) -> bool:
        mouse = pygame.mouse.get_pos()
        pressionado = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and pressionado:
            if not self._clicado:
                self._clicado = True
                return True
        else:
            self._clicado = False
        return False


class HUD:
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.SysFont("Arial", 18, bold=True)

    def desenhar(self, fase: int, pontos: int, pontos_fase: int, meta: int,
                 tempo: float, inventario_nome: str, pecas: int = 0, residuos_esteira: int = 0):
        pygame.draw.rect(self.tela, (18, 20, 28), (0, 0, LARGURA_TELA, 52))
        pygame.draw.line(self.tela, (60, 70, 90), (0, 52), (LARGURA_TELA, 52), 2)

        cor_acum = VERMELHO if residuos_esteira >= MAX_RESIDUOS_ACUMULADOS - 3 else BRANCO
        itens = [
            (f"Fase {fase}/{TOTAL_FASES}", BRANCO, 10),
            (f"Pts: {pontos}", AMARELO, 110),
            (f"Meta: {pontos_fase}/{meta}", VERDE, 220),
            (f"Tempo: {max(0, int(tempo))}s", VERMELHO if tempo < 10 else BRANCO, 360),
            (f"Item: {inventario_nome}", CIANO, 500),
            (f"Peças: {pecas}", (255, 200, 50), 660),
            (f"Esteira: {residuos_esteira}/{MAX_RESIDUOS_ACUMULADOS}", cor_acum, 780),
        ]
        for texto, cor, x in itens:
            img = self.fonte.render(texto, True, cor)
            self.tela.blit(img, (x, 16))
