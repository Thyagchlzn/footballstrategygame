'''
this is responsible for storing all the information abt the current state of a chess game
it will also be responsible for determining the valid moves at the current state.
it will also keep move log
'''
#defining some constant values for style of play
POSITIONAL=0
DIRECT=1
SITBACK=2
HIGHPRESS=3
class GameState():

    def __init__(self,bluelineup,redlineup,whosfirst,dattstyle,ddefstyle):
        #can use numpy to increase speed'
        #each list represent a row '

        self.board=[
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        for i in range(0,3):
            for j in range(0,5):
                if whosfirst:
                    self.board[5-i][1+j]=redlineup[i][j]
                    self.board[6+i][1+j]=-bluelineup[i][j]
                else:
                    self.board[7- i][1 + j] = redlineup[i][j]
                    self.board[8+ i][1 + j] = -bluelineup[i][j]
        self.movefunctions={9:self.getstmoves,7:self.getwrmoves,8:self.getmfmoves,6:self.getdmmoves,2:self.getfbmoves,3:self.getcbmoves,
                            1:self.getgkmoves,10:self.gettrqmoves}
        self.bluetomove=True if whosfirst else False
        self.movesperturn=0
        self.goalallowed=''
        self.redscore=0
        self.bluescore=0
        self.log=[]
        self.ball=(8,3) if whosfirst else (5,3)
        self.possession=False#if that team has ball  possession
        self.prevpossession=whosfirst #0 red 1 blue
        self.offside=self.getoffside()
        self.ai=False
        self.tacklemoves=False
        self.cutthroughpass=False
        self.shots=[]  #moveordering
        self.passes=[]
        self.tackles=[]
        self.running=[]
        self.throughpasses=[]
        self.possiblepasses=0
        self.attstyle=dattstyle
        self.defstyle=ddefstyle
        self.oppplayerhigh=self.computeplayerhigh()
    def restart(self,board,ball):
        self.board=board
        self.ball=(ball[0],ball[1])
    def computeplayerhigh(self):
     try:
        if  self.defstyle[1 if not self.bluetomove else -1]==HIGHPRESS:
            if self.bluetomove:

                for i in range(12,0,-1):
                    for j in range(7):
                        if self.board[i][j]*1>0:
                                return i
            else:

                for i in range(1,13):
                    for j in range(7):
                        if self.board[i][j]*-1>0:
                            return i
     except:
         print(self.defstyle,self.bluetomove,self.ball,self.attstyle)

    def ispossession(self):

        if self.bluetomove and self.board[self.ball[0]][self.ball[1]]<0:#if same team
            self.possession=True
            return True
        elif  self.bluetomove and self.board[self.ball[0]][self.ball[1]] > 0 :
            self.possession = False
            self.prevpossession=0
            return False
        elif self.bluetomove and  self.board[self.ball[0]][self.ball[1]]==0 :
            #if self.prevpossession:
            #    return True
            #else:
                return False


        elif not self.bluetomove and self.board[self.ball[0]][self.ball[1]]>0:
            self.possession=True
            return True

        elif not self.bluetomove and self.board[self.ball[0]][self.ball[1]] < 0 :
            self.possession = False
            self.prevpossession=1
            return False
        elif not self.bluetomove and  self.board[self.ball[0]][self.ball[1]]==0 :
            #if self.prevpossession:#this avoids unnecessary loss of possession
            #    return False
            #else:
                return True

    def checkgoal(self):
        if self.ball[0]==13 and self.ball[1] in (2,3,4):
            self.goalallowed="-1"
            self.redscore+=1
        elif self.ball[0]==0 and self.ball[1] in (2,3,4):
            self.goalallowed="1"
            self.bluescore += 1
    def getoffside(self):
        off=6 #row which has the last line of defense
        if (not self.bluetomove and self.possession) or (self.bluetomove and not self.possession):#reds turn so cal blue offside
            for i in range(12,6,-1):
                for j in range(0,7):
                    if self.board[i][j]<0:#make sure its blue
                        if self.board[i][j]!= -1 and self.board[i][j]!=0:
                            off=i
                            return  off
                    elif self.board[i][j]>0 and self.ball==(i,j):

                        return i
            else:
                return 1

        elif (self.bluetomove and self.possession) or(not self.bluetomove and not self.possession):#blue turn so cal red offside
            for i in range(1,7,1):
                for j in range(0,7):
                    if self.board[i][j]>0:#make sure its red
                        if self.board[i][j]!=1 and self.board[i][j]!=0:
                            off=i
                            return off
                    elif self.board[i][j]<0 and self.ball==(i,j):

                        return i
            else:
                return 11






    def makemove(self,move):
        #cannot move empty space to a position
        if move.piecemoved==0:
            return
        if move.movetype=='p':
            self.ball=(move.erow,move.ecol)
        elif move.movetype=='t':
            self.ball=(move.srow,move.scol)
        elif move.movetype=='k':
            self.ball=(move.erow,move.ecol)
        elif move.movetype=='s':
            self.ball=(move.erow,move.ecol)
        elif move.movetype=='r':
            self.board[move.srow][move.scol]=0
            self.board[move.erow][move.ecol]=move.piecemoved
        elif move.movetype=='c':
            self.board[move.srow][move.scol]=0
            self.board[move.erow][move.ecol]=move.piecemoved
            self.ball=(move.erow,move.ecol)
        self.log.append(move)
        self.movesperturn = self.movesperturn + 1

        if self.ispossession() and self.movesperturn==1 :
            self.movesperturn = self.movesperturn + 1

        else :
            self.movesperturn=self.movesperturn

        self.checkgoal()
        if self.movesperturn==1 or self.movesperturn==3:#restricting only 2max moves

            self.bluetomove = not self.bluetomove
            self.movesperturn=0



    '''undo moves in board'''
    def undomove(self):
        if len(self.log)!=0:
            move=self.log.pop()
            self.board[move.srow][move.scol]=move.piecemoved
            self.board[move.erow][move.ecol]=move.piececaptured
            self.ball=move.ballpos
            self.goalallowed = ''

            if move.moveId[-3:-1] in ('20','30','40') and self.bluescore!=0:
                self.bluescore-=1
            elif move.moveId[-4:-1] in ('213','313','413') and self.redscore!=0:
                self.redscore-=1
            #three cases undo can be called
            #after two moves (self.movesperturn==0) self.pos=false turn changed
            if self.movesperturn==0 and self.ispossession()==False:

                self.movesperturn=2
                self.bluetomove = not self.bluetomove
                return
            #after 1st move(if it has another move)self.movesperturn=2 and sel.pos=true
            elif self.movesperturn==2 :
                self.movesperturn = 0
                return
            #after 1st move(only move)turn changed,sef.movesperturn=0 self.possession=true (because if it had possession then now self.po is false)
            elif self.ispossession()==True and self.movesperturn==0:
                self.bluetomove = not self.bluetomove
                self.movesperturn = 0
                return






    #validate moves
    def getvalidmoves(self,ai=False,tacklemoves=False,cutthroughpass=False,moveorder=''):
        self.tacklemoves=tacklemoves
        self.ai=ai
        self.cutthroughpass=cutthroughpass
        self.ispossession()
        #self.checkgoal()
        self.offside=self.getoffside()
        self.oppplayerhigh=self.computeplayerhigh()


        return self.getpossiblemoves(moveorder)
    #possible moves
    def getpossiblemoves(self,moveorder=''):
        #list records all possible move object
        moves=[]
        for r in range(14):
            for c in range(7):
                turn=(r,c)
                if (self.board[turn[0]][turn[1]]<0 and self.bluetomove==True) or (self.board[turn[0]][turn[1]]>0 and self.bluetomove==False):

                    piece=abs(self.board[r][c]) #mapping -1 and 1 to '1'
                    #passing postion of piece and list to record
                    self.movefunctions[piece](r,c,moves,turn)
        if self.tacklemoves:
            moves =  self.tackles + self.shots +self.passes + self.running + self.throughpasses
        elif moveorder=='run':
            moves = self.tackles + self.shots+ self.running + self.passes  + self.throughpasses
        elif self.ai==True and self.possession and self.attstyle[1 if not self.bluetomove else -1]==DIRECT:
            moves=self.shots+self.running+self.tackles+self.passes+self.throughpasses
        else:
            moves=self.shots+self.tackles+self.passes+self.running+self.throughpasses
        self.possiblepasses=len(self.passes)
        self.shots=[]
        self.passes = []
        self.tackles = []
        self.running = []
        self.throughpasses = []

        return moves
    #passing
    def getbasicpass(self,r,c,moves,turn):


        if self.ball == turn:  # player cant pass without ball

            directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            #player=(self.ball[0],self.ball[1])
            for d in directions:
                for i in range(1,13):

                    endrow=(r+d[0]*i)
                    endcol=(c+d[1]*i)

                    if -1<endrow<=len(self.board)-1 and -1<endcol<=7-1 :#on board
                        enemycolor = 1 if self.bluetomove else -1

                        if self.board[endrow][endcol]*enemycolor >0: #pass cant be made through enemy

                            break
                        #to eliminate cols in goal post other than 2,3,4   and can only shoot inside dbox
                        elif (endrow==0  and self.board[turn[0]][turn[1]]<0)   and endcol  in (2,3,4) and r in (1,2) and c in (1,2,3,4,5):

                            self.shots.append(Move((r, c), (endrow, endcol), self.board, 'p', self.ball))
                        elif (endrow==13  and self.board[turn[0]][turn[1]]>0)   and endcol  in (2,3,4) and r in (11,12) and c in (1,2,3,4,5):

                            self.shots.append(Move((r, c), (endrow, endcol), self.board, 'p', self.ball))

                        elif self.board[turn[0]][turn[1]]<0 and endrow<self.offside:

                            continue
                        elif self.board[turn[0]][turn[1]]>0 and endrow>self.offside:

                            continue
                        elif self.board[endrow][endcol]* (-1 if self.bluetomove else 1)>0:

                            self.passes.append(Move((r,c),(endrow,endcol),self.board,'p',self.ball))
                    else:

                        break
        else:

            return


    def getpingpass(self,r,c,moves,turn):

        if self.ball == turn:  # player cant pass without ball

            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            # player=(self.ball[0],self.ball[1])
            for d in directions:
                for i in range(1, 13):

                    endrow = (r + d[0] * i)
                    endcol = (c + d[1] * i)

                    if 0 < endrow <= len(self.board) - 2 and -1 < endcol <= 7 - 1:  # on board
                        enemycolor = 1 if self.bluetomove else -1


                        if self.board[(r + d[0] * 1)][(c + d[1] * 1)]*enemycolor>0:  # pass cant be made if  enemy is one step before in that dir
                            break
                        elif self.board[(endrow + d[0] * -1)][(endcol + d[1] * -1)]* enemycolor>0:#pass cant be recieved if enemy is surrounded

                            continue

                        elif self.board[turn[0]][turn[1]]<0 and endrow<self.offside:#offside checking

                            break
                        elif self.board[turn[0]][turn[1]]>0 and endrow>self.offside:

                            break
                        elif self.board[endrow][endcol]* (-1 if self.bluetomove else 1)>0:

                            self.passes.append(Move((r, c), (endrow, endcol), self.board, 'p', self.ball))
                    else:
                        break
        else:

            return


    def getadvpass(self,r,c,moves,turn):

        if self.ball == turn:  # player cant pass without ball

            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

            for d in directions:
                for i in range(1, 13):

                    endrow = (r + d[0] * i)
                    endcol = (c + d[1] * i)

                    if 0 < endrow <= len(self.board) - 2 and -1 < endcol <= 7 - 1:  # on board
                        enemycolor = 1 if self.bluetomove else -1


                        if self.board[endrow][endcol] == 0:
                           self.passes.append(Move((r, c), (endrow, endcol), self.board, 'k', self.ball))
                    else:
                        break
        else:
            return
    #spl advance pass only for trq
    def getsplpass(self,r,c,moves,turn):
        if self.ball == turn:  # player cant pass without ball

            directions = [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2),(-1, -2), (-2, -1), (-2,1), (1, -2), (1, 2), (2, -1), (2, 1), (-1, 2)]

            for d in directions:
                #for i in range(1, 13):

                    endrow = (r + d[0] )
                    endcol = (c + d[1] )

                    if 0 < endrow <= len(self.board) - 2 and -1 < endcol <= 7 - 1:  # on board
                        enemycolor = 1 if self.bluetomove else -1


                        if self.board[endrow][endcol] == 0:
                           self.passes.append(Move((r, c), (endrow, endcol), self.board, 'k', self.ball))
                        if self.board[endrow][endcol] * (-1 if self.bluetomove else 1)>0:
                           self.passes.append(Move((r, c), (endrow, endcol), self.board, 'p', self.ball))

        else:
            return
    #shooting only inside the box
    def getshoot(self,r,c,moves,turn):

        #check if the player is in the box
        if self.board[turn[0]][turn[1]]<0 and turn[0]<3 or self.board[turn[0]][turn[1]]>0 and turn[0]>10:
          if self.ball == turn :  # player cant shoot without ball

            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

            for d in directions:
                for i in range(1, 13):

                    endrow = (r + d[0] * i)
                    endcol = (c + d[1] * i)

                    if -1 < endrow <= 14 - 1 and -1 < endcol <= 7 - 1:  # on board
                        enemycolor = 'a' if self.bluetomove else 'b'


                        if abs(self.board[endrow][endcol]) == 1:  # shoot cant be made through   gk
                            break
                        elif endrow in (0,13) and endcol in (2,3,4):

                            self.shots.append(Move((r, c), (endrow, endcol), self.board, 's', self.ball))
                    else:
                        break
          else:
              return
        else:
            return


    #tackling
    def getknickup(self,r,c,moves,turn):
        #upward respective to blue or red
        if self.board[self.ball[0]][self.ball[1]]* turn>0:#player cant tackle their own mate
            return
        if self.bluetomove and self.ball[0]+1==r and c==self.ball[1]:
            self.tackles.append(Move((r, c), (r - 1, c), self.board, 't', self.ball))
        elif not(self.bluetomove) and self.ball[0]-1==r and c==self.ball[1]:
            self.tackles.append(Move((r, c), (r +1, c), self.board, 't', self.ball))
    def getknickside(self,r,c,moves,turn):
        #left or right
        if self.board[self.ball[0]][self.ball[1]]* turn>0:  # player cant tackle their own mate
            return
        if  self.ball[1] + 1 == c and r == self.ball[0]:
            self.tackles.append(Move((r, c), (r, c-1), self.board, 't', self.ball))
        elif self.ball[1] - 1 == c and r == self.ball[0]:
            self.tackles.append(Move((r, c), (r , c+1), self.board, 't', self.ball))
    def getknickdiag(self,r,c,moves,turn):
        if self.board[self.ball[0]][self.ball[1]]*turn>0:  # player cant tackle their own mate
            return
        if  self.ball[1] + 1 == c and r == self.ball[0]+1:#upward right
            self.tackles.append(Move((r, c), (r-1, c-1), self.board, 't', self.ball))
        elif self.ball[1] - 1 == c and r == self.ball[0]-1:#downward left
            self.tackles.append(Move((r, c), (r+1 , c+1), self.board, 't', self.ball))
        elif  self.ball[1] + 1 == c and r == self.ball[0]-1:#upward left
            self.tackles.append(Move((r, c), (r+1, c-1), self.board, 't', self.ball))
        elif self.ball[1] - 1 == c and r == self.ball[0]+1:#downward right
            self.tackles.append(Move((r, c), (r-1 , c+1), self.board, 't', self.ball))
    def getknickback(self,r,c,moves,turn):
        # downward respective to blue or red
        if self.board[self.ball[0]][self.ball[1]]* turn>0:  # player cant tackle their own mate
            return
        if self.bluetomove and self.ball[0] - 1 == r and c == self.ball[1]:
            self.tackles.append(Move((r, c), (r + 1, c), self.board, 't', self.ball))
        elif not (self.bluetomove) and self.ball[0] + 1 == r and c == self.ball[1]:
            self.tackles.append(Move((r, c), (r - 1, c), self.board, 't', self.ball))


    #movement
    def getonespace(self,r,c,moves):
        if (r,c)==self.ball:
            #player has the ball
            type='c'
        else:
            type='r'
        #generated only for carry or run
        #array bound exception
        #up
        neglect=10
        if self.possession==True and self.ai==True:
            neglect=-1 if self.bluetomove==True else 1

        for i in [-1,0,1]:
            for j in [-1,0,1]:
             if i!=neglect :
                if r-i>14-2 or c-j>7-1 or c-j<0 or r-i<1:
                    continue
                elif self.bluetomove and r-i < self.offside and self.possession and type=='r' and self.ai==True:
                    continue
                elif not self.bluetomove and r-i > self.offside and self.possession and type=='r' and self.ai==True:

                    continue
                else:
                    if self.board[r-i][c-j]==0:
                        self.running.append(Move((r,c),(r-i,c-j),self.board,type,self.ball))
    def gettwospace(self,r,c,moves):
        if (r,c)==self.ball:
            #player has the ball
            self.getonespace(r,c,moves)
            return
        else:
            type='r'

        #generated only for carry or run
        #array bound exception
        #up
        neglect = 10
        if self.possession == True and self.ai==True:
            neglect = -1 if self.bluetomove == True else 1
        for i in [-1,0,1]:
            for j in [-1,0,1]:
              if i!=neglect:
                if r-i>14-2 or c-j>7-1 or c-j<0 or r-i<1:
                    continue
                else:
                    if self.board[r-i][c-j]==0:
                        self.running.append(Move((r,c),(r-i,c-j),self.board,type,self.ball))
                        if r - i*2 > 14 - 2 or c - j*2 > 7 - 1 or c-j*2<0 or r-i*2<1:
                            continue
                        elif self.bluetomove and r - i*2 < self.offside and self.possession and type == 'r' and self.ai==True:
                            continue
                        elif not self.bluetomove and r - i*2 > self.offside and self.possession and type == 'r' and self.ai==True:

                            continue
                        else:
                            if self.board[r - i*2][c - j*2] == 0:
                                self.running.append(Move((r, c), (r - i*2, c - j*2), self.board, type, self.ball))
    #passing

    def getstmoves(self,r,c,moves,turn):
        #print([(x.moveId, x.srow, x.scol) for x in moves])
        if self.tacklemoves==True:
            self.getknickup(r, c, moves, self.board[turn[0]][turn[1]])
        else:
            self.getshoot(r, c, moves, turn)
            self.getknickup(r,c,moves,self.board[turn[0]][turn[1]])
            self.getbasicpass(r,c,moves,turn)
            self.getonespace(r, c, moves)


    def getfbmoves(self,r,c,moves,turn):
        #self.getonespace(r, c, moves)
        if self.tacklemoves == True:
            self.getknickup(r, c, moves, self.board[turn[0]][turn[1]])
        else:
            self.getknickup(r, c, moves,self.board[turn[0]][turn[1]])
            self.getbasicpass(r, c, moves, turn)
            self.getpingpass(r,c,moves,turn)
            self.gettwospace(r, c, moves)
    def getcbmoves(self,r,c,moves,turn):
        if self.tacklemoves == True:
            self.getknickup(r, c, moves, self.board[turn[0]][turn[1]])
            self.getknickside(r, c, moves, self.board[turn[0]][turn[1]])
            self.getknickdiag(r, c, moves, self.board[turn[0]][turn[1]])
            self.getknickback(r, c, moves, self.board[turn[0]][turn[1]])

        else:
            self.getknickup(r, c, moves,self.board[turn[0]][turn[1]])
            self.getknickside(r, c, moves, self.board[turn[0]][turn[1]])
            self.getknickdiag(r, c, moves, self.board[turn[0]][turn[1]])
            self.getknickback(r,c,moves,self.board[turn[0]][turn[1]])
            self.getbasicpass(r, c, moves, turn)
            self.getonespace(r, c, moves)
    def gettrqmoves(self,r,c,moves,turn):
        if self.tacklemoves == True:
            self.getknickup(r, c, moves, self.board[turn[0]][turn[1]])
            return
        elif self.cutthroughpass==True:
            self.getknickup(r, c, moves, self.board[turn[0]][turn[1]])
            self.getbasicpass(r, c, moves, turn)
            self.getpingpass(r, c, moves, turn)
            self.getonespace(r, c, moves)
        else:
            self.getknickup(r, c, moves,self.board[turn[0]][turn[1]])
            self.getbasicpass(r, c, moves, turn)
            #self.getpingpass(r,c,moves,turn)
            self.getonespace(r, c, moves)
            self.getsplpass(r,c,moves,turn)#2 square passes already one covered in basic pass
    def getmfmoves(self,r,c,moves,turn):
        if self.tacklemoves == True:
            self.getknickup(r, c, moves, self.board[turn[0]][turn[1]])
            self.getknickside(r, c, moves, self.board[turn[0]][turn[1]])
            return
        elif self.cutthroughpass==True:
            self.getknickup(r, c, moves, self.board[turn[0]][turn[1]])
            self.getknickside(r, c, moves, self.board[turn[0]][turn[1]])
            self.getbasicpass(r, c, moves, turn)
            self.getpingpass(r, c, moves, turn)
            self.getonespace(r, c, moves)
        else:
            self.getknickup(r, c, moves,self.board[turn[0]][turn[1]])
            self.getknickside(r,c,moves,self.board[turn[0]][turn[1]])
            self.getbasicpass(r, c, moves, turn)
            self.getpingpass(r,c,moves,turn)
            self.getonespace(r, c, moves)
            self.getadvpass(r,c,moves,turn)
    def getdmmoves(self,r,c,moves,turn):
        if self.tacklemoves==True:
            self.getknickup(r, c, moves, self.board[turn[0]][turn[1]])
            self.getknickside(r, c, moves, self.board[turn[0]][turn[1]])
            self.getknickdiag(r, c, moves, self.board[turn[0]][turn[1]])

        else:
            self.getknickup(r, c, moves,self.board[turn[0]][turn[1]])
            self.getknickside(r,c,moves,self.board[turn[0]][turn[1]])
            self.getknickdiag(r,c,moves,self.board[turn[0]][turn[1]])
            self.getbasicpass(r, c, moves, turn)
            self.getpingpass(r,c,moves,turn)
            self.getonespace(r, c, moves)
    def getwrmoves(self,r,c,moves,turn):
        #self.getonespace(r, c, moves)
        if self.tacklemoves==True:
            self.getknickup(r, c, moves, self.board[turn[0]][turn[1]])
        else:
            self.getknickup(r, c, moves,self.board[turn[0]][turn[1]])
            self.getbasicpass(r, c, moves, turn)
            self.gettwospace(r, c, moves)
        #only for offball movement 2space
    def getgkmoves(self,r,c,moves,turn):
        if self.tacklemoves==True:
            return
        self.getonespace(r, c, moves)
        self.getbasicpass(r, c, moves, turn)

class Move():
    def __init__(self,start,end,board,type,ball):
        #keeping track of movements
        self.srow=start[0]
        self.scol=start[1]
        self.erow=end[0]
        self.ecol=end[1]
        self.piecemoved=board[self.srow][self.scol]
        self.piececaptured=board[self.erow][self.ecol]
        self.movetype=type #p ,s ,t ,c
        self.moveId=str(self.scol)+str(self.srow)+str(self.ecol)+str(self.erow)+self.movetype
        #print(self.moveId)
        self.ballpos=ball




    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveId==other.moveId
        return False

