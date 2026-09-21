"""
Cenas do jogo EcoSort 2D: Menu, Partida, Pausa, FaseCompleta, GameOver, Vitoria, Ranking, Dialogo.
"""

import math
import pygame
from scripts.personagem import Personagem
from scripts.esteira import Esteira
from scripts.lixeira import Lixeira
from scripts.interfaces import Texto, Botao, HUD
from scripts.constantes import *


class CenaBase:
    def __init__(self, tela):
        self.tela = tela
        self.estado = "menu"

    def atualizar(self, dt: float) -> str:
        return self.estado

    def processar_evento(self, evento) -> None:
        pass


class Menu(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)
        self.titulo = Texto(tela, "EcoSort 2D", LARGURA_TELA // 2, 140, VERDE, 52, True)
        self.subtitulo = Texto(tela, "Operação Reciclagem — EcoBot-01", LARGURA_TELA // 2, 200, BRANCO, 24, True)
        self.botao_jogar = Botao(tela, "JOGAR", LARGURA_TELA // 2 - 110, 320, 220, 55)
        self.botao_ranking = Botao(tela, "RANKING", LARGURA_TELA // 2 - 110, 400, 220, 55,
                                  cor_fundo=LARANJA, cor_hover=(180, 100, 20))
        self.instrucoes = [
            "WASD / Setas  →  Mover (8 direções)",
            "Colisão       →  Coletar resíduo / peça / emergência",
            "E / ESPAÇO    →  Depositar na lixeira",
            "ESC           →  Pausar",
        ]

    def atualizar(self, dt: float) -> str:
        self.estado = "menu"
        self.tela.fill(CINZA_ESCURO)
        for i in range(8):
            s = pygame.Surface((LARGURA_TELA, 60), pygame.SRCALPHA)
            s.fill((40, 50, 70, 30 + i * 8))
            self.tela.blit(s, (0, 100 + i * 80))

        self.titulo.desenhar()
        self.subtitulo.desenhar()
        for i, linha in enumerate(self.instrucoes):
            Texto(self.tela, linha, LARGURA_TELA // 2, 480 + i * 28, CINZA_CLARO, 18, True).desenhar()
        self.botao_jogar.desenhar()
        self.botao_ranking.desenhar()

        if self.botao_jogar.get_click():
            self.estado = "dialogo"
        if self.botao_ranking.get_click():
            self.estado = "ranking"
        return self.estado


class Dialogo(CenaBase):
    """Gerente do Galpão — introdução no início do expediente."""

    def __init__(self, tela):
        super().__init__(tela)
        self.linhas = [
            "Gerente do Galpão:",
            "",
            "Bem-vindo ao turno, EcoBot-01!",
            "Separe os resíduos nas lixeiras corretas.",
            "Não deixe a esteira lotar (máx. 10 itens).",
            "Peças douradas melhoram sua velocidade.",
            "Botão vermelho = Parada de Emergência (5s).",
            "",
            "Pressione ENTER para começar o expediente.",
        ]
        self.botao = Botao(tela, "INICIAR TURNO", LARGURA_TELA // 2 - 130, 620, 260, 50,
                           cor_fundo=VERDE, cor_hover=VERDE_ESCURO)

    def processar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            self.estado = "partida"

    def atualizar(self, dt: float) -> str:
        self.estado = "dialogo"
        self.tela.fill(CINZA_ESCURO)
        # Caixa de diálogo
        caixa = pygame.Rect(80, 120, LARGURA_TELA - 160, 460)
        pygame.draw.rect(self.tela, (30, 35, 45), caixa, border_radius=12)
        pygame.draw.rect(self.tela, VERDE, caixa, 3, border_radius=12)

        for i, linha in enumerate(self.linhas):
            cor = AMARELO if i == 0 else BRANCO
            Texto(self.tela, linha, LARGURA_TELA // 2, 160 + i * 36, cor, 22, True).desenhar()

        self.botao.desenhar()
        if self.botao.get_click():
            self.estado = "partida"
        return self.estado


class Partida(CenaBase):
    def __init__(self, tela, ranking_ref: list):
        super().__init__(tela)
        self.ranking = ranking_ref
        self.fase_atual = 1
        self.pontuacao = 0
        self.pontuacao_fase = 0
        self.tempo_restante = 55.0
        self.mensagem = ""
        self.tempo_msg = 0.0
        self.hud = HUD(tela)
        self.personagem = None
        self.esteiras: list = []
        self.lixeiras = []
        self.alerta_sobrecarga = False
        self._iniciar_fase()

    def _iniciar_fase(self):
        vel, intervalo, tempo = DIFICULDADE[self.fase_atual]
        tipos = MATERIAIS_POR_FASE[self.fase_atual]
        self.tempo_restante = float(tempo)
        self.pontuacao_fase = 0
        self.mensagem = ""
        self.tempo_msg = 0.0
        self.alerta_sobrecarga = False

        pecas_anteriores = self.personagem.pecas if self.personagem else 0
        self.personagem = Personagem(LARGURA_TELA // 2 - 26, ALTURA_TELA - 160)
        for _ in range(pecas_anteriores):
            self.personagem.coletar_peca()

        self.esteiras = []
        # Esteira principal (desce)
        e1 = Esteira(200, 55, LARGURA_TELA - 400, ALTURA_TELA - 180, invertida=False)
        e1.definir_dificuldade(vel, intervalo, tipos)
        self.esteiras.append(e1)

        # Segunda esteira a partir da fase 4 (sobe, lado direito)
        if self.fase_atual >= FASE_SEGUNDA_ESTEIRA:
            e2 = Esteira(LARGURA_TELA - 180, 55, 140, ALTURA_TELA - 180, invertida=True)
            e2.definir_dificuldade(vel * 0.9, intervalo * 1.1, tipos)
            self.esteiras.append(e2)

        self.lixeiras = []
        n = len(tipos)
        espaco = (LARGURA_TELA - 80) // max(n, 1)
        for i, tipo in enumerate(tipos):
            x = 40 + i * espaco + (espaco - 78) // 2
            self.lixeiras.append(Lixeira(x, ALTURA_TELA - 120, tipo))

    def processar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.estado = "pausa"
            elif evento.key in (pygame.K_e, pygame.K_SPACE):
                self._tentar_depositar()

    def _tentar_depositar(self):
        if not self.personagem.tem_item():
            return
        melhor, menor = None, float("inf")
        px, py = self.personagem.rect.center
        for l in self.lixeiras:
            dist = math.hypot(px - l.rect.centerx, py - l.rect.centery)
            if dist < menor and dist < 110:
                menor, melhor = dist, l
        if melhor is None:
            self.mensagem = "Aproxime-se de uma lixeira!"
            self.tempo_msg = 1.4
            return
        item = self.personagem.depositar()
        ok, pts = melhor.validar_deposito(item)
        self.pontuacao += pts
        if pts > 0:
            self.pontuacao_fase += pts
        self.mensagem = f"+{pts}  Correto!" if ok else f"{pts}  Tipo errado!"
        self.tempo_msg = 1.2 if ok else 1.4

    def _total_residuos_nas_esteiras(self) -> int:
        return sum(e.quantidade_residuos() for e in self.esteiras)

    def atualizar(self, dt: float) -> str:
        self.estado = "partida"
        teclas = pygame.key.get_pressed()
        self.personagem.processar_input(teclas)
        self.personagem.atualizar((0, 55, LARGURA_TELA, ALTURA_TELA - 130), dt)

        perdidos = 0
        for e in self.esteiras:
            perdidos += e.atualizar(dt)
        if perdidos > 0:
            perda = perdidos * PONTOS_ITEM_PERDIDO
            self.pontuacao = max(0, self.pontuacao + perda)
            self.mensagem = f"{perda}  Item perdido!"
            self.tempo_msg = 1.2

        for l in self.lixeiras:
            l.atualizar(dt)

        # Coleta peças
        for e in self.esteiras:
            for p in e.obter_pecas_ativas():
                if self.personagem.colide_com(p) and p.ativo:
                    p.ativo = False
                    self.personagem.coletar_peca()
                    self.pontuacao += PONTOS_POR_PECA
                    self.mensagem = f"+{PONTOS_POR_PECA}  Peça! Velocidade ↑"
                    self.tempo_msg = 1.0
                    break

        # Coleta emergência
        for e in self.esteiras:
            for em in e.obter_emergencias_ativas():
                if self.personagem.colide_com(em) and em.ativo:
                    em.ativo = False
                    for est in self.esteiras:
                        est.ativar_pausa(DURACAO_PARADA_EMERGENCIA)
                    self.mensagem = "PARADA DE EMERGÊNCIA! 5s"
                    self.tempo_msg = 2.0
                    break

        # Coleta resíduos
        if not self.personagem.tem_item():
            for e in self.esteiras:
                for r in e.obter_residuos_ativos():
                    if self.personagem.colide_com(r):
                        if self.personagem.coletar(r):
                            self.mensagem = f"Coletou {NOMES_MATERIAL[r.tipo]}"
                            self.tempo_msg = 0.7
                            break

        # Alerta sobrecarga
        total_res = self._total_residuos_nas_esteiras()
        self.alerta_sobrecarga = total_res >= MAX_RESIDUOS_ACUMULADOS - 3

        # Game over por acúmulo
        if total_res >= MAX_RESIDUOS_ACUMULADOS:
            self._salvar_ranking()
            self.estado = "game_over"
            return self.estado

        self.tempo_restante -= dt
        if self.tempo_msg > 0:
            self.tempo_msg -= dt

        meta = META_PONTOS[self.fase_atual]
        if self.pontuacao_fase >= meta:
            if self.fase_atual >= TOTAL_FASES:
                self._salvar_ranking()
                self.estado = "vitoria"
            else:
                self.fase_atual += 1
                self.estado = "fase_completa"
            return self.estado

        if self.tempo_restante <= 0:
            self.tempo_restante = 0
            self._salvar_ranking()
            self.estado = "game_over"
            return self.estado

        self._desenhar()
        return self.estado

    def _salvar_ranking(self):
        self.ranking.append((getattr(self, "nome_jogador", "Jogador"), self.pontuacao, self.fase_atual))
        self.ranking.sort(key=lambda t: t[1], reverse=True)
        del self.ranking[10:]

    def _desenhar(self):
        self.tela.fill((28, 32, 42))
        pygame.draw.rect(self.tela, (40, 44, 55), (0, ALTURA_TELA - 130, LARGURA_TELA, 130))
        for i in range(0, LARGURA_TELA, 60):
            pygame.draw.line(self.tela, (50, 55, 68), (i, ALTURA_TELA - 130), (i, ALTURA_TELA), 1)

        for e in self.esteiras:
            e.desenhar(self.tela)
        for l in self.lixeiras:
            l.desenhar(self.tela)
        self.personagem.desenhar(self.tela)

        inv = "Vazio"
        if self.personagem.tem_item():
            inv = NOMES_MATERIAL[self.personagem.inventario.tipo]

        self.hud.desenhar(
            self.fase_atual, self.pontuacao, self.pontuacao_fase,
            META_PONTOS[self.fase_atual], self.tempo_restante, inv,
            self.personagem.pecas, self._total_residuos_nas_esteiras()
        )

        if self.tempo_msg > 0 and self.mensagem:
            cor = VERDE if "+" in self.mensagem or "Coletou" in self.mensagem or "Peça" in self.mensagem or "PARADA" in self.mensagem else VERMELHO
            Texto(self.tela, self.mensagem, LARGURA_TELA // 2, 90, cor, 26, True).desenhar()

        if self.alerta_sobrecarga:
            Texto(self.tela, "⚠ ESTEIRA SOBRECARGADA!", LARGURA_TELA // 2, 130, VERMELHO, 22, True).desenhar()


class Pausa(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)
        self.titulo = Texto(tela, "PAUSA", LARGURA_TELA // 2, 280, AMARELO, 56, True)
        self.dica = Texto(tela, "ESC = Continuar   |   Q = Menu", LARGURA_TELA // 2, 370, BRANCO, 24, True)

    def processar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.estado = "partida"
            elif evento.key == pygame.K_q:
                self.estado = "menu"

    def atualizar(self, dt: float) -> str:
        self.estado = "pausa"
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.tela.blit(overlay, (0, 0))
        self.titulo.desenhar()
        self.dica.desenhar()
        return self.estado


class FaseCompleta(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)
        self.titulo = Texto(tela, "FASE COMPLETA!", LARGURA_TELA // 2, 260, VERDE, 48, True)
        self.botao = Botao(tela, "PRÓXIMA FASE", LARGURA_TELA // 2 - 130, 380, 260, 55,
                           cor_fundo=VERDE, cor_hover=VERDE_ESCURO)
        self.precisa_reiniciar_fase = False

    def atualizar(self, dt: float) -> str:
        self.estado = "fase_completa"
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.tela.blit(overlay, (0, 0))
        self.titulo.desenhar()
        self.botao.desenhar()
        if self.botao.get_click():
            self.precisa_reiniciar_fase = True
            self.estado = "partida"
        return self.estado


class GameOver(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)
        self.titulo = Texto(tela, "GAME OVER", LARGURA_TELA // 2, 240, VERMELHO, 56, True)
        self.botao_menu = Botao(tela, "MENU", LARGURA_TELA // 2 - 110, 380, 220, 55)
        self.botao_rank = Botao(tela, "RANKING", LARGURA_TELA // 2 - 110, 460, 220, 55, cor_fundo=LARANJA)

    def atualizar(self, dt: float) -> str:
        self.estado = "game_over"
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.tela.blit(overlay, (0, 0))
        self.titulo.desenhar()
        self.botao_menu.desenhar()
        self.botao_rank.desenhar()
        if self.botao_menu.get_click():
            self.estado = "menu"
        if self.botao_rank.get_click():
            self.estado = "ranking"
        return self.estado


class Vitoria(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)
        self.titulo = Texto(tela, "VITÓRIA!", LARGURA_TELA // 2, 220, AMARELO, 60, True)
        self.sub = Texto(tela, "Você completou as 5 fases!", LARGURA_TELA // 2, 300, BRANCO, 26, True)
        self.botao = Botao(tela, "MENU", LARGURA_TELA // 2 - 110, 400, 220, 55, cor_fundo=VERDE)

    def atualizar(self, dt: float) -> str:
        self.estado = "vitoria"
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.tela.blit(overlay, (0, 0))
        self.titulo.desenhar()
        self.sub.desenhar()
        self.botao.desenhar()
        if self.botao.get_click():
            self.estado = "menu"
        return self.estado


class Ranking(CenaBase):
    def __init__(self, tela, ranking_ref: list):
        super().__init__(tela)
        self.ranking = ranking_ref
        self.titulo = Texto(tela, "TOP 10 RANKING", LARGURA_TELA // 2, 80, AMARELO, 48, True)
        self.botao = Botao(tela, "VOLTAR", LARGURA_TELA // 2 - 100, ALTURA_TELA - 90, 200, 50)

    def atualizar(self, dt: float) -> str:
        self.estado = "ranking"
        self.tela.fill(CINZA_ESCURO)
        self.titulo.desenhar()
        if not self.ranking:
            Texto(self.tela, "Nenhuma pontuação ainda.", LARGURA_TELA // 2, 300, CINZA, 26, True).desenhar()
        else:
            fonte = pygame.font.SysFont("Arial", 24, bold=True)
            for i, (nome, pts, fase) in enumerate(self.ranking[:10]):
                cor = AMARELO if i == 0 else BRANCO
                linha = f"{i+1:2d}.  {nome:<14}  {pts:5d} pts   (Fase {fase})"
                self.tela.blit(fonte.render(linha, True, cor), (LARGURA_TELA // 2 - 220, 160 + i * 42))
        self.botao.desenhar()
        if self.botao.get_click():
            self.estado = "menu"
        return self.estado
