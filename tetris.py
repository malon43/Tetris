import pygame
from random import shuffle
from sys import exit


clock = pygame.time.Clock()

displayDimensions = width, height = 600, 800
blockSize = 24
blockGap = 3
white = (255, 255, 255)
black = (0, 0, 0)
cyan = (0, 255, 255)  # I, 1
blue = (0, 0, 255)  # J, 2
orange = (255, 165, 0)  # L, 3
yellow = (255, 255, 0)  # O, 4
lime = (0, 255, 0)  # S, 5
purple = (128, 0, 128)  # T, 6
red = (255, 0, 0)  # Z, 7

colorList = [cyan, blue, orange, yellow, lime, purple, red]

showGhostPiece = True
themeVolume = 1

boardSize = (12 * blockSize + 11 * blockGap, 21 * blockSize + 20 * blockGap)
bsbg = blockSize + blockGap
startPosOutline = (int((displayDimensions[0] - boardSize[0]) / 2), int((displayDimensions[1] - boardSize[1]) / 2))
startPosBoard = (startPosOutline[0] + bsbg, startPosOutline[1] - 2 * bsbg)
scoreboardXCenter = displayDimensions[0] - startPosOutline[0] // 2

tetrominos = ["I", "J", "L", "O", "S", "T", "Z"]
tetrominosBag = []

downWait = 2
sideWait1 = 10
sideWait2 = 2

I = [[
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
], [
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0]
], [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0]
], [
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0]
]]
J = [[
    [2, 0, 0],
    [2, 2, 2],
    [0, 0, 0]
], [
    [0, 2, 2],
    [0, 2, 0],
    [0, 2, 0]
], [
    [0, 0, 0],
    [2, 2, 2],
    [0, 0, 2]
], [
    [0, 2, 0],
    [0, 2, 0],
    [2, 2, 0]
]]
L = [[
    [0, 0, 3],
    [3, 3, 3],
    [0, 0, 0]
], [
    [0, 3, 0],
    [0, 3, 0],
    [0, 3, 3]
], [
    [0, 0, 0],
    [3, 3, 3],
    [3, 0, 0]
], [
    [3, 3, 0],
    [0, 3, 0],
    [0, 3, 0]
]]
O = [[
    [4, 4],
    [4, 4]
], [
    [4, 4],
    [4, 4],
], [
    [4, 4],
    [4, 4]
], [
    [4, 4],
    [4, 4]
]]
S = [[
    [0, 5, 5],
    [5, 5, 0],
    [0, 0, 0]
], [
    [0, 5, 0],
    [0, 5, 5],
    [0, 0, 5]
], [
    [0, 0, 0],
    [0, 5, 5],
    [5, 5, 0]
], [
    [5, 0, 0],
    [5, 5, 0],
    [0, 5, 0]
]]
T = [[
    [0, 6, 0],
    [6, 6, 6],
    [0, 0, 0]
], [
    [0, 6, 0],
    [0, 6, 6],
    [0, 6, 0]
], [
    [0, 0, 0],
    [6, 6, 6],
    [0, 6, 0]
], [
    [0, 6, 0],
    [6, 6, 0],
    [0, 6, 0]
]]
Z = [[
    [7, 7, 0],
    [0, 7, 7],
    [0, 0, 0]
], [
    [0, 0, 7],
    [0, 7, 7],
    [0, 7, 0]
], [
    [0, 0, 0],
    [7, 7, 0],
    [0, 7, 7]
], [
    [0, 7, 0],
    [7, 7, 0],
    [7, 0, 0]
]]

pygame.init()
pygame.font.init()

mainDisplay = pygame.display.set_mode(displayDimensions)
menuDisplay = pygame.Surface(displayDimensions, pygame.SRCALPHA)
pauseDisplay = pygame.Surface(displayDimensions, pygame.SRCALPHA)
gameDisplay = pygame.Surface(displayDimensions, pygame.SRCALPHA)

fontBasic = pygame.font.Font("fonts/prstart.ttf", 20)
fontBig = pygame.font.Font("fonts/prstart.ttf", 32)

lvlText = fontBasic.render("LEVEL", False, white)
lnsText = fontBasic.render("LINES", False, white)
scrText = fontBasic.render("SCORE", False, white)
nextTetrominoText = fontBasic.render("NEXT", False, white)
gameOverText = fontBig.render("GAME OVER", False, white)
sgpText = fontBasic.render("SHOW GHOST PIECE", False, white)
volumeText = fontBasic.render("VOLUME", False, white)
settingsText = fontBig.render("SETTINGS", False, white)

lvlTextRect = lvlText.get_rect()
lnsTextRect = lnsText.get_rect()
scrTextRect = scrText.get_rect()
lvlTextRectGO = lvlText.get_rect()
lnsTextRectGO = lnsText.get_rect()
scrTextRectGO = scrText.get_rect()
sgpTextSize = sgpText.get_size()
volumeTextRect = volumeText.get_rect()

nextTetrominoTextRect = nextTetrominoText.get_rect()
gameOverTextRect = gameOverText.get_rect()
settingsTextRect = settingsText.get_rect()

lvlTextRect.center = (scoreboardXCenter, 300)
lnsTextRect.center = (scoreboardXCenter, 400)
scrTextRect.center = (scoreboardXCenter, 500)
nextTetrominoTextRect.center = (scoreboardXCenter, startPosOutline[1] + 3 * bsbg - 25)
gameOverTextRect.center = (width // 2, 100)
lvlTextRectGO.center = (width // 2, 300)
lnsTextRectGO.center = (width // 2, 400)
scrTextRectGO.center = (width // 2, 500)
settingsTextRect.center = (width // 2, 100)
sgpTextPos = ((width - sgpTextSize[0]) // 2 - sgpTextSize[1], 250)
volumeTextRect.center = (width // 2, 400)

#  Texture Loading
bgTexture = pygame.image.load("textures/background.png")
rButtonTexture = pygame.image.load("textures/buttonRight.png")
lButtonTexture = pygame.image.load("textures/buttonLeft.png")
rPlayButtonTexture = pygame.image.load("textures/playButtonRight.png")
tetrisLogo = pygame.image.load("textures/tetrisLogo.png")
mainMenuButtonTexture = pygame.image.load("textures/mainMenuButton.png")
quitButtonTexture = pygame.image.load("textures/quitButton.png")
icon = pygame.image.load("textures/icon.png")

buttonSize = rPlayButtonTexture.get_size()
gOButtonSize = mainMenuButtonTexture.get_size()
logoSize = tetrisLogo.get_size()

pygame.mixer.music.load("music/tetrisTheme.ogg")

pygame.display.set_caption("Tetris Clone No.\u0236")
pygame.display.set_icon(icon)

mMButtonPos = ((width // 2 - gOButtonSize[0] - (width - 2 * gOButtonSize[0]) // 6), 600)
qButtonPos = ((width // 2 + (width - 2 * gOButtonSize[0]) // 6), 600)


class SlidingButton:
    def __init__(self, texture, start, sposition, direction):
        self.t = 50
        self.acc = 0.7
        self.speed = 9
        self.texture = texture
        self.start = start
        self.end = start + self.t
        self.xPosition, self.yPosition = sposition
        self.sPosition = sposition
        self.direction = direction  # -1 moving to left, 1 moving to right

    def reset_speed(self):
        self.speedClone = self.speed

    def reset_position(self):
        self.xPosition, self.yPosition = self.sPosition

    def move_button_in(self, time):
        if self.end >= time >= self.start and (self.xPosition < 0 or self.xPosition > width - buttonSize[0]):
            if (time - self.start) / self.t > 0.76 and self.speedClone > 0:
                self.speedClone -= self.acc
            self.xPosition += self.direction * self.speedClone
        elif self.end < time:
            if self.direction == 1:
                self.xPosition = 0
            elif self.direction == -1:
                self.xPosition = width - buttonSize[0]
        menuDisplay.blit(self.texture, (self.xPosition, self.yPosition))

    def move_button_out(self, time):
        if self.end >= time >= self.start:
            if (time - self.start) / self.t < 0.25:
                self.speedClone += self.acc
            self.xPosition -= self.direction * self.speedClone
        menuDisplay.blit(self.texture, (self.xPosition, self.yPosition))


class SlidingLogo:
    def __init__(self, texture, start, sposition, speed):
        self.t = 40
        self.speed = speed
        self.texture = texture
        self.start = start
        self.end = start + self.t
        self.xPosition, self.yPosition = sposition

    def move_logo_in(self, time):
        if self.start <= time <= self.end:
            self.yPosition += self.speed
        menuDisplay.blit(self.texture, (self.xPosition, self.yPosition))

    def move_logo_out(self, time):
        if self.start <= time <= self.end:
            self.yPosition -= self.speed
        menuDisplay.blit(self.texture, (self.xPosition, self.yPosition))

button1pos = ((198, 300), (600, 354))
button2pos = ((0, 400), (402, 454))
button3pos = ((198, 500), (600, 554))

playButton1 = SlidingButton(rPlayButtonTexture, 10, (600, button1pos[0][1]), -1)
playButton2 = SlidingButton(lButtonTexture, 35, (-400, button2pos[0][1]), 1)
playButton3 = SlidingButton(rButtonTexture, 60, (600, button3pos[0][1]), -1)
tLogo = SlidingLogo(tetrisLogo, 0, (199, -logoSize[1]), 5)


def quitplz():
    pygame.quit()
    exit()


def random_tetromino():
    global tetrominosBag
    if len(tetrominosBag) == 0:
        tetrominosBag = tetrominos[:]
        shuffle(tetrominosBag)
    return tetrominosBag.pop()


def translate_to_list(t_name):
    if t_name == "I":
        t = I
    elif t_name == "J":
        t = J
    elif t_name == "L":
        t = L
    elif t_name == "O":
        t = O
    elif t_name == "S":
        t = S
    elif t_name == "T":
        t = T
    elif t_name == "Z":
        t = Z
    return t


def line_out_animation(board, level, lines, score):
    gameDisplay.blit(bgTexture, (0, 0))
    draw_board_outline()
    draw_board(board)
    draw_scoreboard(level, lines, score)
    mainDisplay.blit(gameDisplay, (0, 0))
    pygame.display.update()
    pygame.time.delay(100)


def line_checker(board, level, lines_total, score):
    lines = 0
    for y, yn in zip(board, range(len(board))):
        for x in y:
            if x == 0:
                break
        else:
            if lines > 0:
                line_out_animation(board, level, lines_total, score)
            board.pop(yn)
            board.insert(0, [0] * 10)
            lines += 1
    return board, lines


def draw_next_tetromino(next_tetromino, pos):

    t = translate_to_list(next_tetromino)

    for y, yn in zip(t[0], range(len(t[0]))):
        for x, xn in zip(y, range(len(t[0][0]))):
            if x > 0:
                pygame.draw.rect(gameDisplay, colorList[x - 1], (pos[0] + xn * bsbg, pos[1] + yn * bsbg,
                                                                 blockSize, blockSize))


def draw_scoreboard(level, lines, score):
    lvlTextNumber = fontBasic.render(str(level), False, white)
    lnsTextNumber = fontBasic.render(str(lines), False, white)
    scrTextNumber = fontBasic.render(str(score), False, white)

    lvlTextNumberRect = lvlTextNumber.get_rect()
    lnsTextNumberRect = lnsTextNumber.get_rect()
    scrTextNumberRect = scrTextNumber.get_rect()

    lvlTextNumberRect.center = (scoreboardXCenter, 325)
    lnsTextNumberRect.center = (scoreboardXCenter, 425)
    scrTextNumberRect.center = (scoreboardXCenter, 525)

    gameDisplay.blit(lvlText, lvlTextRect)
    gameDisplay.blit(lvlTextNumber, lvlTextNumberRect)
    gameDisplay.blit(lnsText, lnsTextRect)
    gameDisplay.blit(lnsTextNumber, lnsTextNumberRect)
    gameDisplay.blit(scrText, scrTextRect)
    gameDisplay.blit(scrTextNumber, scrTextNumberRect)
    gameDisplay.blit(nextTetrominoText, nextTetrominoTextRect)


def draw_sidebar(score, lines, level, next_tetromino, ntpos):
    draw_next_tetromino(next_tetromino, ntpos)
    draw_scoreboard(level, lines, score)


def draw_tetromino(aT, tP):
    t = translate_to_list(aT)
    for y, yn in zip(t[tP[1]], range(len(t[0]))):
        if tP[0][1] + yn > 1:
            for x, xn in zip(y, range(len(t[0][0]))):
                if x > 0:
                    pygame.draw.rect(gameDisplay, colorList[x - 1],
                                 (startPosBoard[0] + tP[0][0] * bsbg + xn * bsbg,
                                  startPosBoard[1] + tP[0][1] * bsbg + yn * bsbg, blockSize, blockSize))


def can_tetromino_fall(board, aT, tP):
    t = translate_to_list(aT)
    for y, yn in zip(t[tP[1]], range(len(t[0][0]))):
        for x, xn in zip(y, range(len(t[0][0]))):
            if x > 0:
                try:
                    if board[tP[0][1] + yn + 1][tP[0][0] + xn] > 0:
                        return False
                except IndexError:
                    return False
    return True


def can_tetromino_move(board, aT, tP, direction):
    t = translate_to_list(aT)
    for y, yn in zip(t[tP[1]], range(len(t[0][0]))):
        for x, xn in zip(y, range(len(t[0][0]))):
            if x > 0:
                try:
                    if board[tP[0][1] + yn][tP[0][0] + xn + direction] > 0 or (tP[0][0] + xn <= 0 and direction == -1):
                        return False
                except IndexError:
                    return False
    return True


def can_tetromino_rotate(board, aT, tP, direction):
    t = translate_to_list(aT)
    for y, yn in zip(t[tP[1] + direction], range(len(t[0][0]))):
        for x, xn in zip(y, range(len(t[0][0]))):
            if x > 0:
                try:
                    if board[tP[0][1] + yn][tP[0][0] + xn] > 0 or tP[0][0] + xn < 0:
                        return False
                except IndexError:
                    return False
    return True


def solidify_tetromino(board, aT, tP):
    end_game = False
    t = translate_to_list(aT)
    for y, yn in zip(t[tP[1]], range(len(t[0][0]))):
        for x, xn in zip(y, range(len(t[0][0]))):
            if x > 0:
                if board[tP[0][1] + yn][tP[0][0] + xn] == 0:
                    board[tP[0][1] + yn][tP[0][0] + xn] = x
                else:
                    end_game = True
    return board, end_game


def tp_tetromino_down(board, aT, tP):
    while can_tetromino_fall(board, aT, tP):
        tP[0][1] += 1
    return solidify_tetromino(board, aT, tP)


def draw_ghost_tetromino(board, aT, tP):
    t = translate_to_list(aT)
    tcoords = [tP[0][0], tP[0][1]]
    while can_tetromino_fall(board, aT, [tcoords, tP[1]]):
        tcoords[1] += 1

    for y, yn in zip(t[tP[1]], range(len(t[0]))):
        if tcoords[1] + yn > 1:
            for x, xn in zip(y, range(len(t[0][0]))):
                if x > 0:
                    pygame.draw.rect(gameDisplay, colorList[x - 1],
                                 (startPosBoard[0] + tcoords[0] * bsbg + xn * bsbg,
                                  startPosBoard[1] + tcoords[1] * bsbg + yn * bsbg,
                                  blockSize, blockSize), 1)


def draw_board_outline():
    for a in range(21):
        pygame.draw.rect(gameDisplay, white, (startPosOutline[0], startPosOutline[1] + a * bsbg, blockSize, blockSize))
        pygame.draw.rect(gameDisplay, white, (startPosOutline[0] + 11 * bsbg,
                                              startPosOutline[1] + a * bsbg, blockSize, blockSize))
    for b in range(10):
        pygame.draw.rect(gameDisplay, white, (startPosOutline[0] + (b + 1) * bsbg,
                                              startPosOutline[1] + 20 * bsbg, blockSize, blockSize))


def board_outline_animation(size):
    for a in range(21):
        pygame.draw.rect(gameDisplay, white, (startPosOutline[0] + blockSize / 2 - size,
                                              startPosOutline[1] + a * bsbg + blockSize / 2 - size, 2 * size, 2 * size))
        pygame.draw.rect(gameDisplay, white, (startPosOutline[0] + 11 * bsbg + blockSize / 2 - size,
                                              startPosOutline[1] + a * bsbg + blockSize / 2 - size, 2 * size, 2 * size))
    for b in range(10):
        pygame.draw.rect(gameDisplay, white, (startPosOutline[0] + (b + 1) * bsbg + blockSize / 2 - size,
                                              startPosOutline[1] + 20 * bsbg + blockSize / 2 - size,
                                              2 * size, 2 * size))


def game_in_animation():
    for size in range(1, blockSize // 2 + 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitplz()
        gameDisplay.blit(bgTexture, (0, 0))
        board_outline_animation(size)
        mainDisplay.blit(gameDisplay, (0, 0))
        pygame.display.update()
        clock.tick(60)


def board_animation(size, board):
    for y, yn in zip(board, range(len(board))):
        for x, xn in zip(y, range(len(y))):
            if yn >= 2 and x > 0:
                pygame.draw.rect(gameDisplay, colorList[x - 1],
                                 (startPosBoard[0] + xn * bsbg + blockSize / 2 - size,
                                  startPosBoard[1] + yn * bsbg + blockSize / 2 - size, 2 * size, 2 * size))


def game_out_animation(board):
    for size in range(blockSize // 2, 0, -1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitplz()
        gameDisplay.blit(bgTexture, (0, 0))
        board_outline_animation(size)
        board_animation(size, board)
        mainDisplay.blit(gameDisplay, (0, 0))
        pygame.display.update()
        clock.tick(60)
    gameDisplay.blit(bgTexture, (0, 0))
    mainDisplay.blit(gameDisplay, (0, 0))
    pygame.display.update()


def draw_board(board):
    for y, yn in zip(board, range(len(board))):
        for x, xn in zip(y, range(len(y))):
            if yn >= 2 and x > 0:
                pygame.draw.rect(gameDisplay, colorList[x - 1],
                                 (startPosBoard[0] + xn * bsbg, startPosBoard[1] + yn * bsbg, blockSize, blockSize))


def mm_in_animation():
    pygame.mouse.set_visible(False)
    playButton1.reset_position()
    playButton2.reset_position()
    playButton3.reset_position()
    playButton1.reset_speed()
    playButton2.reset_speed()
    playButton3.reset_speed()
    for bTime in range(110):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitplz()
        menuDisplay.blit(bgTexture, (0, 0))
        playButton1.move_button_in(bTime)
        playButton2.move_button_in(bTime)
        playButton3.move_button_in(bTime)
        tLogo.move_logo_in(bTime)
        mainDisplay.blit(menuDisplay, (0, 0))
        pygame.display.update()
        clock.tick(60)


def mm_out_animation():
    pygame.mouse.set_visible(False)
    playButton1.reset_speed()
    playButton2.reset_speed()
    playButton3.reset_speed()
    for aTime in range(110):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitplz()
        menuDisplay.blit(bgTexture, (0, 0))
        playButton1.move_button_out(aTime)
        playButton2.move_button_out(aTime)
        playButton3.move_button_out(aTime)
        tLogo.move_logo_out(aTime)
        mainDisplay.blit(menuDisplay, (0, 0))
        pygame.display.update()
        clock.tick(60)


def game_over_screen(level, lines, score):
    global tetrominosBag
    pygame.mouse.set_visible(True)
    pygame.mixer.music.fadeout(500)

    lvlTextNumber = fontBasic.render(str(level), False, white)
    lnsTextNumber = fontBasic.render(str(lines), False, white)
    scrTextNumber = fontBasic.render(str(score), False, white)

    lvlTextNumberRect = lvlTextNumber.get_rect()
    lnsTextNumberRect = lnsTextNumber.get_rect()
    scrTextNumberRect = scrTextNumber.get_rect()

    lvlTextNumberRect.center = (width // 2, 325)
    lnsTextNumberRect.center = (width // 2, 425)
    scrTextNumberRect.center = (width // 2, 525)

    gameDisplay.blit(lvlText, lvlTextRectGO)
    gameDisplay.blit(lvlTextNumber, lvlTextNumberRect)
    gameDisplay.blit(lnsText, lnsTextRectGO)
    gameDisplay.blit(lnsTextNumber, lnsTextNumberRect)
    gameDisplay.blit(scrText, scrTextRectGO)
    gameDisplay.blit(scrTextNumber, scrTextNumberRect)
    gameDisplay.blit(gameOverText, gameOverTextRect)
    gameDisplay.blit(mainMenuButtonTexture, mMButtonPos)
    gameDisplay.blit(quitButtonTexture, qButtonPos)
    mainDisplay.blit(gameDisplay, (0, 0))

    pygame.display.update()

    game_over = True

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitplz()
            elif event.type == pygame.MOUSEBUTTONUP:
                mpos = pygame.mouse.get_pos()
                if mMButtonPos[0] <= mpos[0] <= mMButtonPos[0] + gOButtonSize[0] and\
                                        mMButtonPos[1] <= mpos[1] <= mMButtonPos[1] + gOButtonSize[1]:
                    tetrominosBag = tetrominos[:]
                    return True
                elif qButtonPos[0] <= mpos[0] <= qButtonPos[0] + gOButtonSize[0] and\
                                        qButtonPos[1] <= mpos[1] <= qButtonPos[1] + gOButtonSize[1]:
                    quitplz()


def game():
    global themeVolume, lastThemeVolume
    pygame.mouse.set_visible(False)
    pygame.mixer.music.play(-1)
    gBoard = [[0] * 10 for i in range(22)]
    activeTetromino = random_tetromino()
    nextTetromino = random_tetromino()
    tetrominoProps = [[4, 0], 0]  # Coords, rotation
    if activeTetromino == "I":
        tetrominoProps[0][0] = 3
    nextTetrominoPos = [displayDimensions[0] - (startPosOutline[0] - blockSize) // 2 - bsbg - blockSize,
                        startPosOutline[1] + 3 * bsbg]
    if nextTetromino == "I":
        nextTetrominoPos[0] = displayDimensions[0] - (startPosOutline[0] - blockGap) // 2 - 2 * bsbg
    elif nextTetromino == "O":
        nextTetrominoPos[0] = displayDimensions[0] - (startPosOutline[0] - blockGap) // 2 - bsbg

    left_down = False
    right_down = False
    down_down = False

    down_countdown = 0
    right_countdown1 = 0
    left_countdown1 = 0
    right_countdown2 = 0
    left_countdown2 = 0
    s_cycle_left = 0
    s_cycle_right = 0
    lines_total = 0
    level = 0
    score = 0
    fallDelay = 33
    updatedisplay = True

    playing = True
    while playing:
        if not pygame.key.get_focused():
            pause_menu(True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitplz()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_menu(False)
                elif event.key == pygame.K_m:
                    if themeVolume == 0:
                        if lastThemeVolume == 0:
                            themeVolume = 1
                        else:
                            themeVolume = lastThemeVolume
                    else:
                        lastThemeVolume = themeVolume
                        themeVolume = 0
                    pygame.mixer.music.set_volume(themeVolume)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    down_down = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if can_tetromino_rotate(gBoard, activeTetromino, tetrominoProps, 1):
                        tetrominoProps[1] += 1
                        if tetrominoProps[1] >= 3:
                            tetrominoProps[1] = -1
                    updatedisplay = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    right_down = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left_down = True
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    gBoard, gameOver = tp_tetromino_down(gBoard, activeTetromino, tetrominoProps)

                    if gameOver:
                        game_out_animation(gBoard)
                        go_to_main_menu = game_over_screen(level, lines_total, score)
                        if go_to_main_menu:
                            return True

                    activeTetromino = nextTetromino
                    nextTetromino = random_tetromino()
                    tetrominoProps = [[4, 0], 0]
                    if activeTetromino == "I":
                        tetrominoProps[0][0] = 3
                    nextTetrominoPos = [
                    displayDimensions[0] - (startPosOutline[0] - blockSize) // 2 - bsbg - blockSize,
                        startPosOutline[1] + 3 * bsbg]
                    if nextTetromino == "I":
                        nextTetrominoPos[0] = displayDimensions[0] - (startPosOutline[0] - blockGap) // 2\
                                             - 2 * bsbg
                    elif nextTetromino == "O":
                        nextTetrominoPos[0] = displayDimensions[0] - (startPosOutline[0] - blockGap) // 2 - bsbg
                    gBoard, lines = line_checker(gBoard, level, lines_total, score)
                    if lines == 1:
                        score += 40 * (level + 1)
                    elif lines == 2:
                        score += 100 * (level + 1)
                    elif lines == 3:
                        score += 300 * (level + 1)
                    elif lines == 4:
                        score += 1200 * (level + 1)
                    lines_total += lines
                    level = lines_total // 10
                    updatedisplay = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    down_down = False
                    down_countdown = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    right_down = False
                    right_countdown1 = 0
                    right_countdown2 = 0
                    s_cycle_right = 0

                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left_down = False
                    left_countdown1 = 0
                    left_countdown2 = 0
                    s_cycle_left = 0

        if left_down and not right_down:
            if (s_cycle_left == 1 and left_countdown1 <= 0) or (s_cycle_left >= 2 and left_countdown2 <= 0)\
                    or s_cycle_left == 0:
                if can_tetromino_move(gBoard, activeTetromino, tetrominoProps, -1):
                    tetrominoProps[0][0] -= 1
                    s_cycle_left += 1
                    left_countdown1 = sideWait1
                    left_countdown2 = sideWait2
                    updatedisplay = True
            else:
                left_countdown1 -= 1
                left_countdown2 -= 1

        if right_down and not left_down:
            if (s_cycle_right == 1 and right_countdown1 <= 0) or (s_cycle_right >= 2 and right_countdown2 <= 0)\
                    or s_cycle_right == 0:
                if can_tetromino_move(gBoard, activeTetromino, tetrominoProps, 1):
                    tetrominoProps[0][0] += 1
                    s_cycle_right += 1
                    right_countdown1 = sideWait1
                    right_countdown2 = sideWait2
                    updatedisplay = True
            else:
                right_countdown1 -= 1
                right_countdown2 -= 1

        if down_down:
            if down_countdown <= 0:
                if can_tetromino_fall(gBoard, activeTetromino, tetrominoProps):
                    tetrominoProps[0][1] += 1
                else:
                    gBoard, gameOver = solidify_tetromino(gBoard, activeTetromino, tetrominoProps)

                    if gameOver:
                        game_out_animation(gBoard)
                        go_to_main_menu = game_over_screen(level, lines_total, score)
                        if go_to_main_menu:
                            return True

                    activeTetromino = nextTetromino  # Having this here is bullshit
                    nextTetromino = random_tetromino()
                    tetrominoProps = [[4, 0], 0]  # Coords, rotation
                    if activeTetromino == "I":
                        tetrominoProps[0][0] = 3
                    nextTetrominoPos = [
                        displayDimensions[0] - (startPosOutline[0] - blockSize) // 2 - bsbg - blockSize,
                        startPosOutline[1] + 3 * bsbg]
                    if nextTetromino == "I":
                        nextTetrominoPos[0] = displayDimensions[0] - (startPosOutline[0] - blockGap) // 2 \
                                              - 2 * bsbg
                    elif nextTetromino == "O":
                        nextTetrominoPos[0] = displayDimensions[0] - (startPosOutline[0] - blockGap) // 2 - bsbg
                    gBoard, lines = line_checker(gBoard, level, lines_total, score)
                    if lines == 1:
                        score += 40 * (level + 1)
                    elif lines == 2:
                        score += 100 * (level + 1)
                    elif lines == 3:
                        score += 300 * (level + 1)
                    elif lines == 4:
                        score += 1200 * (level + 1)
                    lines_total += lines
                    level = lines_total // 10
                down_countdown = downWait
                updatedisplay = True
            else:
                down_countdown -= 1

        if fallDelay <= 0:
            if can_tetromino_fall(gBoard, activeTetromino, tetrominoProps):
                tetrominoProps[0][1] += 1
            else:
                gBoard, gameOver = solidify_tetromino(gBoard, activeTetromino, tetrominoProps)

                if gameOver:
                    game_out_animation(gBoard)
                    go_to_main_menu = game_over_screen(level, lines_total, score)
                    if go_to_main_menu:
                        return True

                activeTetromino = nextTetromino
                nextTetromino = random_tetromino()
                tetrominoProps = [[4, 0], 0]
                if activeTetromino == "I":
                    tetrominoProps[0][0] = 3
                nextTetrominoPos = [
                    displayDimensions[0] - (startPosOutline[0] - blockSize) // 2 - bsbg - blockSize,
                    startPosOutline[1] + 3 * bsbg]
                if nextTetromino == "I":
                    nextTetrominoPos[0] = displayDimensions[0] - (startPosOutline[0] - blockGap) // 2 \
                                          - 2 * bsbg
                elif nextTetromino == "O":
                    nextTetrominoPos[0] = displayDimensions[0] - (startPosOutline[0] - blockGap) // 2 - bsbg
                gBoard, lines = line_checker(gBoard, level, lines_total, score)
                if lines == 1:
                    score += 40 * (level + 1)
                elif lines == 2:
                    score += 100 * (level + 1)
                elif lines == 3:
                    score += 300 * (level + 1)
                elif lines == 4:
                    score += 1200 * (level + 1)
                lines_total += lines
                level = lines_total // 10

            if level < 10:
                fallDelay = (11 - level) * 3
            else:
                fallDelay = 3
            updatedisplay = True
        else:
            fallDelay -= 1

        # Render everything
        if updatedisplay:
            updatedisplay = False
            gameDisplay.blit(bgTexture, (0, 0))
            draw_board_outline()
            draw_board(gBoard)
            if showGhostPiece:
                draw_ghost_tetromino(gBoard, activeTetromino, tetrominoProps)
            draw_tetromino(activeTetromino, tetrominoProps)
            draw_sidebar(score, lines_total, level, nextTetromino, nextTetrominoPos)
            mainDisplay.blit(gameDisplay, (0, 0))
            pygame.display.update()
        clock.tick(60)


def main_menu():
    pygame.mouse.set_visible(True)
    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitplz()
            elif event.type == pygame.MOUSEBUTTONUP:
                mpos = pygame.mouse.get_pos()
                if button1pos[0][0] <= mpos[0] <= button1pos[1][0] and button1pos[0][1] <= mpos[1] <= button1pos[1][1]:
                    mm_out_animation()
                    game_in_animation()
                    mm = game()
                    if mm:
                        mm_in_animation()
                        main_menu()
                elif button2pos[0][0] <= mpos[0] <= button2pos[1][0] and button2pos[0][1] <= mpos[1] <= button2pos[1][1]:
                    mm_out_animation()
                    settings_menu()
                    mm_in_animation()



def pause_menu(unpause_on_focus):
    pygame.mouse.set_visible(True)
    themeplaytime = pygame.mixer.music.get_pos()
    pygame.mixer.music.fadeout(250)
    paused = True
    pauseDisplay.fill((255, 255, 255, 100))
    mainDisplay.blit(pauseDisplay, (0, 0))
    pygame.display.update()
    while paused:
        if unpause_on_focus and pygame.key.get_focused():
            paused = False
            pygame.mouse.set_visible(False)
            pygame.mixer.music.play(-1, themeplaytime)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitplz()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                    pygame.mouse.set_visible(False)
                    pygame.mixer.music.play(-1, themeplaytime)


def draw_settings():
    mainDisplay.blit(bgTexture, (0, 0))
    mainDisplay.blit(settingsText, settingsTextRect)
    mainDisplay.blit(sgpText, sgpTextPos)
    mainDisplay.blit(volumeText, volumeTextRect)
    pygame.draw.rect(mainDisplay, white, (sgpTextPos[0] + sgpTextSize[0] + sgpTextSize[1],
                                          sgpTextPos[1],sgpTextSize[1], sgpTextSize[1]), 1)
    if showGhostPiece:
        pygame.draw.lines(mainDisplay, white, False,
                          [(sgpTextPos[0] + sgpTextSize[0] + sgpTextSize[1], sgpTextPos[1] + sgpTextSize[1] // 2 - 2),
                           (sgpTextPos[0] + sgpTextSize[0] + sgpTextSize[1] * 1.5, sgpTextPos[1] + sgpTextSize[1] - 3),
                           (sgpTextPos[0] + sgpTextSize[0] + sgpTextSize[1] * 2, sgpTextPos[1] - sgpTextSize[1] // 2)],
                          3)


def settings_menu():
    global showGhostPiece, themeVolume
    pygame.mouse.set_visible(True)
    draw_settings()
    pygame.display.update()
    menu = True
    slider = False
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitplz()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                if sgpTextPos[0] + sgpTextSize[0] + sgpTextSize[1] <= mpos[0] <= sgpTextPos[0] + sgpTextSize[0] + \
                                sgpTextSize[1] * 2 and sgpTextPos[1] <= mpos[1] <= sgpTextPos[1] + sgpTextSize[1]:
                    showGhostPiece = not showGhostPiece
                    draw_settings()
                    pygame.display.update()





mm_in_animation()
main_menu()

quitplz()
