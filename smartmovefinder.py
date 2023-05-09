import random
from chessengine import Move,POSITIONAL,SITBACK,HIGHPRESS,DIRECT
import numpy as np
from ttable import *
from math import  floor,ceil
import time
TRANSPOSITIONAL_TABLE={}#hash index key may contain more than one obj
UB=2
LB=0
EXACT=1

class Tentry:
    move=[Move((0,0),(0,0),[[1,1],[1,1]],'t',(1,1))] #list

    depth=-2
    turn=0
    ball=(0,0)
    score=0
    flag=EXACT
    def __init__(self,bestmove,bestscore,depth,turn,flag,ball):
        self.move = bestmove  # list

        self.depth = depth
        self.turn = turn
        self.ball = ball
        self.score = bestscore
        self.flag = flag

def Tretrieve(gs,turn,hashvalue):
    #if  hashvalue  in TRANSPOSITIONAL_TABLE.keys():
    try:
        tentrylist=TRANSPOSITIONAL_TABLE[hashvalue]
        for  tentry in tentrylist:
            if tentry.ball==gs.ball and tentry.turn == turn:
                return tentry #obj
        return Tentry([Move((0,0),(0,0),[[1,1],[1,1]],'t',(1,1))] ,0,-2,0,EXACT,(0,0))
    except:
        #print(Tentry([Move((0,0),(0,0),[[1,1],[1,1]],'t',(1,1))] ,0,-1,0,EXACT,(0,0)))
        return Tentry([Move((0,0),(0,0),[[1,1],[1,1]],'t',(1,1))] ,0,-2,0,EXACT,(0,0))


def Tstore(hashvalue,bestmove,bestscore,depth,turn,flag,ball):
    tentry=Tentry(bestmove,bestscore,depth,turn,flag,ball)
    try:
        tentrylist=TRANSPOSITIONAL_TABLE[hashvalue]
        if len(tentrylist)==0:
            TRANSPOSITIONAL_TABLE[hashvalue] = [tentry]
        elif len(tentrylist)>0:
            tentrylist.append(tentry)
            TRANSPOSITIONAL_TABLE[hashvalue] = tentrylist
    except:
        TRANSPOSITIONAL_TABLE[hashvalue]=[tentry]


DEPTH=2
GOAL=2000
agilityval={1:0.5,3:0.5,6:1,9:1.5,8:1.5,7:2,2:1,10:2}
defpower={2:[(1,0)],
          3:[(-1,0),(-1,1),(-1,-1),(1,0),(1,1),(1,-1),(0,1),(0,-1)],
          6:[(1,0),(1,-1),(1,1),(0,-1),(0,1)],
          8:[(1,0),(0,1),(0,-1)],
          7:[(1,0)],9:[(1,0)],10:[(1,0)]}
fullbackval=np.array([[
            [3,3,0,0,0,3,3],
            [3,3,1,0,1,3,3],
            [4,4,1,0,1,4,4],
            [4,4,1,0,1,4,4],
            [3,3,1,0,1,3,3],
            [3,3,1,0,1,3,3],
            [2,2,1,0,1,2,2],
            [2,2,1,0,1,2,2],
            [1,1,0,0,0,1,1],
            [1,1,0,0,0,1,1],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]],
    [
            [0,0,0,0,0,0,0],
            [1,1,0,0,0,1,1],
            [1,1,0,0,0,1,1],
            [2,2,1,0,1,2,2],
            [2,2,1,0,1,2,2],
            [3,3,0,0,0,3,3],
            [3,3,0,0,0,3,3],
            [4,4,1,0,1,4,4],
            [4,4,1,0,1,4,4],
            [3,3,1,0,1,3,3],
            [3,3,1,0,1,3,3],
            [3,3,1,0,1,3,3]]
])
centerbackval=np.array([[
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,1,1,1,1,1,0],
            [0,2,3,3,3,2,0],
            [0,2,3,3,3,2,0],
            [0,2,4,4,4,2,0],
            [0,2,4,4,4,2,0],
            [0,1,1,1,1,1,0],
            [0,1,1,1,1,1,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]],
    [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,1,1,1,1,1,0],
            [0,2,2,2,2,2,0],
            [1,2,3,3,3,2,1],
            [1,2,3,3,3,2,1],
            [1,3,4,4,4,3,1],
            [1,3,4,4,4,3,1],
            [1,3,4,4,4,3,1],
            [2,3,4,3,4,3,2]]
])
wingerval=np.array([[
            [3,3,0,0,0,3,3],
            [3,3,1,0,1,3,3],
            [4,4,1,0,1,4,4],
            [4,4,1,0,1,4,4],
            [3,3,1,0,1,3,3],
            [3,3,1,0,1,3,3],
            [2,2,1,0,1,2,2],
            [1,1,0,0,0,1,1],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
],
    [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1,1,0,0,0,1,1],
            [1,1,0,0,0,1,1],
            [2,2,1,0,1,2,2],
            [3,3,1,0,1,3,3],
            [4,4,1,0,1,4,4],
            [4,4,1,0,1,4,4],
            [3,3,0,0,0,3,3],
            [1,1,0,0,0,1,1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]

    ]
])
strikerval=np.array([[
            [0,1,4,4,4,1,0],
            [0,1,4,4,4,1,0],
            [0,1,3,3,3,1,0],
            [0,1,3,3,3,1,0],
            [0,1,2,2,2,1,0],
            [0,1,1,1,1,1,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]],
    [   [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 1, 2, 2, 2, 1, 0],
        [0, 1, 3, 3, 3, 1, 0],
        [0, 1, 4, 4, 4, 1, 0],
        [0, 1, 4, 4, 4, 1, 0],
        [0, 1, 3, 3, 3, 1, 0],
        [0, 1, 2, 2, 2, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]

        ]
])
trequaristaval=np.array([[
            [0,2,2,2,2,2,0],
            [0,2,4,4,4,2,0],
            [0,2,4,4,4,2,0],
            [0,2,3,3,3,2,0],
            [0,2,3,3,3,2,0],
            [0,2,1,1,1,2,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]],
    [   [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 1, 2, 2, 2, 1, 0],
        [0, 1, 3, 3, 3, 1, 0],
        [0, 1, 4, 4, 4, 1, 0],
        [0, 1, 4, 4, 4, 1, 0],
        [0, 1, 3, 3, 3, 1, 0],
        [0, 1, 2, 2, 2, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]

        ]
])
midval=np.array([[

            [0,0,0,0,0,0,0],
            [1,1,2,2,2,1,1],
            [1,2,4,4,4,2,1],
            [1,2,4,4,4,2,1],
            [1,2,3,3,3,2,1],
            [1,2,3,3,3,2,1],
            [1,2,2,2,2,2,1],
            [0,1,1,1,1,1,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]],
    [   [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [1, 1, 2, 2, 2, 1, 1],
        [1, 2, 2, 2, 2, 2, 1],
        [1, 2, 3, 3, 3, 2, 1],
        [1, 2, 4, 4, 4, 2, 1],
        [1, 2, 4, 4, 4, 2, 1],
        [1, 2, 3, 3, 3, 2, 1],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0]
        ]
])
dmval=np.array([[
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,1,2,2,2,1,0],
            [0,2,3,3,3,2,0],
            [0,2,4,4,4,2,0],
            [0,2,4,4,4,2,0],
            [0,2,3,3,3,2,0],
            [0,2,3,3,3,2,0],
            [0,1,2,2,2,1,0],
            [0,1,2,2,2,1,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]],
    [   [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 2, 2, 1, 0],
        [0, 2, 3, 3, 3, 2, 0],
        [0, 1, 3, 3, 3, 1, 0],
        [0, 2, 4, 4, 4, 2, 0],
        [0, 2, 4, 4, 4, 2, 0],
        [0, 2, 4, 4, 4, 2, 0],
        [0, 2, 3, 3, 3, 2, 0],
        [0, 1, 1, 1, 1, 1, 0],

        ]
])

gkval=np.array([[
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 3, 3, 3, 1, 0],
    [0, 2, 4, 4, 4, 2, 0],
    [0, 2, 4, 4, 4, 2, 0]],
    [   [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 3, 3, 3, 1, 0],
        [0, 2, 4, 4, 4, 2, 0]

        ]
])


piecelog={10:trequaristaval,9:strikerval,7:wingerval,8:midval,6:dmval,3:centerbackval,2:fullbackval,1:gkval}
def getppm(gs,turn):
    if gs.ispossession():

        if (gs.ball[0] < 5 and gs.ball[0] > 0 and turn == False) or (
                gs.ball[0] < 13 and gs.ball[0] > (12 - 4) and turn == True):
            progression = 5
            passingopt = 3
            moveorder="run"
        elif (gs.ball[0] < 9 and gs.ball[0] > 4 and turn == False) or (
                gs.ball[0] < (12 - 3) and gs.ball[0] > (12 - 7) and turn == True):
            progression = 3
            passingopt = 5
            moveorder='pass'
        else:
            progression = 2
            passingopt = 1
            moveorder='run'
    else:
        progression,passingopt=(1,1)
        moveorder='run'
    return  progression,passingopt,moveorder
def getattattributes(style):


        if style==POSITIONAL:
            progression = 1
            positionopt = 1
            passingopt=3
        elif style==DIRECT:
            progression = 3
            positionopt = 1
            passingopt=0.5

        else:
            progression = 2
            positionopt = 3
            passingopt=2



        return  progression,positionopt,passingopt
def computepressline(ball,turn):
    if (ceil(ball/4)==1 and turn==-1) :
        return 1
    elif  (ceil(ball/4)==3 and turn==1):
        return 12
    elif (ceil(ball/4)==2 and turn==-1) or (ceil(ball/4)==1 and turn==1):
        return 4
    elif (ceil(ball/4)==2 and turn==1) or (ceil(ball/4)==3 and turn==-1):
        return 8

def getdefattributes(gs,style,turn):


        if style == SITBACK:
            defline = 3 if turn==1 else 10
            pressstarting = 5  if turn==1 else 7
            pressingimp = 3
            backlineimp = 5

        elif style == HIGHPRESS:

            defline = gs.oppplayerhigh

            pressstarting = computepressline(gs.ball[0],turn)

            pressingimp = 5
            backlineimp = 1

        else:
            defline = 5  if turn==1 else 7
            pressstarting = 6  if turn==1 else 6
            pressingimp = 3
            backlineimp = 3

        return defline, pressstarting,pressingimp,backlineimp
def randommove(validmoves):
    print(len(validmoves))
    return validmoves[random.randint(0,len(validmoves)-1)]

def findbestmove(gs,returnqueue):
    global nextmove,secondmove
    global counter
    global attacking
    nextmove = None
    secondmove=None
    attacking = False
    validmoves=gs.getvalidmoves(ai=True,moveorder='run')
    counter = 0
    random.shuffle(validmoves)

    #alphabetarec(gs,validmoves,DEPTH,-GOAL,GOAL,1 if not gs.bluetomove else -1 ,None)
    #negascout(gs,validmoves,alpha,beta,depth_left,1 if not gs.bluetomove else -1 ,None)
    search_controller(gs,validmoves,1 if not gs.bluetomove else -1,DEPTH)
    returnqueue.put([nextmove,secondmove]) if secondmove!=None else returnqueue.put([nextmove])#list of succesive moves for that turn
    print("checkingcounter",counter,nextmove,secondmove)
    #print("score",scoreboar(gs,nextmove,secondmove))
    return  returnqueue

#positive score good for red ; negative score good for blue
def scoreboar(gs,prevmove,latestmove=None,progression=1,passingopt=1):
    score=0
    turn=1 if  not gs.bluetomove else -1
    hz=[0]*6 #for positional play
    vz=[0]*7 #for positional play
    totz=[]
    markedplayers=[]
    penalty = 0 if gs.possession else 1
    style=gs.attstyle[turn] if penalty==0 else gs.defstyle[turn]
    positionimp=1

    if gs.possession:

        progression, positionimp, passingopt=getattattributes(style)
    else:
        defline, pressstarting, pressingimp, backlineimp=getdefattributes(gs,style,turn)

        #print(defline, pressstarting, pressingimp, backlineimp,turn)
    #print("red " if not gs.bluetomove else "blue" ,turn,gs.offside,gs.goalallowed,gs.ispossession())
    if gs.goalallowed not in ('', turn) :
        if turn==1:
         score = score + GOAL
        else :
            score=score-GOAL

    if prevmove.movetype=='t':
        #print(prevmove.moveId,"some tackle chance")
        if turn==1:
         score = score +GOAL
        else :
            score=score-GOAL
    else:

        score = (score + ((13 - gs.ball[0])/2)*progression * turn) if turn < 0 else (score + ((gs.ball[0])/2)*progression * turn)
    try:
        if style==HIGHPRESS:
            score=score-turn*150 if (gs.offside>defline and turn==-1 and gs.ball[0]<defline) or (gs.offside<defline and turn==1 and gs.ball[0]>defline) else score
    except:
        print(defline,style,gs.possession,gs.ispossession())
    #positionimp=2 if penalty==1 else 1  #for positional play
    for i in range(1, 13):
        for j in range(0, 7):
            piece = gs.board[i][j]
            if piece * turn > 0:  # considering only same side i.e the current side turn
                r = i - 1 if turn < 0 else 11 - (i - 1)
                c = j if turn < 0 else 6 - j
                score = score + (piecelog[abs(piece)][penalty][r][c])*turn*positionimp # adding normal positional val


                if penalty==1 and abs(piece)!=1:
                # indicates out of possession
                    #score= score- max(abs(i-gs.ball[0]),abs(j-gs.ball[1]))*turn
                    score= score- (abs(i-gs.ball[0])+abs(j-gs.ball[1]))*turn
                    if style==SITBACK:
                        if abs(piece) in (2,3) and( (i >defline and turn==1 and gs.ball[0]>defline) or (i<defline+1 and turn==-1 and gs.ball[0]<defline)):
                            score=score-5*turn*(i-defline) if turn==1 else score-5*turn*(defline-i)
                        elif abs(piece) in (6,8,10) and( (i >defline+1 and turn==1) or (i<defline and turn==-1)):
                            score = score - 5 * turn * (i - defline+1) if turn == 1 else score - 5 * turn * (defline - i)

                    if abs(piece) in (3,2) and i==gs.offside:#rigid backline
                         score = score + backlineimp * turn
                    try:
                        if  ((i<=pressstarting and turn==1)or (i>=pressstarting and turn==-1)):
                            for (x,y) in defpower[abs(piece)]:
                                if i not in (1, 12) and j not in (0, 6):
                                    p = gs.board[x + (i * turn * 1)][y + (j * turn * 1)]
                                    if p*piece>0:
                                        score = score + pressingimp * turn
                                        if style==HIGHPRESS:
                                            markedplayers.append(abs(x))
                    except:
                        print(defline, style, gs.possession, gs.ispossession(),gs.bluetomove)
                        #if  gs.board[i-1 if piece<0 else i+1][j]*piece<0 :

                        #   score=score+pressingimp*turn#this measuress the extent of pressing
                        #elif j not in (0,6):
                        #   if gs.board[i][j-1]*piece<0 or gs.board[i][j+1]*piece<0:

                         #   score=score+pressingimp*turn*0.75

                elif penalty==0:
                    score = score + gs.possiblepasses * passingopt
                    if style!=POSITIONAL:
                      if i in (4,5,6,7) and j not in (0,6):#if two players are beside with one another
                        if gs.board[i][j - 1] * piece > 0 and gs.board[i][j + 1] * piece > 0:
                           score = score - 15 * turn

                    elif style==POSITIONAL:
                        x=ceil(i/2)-1
                        y=j if j not in (2,3,4) else 3
                        hz[x]+=1
                        vz[y]+=1
                        if hz[x]>3:
                            totz.append(x)
                        if vz[y]>2:
                            totz.append(y+6)


            elif turn* piece<0 and abs(piece)!=1 and ((gs.ball[0]<6 and turn==1)  or (gs.ball[0]>6 and turn==-1) ) and (penalty==0 or style==SITBACK):

                for (x,y) in  defpower[abs(piece)]:
                 if i not in (1,12) and j not in (0,6):
                   p=gs.board[x+(i*turn*-1)][y+(j*turn*-1)]
                   if p*piece>0:

                    score=score-15*turn
                   elif p*piece>0 and abs(p) in (7,9) and style==SITBACK:
                       score = score - 50 * turn


    score = score- (len(markedplayers)-len(set(markedplayers))) * 50 * turn if style == HIGHPRESS else score
    score=score if  style==POSITIONAL else score - len(set(totz)) * 150 * turn
    return score
#new sophisticated evaluationfunction that is based on style of play


#new implementation





def quiesce(gs,validmoves,alpha, beta,depth_left,turnmultiplier,prevmove,latestmove=None,progression=1,passingopt=1):
    """ Apply a Quiescence Search to aid combat the horizon effect """
    global counter
    turn = gs.bluetomove
    progression, passingopt, moveorder = getppm(gs, turn)
    standing_pat = turnmultiplier*scoreboar(gs,prevmove,latestmove,progression,passingopt)

    if standing_pat >= beta:                                      # If current eval >= beta(max score)
        return beta
    alpha = max(alpha, standing_pat)                              # Set lower bound

    for move in gs.getvalidmoves(ai=True):                           # For each possible move:
        if prevmove.movetype in ('s','t') :
            gs.makemove(move)                                 # Get Move
            if (gs.goalallowed == '1' and gs.bluetomove )or( gs.goalallowed=='-1' and not gs.bluetomove):

                return alpha
            elif turn == gs.bluetomove or move.movetype == 'k':

                nextmoves = gs.getvalidmoves(
                    ai=True)  # cutthrough pass is to eliminate the probability that a player would simply attempt a through ball at the end of play
                # generating for 2nd turn
                for mo in nextmoves:

                    counter = counter + 1
                    if (mo.movetype != 'k' ):  # second move th pass more likely to loose ball
                        gs.makemove(mo)  # 2nd turn

                        opponentmoves = gs.getvalidmoves(ai=True,
                                                         tacklemoves=True)  # if depth_left!=1 else []#priortising tackle moves first
                        if len(opponentmoves) != 0:
                            if opponentmoves[0].movetype == 't':
                                gs.undomove()
                                score=beta-1
                                continue
                        score = -quiesce(gs,opponentmoves,-beta, -alpha,depth_left,-turnmultiplier,move)
                        gs.undomove()

            elif move.movetype != 'k' or turn != gs.bluetomove:
                counter = counter + 1

                opponentmoves =[]# gs.getvalidmoves(ai=True)# if depth_left != 1 else []
                score = -quiesce(gs,opponentmoves,-beta, -alpha,depth_left,turnmultiplier,move)


            gs.undomove()                                      # Undo Move

            if score >= beta:
                return beta                                       # Return new score
            alpha = max(alpha, score)                             # Adjust search window

    return alpha

# Searching the best move using NegaScout Search.
def negascout(gs,validmoves, alpha, beta, depth_left,turnmultiplier,prevmove=None,latestmove=None,hashvalue=0,zobristtable=None):
    global  counter
    """
    Searches the best move using NegaScout, incorporating Alpha-Beta Pruning and NegaMax but adding additional
    NegaScout search and calling the Quiesce search.
    :param alpha: current Alpha score.
    :param beta: current Beta score.
    :param depth_left: search depth remaining.
    :return: best score found.
    """
    oldalpha=alpha

    b = beta
    turn = gs.bluetomove
    progression, passingopt, moveorder = getppm(gs, turn)
    #transpostion table code
    tentry=Tretrieve(gs,turn,hashvalue)#must return a single object corresponding to the turn ,ball and hashvalue
    if tentry.depth>=depth_left:
        if tentry.flag==EXACT:
            return tentry.score
        elif tentry.flag==LB :
            alpha=max(alpha,tentry.score)
        elif tentry.flag==UB:
            beta = min(beta,tentry.score)
        if alpha>=beta :
            return tentry.score
    if depth_left == 0:                                      # If max depth reached:
        return quiesce(gs,validmoves,alpha, beta,depth_left,turnmultiplier,prevmove)                     # Complete Quiesce Search
        #return turnmultiplier*scoreboar(gs,prevmove,latestmove)
    possesionatstart = gs.ispossession()
    # heavily peanalising possession losing

    if tentry.depth>=0:
        if tentry.move[0] in gs.getvalidmoves(ai=True,moveorder='pass'):
            gs.makemove(tentry.move[0])
        hashvalue = updateHash(hashvalue, zobristtable, tentry.move[0])
        if len(tentry.move)>1 :
         if tentry.move[1] in gs.getvalidmoves(ai=True,moveorder='pass'):
            gs.makemove(tentry.move[1])
            hashvalue = updateHash(hashvalue, zobristtable, tentry.move[1])

        best_score=-negascout(gs,validmoves,-beta,-alpha,depth_left-1,-turnmultiplier,tentry.move[0],tentry.move[1] if len(tentry.move)>1 else None,hashvalue,zobristtable)
        gs.undomove()
        hashvalue = updateHashundo(hashvalue, zobristtable, tentry.move[0])
        if len(tentry.move)>1:
            gs.undomove()
            hashvalue = updateHashundo(hashvalue, zobristtable, tentry.move[1])
        bestmove=tentry.move
        if best_score>= beta:
            if best_score <= oldalpha:
                ttflag = UB
            elif best_score >= beta:
                ttflag = LB
            else:
                ttflag = EXACT
            Tstore(hashvalue,bestmove, best_score,depth_left,turn, ttflag, gs.ball)

    else:
        best_score = -9999
        for move in gs.getvalidmoves(ai=True):  # finding best move for 1st turn
          if move not in tentry.move:
            gs.makemove(move)  # 1st turn
            hashvalue = updateHash(hashvalue, zobristtable, move)
            # for giving bonus move if it has after one move this will also cover for regaining possession
            if (gs.goalallowed == '1' and gs.bluetomove )or( gs.goalallowed=='-1' and not gs.bluetomove):

                return 9999

            elif turn == gs.bluetomove or move.movetype == 'k':

                nextmoves = gs.getvalidmoves(ai=True,moveorder=moveorder)  # cutthrough pass is to eliminate the probability that a player would simply attempt a through ball at the end of play
                # generating for 2nd turn
                for mo in nextmoves:

                    counter = counter + 1
                    if  (mo.movetype != 'k'):  # second move th pass more likely to loose ball
                        gs.makemove(mo)  # 2nd turn
                        hashvalue = updateHash(hashvalue, zobristtable, mo)
                        opponentmoves = gs.getvalidmoves(ai=True,
                                                         tacklemoves=True)  if depth_left!=1 else []#priortising tackle moves first
                        if len(opponentmoves) != 0:
                            if opponentmoves[0].movetype == 't':
                                gs.undomove()
                                hashvalue = updateHashundo(hashvalue, zobristtable, mo)
                                score=0
                                continue
                        score = -1 * negascout(gs, opponentmoves, -b, -alpha, depth_left - 1, -turnmultiplier, move, mo,hashvalue,zobristtable)

                        # NegaScout Search:
                        if score > best_score:
                            if alpha < score < beta:  # NegaScout condition
                                best_score = max(score, best_score)
                                bestmove=[move,mo]
                            else:

                                best_score = -negascout(gs, opponentmoves, -beta, -score, depth_left - 1, -turnmultiplier, move,mo,hashvalue,zobristtable)
                            """
                            if best_score>=beta:
                                hashvalue = updateHashundo(hashvalue, zobristtable, mo)
                                if best_score <= oldalpha:
                                    ttflag = UB
                                elif best_score >= beta:
                                    ttflag = LB
                                else:
                                    ttflag = EXACT
                                Tstore(hashvalue, bestmove, best_score, depth_left, turn, ttflag, gs.ball)
                        alpha = max(score, alpha)  # Adjust search window
                        if alpha >= beta:  # Alpha Beta Pruning condition
                            return alpha  # Prune branch

                        b = alpha + 1"""
                    gs.undomove()#hash undo done before


            elif move.movetype != 'k' or turn != gs.bluetomove:
                counter = counter + 1

                opponentmoves =[]
                # gs.getvalidmoves(ai=True) if depth_left != 1 else []
                score =-1 * negascout(gs, opponentmoves, -b, -alpha, depth_left - 1, -turnmultiplier, move,None,hashvalue,zobristtable)

                # NegaScout Search:
                if score > best_score:
                    if alpha < score < beta:  # NegaScout condition
                        best_score = max(score, best_score)
                        bestmove=[move]
                    else:

                        best_score = -negascout(gs, opponentmoves, -beta, -score, depth_left - 1, -turnmultiplier, move,None,hashvalue,zobristtable)


            gs.undomove()

            hashvalue = updateHashundo(hashvalue, zobristtable, move)
            if score>best_score and best_score>=beta:
                if best_score <= oldalpha:
                    ttflag = UB
                elif best_score >= beta:
                    ttflag = LB
                else:
                    ttflag = EXACT
                Tstore(hashvalue,bestmove, best_score,depth_left,turn, ttflag, gs.ball)
            alpha = max(score, alpha)  # Adjust search window
            if alpha >= beta:  # Alpha Beta Pruning condition
                return alpha  # Prune branch

            b = alpha + 1
    return best_score

def search_controller(gs,validmoves,turnmultiplier,depth):
    """
    Controls the NegaScout and Quiesce search.
    :return: best move found.
    """
    global nextmove, counter, secondmove, attacking
    zobristtable = initTable()
    hashvalue=computeHash(gs.board,zobristtable)
    moveorder = 'pass'
    best_move = None
    best_value = -9999  # Set as INF (essentially)
    alpha = -10000      # Set as INF (essentially)
    beta = 10000        # Set as INF (essentially)

    turn = gs.bluetomove
    #print(turn)
    #possesionatstart = gs.ispossession()
    # heavily peanalising possession losing
    progression,passingopt,moveorder=getppm(gs,turn)
    for move in gs.getvalidmoves(ai=True,moveorder='run'):#finding best move for 1st turn

        gs.makemove(move) #1st turn
        hashvalue=updateHash(hashvalue,zobristtable,move)
        if  (gs.goalallowed == '1' and gs.bluetomove )or( gs.goalallowed=='-1' and not gs.bluetomove):
            nextmove=move
            secondmove=None
            return
         # for giving bonus move if it has after one move this will also cover for regaining possession
        elif turn==gs.bluetomove or move.movetype=='k':

            nextmoves = gs.getvalidmoves(ai=True,moveorder=moveorder)#cutthrough pass is to eliminate the probability that a player would simply attempt a through ball at the end of play
            #generating for 2nd turn
            for mo in nextmoves:

                counter=counter+1
                if  (mo.movetype!='k' ):#second move th pass more likely to loose ball
                            gs.makemove(mo)#2nd turn
                            hashvalue = updateHash(hashvalue, zobristtable, move)
                            opponentmoves = gs.getvalidmoves(ai=True,tacklemoves=True,cutthroughpass=True) if depth!=1 else []#priortising tackle moves first
                            if len(opponentmoves)!=0:
                                if opponentmoves[0].movetype=='t':
                                    gs.undomove()
                                    hashvalue = updateHashundo(hashvalue, zobristtable, move)
                                    continue
                            score=-1 *negascout(gs,opponentmoves,-beta,-alpha,depth-1,-turnmultiplier,move,mo,hashvalue,zobristtable)


                            if score > best_value:
                                best_value = score

                                secondmove = mo
                                nextmove = move
                            gs.undomove()
                            hashvalue = updateHashundo(hashvalue, zobristtable, move)


        elif move.movetype!='k' and turn!=gs.bluetomove:
                counter=counter+1

                opponentmoves = []

                score =-1 *negascout(gs,opponentmoves,-beta,-alpha,depth-1,-turnmultiplier,move,None,hashvalue,zobristtable)

                if score > best_value:
                    best_value = score

                    secondmove = None
                    nextmove = move


        gs.undomove()
        hashvalue = updateHashundo(hashvalue, zobristtable, move)

