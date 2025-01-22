import pygame

class SnakePiece:
    def __init__(self, pos: pygame.Vector2, dir: pygame.Vector2, size: int):
        self.rect = pygame.Rect(pos.x, pos.y, size, size) 
        self.pos = pos
        self.dir = dir
        self.prevPos = pos

    def updatePos(self, pos: pygame.Vector2, dir: pygame.Vector2):
        self.setPos(pos)
        self.setRectPos(pos)
        self.setDir(dir)

    def setPos(self, pos: pygame.Vector2):
        self.prevPos = self.pos
        self.pos = pos 

    def setDir(self, dir: pygame.Vector2):
        self.dir = pygame.Vector2(dir.x, dir.y)
        
    def setRectPos(self, pos: pygame.Vector2):
        # self.rect.move(pos.x - self.prevPos.x, pos.y - self.prevPos.y)
        self.rect.x = int(pos.x)
        self.rect.y = int(pos.y)

    def __str__(self) -> str:
        temp = f"pos: {self.pos},\ndir: {self.dir}\n"
        rectStr = str(self.rect)
        return temp + rectStr
