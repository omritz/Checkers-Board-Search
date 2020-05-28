import random as random
import copy as copy
import math
import numpy as np
import sys

# This script contains 5 Algorithms to search a path from a Starting board, 
# according to the rules of Checkers, to a goal board.
# you can simply insert the boards under this lines or while runing the main.



startBoard = [[1,0,1,0,1,0],
              [0,0,0,1,0,1],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [1,0,0,0,0,0],
              [0,0,0,0,0,0]]

goalBoard = [[1,0,1,0,1,0],
             [0,0,0,1,0,0],
             [0,0,0,0,1,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0]]


def makeBoard(b):
    ''' Preparing The board for printing  '''
    board = []
    for r in range(7):
        brow = []
        for c in range(7):
            if r == c == 0:
                 brow.append('# ')   
            elif r == 0:
                 brow.append(str(c))
            elif c == 0:
                 brow.append(str(r)+':')
            else:
                 brow.append(' ')
        board.append(brow)
    for i in range(6):
        for j in range(6):
            if b[i][j] == 1 or b[i][j] == 2 :
                board[i+1][j+1]='*'
    return board

def printBoard(b):
    ''' Print each row of the board '''
    for row in b:
        print (' '.join(row))

def initBoard(b1, b2):
    '''Initialized the board for the huristic score'''
    tempBoard = [[0 for x in range(6)] for y in range(6)] 
    for i in range(6):
        for j in range(6):
            if b1[i][j] == b2[i][j] == 1:
                tempBoard[i][j] = 2 # thers is one and it should be there
            if b1[i][j] == 1 and b2[i][j] == 0:
                tempBoard[i][j] = 1 # thers is one and it shouldnt be there
            if b1[i][j] == 0 and b2[i][j] == 1:
                tempBoard[i][j] = 3 # there isnt one and it should be there
    return tempBoard

def printMyWay(listOfBoards,sBoard, gBoard):
    '''Print the final path '''
    c = 0
    for b in listOfBoards:
        c += 1
        output = "Board " + str(c)
        if (np.array_equal(b, sBoard)):
            print(output + " (starting position):")
        elif (np.array_equal(b, gBoard)):
            print (output + " (goal position):")
        else:
            print(output+ ":")
        printBoard(makeBoard(b))
        print ("-----") 

def printMyWayDetail(listOfBoards,sBoard, gBoard):
    '''Print the final path with details '''
    c = 0
    for b in listOfBoards:
        c += 1
        output = "Board " + str(c) + " heuristic value = " + str(b[1])
        if (np.array_equal(b[0], sBoard)):
            print(output + " (starting position):")
        elif (np.array_equal(b[0], gBoard)):
            print (output + " (goal position):")
        else:
            print(output+ ":")
        printBoard(makeBoard(b[0]))
        print ("-----") 

def printBag(bag, counter, key):
    ''' Print each bag in locl beam search '''
    c = 0
    for b in bag:
        c += 1
        output = "Board " + key + " in Bag, level " + str(counter)
        print(output+ ":")
        printBoard(makeBoard(b))
        print ("-----")


def score(t):
    ''' Huristic score for each board '''
    ones = []
    threes = []
    twos = 0
    target = 0
    tempScore = 0
    for i in range(6):
        for j in range(6):
            if goalBoard[i][j] == 1:
                target += 1
    for i in range(6):
        for j in range(6):
            if t[i][j] == 1:
                ones.append([i,j])
            if t[i][j] == 3:
                threes.append([i,j])
            if t[i][j] == 2:
                twos +=1               
    if len(ones) == len(threes) != 0:
        for i in range(len(ones)):
            if (threes[i][0]<=ones[i][0]):
                return 50
            tempScore += (threes[i][0] - ones[i][0])
    elif  len(ones) == len(threes) == 0:
        if twos == target:
            return 0
        else:
            return 50     
    else:
        if not ones:
            return 50
        if len(ones) < len(threes):
            return 50    
        if(len(threes) == 0):
            for i in range(len(ones)):        
                tempScore += (6 - ones[i][0])
        else:    
            for i in range(len(ones)-len(threes), len(ones)):        
                tempScore += (6 - ones[i][0])
            if len(ones) < len(threes):
                return 50       
            for i in range(len(threes)):
                if (threes[i][0]<=ones[i][0]):
                    return 50    
                tempScore += (threes[i][0] - ones[i][0])
        
    return tempScore

def isLegal(i, j, temp): 
    ''' Check if step is legal '''
    if i == 6:
        return True
    if j >= 0 and j < 6 and i < 6  and temp[i][j] != 1:
        return True
    else:
        return False


def makeMove(temp, current, restart):
    ''' Get the next state with random steps '''
    noMove = 0 
    x = 0
    if(restart != 0):
        x = random.random()
    if(current[0] != [0,0]):    
        if current[0][1] == 5:
            current[0][1] = 0
            current[0][0] += 1
        else:
            current[0][1] += 1
    for i in range(current[0][0], 6):    
        for j in range(current[0][1],6):
            current[0][1] = 0
            if temp[i][j] == 1:
                if i == 5:
                    temp[i][j] = 0
                    return temp 
                if(isLegal(i+1, j+1, temp) and temp[i+1][j+1] != 2 and x <= 0.5 ):
                    current.pop()
                    current.append([i,j])
                    temp[i][j] = 0
                    if(temp[i+1][j+1] != 3):
                        temp[i+1][j+1] = 1
                    else:
                        temp[i+1][j+1] = 2       
                    return temp
                elif(isLegal(i+1, j-1, temp) and temp[i+1][j-1] != 2):   
                    temp[i][j] = 0
                    current.pop()
                    current.append([i,j])
                    if(temp[i+1][j-1] != 3):
                        temp[i+1][j-1] = 1
                    else:
                        temp[i+1][j-1] = 2  
                    return temp
                elif isLegal(i+1, j+1, temp) and temp[i+1][j+1] == 2 and x <= 0.5:
                    if isLegal(i+2, j, temp):
                        current.pop()
                        current.append([i,j])                        
                        if i == 4:
                            pass
                        elif(temp[i+2][j] != 3 != 2):
                            temp[i+2][j] = 1
                        else:
                            temp[i+2][j] = 2
                        temp[i+1][j+1] = 0          
                        return temp
                    elif isLegal(i+2, j+2, temp):
                        current.pop()
                        current.append([i,j])
                        if i == 4:
                            pass
                        elif(temp[i+2][j+2] != 3 != 2):
                            temp[i+2][j+2] = 1
                        else:
                            temp[i+2][j+2] = 2
                        temp[i+1][j+1] = 0    
                        return temp
                elif isLegal(i+1, j-1, temp) and temp[i+1][j-1] == 2:
                    if isLegal(i+2, j, temp):
                        current.pop()
                        current.append([i,j])
                        if i == 4:
                            pass
                        elif(temp[i+2][j] != 3 != 2):
                            temp[i+2][j] = 1
                        else:
                            temp[i+2][j] = 2
                        temp[i+1][j-1] = 0    
                        return temp
                    elif isLegal(i+2, j-2, temp):
                        current.pop()
                        current.append([i,j])
                        if i == 4:
                            pass
                        elif(temp[i+2][j-2] != 3 != 2):
                            temp[i+2][j-2] = 1
                        else:
                            temp[i+2][j-2] = 2
                        temp[i+1][j-1] = 0    
                        return temp   
            
    current.pop()
    current.append([5,5])               
    return None

def hillClimbing(b1, b2):
    ''' Hill climbing search algorithm '''
    restartCounter = 0
    boards = []
    minS=50
    while restartCounter != 5 and minS !=0:
        board = initBoard(b1, b2)
        temp = copy.deepcopy(board)
        boards.append(copy.deepcopy(board))
        minS = score(board)
        S = 50
        while minS != 0:
            currnetCheck = [[0,0]]
            while S >= minS and currnetCheck != [[5,5]]:
                temp = makeMove(copy.deepcopy(board), currnetCheck, restartCounter)
                if not temp:
                    S = 50
                else:    
                    S = score(temp)
            if S == 50:
                restartCounter +=1
                break
                if restartCounter == 5:
                    break
            if (S < minS):
                board = copy.deepcopy(temp)
                minS = S
                if minS == 0:
                    boards.append(copy.deepcopy(board)) 
                    break
                else:
                    boards.append(copy.deepcopy(board)) 
                                     
    printMyWay(boards,initBoard(b1, b2),initBoard(b2, b2))               
    if minS != 0:
        print("No path Found")        

    

def SA(b1, b2, isDetail):
    ''' Simulated annealing search algorithm '''
    T = 50
    boards = []
    badBoards = []
    board = initBoard(b1, b2)
    temp = copy.deepcopy(board)
    boards.append(copy.deepcopy(temp))
    minS = score(temp)
    S = 50
    if minS == 0:
        printMyWay(boards,initBoard(b1, b2),initBoard(b2, b2))
    while T >= 1 and minS != 0:
        currnetCheck = [[0,0]]
        temp = makeMove(copy.deepcopy(temp),currnetCheck, 1)
        if not temp:
            S = 50
            temp = copy.deepcopy(board)
            boards.append(copy.deepcopy(temp))
        else:
            S = score(temp)
        if minS - S > 0:
            minS = S
            boards.append(copy.deepcopy(temp))
            if minS == 0:
                printMyWay(boards,initBoard(b1, b2),initBoard(b2, b2))    
                break       
        else:
            prob = math.exp((minS - S)/T)    
            x = random.random()
            if prob > x:
                boards.append(copy.deepcopy(temp)) 
            else:
                badBoards.append(copy.deepcopy(temp))
        T = T - T*(1/(minS+S)) # Cooling function
    if isDetail:
        a = boards + badBoards
        printMyWay(a,initBoard(b1, b2),initBoard(b2, b2))                 
    if minS != 0:
        printMyWay(boards,initBoard(b1, b2),initBoard(b2, b2))
        print("No path found.")



def bestBag(board):
    ''' Return the 3 legal boards '''
    minS = score(board)
    Bag = []
    S = 50
    kCounter = 0  
    currnetCheck = [[0,0]] 
    while kCounter != 3:
        temp = makeMove(copy.deepcopy(board), currnetCheck, 1 )
        if not temp:
            S = 50
            kCounter += 1
        else:    
            S = score(temp)
        if S < minS:
            Bag.append(copy.deepcopy(temp))
            kCounter += 1
    return Bag        

def localBeam(b1, b2, isDetail):
    ''' Local beam search algorithm (beam = 3) '''
    boradBag = []
    temp = []
    final= {'1': [], '2': [], '3': []}
    finalKey = '1'
    counter = 0
    board = initBoard(b1, b2)
    minS = score(board)
    S = 50
    boradBag = bestBag(copy.deepcopy(board))
    for key, value in final.items():
        value.append(copy.deepcopy(board))    
    while minS != 0 and counter != 100: 
        for key, value in final.items():
            boradBag = bestBag(copy.deepcopy(value[-1]))
            for b in boradBag:
                S = score(b)
                if S <= minS:
                    minS = S
                    temp.append(b)
                    if minS == 0:
                        finalKey = key
                        break
            if temp:        
                final[key].append(temp[np.random.randint(0,len(temp))])
                temp.clear()
            if isDetail:
                printBag(boradBag, counter, key)
            boradBag.clear()
        counter += 1          
    if minS == 0:
        printMyWay(final[finalKey],initBoard(b1, b2),initBoard(b2, b2))
    else:
        printMyWay(final[finalKey],initBoard(b1, b2),initBoard(b2, b2))
        print("No path Found.")        

def reproduce(dad, mom):
    ''' Create new board from two legal boards 
        by chosen random index from each board '''
    child = [[0 for x in range(6)] for y in range(6)]
    d1 = []
    m1 = []
    for r in range(len(dad)):
        for c in range(len(dad[r])):
            if dad[r][c] == 1:
                d1.append([r,c])
    for r in range(len(mom)):
        for c in range(len(mom[r])):
            if mom[r][c] == 1:
                m1.append([r,c])
    for r in range(len(dad)):
        for c in range(len(dad[r])):
            if dad[r][c] == mom[r][c] == 2 or dad[r][c] == mom[r][c] == 3:
                child[r][c] = dad[r][c]
    if len(d1) == len(m1):
        for i in range(len(d1)):
            x=random.random()
            if x <= 0.5:
                child[d1[i][0]][d1[i][1]] = 1
            else: 
                child[m1[i][0]][m1[i][1]] = 1
    elif len(d1) > len(m1):
        for i in range(len(m1)):
            x=random.random()
            if x <= 0.5:
                child[d1[i][0]][d1[i][1]] = 1
            else: 
                child[m1[i][0]][m1[i][1]] = 1
        for i in range(len(m1),len(d1)):        
            child[d1[i][0]][d1[i][1]] = 1
    else:
        for i in range(len(d1)):
            x=random.random()
            if x <= 0.5:
                child[d1[i][0]][d1[i][1]] = 1
            else: 
                child[m1[i][0]][m1[i][1]] = 1
        for i in range(len(d1),len(m1)):        
            child[m1[i][0]][m1[i][1]] = 1
                        
    return child


def GeneticAlgorithm(b1, b2, isDetail):
    ''' Genetic search limited for 100 generations '''
    board = initBoard(b1, b2)
    minS = score(board)
    S = 50
    dad = [] 
    mom = []
    child=[]
    population = []
    final = []
    currnetCheck = [[0,0]]
    final.append(copy.deepcopy(board))
    population.append(copy.deepcopy(board))
    for i in range(100):
        while not dad or not mom:
            print('dont have dad and mom yet!!!')
            dad = makeMove(copy.deepcopy(board), [[0,0]], 1 )
            mom = makeMove(copy.deepcopy(board), [[0,0]], 1 )
        child =  reproduce(dad, mom)
        if score(child) == 50:
            print("broken child ", child)
        elif score(child) == 0:
            final.append(copy.deepcopy(child))
            population.append(copy.deepcopy(child))    
            break
        else:
            population.append(copy.deepcopy(child))    
            x=random.random()
            if x > 0.5:
                board = copy.deepcopy(child)
                final.append(copy.deepcopy(child))
        dad.clear()
        mom.clear()
    if isDetail:
        printMyWay(population,initBoard(b1, b2),initBoard(b2, b2))
    else:
        printMyWay(final,initBoard(b1, b2),initBoard(b2, b2))
    if score(child) != 0:
        print("No Path Found")

def findFrontier(b ,goal):
    ''' Return an array of all the next states sorted by score '''
    boards = []
    for r in range(len(b)):
        for c in range (len(b[r])):
            if b[r][c] == 1:
                board1 = copy.deepcopy(b)
                board2 = copy.deepcopy(b)
                if isLegal(r+1,c+1,board1):
                    board1[r][c] = 0
                    if r!=5:
                        board1[r+1][c+1] = 1
                    if r == 5:
                        pass 
                if isLegal(r+1,c-1,board2):
                    board2[r][c] = 0
                    if r!=5:
                        board2[r+1][c-1] = 1
                    if r ==5:
                        pass        
                boards.append(initBoard(copy.deepcopy(board1),goal))
                boards.append(initBoard(copy.deepcopy(board2),goal)) 
    boards.sort(key = score)
    return boards
    
def tempBoard(b):
    ''' initialized temp board '''
    temp = [[0 for x in range(6)] for y in range(6)] 
    for r in range(len(b)):
        for c in range (len(b[r])):
            if b[r][c] == 1 or b[r][c] == 2:
                temp[r][c] = 1
    return temp            

def AStar(b1, b2, isDetail):
    ''' A Star search algorithm  '''
    board = initBoard(b1, b2)
    minS = score(board)
    S = 50
    frontier = findFrontier(b1, b2)
    exploared=[]
    exploaredDetail=[]
    exploared.append(copy.deepcopy(board))
    exploaredDetail.append([copy.deepcopy(board),minS])
    finish = False
    while not finish:
        if not frontier:
            finish = True
            break
        if minS == 0:
            finish = True
            break
        S = score(frontier[0])
        if S < minS:
            minS = S
            exploared.append(copy.deepcopy(frontier[0]))
            exploaredDetail.append([copy.deepcopy(frontier[0]),minS]) 
        frontier = findFrontier(tempBoard(exploared[-1]), b2)
        print(frontier)
    if isDetail:
        printMyWayDetail(exploaredDetail, initBoard(b1, b2), initBoard(b2, b2))
    else:            
        printMyWay(exploared, initBoard(b1, b2), initBoard(b2, b2))


def findPlayPath(algNum, b1, b2, isDetail):
    if algNum == "1":
        hillClimbing(b1, b2)
    elif algNum == "2":     
        SA(b1, b2, isDetail) 
    elif algNum == "3":
        localBeam(b1, b2, isDetail)
    elif algNum == "4":
        GeneticAlgorithm(b1, b2, isDetail) 
    elif algNum == "5":
        AStar(b1, b2, isDetail)
    else:
        print("Illegal value, please insert value between 1-5!")
    
          


if  __name__ == "__main__":
 
    algNum = input("Please choose Search method(1-5): \n1. Hill climbing\n2. Simulated annealing\n3. Local beam\n4. Genetic\n5. A Star  ")
    ans =  input("Did you insert the boards in the top of the script (y/n)? ")
    if ans != 'y':
        print ("Please insert the starting board as array, space between each number (1 for * , 0 for empty cell) \nand press enter for the next row")
        a = [[0]*6 for _ in range(6)]
        for i in range(6):
            a[i] = [int(j) for j in input("Row "+ str(i+1) + ": ").strip().split(" ")]
        printBoard(makeBoard(a))
        ans = input("Do you confirm the board (y/n)? ")
        if ans == 'y':
            startBoard = copy.deepcopy(a)
        else:
            sys.exit(0)   
        print ("Please insert the goal board as array, space between each number (1 for * , 0 for empty cell) \nand press enter for the next row")    
        a = [[0]*6 for _ in range(6)]
        for i in range(6):
            a[i] = [int(j) for j in input("Row "+ str(i+1) + ": ").strip().split(" ")]
        printBoard(makeBoard(a))
        ans = input("Do you confirm the board (y/n)? ")
        if ans == 'y':
            goalBoard = copy.deepcopy(a)  
        else:
            sys.exit(0)              
    isDetail = input("Do you want Detail output (y/n)?\n ")
    if isDetail == 'y':
        isDetail = True
    else:
        isDetail = False    
    findPlayPath(algNum, startBoard, goalBoard, isDetail)


   





