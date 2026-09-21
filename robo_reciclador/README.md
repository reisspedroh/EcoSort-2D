# EcoSort 2D: Operação Reciclagem

Jogo 2D top-down educativo (Pygame + POO) com backend Django para ranking.

## Como rodar o jogo

```bash
pip install pygame requests
cd robo_reciclador
python main.py
```

## Controles
- WASD / Setas — mover (8 direções)
- Colisão — coletar resíduo, peça ou botão de emergência
- E / Espaço — depositar na lixeira
- ESC — pausar

## Funcionalidades
- 5 fases com liberação gradual de materiais (inclui Pilhas/Perigoso)
- Peças de upgrade (velocidade + visual)
- Parada de Emergência (congela esteiras 5s)
- Segunda esteira a partir da Fase 4
- Game over por tempo ou acúmulo de 10 resíduos na esteira
- Diálogo do Gerente do Galpão no início
- Ranking local + cliente pronto para API Django

## Backend Django

```bash
cd ecosort_backend
pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```

Endpoints: `/api/jogador/`, `/api/pontuacao/`, `/api/ranking/`
