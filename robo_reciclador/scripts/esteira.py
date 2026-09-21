"""
Esteira transportadora: spawna e move resíduos, peças e botões de emergência.
Suporta pausa (parada de emergência) e sentido invertido (segunda esteira).
"""

import random
import pygame
from scripts.objeto_jogo import ObjetoJogo
from scripts.residuo import Residuo
from scripts.peca import Peca
from scripts.emergencia import ParadaEmergencia
from scripts.constantes import *


class Esteira(ObjetoJogo):
    def __init__(self, x: float, y: float, largura: int, altura: int, invertida: bool = False):
        super().__init__(x, y, largura, altura)
        self.residuos: list = []
        self.pecas: list = []
        self.emergencias: list = []
        self.velocidade = 1.5
        self.intervalo_spawn = 1.8
        self.tempo_desde_ultimo = 0.0
        self.tipos_disponiveis = list(TipoMaterial)
        self.offset_visual = 0.0
        self.invertida = invertida
        self.pausada = False
        self.tempo_pausa = 0.0

    def definir_dificuldade(self, velocidade: float, intervalo: float, tipos: list) -> None:
        self.velocidade = velocidade
        self.intervalo_spawn = intervalo
        self.tipos_disponiveis = tipos

    def ativar_pausa(self, duracao: float) -> None:
        self.pausada = True
        self.tempo_pausa = duracao

    def atualizar(self, dt: float) -> int:
        if self.pausada:
            self.tempo_pausa -= dt
            if self.tempo_pausa <= 0:
                self.pausada = False
                self.tempo_pausa = 0.0
            return 0

        self.tempo_desde_ultimo += dt
        sentido = -1 if self.invertida else 1
        self.offset_visual = (self.offset_visual + self.velocidade * 30 * dt * sentido) % 48

        if self.tempo_desde_ultimo >= self.intervalo_spawn:
            self._spawn_item()
            self.tempo_desde_ultimo = 0.0

        perdidos = 0

        for r in self.residuos:
            if r.ativo:
                if self.invertida:
                    r.y -= abs(self.velocidade)
                else:
                    r.y += abs(self.velocidade)
                r.atualizar_rect()
                if hasattr(r, "tempo_vida"):
                    r.tempo_vida += dt
                if (not self.invertida and r.y > ALTURA_TELA + 30) or (self.invertida and r.y < -40):
                    r.ativo = False
                    perdidos += 1
        self.residuos = [r for r in self.residuos if r.ativo]

        for p in self.pecas:
            if p.ativo:
                if self.invertida:
                    p.y -= abs(self.velocidade)
                else:
                    p.y += abs(self.velocidade)
                p.atualizar(dt)
        self.pecas = [p for p in self.pecas if p.ativo]

        for e in self.emergencias:
            if e.ativo:
                if self.invertida:
                    e.y -= abs(self.velocidade)
                else:
                    e.y += abs(self.velocidade)
                e.atualizar(dt)
        self.emergencias = [e for e in self.emergencias if e.ativo]

        return perdidos

    def _spawn_item(self) -> None:
        margem = 50
        x = random.randint(int(self.x) + margem, int(self.x) + self.largura - margem - 36)
        y = self.rect.bottom - 10 if self.invertida else self.y - 25

        roll = random.random()
        if roll < CHANCE_SPAWN_EMERGENCIA:
            self.emergencias.append(ParadaEmergencia(x, y))
        elif roll < CHANCE_SPAWN_EMERGENCIA + CHANCE_SPAWN_PECA:
            self.pecas.append(Peca(x, y))
        else:
            if not self.tipos_disponiveis:
                return
            tipo = random.choice(self.tipos_disponiveis)
            self.residuos.append(Residuo(x, y, tipo))

    def obter_residuos_ativos(self) -> list:
        return [r for r in self.residuos if r.ativo]

    def obter_pecas_ativas(self) -> list:
        return [p for p in self.pecas if p.ativo]

    def obter_emergencias_ativas(self) -> list:
        return [e for e in self.emergencias if e.ativo]

    def quantidade_residuos(self) -> int:
        return len(self.obter_residuos_ativos())

    def desenhar(self, superficie: pygame.Surface) -> None:
        cor_base = (45, 48, 58) if not self.pausada else (70, 50, 50)
        pygame.draw.rect(superficie, cor_base, self.rect)
        pygame.draw.rect(superficie, (70, 75, 90), self.rect, 2)

        for i in range(-1, self.altura // 48 + 3):
            y = self.rect.y + i * 48 + int(self.offset_visual)
            pygame.draw.line(superficie, (65, 70, 85),
                             (self.rect.x + 8, y), (self.rect.right - 8, y), 3)

        pygame.draw.rect(superficie, (90, 95, 110), (self.rect.x, self.rect.y, 10, self.altura))
        pygame.draw.rect(superficie, (90, 95, 110), (self.rect.right - 10, self.rect.y, 10, self.altura))

        if self.pausada:
            fonte = pygame.font.SysFont("Arial", 18, bold=True)
            txt = fonte.render(f"PARADA {self.tempo_pausa:.1f}s", True, VERMELHO)
            superficie.blit(txt, txt.get_rect(center=self.rect.center))

        for r in self.residuos:
            r.desenhar(superficie)
        for p in self.pecas:
            p.desenhar(superficie)
        for e in self.emergencias:
            e.desenhar(superficie)
