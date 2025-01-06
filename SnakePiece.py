import pygame

class SnakePiece:
    def __init__(self, rect):
        self.pos = pygame.Vector2(0, 0)
        self.rect = rect
        self.previousPos = pygame.Vector2(0, 0)

    def setPos(self, pos):
        self.previousPos = self.pos
        self.pos = pos 
        
    # def pos():
    #     return self.__pos

    # def rect():
    #     return self.__rect

    def setRectPos(self, pos):
        self.rect.x = pos.x
        self.rect.y = pos.y