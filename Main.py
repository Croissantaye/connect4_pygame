# Example file showing a basic pygame "game loop"
import pygame
import random
import numpy
import Controls 
import SnakePiece

# pygame setup
pygame.init()
grid = pygame.Vector2(30, 20)
gridScale = 20
screen = pygame.display.set_mode((grid.x * gridScale, grid.y * 20))
clock = pygame.time.Clock()
frameRate = 60
running = True
dt = 0
squareSize = 20
speed = 100
movesPerSecond = 1
frameCounter = 0
movementVector = pygame.Vector2(0,0)

screenCenter = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
headPos = screenCenter
snakeSquares = [SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)), 
# SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)),
# SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)),
# SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)),
# SnakePiece.SnakePiece(pygame.Rect(0, 0, squareSize, squareSize)),
]

def drawScreenGrid():
        screen.fill(pygame.Color(255, 255, 255, 255))
        for x in range(int(grid.x)):
            isOddRow = x % 2 == 1
            for y in range(int(grid.y)):
                yOffset = 1
                if(isOddRow):
                    yOffset = 0
                if(y % 2 == yOffset):
                    tile = pygame.Rect(gridScale * x, gridScale * y, gridScale, gridScale)
                    pygame.draw.rect(screen, "grey", tile)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    drawScreenGrid()

    # keep inside the screen
    headPos = pygame.Vector2(
    numpy.clip(headPos.x + movementVector.x, 0, screen.get_width() - squareSize), 
    numpy.clip(headPos.y + movementVector.y, 0, screen.get_height() - squareSize)
    )
    movementVector = Controls.getMovementVector(movementVector, speed, frameRate)

    # check collision with walls
    isWallCollision = False
    if(headPos.x == screen.get_width() - squareSize or 
    headPos.x == 0 or
    headPos.y == screen.get_height() - squareSize or
    headPos.y == 0):
        isWallCollision = True
    
    # RENDER YOUR GAME HERE
    numSnakeSquares = len(snakeSquares)
    previousSnakeSquarePos = headPos 
    for i in range(numSnakeSquares):
        if(i == 0):
            snakeSquares[i].setRectPos(headPos)
            snakeSquares[i].setPos(headPos)
            pygame.draw.rect(screen, "red", snakeSquares[i])
        else:
            previousSnakeSquarePos = snakeSquares[i -1].previousPos
            # normalMovementVector = pygame.Vector2(0, 0)
            # if movementVector.magnitude() != 0:
            #     normalMovementVector = movementVector.normalize()
            # offset = pygame.Vector2(normalMovementVector.x * squareSize, normalMovementVector.y * squareSize)
            # previousSnakeSquarePos = pygame.Vector2(previousSnakeSquarePos.x - offset.x, previousSnakeSquarePos.y - offset.y)
            
            snakeSquares[i].setRectPos(previousSnakeSquarePos)
            snakeSquares[i].setPos(previousSnakeSquarePos)
            pygame.draw.rect(screen, pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), snakeSquares[i])

    # if collision, end game
    if(isWallCollision):
        running = False
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(frameRate) / 1000

pygame.quit()