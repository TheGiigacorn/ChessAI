# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
import random
import time
# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Chess. """

    @property
    def game(self) -> 'games.chess.game.Game':
        """games.chess.game.Game: The reference to the Game instance this AI is playing.
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self) -> 'games.chess.player.Player':
        """games.chess.player.Player: The reference to the Player this AI controls in the Game.
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self) -> str:
        """This is the name you send to the server so your AI will control the player named this string.

        Returns:
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Chess Python Player" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self) -> None:
        """This is called once the game starts and your AI knows its player and game. You can initialize your AI here.
        """
        self.pointvalue = [5, 9, -1, 1, 3, 3]
        # 15 minute time limit
        self.timeleft = 900
        self.seconds = time.time()
        
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        # <<-- /Creer-Merge: start -->>

    def game_updated(self) -> None:
        """This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        timepassed = time.time() - self.seconds
        self.timeleft = self.timeleft - timepassed 
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won: bool, reason: str) -> None:
        """This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def make_move(self) -> str:
        """This is called every time it is this AI.player's turn to make a move.

        Returns:
            str: A string in Universal Chess Inferface (UCI) or Standard Algebraic Notation (SAN) formatting for the move you want to make. If the move is invalid or not properly formatted you will lose the game.
        """
        

        #create a 8 x 8 board to simulate game
        board = [[' ' for i in range(8)] for j in range(8)]
        nums = ['1','2','3','4','5','6','7','8']
        validmoves = []
        wcheckedmoves = []
        bcheckedmoves = []
        castlelist = []
        pieceworth = [5, 9, -1, 1, 3, 3]
        splitfen = self.game.fen.split(' ',1)

        castleinfo = splitfen[1].split(' ')[1]
        for i in range(len(castleinfo)):
            castlelist.append(castleinfo[i])

        passantinfo = splitfen[1].split(' ')[2]

        #this variable holds all board information
        rowinfo = splitfen[0].split("/")
    
        side = splitfen[1][0]
        #parses rowinfo and correcly assembles the board
        for i in range(len(rowinfo)):
            temp = 0
            for j in range(len(rowinfo[i])):
                if rowinfo[i][j] == '8':
                    continue
                if rowinfo[i][j] in nums:
                    temp = temp + int(rowinfo[i][j]) - 1
                    temp+=1
                else:
                    board[i][temp] = rowinfo[i][j]
                    temp+=1

        
        #contains functionality for white side
        wcheckedmoves = self.moveWhite(board, wcheckedmoves, validmoves, castlelist, passantinfo)




        #black side functionality, everything is very similar to white side except for piece lists and pawn funtionality
        validmoves = []
        bcheckedmoves = self.moveblack(board, bcheckedmoves, validmoves, castlelist, passantinfo)

        self.game.print()

        #picks random number in range of move list length
        '''rand = random.randrange(0,len(checkedmoves))'''
                    

        # <<-- Creer-Merge: makeMove -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for makeMove
        #return "d2d4"
    

        #depth limit for itterative deepening minimax
        

        #get start time before turns start
        t0 = time.time()
        timelimit = t0 + self.timeleft*0.022

        #calculate time it takes to move at depth 0
        besta = self.maxChoice(board, wcheckedmoves, bcheckedmoves, 0, side, castlelist, passantinfo)
        t1 = time.time()

        depth = 4
        for j in range(depth):
            bestmoveindx = self.maxChoice(board, wcheckedmoves, bcheckedmoves, depth, side, castlelist, passantinfo)
            t2 = time.time()

            timeratio = (t2-t1)/(t1-t0)
            timepredict = (t2-t1)*timeratio

            t0 = t1
            t1 = t2
            #if next turn will take more time then time left they we use whatever move was already found
            if t2 + timepredict > timelimit:
                break

        
        if side == 'w':
            move = wcheckedmoves[bestmoveindx]
        if side == 'b':
            move = bcheckedmoves[bestmoveindx]
        tmpi = 8-int(move[1])
        tmpj = int(ord(move[0])) - 97
        tmpy = 8-int(move[3])
        tmpx = int(ord(move[2])) - 97
        landloc = board[tmpy][tmpx]
        pickedpiece = board[tmpi][tmpj]
        if landloc == ' ':
            taken = '-'
        if landloc != ' ':
            taken = 'x'

        print(pickedpiece,move[:2],taken,move[2:],sep='')
        if side == 'w':
            return wcheckedmoves[bestmoveindx]
        if side == 'b':
            return bcheckedmoves[bestmoveindx]

        # <<-- /Creer-Merge: makeMove -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>



    def moveWhite(self, board, wcheckedmoves, validmoves, castlelist, passantinfo):
        #all friendly pieces
        piecelist = ['R','Q','K','P','B','N']
        #all enemy pieces
        enemypiece = ['r','q','k','p','b','n']
        #bool that shows if king is in check
        check = False
        #list with locations of where peices can move to break check
        saveKing = []
        #validmoves for the king
        kingmoves = []
        safemoves = []


            
        #searches the board for king
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'K':

                    #finds out if king is in check and if he is which spaces need to be covered
                    check, saveKing = self.kingCheck(board, i, j, enemypiece, piecelist)
                        
                    board[i][j] = ' '
                    #simulates kings moves to check which ones are valid
                    self.checkKingMoves(board, i, j, enemypiece, piecelist, kingmoves)


                    #checks for option to castle and if it is possible adds to valid list
                    if not check:
                        if j+2 == 6:
                            if 'K' in castlelist and board[i][j+1] == ' ' and board[i][j+2] == ' ':
                                castlecheck1, hold = self.kingCheck(board, i, j+1, enemypiece, piecelist)
                                castlecheck2, hold = self.kingCheck(board, i, j+2, enemypiece, piecelist)
                                if not castlecheck1 and not castlecheck2:
                                    validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j+2) + str(8-i)))
                        if j-3 == 1:
                            if 'Q' in castlelist and board[i][j-1] == ' ' and board[i][j-2] == ' ' and board[i][j-3] == ' ':
                                castlecheck3, hold = self.kingCheck(board, i, j-1, enemypiece, piecelist)
                                castlecheck4, hold = self.kingCheck(board, i, j-2, enemypiece, piecelist)
                                castlecheck5, hold = self.kingCheck(board, i, j-3, enemypiece, piecelist)
                                if not castlecheck3 and not castlecheck4 and not castlecheck5:
                                    validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j-2) + str(8-i)))
                    board[i][j] = 'K'
                        
                    #vaiables to simulate other moves later
                    kingi = i
                    kingj = j


        #searches board for rest of peices now that we have state of king
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] in piecelist:
                            

                    #white side pawn functionality
                    if board[i][j] == 'P':
                        #move 2 space forward
                        if i == 6 and board[4][j] == ' ' and board[5][j] == ' ':
                            numseq = str(j) + str(8-i) + str(j) + str((8-i)+2)
                            validmoves.append(self.uciConvert(numseq))

                        #move 1 space forward
                        if i-1 >= 0:
                            if board[i-1][j] == ' ':
                                numseq = str(j) + str(8-i) + str(j) + str((8-i)+1)
                                validmoves.append(self.uciConvert(numseq))

                        #take out piece
                        if j==0 and i-1 <= 0:
                            if board[i-1][j+1] in enemypiece:
                                numseq = str(j) + str(8-i) + str(j+1) + str(8-i+1)
                                validmoves.append(self.uciConvert(numseq))
                        if j!=0 and j!=7 and i-1 <= 0:
                            if board[i-1][j+1] in enemypiece:
                                numseq = str(j) + str(8-i) + str(j+1) + str(8-i+1)
                                validmoves.append(self.uciConvert(numseq))
                            if board[i-1][j-1] in enemypiece:
                                numseq = str(j) + str(8-i) + str(j-1) + str(8-i+1)
                                validmoves.append(self.uciConvert(numseq))
                        if j==7 and i-1 <= 0:
                            if board[i-1][j-1] in enemypiece:
                                numseq = str(j) + str(8-i) + str(j-1) + str(8-i+1)
                                validmoves.append(self.uciConvert(numseq))
                        #en passant
                        if j+1 <= 7:
                            if self.uciConvert(str(j+1) + str(8-i+1)) in passantinfo:
                                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j+1) + str(8-i+1)))
                        if j-1 >= 0:
                            if self.uciConvert(str(j-1) + str(8-i+1)) in passantinfo:
                                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j-1) + str(8-i+1)))


                    #white side rook movement
                    if board[i][j] == 'R':
                        self.fileMovement(board, i, j, validmoves, enemypiece, piecelist)
                        self.rankMovement(board, i, j, validmoves, enemypiece, piecelist)
                    if board[i][j] == 'B':
                        self.diagonalMovement(board, i , j, validmoves, enemypiece, piecelist)
                    if board[i][j] == 'Q':
                        self.fileMovement(board, i, j, validmoves, enemypiece, piecelist)
                        self.rankMovement(board, i, j, validmoves, enemypiece, piecelist)
                        self.diagonalMovement(board, i, j, validmoves, enemypiece, piecelist)
                    if board[i][j] == 'N':
                        self.knightMovement(board, i, j, enemypiece, piecelist, validmoves)

        #loops through all "valid moves"
        for s in validmoves:
            #checks each move in valid moves and if it endagers the king it is removed from the list
            safe = self.simulated(board, s, kingi, kingj, enemypiece, piecelist)
            if safe:
                safemoves.append(s)

        #loops through all safe moves
        for c in safemoves:
            #if the king is in check weeds out moves that will not save the king
            if check:
                if c[2:] in saveKing:
                    wcheckedmoves.append(c)
            if not check:
                wcheckedmoves.append(c)
        #print(wcheckedmoves, ' ', check)
        #adds valid king moves onto list with other valid moves
        wcheckedmoves = wcheckedmoves + kingmoves
        return wcheckedmoves



    def moveblack(self, board, bcheckedmoves, validmoves, castlelist, passantinfo):
        #friendly peices
        piecelist = ['r','q','k','p','b','n']
        #enemy pieces
        enemypiece = ['R','Q','K','P','B','N']
        #bool for if king is in check
        check = False
        saveKing = []
        kingmoves = []
        safemoves = []

        #same as white side, searches for king and makes sure he isnt in check
        #print(board)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'k':
                    check, saveKing = self.kingCheck(board, i, j, enemypiece, piecelist)
                    board[i][j] = ' '
                    self.checkKingMoves(board, i, j, enemypiece, piecelist, kingmoves)


                    #checks for option to castle and if it is possible adds to valid list
                    if not check:
                        if j+2 == 6:
                            if 'k' in castlelist and board[i][j+1] == ' ' and board[i][j+2] == ' ':
                                castlecheck1, hold = self.kingCheck(board, i, j+1, enemypiece, piecelist)
                                castlecheck2, hold = self.kingCheck(board, i, j+2, enemypiece, piecelist)
                                if not castlecheck1 and not castlecheck2:
                                    validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j+2) + str(8-i)))
                        if j-3 == 1:
                            if  'q' in castlelist and board[i][j-1] == ' ' and board[i][j-2] == ' ' and board[i][j-3] == ' ':
                                castlecheck3, hold = self.kingCheck(board, i, j-1, enemypiece, piecelist)
                                castlecheck4, hold = self.kingCheck(board, i, j-2, enemypiece, piecelist)
                                castlecheck5, hold = self.kingCheck(board, i, j-3, enemypiece, piecelist)
                                if not castlecheck3 and not castlecheck4 and not castlecheck5:
                                    validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j-2) + str(8-i)))

                    board[i][j] = 'k'
                    kingi = i
                    kingj = j

        #checks for rest of black pieces
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] in piecelist:


                    #white side pawn functionality
                    if board[i][j] == 'p':
                        #move piece forward 2
                        if i == 1 and board[2][j] == ' ' and board[3][j] == ' ':
                            numseq = str(j) + str(8-i) + str(j) + str((8-i)-2)
                            validmoves.append(self.uciConvert(numseq))
                        #move piece forward 1
                        if i+1 <= 7:
                            if board[i+1][j] == ' ':
                                numseq = str(j) + str(8-i) + str(j) + str((8-i)-1)
                                validmoves.append(self.uciConvert(numseq))
                        #take enemy piece out
                        if j==0 and i+1 <= 7:
                            if board[i+1][j+1] in enemypiece:
                                numseq = str(j) + str(8-i) + str(j+1) + str(8-i-1)
                                validmoves.append(self.uciConvert(numseq))
                        if j!=0 and j!=7 and i+1 <= 7:
                            if board[i+1][j+1] in enemypiece:
                                numseq = str(j) + str(8-i) + str(j+1) + str(8-i-1)
                                validmoves.append(self.uciConvert(numseq))
                            if board[i+1][j-1] in enemypiece:
                                numseq = str(j) + str(8-i) + str(j-1) + str(8-i-1)
                                validmoves.append(self.uciConvert(numseq))
                        if j==7 and i+1 <= 7:
                            if board[i+1][j-1] in enemypiece:
                                numseq = str(j) + str(8-i) + str(j-1) + str(8-i-1)
                                validmoves.append(self.uciConvert(numseq))
                        #en passant
                        if j+1 <= 7:
                            if self.uciConvert(str(j+1) + str(8-i-1)) in passantinfo:
                                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j+1) + str(8-i-1)))
                        if j-1 >= 0:
                            if self.uciConvert(str(j-1) + str(8-i-1)) in passantinfo:
                                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j-1) + str(8-i-1)))

                    #moves the rook
                    if board[i][j] == 'r':
                        self.fileMovement(board, i, j, validmoves, enemypiece, piecelist)
                        self.rankMovement(board, i, j, validmoves, enemypiece, piecelist)
                    #moves the bishop
                    if board[i][j] == 'b':
                        self.diagonalMovement(board, i, j, validmoves, enemypiece, piecelist)
                    #moves the queen
                    if board[i][j] == 'q':
                        self.fileMovement(board, i, j, validmoves, enemypiece, piecelist)
                        self.rankMovement(board, i, j, validmoves, enemypiece, piecelist)
                        self.diagonalMovement(board, i, j, validmoves, enemypiece, piecelist)
                    #moves the knight
                    if board[i][j] == 'n':
                        self.knightMovement(board, i, j, enemypiece, piecelist, validmoves)
            
            
        #takes "valid" moves and weeds out ones that endanger the king
        for s in validmoves:
            safe = self.simulated(board, s, kingi, kingj, enemypiece, piecelist)
            if safe:
                safemoves.append(s)

        #takes improved list and chenges it if king is in check to protect him
        for c in safemoves:
            if check:
                if c[2:] in saveKing:
                    bcheckedmoves.append(c)
            if not check:
                bcheckedmoves.append(c)
        #print(bcheckedmoves, ' ', check)
        bcheckedmoves = bcheckedmoves + kingmoves
        return bcheckedmoves

    #funciton that finds the cost for every valid move given to it and returns it
    def movecost(self, board, wcheckedmoves, bcheckedmoves, side):
        allypiece = ['r', 'q', 'k', 'p', 'b', 'n']
        enemypiece = ['','','','','','']
        costlist = []
        
        if side == 'w':
            #loop changes allypiece to be uppercase to work with kingCheck
            for i in range(len(allypiece)):
                enemypiece[i] = allypiece[i]
                allypiece[i] = allypiece[i].upper()
            #loops through all the possible whiteside moves
            for i in wcheckedmoves:
                
                cost = 0
                piece = i[:2]

                #comverts move back to numbers to be used and indices for the board
                tmpi = 8-int(piece[1])
                tmpj = int(ord(piece[0])) - 97
                currpiece = board[tmpi][tmpj]
                toland = i[2:]
                tmpx = 8-int(toland[1])
                tmpy = int(ord(toland[0])) - 97
                landspot = board[tmpx][tmpy]
                if landspot in enemypiece:
                    indx = enemypiece.index(landspot)
                    cost = cost + int(self.pointvalue[indx])
                #if pawn gets promoted add 9 points and subtract 1
                if currpiece == 'P' and tmpx == 0:
                    cost += 8

                #calls kingCheck to see if piece of current move will be in check after moving it
                unsafe, temp = self.kingCheck(board, tmpx, tmpy, enemypiece, allypiece)

                #if the move the piece takes can result in it being taken we reduce the point value of the move
                if unsafe:
                    indx = allypiece.index(currpiece)
                    cost = cost-int(self.pointvalue[indx])
                costlist.append(cost)

        #this checks side so only one list gets checked
        if side == 'b':
            #changes enemy piece charactes to uppercase
            for i in range(len(allypiece)):
                enemypiece[i] = allypiece[i].upper()
            #loops through all moves black can take
            for i in bcheckedmoves:
                cost = 0

                #converts move back to numbers to be able to use it as indices for the board
                piece = i[:2]
                tmpi = 8-int(piece[1])
                tmpj = int(ord(piece[0])) - 97
                currpiece = board[tmpi][tmpj]
                toland = i[2:]
                tmpx = 8-int(toland[1])
                tmpy = int(ord(toland[0])) - 97
                landspot = board[tmpx][tmpy]
                #adds points to move depinging on which piece it takes
                if landspot in enemypiece:
                    indx = enemypiece.index(landspot)
                    cost = cost + int(self.pointvalue[indx])

                #if pawn gets promoted 
                if currpiece == 'p' and tmpx == 7:
                    cost += 8

                #calls kingCheck to see if piece can be taken after move
                unsafe, temp = self.kingCheck(board, tmpx, tmpy, enemypiece, allypiece)

                #if the move is unsafe then we take points away
                if unsafe:
                    indx = allypiece.index(currpiece)
                    cost = cost-int(self.pointvalue[indx])
                costlist.append(cost)

        return costlist

    #moves piece on self made board to allow gamestate after said move
    def moveone(self, board, move):
        frmi = 8-int(move[1])
        frmj = int(ord(move[0])) - 97
        toi = 8-int(move[3])
        toj = int(ord(move[2])) - 97

        holder = board[frmi][frmj]
        board[frmi][frmj] = ' '
        board[toi][toj] = holder


    #----------------------------------maxChoice is the heuristic function-----------------------------#


    #takes in possible moves and returns the index of the best move possible
    def maxChoice(self, board, wcheckedmoves, bcheckedmoves, depth, side, castlelist, passantinfo):
        #defines values for alpha and beta pruning
        alpha = 999
        beta = -999
        #call movecost to find the costs of the current board state
        costs = self.movecost(board, wcheckedmoves, bcheckedmoves, side)
        besta = []
        boardtemp = [[' ' for i in range(8)] for j in range(8)]
        if side == 'w':
            #loop through all possible moves for white side
            for i in range(len(wcheckedmoves)):
                for r in range(len(board)):
                    for t in range(len(board[r])):
                        boardtemp[r][t] = board[r][t]
                #takes current move that is being analyzed and moves piece based on the move
                self.moveone(boardtemp, wcheckedmoves[i])

                #append all the point values of the possible moves onto list to pick the best one
                besta.append(self.minValue(costs[i], boardtemp, depth, side, castlelist, passantinfo, alpha, beta))

        #same functionality as above just for the black side
        if side == 'b':
            for i in range(len(bcheckedmoves)):
                for r in range(len(board)):
                    for t in range(len(board[r])):
                        boardtemp[r][t] = board[r][t]
                
                self.moveone(boardtemp, bcheckedmoves[i])

                besta.append(self.minValue(costs[i], boardtemp, depth, side, castlelist, passantinfo, alpha, beta))


        #if two moves share the best point value we will pick a random one to move to avoid tying due to repition rule
        if besta.count(max(besta)) > 1:
            indx = random.randrange(besta.count(max(besta)))
            bestindx = [i for i,n in enumerate(besta) if n == max(besta)][indx]
            return bestindx
        else:
            return besta.index(max(besta))


    #minvalue finds the max point value for the opposite side that is currently moving
    def minValue(self, cost, board, depth, side, castlelist, passantinfo, alpha, beta):
        v = cost
        enemies = ['r','q','k','p','b','n']
        friends = ['r','q','k','p','b','n']

        #checking if king is in check is the terminal state of the tree
        #checks to see if the enemy is in check and if they are we add points to move 
        if side == 'w':
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 'k':
                        kingfile = i
                        kingrank = j
            for t in range(len(enemies)):
                enemies[t] = enemies[t].upper()
            check, clist = self.kingCheck(board, kingfile, kingrank, enemies, friends)

        #also chaecks to seee if enemy is in check
        if side == 'b':
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 'K':
                        kingfile = i
                        kingrank = j
            for t in range(len(friends)):
                friends[t] = friends[t].upper()
            check, clist = self.kingCheck(board, kingfile, kingrank, enemies, friends)
        if check:
            return v+5

        #if depth is 0 we reutrn the current point value of the future moves
        if depth == 0:
            return v
    

        #find all possible moves for black side
        validmoves = []
        bcheckedmoves = []
        self.moveblack(board, bcheckedmoves, validmoves, castlelist, passantinfo)
        
        #find all possible moves for white side
        validmoves = []
        wcheckedmoves = []
        self.moveWhite(board, wcheckedmoves, validmoves, castlelist, passantinfo)
        
        #if it is whites turn and the move will create a stalemate and not a check then we take points away to detur this behavior
        if side == 'w':
            if bcheckedmoves == [] and not check:
                return v-5
            
            #gets costs for white moves
            costs = self.movecost(board, wcheckedmoves, bcheckedmoves, 'b')

        #same here exept for black side, we want to detur stalemates and go for checks
        if side == 'b':
            if wcheckedmoves == [] and not check:
                return v-5
            
            #gets costs for black moves
            costs = self.movecost(board, wcheckedmoves, bcheckedmoves, 'w')
    
        #subtract max cost because we want to take points away from the current player for making bad decisions
        v = v - max(costs)
        indx = costs.index(max(costs))
        
        #take the best move and move it on the board so that it can be passed to next function
        if side == 'w':
            self.moveone(board, bcheckedmoves[indx])
        if side == 'b':
            self.moveone(board, wcheckedmoves[indx])

        v = self.maxValue(v, board, depth-1, side, castlelist, passantinfo, alpha, beta)

        if v <= alpha:
            return v
        beta = min([v, beta])

        return v


    #this funciton takes in board state and returns max value move for current player
    def maxValue(self, cost, board, depth, side, castlelist, passantinfo, alpha, beta):
        v = cost
        enemies = ['r','q','k','p','b','n']
        friends = ['r','q','k','p','b','n']

        #checks terminal state just like in minvalue which is if the enemy is in check
        if side == 'w':
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 'k':
                        kingfile = i
                        kingrank = j
            for t in range(len(enemies)):
                enemies[t] = enemies[t].upper()
            check, clist = self.kingCheck(board, kingfile, kingrank, enemies, friends)
        if side == 'b':
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 'K':
                        kingfile = i
                        kingrank = j
            for t in range(len(friends)):
                friends[t] = friends[t].upper()
            check, clist = self.kingCheck(board, kingfile, kingrank, enemies, friends)
        if check:
            return v+5

        #checks if depth limit has been reached 
        if depth == 0:
            return v

        #creates possible moves for black side
        validmoves = []
        bcheckedmoves = []
        self.moveblack(board, bcheckedmoves, validmoves, castlelist, passantinfo)

        #creates possible moves for white side
        validmoves = []
        wcheckedmoves = []
        self.moveWhite(board, wcheckedmoves, validmoves, castlelist, passantinfo)
        if side == 'w':
            #checks if current side is in check due to move and takes points away if so
            if wcheckedmoves == []:
                return v-10
            #gets costs of white side moves of current board state
            costs = self.movecost(board, wcheckedmoves, bcheckedmoves, 'w')
        if side == 'b':
            #checks if current side in in check and takes points away if so
            if bcheckedmoves == []:
                return v-10
            #gets costs of black side moves of current board state
            costs = self.movecost(board, wcheckedmoves, bcheckedmoves, 'b')

        #adds max cost onto point value to maximize currents sides points
        v = v + max(costs)
        indx = costs.index(max(costs))

        if side == 'w':
            self.moveone(board, wcheckedmoves[indx])
        if side == 'b':
            self.moveone(board, bcheckedmoves[indx])
            
        v = self.minValue(v, board, depth-1, side, castlelist, passantinfo, alpha, beta)

        if v >= beta:
            return v
        alpha = max([v, alpha])
        
        return v




    #takes in a string of numbers and converts it to uci format and returns it as a string
    def uciConvert(self, toconvert) -> str:
        newstr = []
        for i in range(len(toconvert)):
            if i%2==0:
                #changes number to respective letter in alphabet
                change = chr(ord('`')+(int(toconvert[i]) + 1))
            else:
                change = toconvert[i]
            newstr.append(change)
        return ''.join(newstr)
        
    
    #takes uci format move and position of king and makes sure king will not be put in danger from the current move. If the move endangers the king returns False
    def simulated(self, board, s, kingi, kingj, enemies, friends) -> bool:
        safe = True
        #convert uci back to string of numbers which is used as indicies on the board
        frmi = 8-int(s[1])
        frmj = int(ord(s[0])) - 97
        toi = 8-int(s[3])
        toj = int(ord(s[2])) - 97

        holder = board[frmi][frmj]
        toholder = board[toi][toj]
        board[frmi][frmj] = ' '
        board[toi][toj] = holder

        #calls kingCheck to make sure simulated move doesnt put king in check
        check, save = self.kingCheck(board, kingi, kingj, enemies, friends)
        if check:
            safe = False

        #return board to original state
        board[frmi][frmj] = holder
        board[toi][toj] = toholder
        return safe


    #takes in a pieces location and moves it along the file that it is currently in
    def fileMovement(self, board, cfile, crank, validmoves, enemies, friends) -> None:
        #checks all spaces below the piece
        for r in range(cfile+1,8):
            #if it is a blank space that move is added to valid list
            if board[r][crank] == ' ':
                numseq = str(crank) + str(8-cfile) + str(crank) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
            #if it is an enemy piece move is added then we break becuase piece cannot move further
            if board[r][crank] in enemies:
                numseq = str(crank) + str(8-cfile) + str(crank) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                break
            #break because cannot pass or land on friendly piece
            if board[r][crank] in friends:
                break
        #file movement above the piece, all if statements are similar to those above
        for r in reversed(range(0,cfile)):
            if board[r][crank] == ' ':
                numseq = str(crank) + str(8-cfile) + str(crank) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
            if board[r][crank] in enemies:
                numseq = str(crank) + str(8-cfile) + str(crank) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                break
            if board[r][crank] in friends:
                break

    #takes in pieces location and mvoes it along the rank the it is currently in
    def rankMovement(self, board, cfile, crank, validmoves, enemies, friends) -> None:
        #checks all spaces to right of piece
        for r in range(crank,8):
            #if space is blank add to valid list
            if board[cfile][r] == ' ':
                numseq = str(crank) + str(8-cfile) + str(r) + str(8-cfile)
                validmoves.append(self.uciConvert(numseq))
            #if space has enemy add to valid list and stop search to right
            if board[cfile][r] in enemies:
                numseq = str(crank) + str(8-cfile) + str(r) + str(8-cfile)
                validmoves.append(self.uciConvert(numseq))
                break
            #if friendly piece stop search to right
            if board[cfile][r] in friends:
                break

        #checks all spaces to left of piece
        for r in reversed(range(0,crank)):
            #if space is blank add to valid list
            if board[cfile][r] == ' ':
                numseq = str(crank) + str(8-cfile) + str(r) + str(8-cfile)
                validmoves.append(self.uciConvert(numseq))
            #if space has enemy add to valid list and stop search to left
            if board[cfile][r] in enemies:
                numseq = str(crank) + str(8-cfile) + str(r) + str(8-cfile)
                validmoves.append(self.uciConvert(numseq))
                break
            #if space has friend stop search to left
            if board[cfile][r] in friends:
                break 

    #takes peices locaation and moves it diagonal to the space it is in
    def diagonalMovement(self, board, cfile, crank, validmoves, enemies, friends) -> None:
        #conter numbers to simulate movement along the rank
        temp = 1
        temp2 = -1

        #for loops simulate movement along the files
        #checks spaces below and to the right of piece
        for r in range(cfile+1,8):
            #out of range check
            if crank + temp > 7:
                break
            #if blank space add to list and increment counter
            if board[r][crank+temp] == ' ':
                numseq = str(crank) + str(8-cfile) + str(crank+temp) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                temp+=1
                continue
            #if enemy add to list and break
            if board[r][crank+temp] in enemies:
                numseq = str(crank) + str(8-cfile) + str(crank+temp) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                break
            #if friend break
            if board[r][crank+temp] in friends:
                break

        #checks spaces below and to left of peice
        for r in range(cfile+1,8):
            #out of range check
            if crank + temp2 < 0:
                break
            #if blank space add to list and increment counter
            if board[r][crank+temp2] == ' ':
                numseq = str(crank) + str(8-cfile) + str(crank+temp2) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                temp2-=1
                continue
            #if enemy add to list and break
            if board[r][crank+temp2] in enemies:
                numseq = str(crank) + str(8-cfile) + str(crank+temp2) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                break
            #if friend break
            if board[r][crank+temp2] in friends:
                break

        #resets counter values for further use
        temp2 = -1
        temp = 1

        #checks spaces above and to the right
        for r in reversed(range(0,cfile)):
            if crank + temp > 7:
                break
            if board[r][crank+temp] == ' ':
                numseq = str(crank) + str(8-cfile) + str(crank+temp) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                temp+=1
                continue
            if board[r][crank+temp] in enemies:
                numseq = str(crank) + str(8-cfile) + str(crank+temp) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                break
            if board[r][crank+temp] in friends:
                break

        #checks spaces above and to the left
        for r in reversed(range(0,cfile)):
            if crank + temp2 < 0:
                break
            if board[r][crank+temp2] == ' ':
                numseq = str(crank) + str(8-cfile) + str(crank+temp2) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                temp2-=1
                continue
            if board[r][crank+temp2] in enemies:
                numseq = str(crank) + str(8-cfile) + str(crank+temp2) + str(8-r)
                validmoves.append(self.uciConvert(numseq))
                break
            if board[r][crank+temp2] in friends:
                break

    #takes position of piece and moves them to closest space that is not in same rank or file as piece. In other words an L shape.
    def knightMovement(self, board, cfile, crank, enemies, friends, validmoves) -> None:
        #out of range check for file 2 above
        if cfile+2 <= 7:
            #out of range check for rank 1 right
            if crank+1 <= 7 and board[cfile+2][crank+1] not in friends:
                validmoves.append(self.uciConvert(str(crank) + str(8-cfile) + str(crank+1) + str(8-cfile-2)))
            #one left
            if crank-1 >= 0 and board[cfile+2][crank-1] not in friends:
                validmoves.append(self.uciConvert(str(crank) + str(8-cfile) + str(crank-1) + str(8-cfile-2)))
        #two below
        if cfile-2 >= 0:
            #one right
            if crank+1 <= 7 and board[cfile-2][crank+1] not in friends:
                validmoves.append(self.uciConvert(str(crank) + str(8-cfile) + str(crank+1) + str(8-cfile+2)))
            #one left
            if crank-1 >= 0 and board[cfile-2][crank-1] not in friends:
                validmoves.append(self.uciConvert(str(crank) + str(8-cfile) + str(crank-1) + str(8-cfile+2)))
        #two right
        if crank+2 <= 7:
            #one above
            if cfile+1 <= 7 and board[cfile+1][crank+2] not in friends:
                validmoves.append(self.uciConvert(str(crank) + str(8-cfile) + str(crank+2) + str(8-cfile-1)))
            #one below
            if cfile-1 >= 0 and board[cfile-1][crank+2] not in friends:
                validmoves.append(self.uciConvert(str(crank) + str(8-cfile) + str(crank+2) + str(8-cfile+1)))
        #two left
        if crank-2 >= 0:
            #one above
            if cfile+1 <= 7 and board[cfile+1][crank-2] not in friends:
                validmoves.append(self.uciConvert(str(crank) + str(8-cfile) + str(crank-2) + str(8-cfile-1)))
            #one below
            if cfile-1 >= 0 and board[cfile-1][crank-2] not in friends:
                validmoves.append(self.uciConvert(str(crank) + str(8-cfile) + str(crank-2) + str(8-cfile+1)))





    #takes position of king as simulates movement of every piece on the king to ensure he is not being checked and returns True if he is along with a list of spaces that need to be covered
    def kingCheck(self, board, cfile, crank, enemies, friends) -> bool:

        #simulates file movement to check for checks in the same file
        #checks file below
        fileranklist = []
        saveKing = []
        check = False
        for r in range(cfile+1,8):
            if board[r][crank] in friends:
                break
            if board[r][crank] == ' ':
                numseq = str(crank) + str(8-r)
                fileranklist.append(self.uciConvert(numseq))
            if board[r][crank] in enemies:
                if board[r][crank] in enemies[:3]:
                    #king more than one space away
                    if r > cfile+1 and board[r][crank] == enemies[2]:
                        continue
                    fileranklist.append(self.uciConvert(str(crank) + str(8-r)))
                    saveKing = saveKing + fileranklist
                    check = True
                    break
                else:
                    break
        fileranklist.clear()
        #checks file above
        for r in reversed(range(0,cfile)):
            if board[r][crank] in friends:
                break
            if board[r][crank] == ' ':
                numseq = str(crank) + str(8-r)
                fileranklist.append(self.uciConvert(numseq))
            if board[r][crank] in enemies:
                if board[r][crank] in enemies[:3]:
                    #king more than one space away
                    if r < cfile-1 and board[r][crank] == enemies[2]:
                        continue
                    fileranklist.append(self.uciConvert(str(crank) + str(8-r)))
                    saveKing = saveKing + fileranklist
                    check = True
                    break
                else:
                    break
        fileranklist.clear()


        #simulates rank movement to check for checks in the same rank
        #chacks rank to right
        for r in range(crank+1,8):
            if board[cfile][r] in friends:
                break
            if board[cfile][r] == ' ':
                numseq = str(r) + str(8-cfile)
                fileranklist.append(self.uciConvert(numseq))
            if board[cfile][r] in enemies:
                if board[cfile][r] in enemies[:3]:
                    #king more than one space away
                    if r > crank+1 and board[cfile][r] == enemies[2]:
                        continue
                    fileranklist.append(self.uciConvert(str(r) + str(8-cfile)))
                    saveKing = saveKing + fileranklist
                    check = True
                    break
                else:
                    break
        fileranklist.clear()
        #checks rank to left
        for r in reversed(range(0,crank)):
            if board[cfile][r] in friends:
                break
            if board[cfile][r] == ' ':
                numseq = str(r) + str(8-cfile)
                fileranklist.append(self.uciConvert(numseq))
            if board[cfile][r] in enemies:
                if board[cfile][r] in enemies[:3]:
                    #king more than one space away
                    if r < crank-1 and board[cfile][r] == enemies[2]:
                        continue
                    fileranklist.append(self.uciConvert(str(r) + str(8-cfile)))
                    saveKing = saveKing + fileranklist
                    check = True
                    break
                else:
                    break
        fileranklist.clear()


        #simulates all diagonal movement to check for checks from each diagonal
        temp = 1
        temp2 = -1
        diaglist = []

        #down and right movement
        for r in range(cfile+1,8):
            if crank + temp > 7:
                break
            if board[r][crank+temp] in friends:
                break
            if board[r][crank+temp] == ' ':
                numseq = str(crank+temp) + str (8-r)
                diaglist.append(self.uciConvert(numseq))
            if board[r][crank+temp] in enemies:
                if board[r][crank+temp] in enemies[1:5]:
                    #black pawn behind white king
                    if temp > 1 and board[r][crank+temp] == 'p':
                        temp+=1
                        continue
                    #king more than one space away
                    if temp > 1 and board[r][crank+temp] == enemies[2]:
                        break
                    #pawn more than one space away
                    if temp > 1 and board[r][crank+temp] == enemies[3]:
                        break
                    diaglist.append(self.uciConvert(str(crank+temp) + str(8-r)))
                    saveKing = saveKing + diaglist
                    check = True
                    break
                else:
                    break
            temp+=1

        diaglist.clear()
        temp = 1

        #down and left movement
        for r in range(cfile+1,8):
            if crank + temp2 < 0:
                break
            if board[r][crank+temp2] in friends:
                break
            if board[r][crank+temp2] == ' ':
                numseq = str(crank+temp2) + str(8-r)
                diaglist.append(self.uciConvert(numseq))
            if board[r][crank+temp2] in enemies:
                if board[r][crank+temp2] in enemies[1:5]:
                    #black pawn behind white king
                    if temp2 < -1 and board[r][crank+temp2] == 'p':
                        temp2-=1
                        continue
                    #king more than one space away
                    if temp2 < -1 and board[r][crank+temp2] == enemies[2]:
                        break
                    #pawn more than one space away
                    if temp2 < -1 and board[r][crank+temp2] == enemies[3]:
                        break
                    diaglist.append(self.uciConvert(str(crank+temp2) + str(8-r)))
                    saveKing = saveKing + diaglist
                    check = True
                    break
                else:
                    break
            temp2-=1
        
        diaglist.clear()
        temp2 = -1

        #up and to the right movement
        for r in reversed(range(0,cfile)):
            if crank + temp > 7:
                break
            if board[r][crank+temp] in friends:
                break
            if board[r][crank+temp] == ' ':
                numseq = str(crank+temp) + str(8-r)
                diaglist.append(self.uciConvert(numseq))
            if board[r][crank+temp] in enemies:
                if board[r][crank+temp] in enemies[1:5]:
                    #white pawn behing black king
                    if temp > 1 and board[r][crank+temp] == 'P':
                        temp+=1
                        continue
                    #king more than one space away
                    if temp > 1 and board[r][crank+temp] == enemies[2]:
                        break
                    #pawn more than one space away
                    if temp > 1 and board[r][crank+temp] == enemies[3]:
                        break
                    diaglist.append(self.uciConvert(str(crank+temp) + str(8-r)))
                    saveKing = saveKing + diaglist
                    check = True
                    break
                else:
                    break
            temp+=1
        diaglist.clear()

        #up and to the left movement
        for r in reversed(range(0,cfile)):
            if crank + temp2 < 0:
                break
            if board[r][crank+temp2] in friends:
                break
            if board[r][crank+temp2] == ' ':
                numseq = str(crank+temp2) + str(8-r)
                diaglist.append(self.uciConvert(numseq))
            if board[r][crank+temp2] in enemies:
                if board[r][crank+temp2] in enemies[1:5]:
                    #white pawn behind black king
                    if temp2 < -1 and board[r][crank+temp2] == 'P':
                        temp2-=1
                        continue
                    #king more than one space away
                    if temp2 < -1 and board[r][crank+temp2] == enemies[2]:
                        break
                    #pawn more than one space away
                    if temp2 < -1 and board[r][crank+temp2] == enemies[3]:
                        break
                    diaglist.append(self.uciConvert(str(crank+temp2) + str(8-r)))
                    saveKing = saveKing + diaglist
                    check = True
                    break
                else:
                    break
            temp2-=1
        diaglist.clear()
    
        #simulates knight movement from knight function to check for checks from knights
        if cfile+2 <= 7:
            if crank+1 <= 7 and board[cfile+2][crank+1] in enemies[-1]:
                saveKing.append(self.uciConvert(str(crank+1) + str(8-cfile-2)))
                check = True
            if crank-1 >= 0 and board[cfile+2][crank-1] in enemies[-1]:
                saveKing.append(self.uciConvert(str(crank-1) + str(8-cfile-2)))
                check = True

        if cfile-2 >= 0:
            if crank+1 <= 7 and board[cfile-2][crank+1] in enemies[-1]:
                saveKing.append(self.uciConvert(str(crank+1) + str(8-cfile+2)))
                check = True
            if crank-1 >= 0 and board[cfile-2][crank-1] in enemies[-1]:
                saveKing.append(self.uciConvert(str(crank-1) + str(8-cfile+2)))
                check = True

        if crank+2 <= 7:
            if cfile+1 <= 7 and board[cfile+1][crank+2] in enemies[-1]:
                saveKing.append(self.uciConvert(str(crank+2) + str(8-cfile-1)))
                check = True
            if cfile-1 >= 0 and board[cfile-1][crank+2] in enemies[-1]:
                saveKing.append(self.uciConvert(str(crank+2) + str(8-cfile+1)))
                check = True

        if crank-2 >= 0:
            if cfile+1 <= 7 and board[cfile+1][crank-2] in enemies[-1]:
                saveKing.append(self.uciConvert(str(crank-2) + str(8-cfile-1)))
                check = True
            if cfile-1 >= 0 and board[cfile-1][crank-2] in enemies[-1]:
                saveKing.append(self.uciConvert(str(crank-2) + str(8-cfile+1)))
                check = True
        return check, saveKing


    #takes king location and simulates each move he can make to ensure he is not putting himself in danger
    def checkKingMoves(self, board, i, j, enemies, friends, validmoves) -> None:
        #one space below
        if i+1 <= 7:
            testcheck, save = self.kingCheck(board, i+1, j, enemies, friends)
            if not testcheck and board[i+1][j] not in friends:
                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j) + str(8-i-1)))
        #one space above
        if i-1 >= 0:
            testcheck, save = self.kingCheck(board, i-1, j, enemies, friends)
            if not testcheck and board[i-1][j] not in friends:
                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j) + str(8-i+1)))
        #one space to right
        if j+1 <= 7:
            testcheck, save = self.kingCheck(board, i, j+1, enemies, friends)
            if not testcheck and board[i][j+1] not in friends:
                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j+1) + str(8-i)))
        #one space to left
        if j-1 >= 0:
            testcheck, save = self.kingCheck(board, i, j-1, enemies, friends)
            if not testcheck and board[i][j-1] not in friends:
                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j-1) + str(8-i)))
        #down and right
        if i+1 <= 7 and j+1 <= 7:
            testcheck, save = self.kingCheck(board, i+1, j+1, enemies, friends)
            if not testcheck and board[i+1][j+1] not in friends:
                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j+1) + str(8-i-1)))
        #down and left
        if i+1 <= 7 and j-1 >= 0:
            testcheck, save = self.kingCheck(board, i+1, j-1, enemies, friends)
            if not testcheck and board[i+1][j-1] not in friends:
                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j-1) + str(8-i-1)))
        #up and right
        if i-1 >= 0 and j+1 <= 7:
            testcheck, save = self.kingCheck(board, i-1, j+1, enemies, friends)
            if not testcheck and board[i-1][j+1] not in friends:
                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j+1) + str(8-i+1)))
        #up and left
        if i-1 >= 0 and j-1 >= 0:
            testcheck, save = self.kingCheck(board, i-1, j-1, enemies, friends)
            if not testcheck and board[i-1][j-1] not in friends:
                validmoves.append(self.uciConvert(str(j) + str(8-i) + str(j-1) + str(8-i+1)))
        
