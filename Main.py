# Example file showing a basic pygame "game loop"
import pygame
import math
import numpy
import Controls 
import SnakePiece

# pygame setup
pygame.init()

def createSnakePieces(startPos: pygame.Vector2, numPieces: int) -> list:
    pieces = list()
    for i in range(numPieces):
        pieces.append(SnakePiece.SnakePiece(pygame.Vector2(startPos.x, startPos.y - (squareSize * i)), pygame.Vector2(), squareSize))
    return pieces

def drawScreenGrid(color):
        screen.fill(pygame.Color(255, 255, 255, 255))
        for x in range(int(grid.x)):
            isOddRow = x % 2 == 1
            for y in range(int(grid.y)):
                yOffset = 1
                if(isOddRow):
                    yOffset = 0
                if(y % 2 == yOffset):
                    tile = pygame.Rect(squareSize * x, squareSize * y, squareSize, squareSize)
                    pygame.draw.rect(screen, color, tile)

grid = pygame.Vector2(40, 30)
squareSize = 20
screen = pygame.display.set_mode((grid.x * squareSize, grid.y * squareSize))
clock = pygame.time.Clock()
frameRate = 60
running = True
dt = 0
speed = 1
movementVector = pygame.Vector2(0, 1)
input = pygame.Vector2(0, 1)

screenCenter = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
headPos = screenCenter
snakeSquares = createSnakePieces(screenCenter, 15)
snakeSquares[0].dir = pygame.Vector2(0, speed)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # keep inside the screen
    headPos = pygame.Vector2(
        numpy.clip(headPos.x + (movementVector.x * speed), 0, screen.get_width() - squareSize), 
        numpy.clip(headPos.y + (movementVector.y * speed), 0, screen.get_height() - squareSize)
    )

    remainder = 0
    color = 'grey'
    input = Controls.getMovementVector(input)

    if(headPos.x % squareSize <= remainder and headPos.y % squareSize <= remainder):
        if(input.dot(movementVector) >= 0):
            movementVector = input

    # check collision with walls
    isWallCollision = False
    if(headPos.x == screen.get_width() - squareSize or 
    headPos.x == 0 or
    headPos.y == screen.get_height() - squareSize or
    headPos.y == 0):
        isWallCollision = True
    

    drawScreenGrid(color)
                    
    # RENDER YOUR GAME HERE
    numSnakeSquares = len(snakeSquares)
    prevPos = headPos
    headColor = "red"
    tailColor = "black"
    snakeColor = headColor 
    for i in range(numSnakeSquares):
        if(i == 0):
            snakeSquares[i].updatePos(headPos, movementVector)
        else:
            if(snakeColor != tailColor):
                snakeColor = tailColor
            square = snakeSquares[i]
            dir = square.dir
            if(square.pos.x % squareSize == 0 and square.pos.y % squareSize == 0):
                if(abs(prevPos.x - square.pos.x) > abs(prevPos.y - square.pos.y)):
                    dir = pygame.Vector2(math.copysign(1, prevPos.x - square.pos.x), 0)
                else:
                    dir = pygame.Vector2(0, math.copysign(1, prevPos.y - square.pos.y))
            square.updatePos(pygame.Vector2(square.pos.x + (dir.x * speed), square.pos.y + (dir.y * speed)), dir)
            distToHead = pygame.Vector2(snakeSquares[0].pos.x - square.pos.x, snakeSquares[0].pos.y - square.pos.y)
            if(distToHead.length_squared() < math.pow(squareSize - (1/3 * squareSize), 2)):
                running = False
        pygame.draw.rect(screen, snakeColor, snakeSquares[i].rect)
        prevPos = snakeSquares[i].pos

    # if collision, end game
    if(isWallCollision):
        running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(frameRate) / 1000

    print()

pygame.quit()
