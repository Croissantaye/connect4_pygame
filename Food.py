import math
import pygame as pg
import SnakePiece as sp

class Food:
    def __init__(self, pos: pg.Vector2, size: int):
        self.pos = pos
        self.size = size
        self.rect = pg.Rect(pos.x, pos.y, size, size)

    def render(self, surface: pg.Surface):
        pg.draw.rect(surface, "green", self.rect)

    def foodCheck(self, head: sp.SnakePiece) -> bool:
        dist = pg.Vector2(head.pos.x - self.pos.x, head.pos.y - self.pos.y)
        isCollided = dist.magnitude_squared() <= math.pow(self.size, 2)
        if(dist.magnitude_squared() == 0):
            print("dist magnitude is 0")
            return False
        return isCollided and dist.normalize().dot(head.dir) == -1

    def __str__(self) -> str:
        return str(self.pos)
