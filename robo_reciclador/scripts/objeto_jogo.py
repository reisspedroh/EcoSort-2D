"""
Classe base abstrata para todas as entidades do jogo.
"""

from abc import ABC, abstractmethod
import pygame


class ObjetoJogo(ABC):
    """
    Classe base abstrata.
    Contém posição, tamanho e o método abstrato desenhar().
    """

    def __init__(self, x: float, y: float, largura: int, altura: int):
        self.x = float(x)
        self.y = float(y)
        self.largura = largura
        self.altura = altura
        self.rect = pygame.Rect(int(x), int(y), largura, altura)
        self.ativo = True

    def atualizar_rect(self) -> None:
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    @abstractmethod
    def desenhar(self, superficie: pygame.Surface) -> None:
        """Método abstrato que obriga as subclasses a implementarem a renderização."""
        pass

    def colide_com(self, outro: "ObjetoJogo") -> bool:
        return self.rect.colliderect(outro.rect)
