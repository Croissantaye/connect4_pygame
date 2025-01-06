import pygame

def getMovementVector(dir, speed, frameRate):
    movementValue = pygame.Vector2(dir.x, dir.y)
    rate = speed / frameRate
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_w]):
        movementValue = pygame.Vector2(0, -1 * rate)
    if(keys[pygame.K_a]):
        movementValue = pygame.Vector2(-1 * rate, 0)
    if(keys[pygame.K_s]):
        movementValue = pygame.Vector2(0, 1 * rate)
    if(keys[pygame.K_d]):
        movementValue = pygame.Vector2(1 * rate, 0)
    return movementValue