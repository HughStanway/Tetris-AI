#17426
from board import Direction, Rotation, Action
from random import Random
from board import Shape
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError              

class AutoPlayer2(Player):
    def __init__(self, seed=None):
        self.random = Random.seed
        self.blockCount = 0
        self.bombLeft = 5
        self.discardLeft = 10
    
    def columnHeight(self, board):
        columnHeight = [0,0,0,0,0,0,0,0,0,0]
        for x in range(10):
            for y in range(23, 0, -1):
                if (x, y) in board.cells:
                    columnHeight[x] = (24 - y)
        
        return columnHeight

    def heightOfTowers(self, board):
        totalHeight = sum(self.columnHeight(board))
        return totalHeight

    def areThereGaps(self, board):
        columnHeight = self.columnHeight(board)
        gaps = [0,0,0,0,0,0,0,0,0,0]
        
        for x in range(10):
            for y in range((24 - columnHeight[x]), 24):
                if (x,y) in board.cells:
                    pass
                else:
                    gaps[x] += 1
        
        return sum(gaps)

    def completeLines(self, board, originalScore):
        score = board.score
        differenceInScore = score - originalScore

        if differenceInScore >= 25:
            return 1
        elif differenceInScore >= 100:
            return 10
        elif differenceInScore >= 400:
            return 50
        elif differenceInScore >= 1600:
            return 1000000
        else:
            return 0

    def bumpinessOfTower(self, board):
        columnHeight = self.columnHeight(board)
        bumpiness = 0

        for x in range(9):
            bumpiness += abs((columnHeight[x] - columnHeight[x + 1]))

        return bumpiness
    
    def stopFallingInEndCollumn(self, board, originalScore):
        x = 9
        for y in range(24):
            if (x,y) in board.cells:
                return -10
        return 0
    
    def stopFallingInEndCollumn2(self, board):
        x = 9
        for y in range(24):
            if (x,y) in board.cells:
                return -10000000
        return 0

    def averageHeight(self, board):
        columnHeight = self.columnHeight(board)
        
        return sum(columnHeight) / 10
    
    def dips(self, board):
        columnHeightMax = max(self.columnHeight(board))
        columnHeight = self.columnHeight(board)
        dips = [0,0,0,0,0,0,0,0,0,0]
        for x in range(10):
            for y in range(columnHeightMax, columnHeight[x]):
                if (x,y) not in board.cells:
                    dips[x] += 1
        
        maxDip = sum(dips)

        return maxDip
    
    def scoreBoard(self, board, oldScore):
        totalHeight = self.heightOfTowers(board) * -0.5
        gaps = self.areThereGaps(board) * -5
        bumpiness = self.bumpinessOfTower(board) * -0.18
        completeLines = self.completeLines(board, oldScore) * 1.3
        averageHeight = self.averageHeight(board) * -0.1
        stopLastColumn = self.stopFallingInEndCollumn(board, oldScore) * 1
        stopLastColumn2 = self.stopFallingInEndCollumn2(board)
        dips = self.dips(board) * -4

        return  completeLines + gaps + bumpiness + totalHeight + stopLastColumn + dips

    def choose_action(self, board):
        highScore = -99999
        originalScore = board.score
        columnHeight = self.columnHeight(board)
        self.blockCount += 1
        
        for rotation in range(4):
            for position in range(-5,5):
                sandbox = board.clone()
                orderOfReturn = []
                
                if max(columnHeight) > 20 and self.bombLeft > 0:
                    self.bombLeft -= 1
                    sandbox.move(Action.Bomb)
                    orderOfReturn.append(Action.Bomb)
                try:
                    if sandbox.next.shape == Shape.I and sandbox.falling.shape != Shape.I and (columnHeight[8] - columnHeight[9]) >= 4 and self.discardLeft > 0:
                        self.discardLeft -= 1
                        sandbox.move(Action.Discard)
                        orderOfReturn.append(Action.Discard)
                        for x in range(4):
                            orderOfReturn.append(Direction.Right)
                            sandbox.move(Direction.Right)
                        orderOfReturn.append(Direction.Drop)
                        sandbox.move(Direction.Drop)
                        return orderOfReturn
                except:
                    pass
                
                if sandbox.falling.shape == Shape.I and columnHeight[9] == 0:
                    for x in range(4):
                        orderOfReturn.append(Direction.Right)
                        sandbox.move(Direction.Right)
                    orderOfReturn.append(Direction.Drop)
                    sandbox.move(Direction.Drop)
                    return orderOfReturn
                
                try:
                    for x in range(rotation):
                        sandbox.rotate(Rotation.Clockwise)
                        orderOfReturn.append(Rotation.Clockwise)
                    
                    if position < 0:
                        for x in range(abs(position)):
                            sandbox.move(Direction.Left)
                            orderOfReturn.append(Direction.Left)
                    
                    elif position > 0:
                        for x in range(abs(position)):
                            sandbox.move(Direction.Right)
                            orderOfReturn.append(Direction.Right)

                    sandbox.move(Direction.Drop)
                    orderOfReturn.append(Direction.Drop)
                    
                    for nextRotation in range(4):
                        for nextPosition in range(-5,5):
                            sandboxClone = sandbox.clone()
                            
                            for x in range(nextRotation):
                                sandboxClone.rotate(Rotation.Clockwise)
                            
                            if nextPosition < 0:
                                for x in range(abs(nextPosition)):
                                    sandboxClone.move(Direction.Left)
                            
                            elif nextPosition > 0:
                                for x in range(abs(nextPosition)):
                                    sandboxClone.move(Direction.Left)

                            sandboxClone.move(Direction.Drop)
                        
                            if self.scoreBoard(sandboxClone, originalScore) > highScore:
                                highScore = self.scoreBoard(sandboxClone, originalScore)
                                finalReturn = orderOfReturn 
                        
                except:
                    pass
        try:
            return finalReturn
        except:
            pass

SelectedPlayer = AutoPlayer2



