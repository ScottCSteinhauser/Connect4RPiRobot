import random

class Connect4Board:
    board = 0  # All board pieces represented as a 42 bit integer, 0 represents empty board
    player1Pieces = 0  # Similar to the above, but only represents the pieces of player 1
    # player2Pieces is always board ^ player1Pieces (xor operator)
    numPieces = 0
    vertWinCheck = 0
    horWinCheck = 0

    diagWinCheckUR = 0


    def __init__(self):
        board = 0
        player1Pieces = 0
        numPieces = 0

    def boardToString(self):
        rows = []
        for i in range(6):
            row = ""
            for j in range(7):
                if (1 << (j*6 + i)) & (self.board & self.player1Pieces) > 0:
                    row += "1 "
                elif (1 << (j*6 + i)) & (self.board ^ self.player1Pieces) > 0:
                    row += "2 "
                else:
                    row += "0 "
            rows += [row]
        return "\n".join(rows[::-1])

    def makeMove(self, column, board = None):
        piece = 1 << (column*6)
        row = 0
        while piece & self.board > 0:
            piece = piece << 1
            row += 1
            if row == 6:
                print("INVALID MOVE")
                return False
        self.board += piece
        if self.numPieces % 2 == 0:
            self.player1Pieces += piece
        self.numPieces += 1
        return True
        # column is number from 0 to 6

    def checkForWin(self, player):
        """Input is 1 or 2 depending on which player is being checked, returns true if there are 4 in a row."""
        if player == 1:
            pieces = self.player1Pieces
        else:
            pieces = self.player1Pieces ^ self.board
        verticalWin = 15
        horizontalWin = 1 + (1 << 6) + (1 << 12) + (1 << 18)
        diagonalWinUR = 1 + (1 << 7) + (1 << 14) + (1 << 21)
        diagonalWinDL = 8 + (1 << 8) + (1 << 13) + (1 << 18)
        # check for vertical win
        p = 0
        for i in range(21):
            curWin = verticalWin << p
            if curWin & pieces == curWin:
                return True
            p+=1
            if (i+1)%3 == 0:
                p+=3
        # check for horizontal win
        p = 0
        for i in range(24):
            curWin = horizontalWin << p
            if curWin & pieces == curWin:
                return True
            p+=1
        # check for diagonal win up right
        p = 0
        for i in range(12):
            curWin = diagonalWinUR << p
            if curWin & pieces == curWin:
                return True
            p += 1
            if (i+1)%3 == 0:
                p += 3
        # check for diagonal win down left
        p = 0
        for i in range(12):
            curWin = diagonalWinDL << p
            if curWin & pieces == curWin:
                return True
            p += 1
            if (i+1)%3 == 0:
                p += 3
        # No wins detected. Return false.
        return False

    def simulateMove(self, column, board, player1Pieces, numPieces):
        piece = 1 << (column*6)
        row = 0
        while piece & board > 0:
            piece = piece << 1
            row += 1
            if row == 6:
                #print("INVALID MOVE")
                return board, player1Pieces
        board += piece
        if numPieces % 2 == 0:
            player1Pieces += piece
        return board, player1Pieces
        # column is number from 0 to 6

    def simulateCheckForWin(self, board, player1Pieces, player):
        """Input is 1 or 2 depending on which player is being checked, returns true if there are 4 in a row."""
        if player == 1:
            pieces = player1Pieces
        else:
            pieces = player1Pieces ^ board
        verticalWin = 15
        horizontalWin = 1 + (1 << 6) + (1 << 12) + (1 << 18)
        diagonalWinUR = 1 + (1 << 7) + (1 << 14) + (1 << 21)
        diagonalWinDL = 8 + (1 << 8) + (1 << 13) + (1 << 18)
        # check for vertical win
        p = 0
        for i in range(21):
            curWin = verticalWin << p
            if curWin & pieces == curWin:
                return True
            p += 1
            if (i + 1) % 3 == 0:
                p += 3
        # check for horizontal win
        p = 0
        for i in range(24):
            curWin = horizontalWin << p
            if curWin & pieces == curWin:
                return True
            p += 1
        # check for diagonal win up right
        p = 0
        for i in range(12):
            curWin = diagonalWinUR << p
            if curWin & pieces == curWin:
                return True
            p += 1
            if (i + 1) % 3 == 0:
                p += 3
        # check for diagonal win down left
        p = 0
        for i in range(12):
            curWin = diagonalWinDL << p
            if curWin & pieces == curWin:
                return True
            p += 1
            if (i + 1) % 3 == 0:
                p += 3
        # No wins detected. Return false.
        return False

    def simulateGame(self, board):
        """Simulates a random game between 1 and 2 from the current board state"""
        curNumPieces = self.numPieces + 1
        player1Pieces = self.player1Pieces
        while True:
            #print(curNumPieces)
            if curNumPieces == 42:
                return 0
            elif self.simulateCheckForWin(board, player1Pieces, 1):
                return 1
            elif self.simulateCheckForWin(board, player1Pieces, 2):
                return 2
            oldBoard = board
            board, player1Pieces = self.simulateMove(random.randint(0,6), board, player1Pieces, curNumPieces)
            if oldBoard != board:
                curNumPieces+=1
        return 0

    def AImakeMove(self, iterations):
        """Treats player 2 as AI, takes in number of simulations to run per move"""
        moveData = [[0,0,0] for x in range(7)]
        minLosses = 10000
        bestAction = 0
        for i in range(7):
            curBoard, player1Pieces = self.simulateMove(i, self.board, self.player1Pieces, self.numPieces)
            for j in range(iterations):
                # print(j)
                moveData[i][self.simulateGame(curBoard)] += 1
            if moveData[i][1] < minLosses:
                minLosses = moveData[i][1]
                bestAction = i
        print(moveData)
        self.makeMove(bestAction)






iterations = 500
b = Connect4Board()
while True:
    move = int(input("Make a move: "))
    b.makeMove(move)
    b.AImakeMove(iterations)
    print(b.boardToString())

    if b.checkForWin(1):
        print("You Win!")
        break
    elif b.checkForWin(2):
        print("You Lost :(")
        break





