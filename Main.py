# Example file showing a basic pygame "game loop"
import pygame
import math
import random
import numpy
import Controls 
import SnakePiece

# pygame setup
pygame.init()
grid = pygame.Vector2(40, 30)
squareSize = 30
screen = pygame.display.set_mode((grid.x * squareSize, grid.y * squareSize))
clock = pygame.time.Clock()
frameRate = 60
running = True
dt = 0
speed = 0.5 
frameCounter = 0
movementVector = pygame.Vector2(0,0)
input = pygame.Vector2(0, 0)

screenCenter = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
headPos = screenCenter
snakeSquares = [SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)), 
# SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)),
# SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)),
# SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)),
# SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)),
]

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

    roundedHeadPos = pygame.Vector2(math.floor(headPos.x), math.floor(headPos.y))
    remainder = 0
    color = 'grey'
    input = Controls.getMovementVector(input, speed, frameRate)
    print('update input ' + str(frameCounter))
    print(input)
    print('movement')
    print(movementVector)
    print(input.dot(movementVector))
    print(roundedHeadPos.x % squareSize)
    print(roundedHeadPos.y % squareSize)
    print(headPos)

    if(headPos.x % squareSize <= remainder and headPos.y % squareSize <= remainder):
        # color = 'orange'
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
    previousSnakeSquarePos = headPos 
    for i in range(numSnakeSquares):
        if(i == 0):
            snakeSquares[i].setRectPos(headPos)
            snakeSquares[i].setPos(headPos)
            pygame.draw.rect(screen, "red", snakeSquares[i])
        # else:
            # previousSnakeSquarePos = snakeSquares[i -1].previousPos
            # normalMovementVector = pygame.Vector2(0, 0)
            # if movementVector.magnitude() != 0:
            #     normalMovementVector = movementVector.normalize()
            # offset = pygame.Vector2(normalMovementVector.x * squareSize, normalMovementVector.y * squareSize)
            # previousSnakeSquarePos = pygame.Vector2(previousSnakeSquarePos.x - offset.x, previousSnakeSquarePos.y - offset.y)
            
            # snakeSquares[i].setRectPos(previousSnakeSquarePos)
            # snakeSquares[i].setPos(previousSnakeSquarePos)
            # pygame.draw.rect(screen, pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), snakeSquares[i])

    # if collision, end game
    if(isWallCollision):
        running = False
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    frameCounter += 1
    dt = clock.tick(frameRate) / 1000

pygame.quit()
