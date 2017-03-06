# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys
from pygame.locals import *
from tetrisConfig import *
import pygame.surfarray
import copy


# to adjust board configuration (size for example) please go to the tetrisConfig file
class TetrisEnv:
    def __init__(self, config):
        global BOARDWIDTH, BOARDHEIGHT, FPS, WINDOWWIDTH, WINDOWHEIGHT, XMARGIN, TOPMARGIN

        BOARDWIDTH = config['BOARDWIDTH']
        BOARDHEIGHT = config['BOARDHEIGHT']
        FPS = config['FPS']

        WINDOWWIDTH = (BOARDWIDTH * BOXSIZE) + BOARDWIDTH * 10
        WINDOWHEIGHT = (BOARDHEIGHT * BOXSIZE) + BOARDHEIGHT * 3
        XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
        TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 10

        pygame.init()
        self.config = config
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        self.BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
        self.board = self.getBlankBoard()
        self.lastMoveDownTime = time.time()
        self.lastMoveSidewaysTime = time.time()
        self.lastFallTime = time.time()
        self.movingDown = False  # note: there is no movingUp variable
        self.movingLeft = False
        self.movingRight = False
        self.score = 0
        self.level, self.fallFreq = self.calculateLevelAndFallFreq(self.score)
        self.fallingPiece = self.getNewPiece()
        self.nextPiece = self.getNewPiece()
        self.game_over = False

    # main method to be put in RLinterface
    def envFn(self, action=None):
        if action == None:
            return self.initialize()
        else:
            s, r = self.update_state(action)
            return s, r

    def fn(self, board):
        y = copy.deepcopy(board)

        for i in range(len(y)):
            for j in range(len(y[0])):
                if (y[i][j] == '.'):
                    y[i][j] = 0
                else:
                    y[i][j] = 1
        return y

    # initialize first state (blank board)
    def initialize(self):
        self.__init__(self.config)
        # drawing everything on the screen
        self.DISPLAYSURF.fill(BGCOLOR)
        self.drawBoard(self.board)

        # update the display
        pygame.display.update()

        binaryboard = self.fn(self.board)

        # return pygame.surfarray.array2d(pygame.display.get_surface())
        return binaryboard, self.fallingPiece

    # def get_legal_actions(self):


    # update state according to a given action and return 'terminal' if it can't fit a new piece on the board
    def update_state(self, actions):

        for action in actions:

            reward = 0
            if self.fallingPiece == None:
                # No falling piece in play, so start a new piece at the top
                self.fallingPiece = self.nextPiece
                self.nextPiece = self.getNewPiece()
                self.lastFallTime = time.time()  # reset lastFallTime

                if not self.isValidPosition(self.board, self.fallingPiece):
                    self.game_over = True  # can't fit a new piece on the board, so game over
                    return 'terminal', reward

            self.checkForQuit()
            if (action == K_LEFT) and self.isValidPosition(self.board, self.fallingPiece,
                                                           adjX=-1):
                self.fallingPiece['x'] -= 1
                self.movingLeft = True
                self.movingRight = False
                self.lastMoveSidewaysTime = time.time()

            elif (action == K_RIGHT) and self.isValidPosition(self.board, self.fallingPiece,
                                                              adjX=1):
                self.fallingPiece['x'] += 1
                self.movingRight = True
                self.movingLeft = False
                self.lastMoveSidewaysTime = time.time()

            # rotating the piece (if there is room to rotate)
            elif action == K_UP:
                self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] + 1) % len(
                    PIECES[self.fallingPiece['shape']])
                if not self.isValidPosition(self.board, self.fallingPiece):
                    self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] - 1) % len(
                        PIECES[self.fallingPiece['shape']])

            # making the piece fall faster with the down key
            elif action == K_DOWN:
                self.movingDown = True
                if self.isValidPosition(self.board, self.fallingPiece, adjY=1):
                    self.fallingPiece['y'] += 1
                self.lastMoveDownTime = time.time()

            # move the current piece all the way down
            elif action == K_SPACE:
                self.movingDown = False
                self.movingLeft = False
                self.movingRight = False
                for i in range(1, BOARDHEIGHT):
                    if not self.isValidPosition(self.board, self.fallingPiece, adjY=i):
                        break
                    self.fallingPiece['y'] += i - 1

                    # let the piece fall if it is time to fall
                    # if time.time() - self.lastFallTime > self.fallFreq:
                    # see if the piece has landed
            if not self.isValidPosition(self.board, self.fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                self.addToBoard()
                self.score += self.removeCompleteLines(self.board)
                # getting reward
                reward += self.removeCompleteLines(self.board)
                self.level, self.fallFreq = self.calculateLevelAndFallFreq(self.score)
                self.fallingPiece = None
            else:
                # piece did not land, just move the piece down
                self.fallingPiece['y'] += 1
                self.lastFallTime = time.time()

            # drawing everything on the screen
            self.DISPLAYSURF.fill(BGCOLOR)
            self.drawBoard(self.board)
            # drawStatus(score, level)
            # drawNextPiece(nextPiece)
            if self.fallingPiece != None:
                self.drawPiece(self.fallingPiece)

            # update the display
            pygame.display.update()
            # adjust FPS
            self.FPSCLOCK.tick(FPS)

            # image_data = pygame.surfarray.array2d(pygame.display.get_surface())

            binaryboard = self.fn(self.board)

            # binaryboard = [fn(j) for j in [i for i in self.board]]

            # return image_data, reward
        return (binaryboard, self.fallingPiece), reward

    def makeTextObjs(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def checkForKeyPress(self):
        # Go through event queue looking for a KEYUP event.
        # Grab KEYDOWN events to remove them from the event queue.
        self.checkForQuit()

        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None

    def showTextScreen(self, text):
        # This function displays large text in the
        # center of the screen until a key is pressed.
        # Draw the text drop shadow
        titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, TEXTSHADOWCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        self.DISPLAYSURF.blit(titleSurf, titleRect)

        # Draw the text
        titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, TEXTCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
        self.DISPLAYSURF.blit(titleSurf, titleRect)

        # Draw the additional "Press a key to play." text.
        pressKeySurf, pressKeyRect = self.makeTextObjs('Press a key to play.', self.BASICFONT, TEXTCOLOR)
        pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
        self.DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

        while self.checkForKeyPress() == None:
            pygame.display.update()
            self.FPSCLOCK.tick()

    def checkForQuit(self):
        for event in pygame.event.get(QUIT):  # get all the QUIT events
            self.terminate()  # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP):  # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.terminate()  # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event)  # put the other KEYUP event objects back

    def calculateLevelAndFallFreq(self, score):
        # Based on the score, return the level the player is on and
        # how many seconds pass until a falling piece falls one space.
        level = int(score / 10) + 1
        fallFreq = 0.27 - (level * 0.02)
        return level, fallFreq

    def getNewPiece(self):
        # return a random new piece in a random rotation and color
        shape = random.choice(list(PIECES.keys()))
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(PIECES[shape]) - 1),
                    'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                    'y': -2,  # start it above the board (i.e. less than 0)
                    'color': random.randint(0, len(COLORS) - 1)}
        return newPiece

    def addToBoard(self):
        # fill in the board based on piece's location, shape, and rotation
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if PIECES[self.fallingPiece['shape']][self.fallingPiece['rotation']][y][x] != BLANK:
                    self.board[x + self.fallingPiece['x']][y + self.fallingPiece['y']] = self.fallingPiece['color']

    def getBlankBoard(self):
        # create and return a new blank board data structure
        board = []
        for i in range(BOARDWIDTH):
            board.append([BLANK] * BOARDHEIGHT)
        return board

    def isOnBoard(self, x, y):
        return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

    def isValidPosition(self, board, piece, adjX=0, adjY=0):
        # Return True if the piece is within the board and not colliding
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                isAboveBoard = y + piece['y'] + adjY < 0
                if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                    continue
                if not self.isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                    return False
                if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                    return False
        return True

    def get_legal_actions(self):
        possibleSpin = [[], [K_UP], [K_UP, K_UP], [K_UP, K_UP, K_UP]]
        possibleXAdj = []

        def to_k_left_right(num):
            if num >= 0:
                temp = [K_RIGHT]*num
                temp.append(K_SPACE)
                return temp
            else:
                temp = [K_LEFT]*num
                temp.append(K_SPACE)
                return temp

        for xAdj in range(-BOARDWIDTH, BOARDWIDTH):
            if self.isValidPosition(self.board, self.fallingPiece, xAdj, 0):
                possibleXAdj.append(xAdj)
        movesAndSpace = map(to_k_left_right, possibleXAdj)

        result = []

        for spin in possibleSpin:
            for move in movesAndSpace:
                spin.extend(move)
                result.append(spin)

        return result

    def isCompleteLine(self, board, y):
        # Return True if the line filled with boxes with no gaps.
        for x in range(BOARDWIDTH):
            if board[x][y] == BLANK:
                return False
        return True

    def removeCompleteLines(self, board):
        # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
        numLinesRemoved = 0
        y = BOARDHEIGHT - 1  # start y at the bottom of the board
        while y >= 0:
            if self.isCompleteLine(board, y):
                # Remove the line and pull boxes down by one line.
                for pullDownY in range(y, 0, -1):
                    for x in range(BOARDWIDTH):
                        board[x][pullDownY] = board[x][pullDownY - 1]
                # Set very top line to blank.
                for x in range(BOARDWIDTH):
                    board[x][0] = BLANK
                numLinesRemoved += 1
                # Note on the next iteration of the loop, y is the same.
                # This is so that if the line that was pulled down is also
                # complete, it will be removed.
            else:
                y -= 1  # move on to check next row up
        return numLinesRemoved

    def convertToPixelCoords(self, boxx, boxy):
        # Convert the given xy coordinates of the board to xy
        # coordinates of the location on the screen.
        return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

    def drawBox(self, boxx, boxy, color, pixelx=None, pixely=None):
        # draw a single box (each tetromino piece has four boxes)
        # at xy coordinates on the board. Or, if pixelx & pixely
        # are specified, draw to the pixel coordinates stored in
        # pixelx & pixely (this is used for the "Next" piece).
        if color == BLANK:
            return
        if pixelx == None and pixely == None:
            pixelx, pixely = self.convertToPixelCoords(boxx, boxy)
        pygame.draw.rect(self.DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
        pygame.draw.rect(self.DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

    def drawBoard(self, board):
        # draw the border around the board
        pygame.draw.rect(self.DISPLAYSURF, BORDERCOLOR,
                         (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

        # fill the background of the board
        pygame.draw.rect(self.DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
        # draw the individual boxes on the board
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                self.drawBox(x, y, board[x][y])

    def drawStatus(self, score, level):
        # draw the score text
        scoreSurf = self.BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 150, 20)
        self.DISPLAYSURF.blit(scoreSurf, scoreRect)

        # draw the level text
        levelSurf = self.BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (WINDOWWIDTH - 150, 50)
        self.DISPLAYSURF.blit(levelSurf, levelRect)

    def drawPiece(self, piece, pixelx=None, pixely=None):
        shapeToDraw = PIECES[piece['shape']][piece['rotation']]
        if pixelx == None and pixely == None:
            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
            pixelx, pixely = self.convertToPixelCoords(piece['x'], piece['y'])

        # draw each of the boxes that make up the piece
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if shapeToDraw[y][x] != BLANK:
                    self.drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

    def drawNextPiece(self, piece):
        # draw the "next" text
        nextSurf = self.BASICFONT.render('Next:', True, TEXTCOLOR)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (WINDOWWIDTH - 120, 80)
        self.DISPLAYSURF.blit(nextSurf, nextRect)
        # draw the "next" piece
        self.drawPiece(piece, pixelx=WINDOWWIDTH - 120, pixely=100)
