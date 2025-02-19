# features still needed to be added
# - food
# - score
# - menu

# Example file showing a basic pygame "game loop"
import pygame as pg
import math
import random as rdm
import numpy
import Controls
import Food as fd
import SnakePiece

# pygame setup
pg.init()
if not pg.font:
    print("Warning, fonts disabled")

def createSnakePieces(startPos: pg.Vector2, numPieces: int) -> list[SnakePiece.SnakePiece]:
    pieces = list()
    for i in range(numPieces):
        pieces.append(SnakePiece.SnakePiece(pg.Vector2(startPos.x, startPos.y - (squareSize * i)), pg.Vector2(), squareSize))
    return pieces

def drawScreenGrid(color):
        screen.fill(pg.Color(255, 255, 255, 255))
        for x in range(int(grid.x)):
            isOddRow = x % 2 == 1
            for y in range(int(grid.y)):
                yOffset = 1
                if(isOddRow):
                    yOffset = 0
                if(y % 2 == yOffset):
                    tile = pg.Rect(squareSize * x, squareSize * y, squareSize, squareSize)
                    pg.draw.rect(screen, color, tile)

grid = pg.Vector2(40, 30)
squareSize = 16
screen = pg.display.set_mode((grid.x * squareSize, grid.y * squareSize))
clock = pg.time.Clock()
frameRate = 60
running = True
dt = 0
speedOptions: list[float] = [0.25,0.5,1,2,4,8]
speedIndex: int = 0
speed = speedOptions[speedIndex]
score = 0
movementVector = pg.Vector2(0, 1)
input = pg.Vector2(0, 1)

screenCenter = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
headPos = screenCenter
snakeSquares = createSnakePieces(screenCenter, 15)
foodSquares: list[fd.Food] = [
    fd.Food(pg.Vector2(squareSize * 5, squareSize * 10), squareSize),
    fd.Food(pg.Vector2(squareSize * 5, squareSize * 20), squareSize)
]
snakeSquares[0].dir = pg.Vector2(0, speed)

while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # keep inside the screen
    headPos = pg.Vector2(
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
                    dir = pg.Vector2(math.copysign(1, prevPos.x - square.pos.x), 0)
                else:
                    dir = pg.Vector2(0, math.copysign(1, prevPos.y - square.pos.y))
            square.updatePos(pg.Vector2(square.pos.x + (dir.x * speed), square.pos.y + (dir.y * speed)), dir)
            distToHead = pg.Vector2(snakeSquares[0].pos.x - square.pos.x, snakeSquares[0].pos.y - square.pos.y)
            if(distToHead.length_squared() < math.pow(squareSize - (1/3 * squareSize), 2)):
                running = False
        pg.draw.rect(screen, snakeColor, snakeSquares[i].rect)
        prevPos = snakeSquares[i].pos

    for food in foodSquares:
        food.render(screen)
        if(food.foodCheck(snakeSquares[0])):
            tail = snakeSquares[numSnakeSquares - 1]
            pos = pg.Vector2(tail.pos.x - (tail.dir.x * squareSize), tail.pos.y - (tail.dir.y * squareSize))
            newSnakeSquare = SnakePiece.SnakePiece(pos, tail.dir, squareSize)
            snakeSquares.append(newSnakeSquare)
            foodSquares.remove(food)
            score += 50
            speedIndex += 1
            if(speedIndex >= len(speedOptions)):
                speedIndex = len(speedOptions) - 1
            speed = speedOptions[speedIndex]

    # if collision, end game
    if(isWallCollision):
        running = False
    
    score += 0.05 * speed
    if pg.font:
        font = pg.font.Font(None, 32)
        text = font.render("score: {score}".format(score = str(math.floor(score))),True, (10, 10, 10))
        textpos = text.get_rect(x = 10, y = 10)
        screen.blit(text, textpos)

    randPos: pg.Vector2 = pg.Vector2(rdm.randint(2, (int(grid.x) - 2)) * squareSize, rdm.randint(2, (int(grid.y) - 2)) * squareSize)

    isNewFoodPos: bool = True
    for x in foodSquares:
        isNewFoodPos = x.pos != randPos
        if(not isNewFoodPos):
            break
        
    if(isNewFoodPos and len(foodSquares) < 3):
        newFoodSquare: fd.Food = fd.Food(randPos, squareSize)
        print("new food square: " + str(newFoodSquare.pos))
        foodSquares.append(newFoodSquare)
        newFoodSquare.render(screen)

    # flip() the display to put your work on screen
    pg.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(frameRate) / 1000

pg.quit()
