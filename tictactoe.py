# Magician
import random
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Literal

"""
Console-format tic tac toe game in Python
"""


# Stores the score and the coordinates of a slot
@dataclass
class PositionInfo:
    # Value in this specific slot on the game board. 0 if not yet taken. 3 if taken by the game. -5 if taken by the player
    value: int = 0
    # Coordinates of this specific slot on the game board
    coordinates: tuple[int, int] | None = None


# Stores the total scores of a vertical/horizontal/diagonal line, along with the coordinates and the vaue
# of each slot of this line
@dataclass
class CountsInfo:
    # Total count of a vertical/horizontal/diagonal line
    count: int = 0
    # Coordinates and vaues of all the slots on this line
    positions: list[tuple[int, int]] = field(default_factory=list)


# Status of the game
gameState = "init"

# The 3 x 3 2D array of the visual game board with default value of each slot set to '-'
gameBoard = None

# The 3 x 3 2D array of the game board scores with default value of each slot set to 0
# If player plays on a slot, that slot yields -5 points
# If game plays on a slot, that slot yields 3 points
gameBoardValues = None

# Up-to-date results of each horizontal/vertical/diagonal line on the game board
gameCounts: list[CountsInfo] = None

# Shape of the token of the game. If set to 'x', game starts first
gamePiece = None

# Shape of the token of the player. If set to 'x', player starts first
playerPiece = None

# Indicating it's player's turn or not
playersTurn = None

# Score for the game
GAME_POINT = 3

# Score for the player
PLAYER_POINT = -5


# Initialize values for the fields that keep track of the game status and scores
def init():
    global gameState
    global gameBoard
    global gameBoardValues
    global gameCounts

    gameState = "init"

    gameBoard = [["-" for _ in range(3)] for _ in range(3)]

    gameBoardValues = {(row, col): 0 for row in range(3) for col in range(3)}

    gameCounts = [CountsInfo() for _ in range(8)]
    # Record all the coordinates on a horizontal/vertical/diagonal line
    # Horizontal lines are stored in indexes 0 to 2 inclusive
    # Vertical lines are stored in indexes 3 to 5 inclusive
    # Diagonal line from top-left to bottom-right is stored in index 6
    # Diagonal line from bottom-left to top-right is stored in index 7
    for rowIdx, row in enumerate(gameBoard):
        for colIdx, _ in enumerate(row):
            # Add coordinates of a slot of a horizontal line
            gameCounts[rowIdx].positions.append((rowIdx, colIdx))
            # Add coordinates of a slot of a vertical line
            gameCounts[rowIdx + len(gameBoard)].positions.append((colIdx, rowIdx))
        # Add coordinates of a slot of a diagonal line from top-left to bottom-right
        gameCounts[len(gameBoard) * 2].positions.append((rowIdx, rowIdx))
        # Add coordinates of a slot of a diagonal line from bottom-left to top-right
        gameCounts[len(gameBoard) * 2 + 1].positions.append(
            (rowIdx, len(gameBoard) - rowIdx - 1)
        )


def getSlotValue(idx1, idx2):
    gamePieceInSlot = gameBoard[idx1][idx2]
    if gamePieceInSlot == gamePiece:
        return GAME_POINT
    elif gamePieceInSlot == playerPiece:
        return PLAYER_POINT
    else:
        return 0


def getrandomnumber(min=1, max=100):
    return random.randint(min, max)


# Print the game board in the console
def drawBoard():
    print("The game board now is:")
    for element in gameBoard:
        print(*element)

    print("The game status is:")
    for element in gameCounts:
        print(f"Total score: {element.count} / Position: {element.positions}")


def getPlayerMove():
    while True:
        print(
            "Please enter the coordinates of your move, e.g. 1,1. The slot on the top-left corner is 0,0, and the slot on the bottom-right corner is 2,2."
        )
        value = input("You will play on: ")
        if (
            len(value) == 3
            and value[0] in "012"
            and value[1] == ","
            and value[2] in "012"
        ):
            indexes = int(value[0]), int(value[2])
            if gameBoardValues[indexes] == 0:
                return indexes
        print("Invalid input. Please enter 0, 1, or 2 in the format x,y.")


def findBestMove(countOfLine):
    indexesOfBestMoves: list[int] = []
    for idx, gameCount in enumerate(gameCounts):
        if gameCount.count == countOfLine:
            indexesOfBestMoves.append(idx)

    if len(indexesOfBestMoves) > 0:
        # Group the match indexes by the number of occurrences and choose the index(es) with highest occurrence
        indexesOfAllWinningMoves = Counter(indexesOfBestMoves)
        indexesCountsOfWinningMove = max(indexesOfAllWinningMoves.values())
        indexesOfBestWinningMoves = [
            value
            for value, count in indexesOfAllWinningMoves.items()
            if count == indexesCountsOfWinningMove
        ]

        print("Indexes of lines with best winning moves: ", indexesOfBestWinningMoves)

        emptySlots = []
        # From the lines with the best move(s), collect the slots that are still empty
        for index in indexesOfBestWinningMoves:
            gameCountOfBestWinningMoves = gameCounts[index]

            for position in gameCountOfBestWinningMoves.positions:
                if gameBoardValues[position] == 0:
                    emptySlots.append(position)

        if len(emptySlots) > 0:
            print("Best winning moves: ", emptySlots)

            randomIdx = 0
            if len(emptySlots) > 1:
                randomIdx = getrandomnumber(0, len(emptySlots) - 1)

            return emptySlots[randomIdx]
    return None


# Find the best spot to place the next move
def findMove():
    # If the central spot is not taken yet, take it
    if gameBoard[1][1] == "-":
        return 1, 1

    """
	Find the best spot to place the next move in the following order
	1. Check for any potential winning spot if there is any line with count 6
	2. Check for any potential losing spot if there is any line with count -10
	3. If player starts: find all available slots on lines with count -5, if any slot appears multiple times, pick the one with highest occurrence, otherwise select randomly
	4. If game starts: find all available slots on lines with count 3, if any slot appears multiple times, pick the one with highest occurrence, otherwise select randomly
	5. Otherwise randomly pick a slot on a line with count 0
	"""
    bestMove = findBestMove(GAME_POINT * 2)
    if bestMove == None:
        bestMove = findBestMove(PLAYER_POINT * 2)
    if bestMove == None:
        if playerPiece == "x":
            bestMove = findBestMove(PLAYER_POINT)
        else:
            bestMove = findBestMove(GAME_POINT)
    if bestMove == None:
        bestMove = findBestMove(0)
    return bestMove


# Verify if the game is over
def updateGameState():
    global gameState

    # Check if there is a winner
    for countsInfo in gameCounts:
        if countsInfo.count == PLAYER_POINT * 3:
            gameState = "lost"
            return
        elif countsInfo.count == GAME_POINT * 3:
            gameState = "won"
            return

    # Otherwise verify if every line is already played by checking if the total count of the line is not 0, and not 0 when mod by 3 or (-)5
    # If yes, even the line is not fully played, the line is not worth playing
    # When all the lines meet this condition, the game is over without a winner
    if all(
        countsInfo.count != 0
        and abs(countsInfo.count) % 3 != 0
        and abs(countsInfo.count % 5) != 0
        for countsInfo in gameCounts
    ):
        gameState = "over"


# Record the move in the board with the corresponding score
def playMove(coordinates: tuple[int, int], gamePiece: Literal["x", "o"], points):
    gameBoard[coordinates[0]][coordinates[1]] = gamePiece
    gameBoardValues[coordinates] = points

    # Update counts info
    for gameCount in gameCounts:
        if coordinates in gameCount.positions:
            gameCount.count += points


def startGame():
    global gameState
    global playersTurn

    gameState = "playing"

    if gamePiece == "x":  # Game starts first
        playersTurn = False
    else:
        playersTurn = True

    while gameState == "playing":
        if playersTurn == True:
            playerMove = getPlayerMove()
            playMove(playerMove, playerPiece, PLAYER_POINT)
        else:
            gameMove = findMove()
            print("I play on: ", gameMove)
            playMove(gameMove, gamePiece, GAME_POINT)

        # Draw current board state
        drawBoard()

        # Switch turn
        playersTurn = not playersTurn

        # Check if there is winner
        updateGameState()
        time.sleep(1)

    if gameState == "won":
        print("You have lost")
    elif gameState == "lost":
        print("You have won")
    else:
        print("Game is over without a winner")


def main():
    global playerPiece
    global gamePiece

    input(
        "Welcome to tic tac toe game. Let's start by deciding who plays first. Please draw a random number by pressing any key. The person who draws bigger number would start first with the token 'x'."
    )
    playerDrawNum = getrandomnumber()
    print("You have drawn", playerDrawNum)
    time.sleep(0.5)

    gameDrawNum = getrandomnumber()
    while playerDrawNum == gameDrawNum:
        gameDrawNum = getrandomnumber()
    print("I have drawn", gameDrawNum)
    time.sleep(0.5)

    if playerDrawNum > gameDrawNum:
        playerPiece = "x"
        gamePiece = "o"
        print("You will start. You will use the token ", playerPiece)
    else:
        playerPiece = "o"
        gamePiece = "x"
        print("I will start. You will use the token ", playerPiece)
    time.sleep(0.5)

    init()
    startGame()


if __name__ == "__main__":
    main()
