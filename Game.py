import InitialGameState
import GameState
import sys
import random
from threading import Thread
from time import sleep




class Game:
    def __init__(self):
        self.gamestates = []
        self.gamestates.append(InitialGameState.InitialGameState(0))
        self.currentState = 0
        self.currentTurn = "B"
        self.playerColor = "B"
        self.aiColor = "W"
        self.timerStop = False
        self.outOfTime = False
        self.possibleEndGame = False
        self.possibleEndGameAB = False
        self.forceAMove = False
        self.aiMadeMove = False
        self.aiBestMove = 'null'
        self.secondState = False

        print ''
        print '----------------------------------------------------------'
        print '----------------------------------------------------------'
        print 'Welcome to Othello!'
        print '----------------------------------------------------------'
        print '----------------------------------------------------------'
        print ''
        print ''
        print 'Here is the current board configuration'
        print '--------------------------------------------'
        print ''
        self.gamestates[self.currentState].printBoard()
        self.flipBoardConfig()



        config = raw_input('AI color (B or W): ')
        print ''

        if config == 'B':
            self.playerColor = "W"
            self.aiColor = "B"


    # ************************************
    # * flipBoardConfig()
    # ************************************
    # Configures the board based on the user input
    def flipBoardConfig(self):
        flipBoard = raw_input('Would you like to flip the configuration of the board? (Y/N)')
        if flipBoard == 'Y':
            self.gamestates[self.currentState].flipBoard()
            print ''
            print 'Here is the new board configuration'
            print '--------------------------------------------'
            print ''
            self.gamestates[self.currentState].printBoard()
            print ''
            self.flipBoardConfig()



    def getPlayerColor(self):
        return self.playerColor

    def getCurrentState(self):
        return self.gamestates[self.currentState]

    def getCurrentTurn(self):
        return self.currentTurn

    def makeMove(self):
        if self.playerColor == self.currentTurn:
            # Players Turn
            self.playerMove()
        else:
            # AIs Turn
            self.AIMove()

    def playerMove(self):
        validMoves = self.gamestates[self.currentState].getValidMoves()
        if validMoves == []:

            if self.possibleEndGame == True:
                self.endGame()
            else:
                print "You have no valid moves!"
                uin = raw_input("Press Enter to confirm and pass your turn or type 'prev' to view the previous Game State")
                if uin == 'prev':
                    self.previousState()
                else:
                    self.possibleEndGame = True
                    self.gamestates.append(
                        GameState.GameState(self.gamestates[self.currentState], 'null', self.playerColor, self.aiColor))
                    self.currentState += 1
                    self.currentTurn = self.aiColor
        else:
            self.possibleEndGame = False
            print 'Options'
            print '------------------------------'
            print '1) View Previous Game State'
            print '2) Quit Game'
            print '------------------------------'
            print 'Available Moves = ' + str(validMoves)
            print ''
            move = raw_input("Make a move or select an option above: ")
            print ''

            if move == "2":
                sys.exit()
            elif move == "1":
                self.previousState()
            else:
                if move in validMoves:
                    print 'Here is the New Move'
                    print '--------------------------------------------'
                    print ''
                    self.gamestates.append(GameState.GameState(self.gamestates[self.currentState], move, self.playerColor, self.aiColor))
                    self.currentState += 1
                    self.gamestates[self.currentState].printBoard()
                    raw_input("Press Enter to confirm new board layout")
                    print ''
                    print '--------------------------------------------'
                    print "AI's Turn"
                    print '--------------------------------------------'
                    print 'Current Game State:'
                    print ''
                    self.gamestates[self.currentState].flipTiles()
                    self.gamestates[self.currentState].calculateScore()
                    self.gamestates[self.currentState].printBoard()
                    self.gamestates[self.currentState].printScoreBoard()
                    self.currentTurn = self.aiColor

                else:
                    print ''
                    print 'Not a Valid Move.. Try Again'

    def AIMove(self):
        validMoves = self.gamestates[self.currentState].getValidMoves()
        if validMoves == []:

            if self.possibleEndGame == True:
                self.endGame()
            else:
                print "AI has no valid moves"
                uin = raw_input(
                    "Press Enter to confirm and pass AI turn or type 'prev' to view the previous Game State")
                if uin == 'prev':
                    self.previousState()
                else:
                    self.gamestates.append(
                        GameState.GameState(self.gamestates[self.currentState], 'null', self.aiColor, self.playerColor))
                    self.currentState += 1
                    self.currentTurn = self.playerColor
        else:
            print 'Options'
            print '------------------------------'
            print '1) View Previous Game State'
            print '2) Quit Game'
            print '------------------------------'
            print 'Available Moves = ' + str(validMoves)
            print ''
            userIn = raw_input("Press Enter to let the AI make its move or select an option above: ")
            if userIn == "1":
                self.previousState()
            elif userIn == '2':
                sys.exit()
            else:
                self.possibleEndGame = False
                if self.forceAMove == False:
                    aiDecision = Thread(target=self.AIDecision)
                    aiDecision.start()
                timer = Thread(target=self.timer)
                timer.start()  # Calls first function
                while self.aiMadeMove == False:
                    sleep(1)

                self.aiMadeMove = False

                print ''
                print 'Here is the New Move'
                print '--------------------------------------------'
                print ''
                self.gamestates[self.currentState].printBoard()
                raw_input("Press Enter to confirm current board layout")
                print ''
                print '--------------------------------------------'
                print "Opponent's Turn"
                print '--------------------------------------------'
                print 'Current Game State:'
                print ''
                self.gamestates[self.currentState].flipTiles()
                self.gamestates[self.currentState].calculateScore()
                self.gamestates[self.currentState].printBoard()
                self.gamestates[self.currentState].printScoreBoard()
                self.currentTurn = self.playerColor

    def AIDecision(self):
        print ("AI is thinking....")
        val, move = self.alphaBetaAI(self.gamestates[self.currentState],'null','null',5,5)
        if self.forceAMove == False:
            self.timerStop = True
            print "The AI's move is: " + move
            self.gamestates.append(GameState.GameState(self.gamestates[self.currentState], move, self.aiColor, self.playerColor))
            self.currentState += 1
            self.aiMadeMove = True
        else:
            self.forceAMove = False

    def timer(self):
        for i in range(10):
            if self.forceAMove == True:
                self.aiforceMove()
                break
            if i == 9:
                self.aiforceMove()
                break
            sleep(1)
            if self.timerStop == True:
                break

        if self.timerStop == False:
            print "AI out of time!!!"
            self.outOfTime = True

        self.timerStop = False

    def aiforceMove(self):
        self.forceAMove = True
        self.timerStop = True
        move = self.aiBestMove
        print "AI's move is: " + move
        self.gamestates.append(
            GameState.GameState(self.gamestates[self.currentState], move, self.aiColor, self.playerColor))
        self.currentState += 1
        self.aiMadeMove = True

    def alphaBetaAI(self,gamestate,alpha,beta,depth,startDepth):

        if self.forceAMove == True:
            self.forceAMove = False
            sys.exit()

        if self.outOfTime == True:
            quit()
        if gamestate.getTotalChips() > 4:
            gamestate.flipTiles()
            gamestate.calculateScore()
        validMoves = gamestate.getValidMoves()

        if depth == 0:
            return self.heuristic(gamestate), "Null"

        if validMoves == []:
            if self.possibleEndGameAB == True:
                return self.heuristic(gamestate), "Null"
            else:
                cmpVal, cmpMove = self.alphaBetaOpponent(GameState.GameState(gamestate, 'null', self.aiColor, self.playerColor), alpha,
                                       beta, depth - 1,startDepth)
                return cmpVal, cmpMove

        self.possibleEndGameAB = False
        bestVal = float("-inf")
        bestMove = validMoves[0]
        if depth == startDepth:
            self.aiBestMove = bestMove

        for move in validMoves:
            cmpVal, cmpMove = self.alphaBetaOpponent(GameState.GameState(gamestate, move, self.aiColor, self.playerColor), alpha, beta, depth - 1,startDepth)
            if cmpVal > bestVal:
                bestVal = cmpVal
                bestMove = move
                if depth == startDepth:
                    self.aiBestMove = bestMove
            if beta != 'null':
                if cmpVal >= beta:
                    return bestVal, bestMove
            if alpha == 'null' or cmpVal > alpha:
                alpha = cmpVal
        return bestVal, bestMove

    def alphaBetaOpponent(self,gamestate,alpha,beta,depth,startDepth):
        if self.forceAMove == True:
            self.forceAMove = False
            sys.exit()

        if self.outOfTime == True:
            quit()
        gamestate.flipTiles()
        gamestate.calculateScore()
        validMoves = gamestate.getValidMoves()

        if depth == 0:
            print self.heuristic(gamestate)
            return self.heuristic(gamestate), "Null"


        #Checks for a pass or an end of game
        if validMoves == []:
            if self.possibleEndGameAB == True:
                return self.heuristic(gamestate), "Null"
            else:
                cmpVal, cmpMove = self.alphaBetaOpponent(GameState.GameState(gamestate, 'null', self.playerColor, self.aiColor), alpha,
                                       beta, depth - 1,startDepth)
                return cmpVal, cmpMove

        self.possibleEndGameAB = False
        bestVal = float("inf")
        bestMove = validMoves[0]
        for move in validMoves:
            cmpVal, cmpMove = self.alphaBetaAI(GameState.GameState(gamestate, move, self.playerColor, self.aiColor),alpha,beta,depth-1,startDepth)
            if cmpVal < bestVal:
                bestVal = cmpVal
                bestMove = move
            if alpha != 'null':
                if cmpVal <= alpha:
                    return bestVal, bestMove
            if beta == 'null' or cmpVal < beta:
                beta = cmpVal
        return bestVal, bestMove




    def endGame(self):
        self.gamestates[self.currentState].calculateScore()
        print ''
        print ''
        print '-------------------------'
        print 'Game Over!'
        print '-------------------------'
        print 'Final Score:'
        print 'Black - ' + str(self.gamestates[self.currentState].getBlackScore())
        print 'White - ' + str(self.gamestates[self.currentState].getWhiteScore())
        print ''
        quit()

    def previousState(self):
        previousState = self.gamestates[self.currentState-1]
        print ''
        print '--------------------------------------------------'
        print 'This is the previous Game State (Preview Only)'
        print '--------------------------------------------------'
        previousState.printBoard()
        print 'What would you like to do?'
        print '1) Return to current Game State'
        print '2) Replay the previous move'
        print '3) Play from this state'
        userIn = raw_input("Please choose an option above:")

        if userIn == '1':
            print 'Taking you back to the current Game State...'
            sleep(2)
            print ''
            print '--------------------------------------------'
            print 'Current Game State'
            print '--------------------------------------------'
            print ''
            gamestate = self.gamestates[self.currentState]
            gamestate.calculateScore()
            gamestate.printBoard()
            gamestate.printScoreBoard()
            self.makeMove()

        elif userIn == '2':
            prevMove = self.gamestates[self.currentState].getMove()
            prevReplay = GameState.GameState(self.gamestates[self.currentState-1], prevMove, previousState.getNextPlayer(), previousState.getPlayer())
            prevReplay.printBoard()

            print 'What would you like to do?'
            print '1) Return to current Game State'
            print '2) View previous state again'
            print '3) Play from the previous state'
            userIn2 = raw_input("Please choose an option above:")
            print ''

            if userIn2 == '1':
                print 'Taking you back to the current Game State...'
                sleep(2)
                print ''
                print '--------------------------------------------'
                print 'Current Game State'
                print '--------------------------------------------'
                print ''
                gamestate = self.gamestates[self.currentState]
                gamestate.calculateScore()
                gamestate.printBoard()
                gamestate.printScoreBoard()
                self.makeMove()

            elif userIn2 == '2':
                self.previousState()

            elif userIn2 == '3':
                self.playFromPrev()

            else:
                print 'Invalid Decision'
                print 'Taking you back to the current Game State...'
                sleep(2)
                print ''
                print '--------------------------------------------'
                print 'Current Game State'
                print '--------------------------------------------'
                print ''
                gamestate = self.gamestates[self.currentState]
                gamestate.calculateScore()
                gamestate.printBoard()
                gamestate.printScoreBoard()
                self.makeMove()


        elif userIn == '3':
            self.playFromPrev()

        else:
            print 'Please Choose a valid option'
            print 'Invalid Decision'
            print 'Taking you back to the current Game State...'
            sleep(2)
            print ''
            print '--------------------------------------------'
            print 'Current Game State'
            print '--------------------------------------------'
            print ''
            gamestate = self.gamestates[self.currentState]
            gamestate.calculateScore()
            gamestate.printBoard()
            gamestate.printScoreBoard()
            self.makeMove()


    def playFromPrev(self):
        print 'Resetting to previous Game State...'
        sleep(2)
        print ''
        print '--------------------------------------------'
        print 'New Current Game State'
        print '--------------------------------------------'
        print ''
        del self.gamestates[-1]
        self.currentState -= 1
        gamestate = self.gamestates[self.currentState]
        gamestate.printBoard()
        gamestate.printScoreBoard()
        self.currentTurn = gamestate.getNextPlayer()



    def heuristic(self,gamestate):

        if self.currentState <= 50:
            return self.calculateStability(gamestate)
        else:
            return self.calculateScoreDifference(gamestate) + self.calculateStability(gamestate)



    def calculateStability(self,gamestate):
        board = gamestate.getBoardArr()

        score = 0
        for i in range(len(board)):
            for j in range(len(board)):
                tile = board[i][j]
                if tile != ' ':
                    oppPlayer = 'W'
                    if tile == 'W':
                        oppPlayer = 'B'
                    if self.takenNextTurnCheck2(gamestate,i,j,oppPlayer):
                        if tile == self.aiColor:
                            score -= 1
                        else:
                            score += 1
                    if self.isStable(board,i,j):
                        if tile == self.aiColor:
                            score += 1
                        else:
                            score -= 1

        return score




    def calculateScoreDifference(self,gamestate):
        if self.aiColor == "W":
            return gamestate.getWhiteScore() - gamestate.getBlackScore()
        else:
            return gamestate.getBlackScore() - gamestate.getWhiteScore()




    def nwCorner(self, boardArr, i, j):
        a = i

        while a >= 0:
            if boardArr[a][j] == ' ':
                # if gamestate.boardArr[a][j] != ' ':
                return False
            a -= 1

        b = j
        while b >= 0:
            if boardArr[i][b] == ' ':
                # if gamestate.boardArr[i][b] != ' ':
                return False
            b -= 1

        a = i
        b = j
        while a >= 0 and b >= 0:
            if boardArr[a][b] == ' ':
                # if gamestate.boardArr[a][b] != ' ':
                return False
            b -= 1
            a -= 1

        return True

    def neCorner(self, boardArr, i, j):
        a = i

        while a <= 7:
            if boardArr[a][j] == ' ':
                # if gamestate.boardArr[a][j] != ' ':
                return False
            a += 1

        b = j
        while b >= 0:
            if boardArr[i][b] == ' ':
                # if gamestate.boardArr[i][b] != ' ':
                return False
            b -= 1

        a = i
        b = j
        while a <= 7 and b >= 0:
            if boardArr[a][b] == ' ':
                # if gamestate.boardArr[a][b] != ' ':
                return False
            b -= 1
            a += 1

        return True

    def seCorner(self, boardArr, i, j):
        a = i

        while a <= 7:
            if boardArr[a][j] == ' ':
                # if gamestate.boardArr[a][j] != ' ':
                return False
            a += 1

        b = j
        while b <= 7:
            if boardArr[i][b] == ' ':
                # if gamestate.boardArr[i][b] != ' ':
                return False
            b += 1

        a = i
        b = j
        while a <= 7 and b <= 0:
            if boardArr[a][b] == ' ':
                # if gamestate.boardArr[a][b] != ' ':
                return False
            b += 1
            a += 1

        return True

    def swCorner(self, boardArr, i, j):
        a = i

        while a >= 0:
            if boardArr[a][j] == ' ':
                # if gamestate.boardArr[a][j] != ' ':
                return False
            a -= 1

        b = j
        while b <= 7:
            if boardArr[i][b] == ' ':
                # if gamestate.boardArr[i][b] != ' ':
                return False
            b += 1

        a = i
        b = j
        while a >= 0 and b <= 7:
            if boardArr[a][b] == ' ':
                # if gamestate.boardArr[a][b] != ' ':
                return False
            b += 1
            a -= 1

        return True

    def isStable(self, boardArr, i, j):
        if self.nwCorner(boardArr, i, j):
            return True

        elif self.neCorner(boardArr, i, j):
            return True

        elif self.seCorner(boardArr, i, j):
            return True

        elif self.swCorner(boardArr, i, j):
            return True

        else:
            return False


    def calculateMobility(self, gamestate):
        if gamestate.nextPlayer == self.playerColor:
            return 0-len(gamestate.getValidMoves())
        else:
            return 0

    def takenNextTurnCheck2(self, gamestate, xIdx, yIdx, opponent):


        north = 'null'
        south = 'null'
        east = 'null'
        west = 'null'
        northEast = 'null'
        northWest = 'null'
        southEast = 'null'
        southWest = 'null'

        # checking North spaces
        for i in range(xIdx - 1, -1, -1):
            if gamestate.boardArr[i][yIdx] == opponent:
                north = opponent
                break
            elif gamestate.boardArr[i][yIdx] == '':
                north = ''
                break

        # checking South spaces
        for i in range(xIdx + 1, len(gamestate.boardArr)):
            if gamestate.boardArr[i][yIdx] == opponent:
                south = opponent
                break
            elif gamestate.boardArr[i][yIdx] == '':
                south = ''
                break

        if north == opponent and south == '':
            return True
        if south == opponent and north == '':
            return True

        # checking East spaces
        for i in range(yIdx + 1, len(gamestate.boardArr)):
            if gamestate.boardArr[xIdx][i] == opponent:
                east = opponent
                break
            elif gamestate.boardArr[xIdx][i] == '':
                east = ''
                break

        # checking West spaces
        for i in range(yIdx - 1, -1, -1):
            if gamestate.boardArr[xIdx][i] == opponent:
                west = opponent
                break
            elif gamestate.boardArr[xIdx][i] == '':
                west = ''
                break

        if west == opponent and east == '':
            return True
        if east == opponent and west == '':
            return True


        # checking NE spaces
        temp = xIdx
        for i in range(yIdx, len(gamestate.boardArr)):
            if gamestate.boardArr[temp][i] == opponent:
                northEast = opponent
                break

            elif gamestate.boardArr[temp][i] == '':
                northEast = ''
                break

            # if on the edge
            elif temp == 0 or i == 0:
                break

            temp -= 1

        # checking SW spaces
        temp = xIdx
        for i in range(yIdx, -1, -1):
            if gamestate.boardArr[temp][i] == opponent:
                southWest = opponent
                break

            elif gamestate.boardArr[temp][i] == '':
                southWest = ''
                break

            # if on the edge
            elif temp == len(gamestate.boardArr) - 1 or i == 0:
                break

            temp += 1


        if northEast == opponent and southWest == '':
            return True
        if southWest == opponent and northEast == '':
            return True


        # checking NW spaces
        temp = xIdx
        for i in range(yIdx, -1, -1):
            if gamestate.boardArr[temp][i] == opponent:
                northWest = opponent
                break

            elif gamestate.boardArr[temp][i] == '':
                northWest = ''
                break

            # if on the edge
            elif temp == 0 or i == 0:
                break

            temp -= 1


        # checking SE spaces
        temp = xIdx
        for i in range(yIdx, len(gamestate.boardArr)):
            if gamestate.boardArr[temp][i] == opponent:
                southEast = opponent
                break

            elif gamestate.boardArr[temp][i] == '':
                southEast = ''
                break

            # if on the edge
            elif temp == len(gamestate.boardArr) - 1:
                break

            temp += 1


        if northWest == opponent and southEast == '':
            return True
        if southEast == opponent and northWest == '':
            return True

        return False






