import pygame

def getMovementVector(dir):
    movementValue = pygame.Vector2(dir.x, dir.y)
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_w]):
        movementValue = pygame.Vector2(0, -1)
    if(keys[pygame.K_a]):
        movementValue = pygame.Vector2(-1, 0)
    if(keys[pygame.K_s]):
        movementValue = pygame.Vector2(0, 1)
    if(keys[pygame.K_d]):
        movementValue = pygame.Vector2(1, 0)
    return movementValue
