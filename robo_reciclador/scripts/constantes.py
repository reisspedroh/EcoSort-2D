"""
Constantes globais do jogo EcoSort 2D: Operação Reciclagem.
"""

from enum import Enum

# Tela
LARGURA_TELA = 1024
ALTURA_TELA = 768
FPS = 60
TITULO = "EcoSort 2D: Operação Reciclagem"

# Cores
PRETO = (15, 15, 20)
BRANCO = (245, 245, 250)
CINZA = (110, 110, 120)
CINZA_ESCURO = (35, 38, 48)
CINZA_CLARO = (180, 185, 195)
VERDE = (60, 200, 90)
VERDE_ESCURO = (30, 120, 50)
VERMELHO = (230, 60, 70)
AMARELO = (250, 210, 50)
AZUL = (60, 140, 230)
AZUL_ESCURO = (30, 70, 140)
LARANJA = (240, 140, 40)
MARROM = (160, 100, 50)
ROXO = (160, 80, 200)
CIANO = (80, 220, 220)
ROSA = (220, 80, 140)

# Tipos de material
class TipoMaterial(Enum):
    PLASTICO = "plastico"
    PAPEL = "papel"
    VIDRO = "vidro"
    METAL = "metal"
    ORGANICO = "organico"
    PERIGOSO = "perigoso"  # Pilhas e Baterias

CORES_MATERIAL = {
    TipoMaterial.PLASTICO: AZUL,
    TipoMaterial.PAPEL: AMARELO,
    TipoMaterial.VIDRO: VERDE,
    TipoMaterial.METAL: CINZA_CLARO,
    TipoMaterial.ORGANICO: MARROM,
    TipoMaterial.PERIGOSO: LARANJA,
}

NOMES_MATERIAL = {
    TipoMaterial.PLASTICO: "Plástico",
    TipoMaterial.PAPEL: "Papel",
    TipoMaterial.VIDRO: "Vidro",
    TipoMaterial.METAL: "Metal",
    TipoMaterial.ORGANICO: "Orgânico",
    TipoMaterial.PERIGOSO: "Pilhas",
}

# Progressão de materiais por fase
MATERIAIS_POR_FASE = {
    1: [TipoMaterial.PLASTICO, TipoMaterial.PAPEL],
    2: [TipoMaterial.PLASTICO, TipoMaterial.PAPEL, TipoMaterial.VIDRO],
    3: [TipoMaterial.PLASTICO, TipoMaterial.PAPEL, TipoMaterial.VIDRO,
        TipoMaterial.METAL],
    4: [TipoMaterial.PLASTICO, TipoMaterial.PAPEL, TipoMaterial.VIDRO,
        TipoMaterial.METAL, TipoMaterial.ORGANICO],
    5: [TipoMaterial.PLASTICO, TipoMaterial.PAPEL, TipoMaterial.VIDRO,
        TipoMaterial.METAL, TipoMaterial.ORGANICO, TipoMaterial.PERIGOSO],
}

# Dificuldade: (velocidade_esteira, intervalo_spawn_segundos, tempo_limite)
DIFICULDADE = {
    1: (1.4, 3.2, 55),
    2: (1.7, 2.8, 50),
    3: (2.1, 2.4, 48),
    4: (2.6, 2.0, 45),
    5: (3.1, 1.7, 40),
}

# Meta de pontos para avançar de fase
META_PONTOS = {
    1: 40,
    2: 70,
    3: 100,
    4: 130,
    5: 160,
}

# Penalidade e limites
PONTOS_ITEM_PERDIDO = -5
MAX_RESIDUOS_ACUMULADOS = 10  # game over se atingir este número na esteira

# Peças de upgrade
CHANCE_SPAWN_PECA = 0.18
BONUS_VELOCIDADE_POR_PECA = 0.35
MAX_PECAS_BONUS = 8
PONTOS_POR_PECA = 3

# Parada de emergência
CHANCE_SPAWN_EMERGENCIA = 0.08
DURACAO_PARADA_EMERGENCIA = 5.0  # segundos

# Segunda esteira a partir da fase 4
FASE_SEGUNDA_ESTEIRA = 4

TOTAL_FASES = 5

# API Django (ajuste a URL quando o servidor estiver rodando)
API_BASE_URL = "http://127.0.0.1:8000/api"
