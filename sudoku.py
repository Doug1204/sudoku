import pygame
import pygame.locals
import time
import numpy
pygame.init()
pygame.display.set_caption('Sudoku')
display_width = 800
display_height = 500
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

grid = numpy.zeros((9, 9))
instant = True
complete = -1


def setUp():
    gameDisplay.fill((255, 255, 255))
    black = (0, 0, 0)
    for i in range(1, 10):
        thickness = 2 if i % 3 == 0 else 1
        pygame.draw.line(gameDisplay, black, (display_height/9*i, 0), (display_height/9*i, display_height), thickness)
        pygame.draw.line(gameDisplay, black, (0, display_height/9*i), (display_height, display_height/9*i), thickness)
        text('Instant:', display_width*0.65,display_height*0.1)
        text(str(instant), display_width*0.75,display_height*0.2)
        text('Press Space', display_width*0.65,display_height*0.3, fontSize=display_height/18)
        text("Press 'r' to reset", display_width*0.7,display_height*0.5, fontSize=display_height/18)
        if complete == 1: text('Complete!!', display_width*0.65,display_height*0.8)
        elif complete == 0: text('Not Possible', display_width*0.65,display_height*0.8)
    
def drawNumbers():
    change = display_height / 9
    x = change / 3.5
    y = change / 5
    for i in grid:
        for j in i:
            j = ' ' if str(j) == '0.0' else j
            text(str(j)[0], x, y)
            x += change
        y += change
        x = change / 3.5

def text(text, x, y, fontSize=display_height / 9):
    font = pygame.font.SysFont(None, round(fontSize))
    text = font.render(text, True, (0, 0, 0))
    gameDisplay.blit(text,(x, y))

def getNum():
    num = ''
    while True:
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if len(key) == 1:
                try:
                    if int(key): return int(key)
                except: pass
            elif key == "backspace": return 0.0
        if len(num) > 1: num = num[:-1]

def getBox():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    coords = (mouse[0], mouse[1])
    scale = display_height / 9
    if click[0] == 1:
        f = lambda x: scale * round(x/scale)
        x = f(mouse[0]) if f(mouse[0]) < mouse[0] else f(mouse[0]-scale)
        y = f(mouse[1]) if f(mouse[1]) < mouse[1] else f(mouse[1]-scale)
        number = getNum()
        grid[int(y/scale)][int(x/scale)] = str(number)

def isPossible():
    for i, valuei in enumerate(grid):
        for j, valuej in enumerate(valuei):
            if list(grid[i]).count(grid[i][j]) > 1 and grid[i][j] != 0.0: return 0
            column = [grid[x][j] for x in range(9)]
            if list(column).count(grid[i][j]) > 1 and grid[i][j] != 0.0: return 0
            boxx = [k for k in [[0, 1, 2], [3, 4, 5], [6, 7, 8]] if j in k][0]
            boxy = [k for k in [[0, 1, 2], [3, 4, 5], [6, 7, 8]] if i in k][0]
            box = grid[numpy.ix_(boxy, boxx)]
            if sum([list(x).count(grid[i][j]) for x in box]) > 1 and grid[i][j] != 0.0: return 0
    return 1

def cross():
    global instant
    global complete
    global grid
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                check = isPossible()
                if not check: complete = check
                if check:
                    solve(0, 0)
                    complete = check
            elif event.key == pygame.K_SPACE:
                instant = not instant
            elif event.key == pygame.K_r:
                complete = -1
                grid = numpy.zeros((9, 9))

def findAvaliable(i, j):
    allNumbers = set((1, 2, 3, 4, 5, 6, 7, 8, 9))
    taken = set()
    for itemInRow in grid[i]:
        if itemInRow: taken.add(int(itemInRow))
    for column in range(9):
        if grid[column][j]: taken.add(int(grid[column][j]))
    boxx = [k for k in [[0, 1, 2], [3, 4, 5], [6, 7, 8]] if j in k][0]
    boxy = [k for k in [[0, 1, 2], [3, 4, 5], [6, 7, 8]] if i in k][0]
    box = grid[numpy.ix_(boxy, boxx)]
    for c in range(3):
        for r in range(3):
            if box[c][r]: taken.add(box[c][r])
    return allNumbers - taken

def solve(i, j):
    cross()

    def nextGrid(i, j):
        j += 1
        if j > 8:
            j = 0
            i += 1
        return i, j

    if i > 8:
        return 1
    if not grid[i][j]:

        avaliable = findAvaliable(i, j)
        
        for num in avaliable:
            if not instant:
                setUp()
                drawNumbers()
                pygame.display.update()
                clock.tick(60)
            grid[i][j] = num
            m, n = nextGrid(i, j)
            if solve(m, n) == 1:
                return 1
        grid[i][j] = '0.0'
        return -1

    i, j = nextGrid(i, j)
    if solve(i, j) == 1:
        return 1
    return -1

def main():
    music = pygame.mixer.music.load('C:\\Users\\Rachel Greenwood\\Desktop\\Python code\\Complete.py\\Sudoku\\BackgroundMusic.mp3')
    pygame.mixer.music.play(-1)
    while True:
        cross()
        setUp()
        drawNumbers()
        getBox()

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
