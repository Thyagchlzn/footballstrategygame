import pygame as p
import chessengine as ce
from chessengine import POSITIONAL,SITBACK,DIRECT,HIGHPRESS
import smartmovefinder as smf
import sys
import menus
import  math
from multiprocessing import  Process,Queue
import numpy as np
import  time
from utils import *

#(255,102,0)
scenarioimages=[]
images={}
lineupimages={}
selectedlineupimages={}
rolesimages={}
activatedrolesimages={}
otherimages={}
squareleny=78
squarelenx=98
gspace=3
panelheight=100
MAXGOAL=1
TIMER=60#in seconds
TURNS=25
MUSIC=True




def drawgamestate(gs,validmoves,selected,movetype,infofont,redname,bluename):
    drawboard(gs.ball,gs.board)#draw outline and ball etc
    highlighter(gs, validmoves, selected, movetype)
    drawinfo(gs,movetype,infofont,redname,bluename)
def drawboard(ball,board):
    screen.fill(background_color)
    #menu symbol
    p.draw.line(screen, start_pos=(1,2), end_pos=(15,2), color=(0, 0, 0), width=5)
    p.draw.line(screen, start_pos=(1,10), end_pos=(15,10), color=(0, 0, 0), width=5)
    p.draw.line(screen, start_pos=(1,18),end_pos=(15,18), color=(0, 0, 0), width=5)

    # upper border
    p.draw.line(screen, start_pos=(8*gspace, 8), end_pos=(dimension[0] - 8*gspace, 8), color=border_orange, width=5)
    # lower border
    p.draw.line(screen, start_pos=(8*gspace, dimension[1] - 8), end_pos=(dimension[0] - 8*gspace, dimension[1] - 8),
                color=border_orange, width=5)
    # left border
    p.draw.line(screen, start_pos=(8*gspace, 6), end_pos=(8*gspace, dimension[1] - 6),
                color=border_orange, width=5)
    # right border
    p.draw.line(screen, start_pos=(dimension[0] - 8*gspace, 6), end_pos=(dimension[0] - 8*gspace, dimension[1] - 6),
                color=border_orange, width=5)
    # mid line
    p.draw.line(screen, start_pos=((dimension[0] - 13) / 2, 11), end_pos=((dimension[0] - 13) / 2, dimension[1] - 6),
                color=border_orange, width=6)
    # d box left(up down close)
    p.draw.line(screen, start_pos=(8*gspace, squareleny + 13),
                end_pos=(squarelenx * 2 + 16, squareleny + 13),
                color=border_orange, width=6)
    p.draw.line(screen, start_pos=(8*gspace, squareleny * 6 + 13),
                end_pos=(squarelenx * 2 + 16, squareleny * 6 + 13),
                color=border_orange, width=6)
    p.draw.line(screen, start_pos=(squarelenx * 2 + 13, squareleny + 13),
                end_pos=(squarelenx * 2 + 13, squareleny * 6+ 13),
                color=border_orange, width=6)
    # box right
    p.draw.line(screen, start_pos=(dimension[0] - 8*gspace, squareleny + 13),
                end_pos=(squarelenx * 11 - 43, squareleny + 13),
                color=border_orange, width=6)
    p.draw.line(screen, end_pos=(dimension[0] - 8*gspace, squareleny * 6 + 13),
                start_pos=(squarelenx * 11 - 43, squareleny * 6 + 13),
                color=border_orange, width=6)
    p.draw.line(screen, start_pos=(dimension[0] - 13 - squarelenx * 2, squareleny + 13),
                end_pos=(dimension[0] - squarelenx * 2 - 13, squareleny * 6 + 13),
                color=border_orange, width=6)
    #goalpost
    #left
    p.draw.line(screen, start_pos=(0, squareleny*2 + 13),
                end_pos=(squarelenx  + 16, squareleny*2 + 13),
                color=border_orange, width=6)
    p.draw.line(screen, start_pos=(0, squareleny * 5 + 13),
                end_pos=(squarelenx + 16, squareleny * 5 + 13),
                color=border_orange, width=6)
    p.draw.line(screen, start_pos=(squarelenx + 13, squareleny*2 + 13),
                end_pos=(squarelenx  + 13, squareleny * 5+ 13),
                color=border_orange, width=6)
    #  right
    p.draw.line(screen, start_pos=(dimension[0], squareleny*2 + 13),
                end_pos=(squarelenx * 12 - 43, squareleny*2 + 13),
                color=border_orange, width=6)
    p.draw.line(screen, end_pos=(dimension[0] , squareleny * 5 + 13),
                start_pos=(squarelenx * 12 - 43, squareleny * 5 + 13),
                color=border_orange, width=6)
    p.draw.line(screen, start_pos=(dimension[0] - 13 - squarelenx , squareleny*2 + 13),
                end_pos=(dimension[0] - squarelenx  - 13, squareleny * 5 + 13),
                color=border_orange, width=6)

    # circle
    p.draw.circle(screen, color=border_orange, width=5, center=(dimension[0] / 2 - 6, dimension[1] / 2 - 5), radius=70)
    p.draw.circle(screen, color=border_orange,  center=(dimension[0] / 2 - 6, dimension[1] / 2 - 5), radius=10)
    #penalty kick circle
    p.draw.circle(screen, color=border_orange, center=((squarelenx + 16)+(((squarelenx * 2 + 13)-(squarelenx + 13))/2), dimension[1] / 2 - 5), radius=10)#left
    p.draw.circle(screen, color=border_orange, center=((squarelenx * 11 - 43)+(((squarelenx * 12 - 43)-(squarelenx * 11 - 43))/2), dimension[1] / 2 - 5), radius=10)#right
    #goalnet


    for j in range(7):
        for i in range(14):
            #pitch
            if ball!=(i,j) and (i!=0 and i!=13):
                p.draw.circle(screen, color=(40, 40, 40), center=(58 + ((i-1) * 102), 48 + (j * 78)), radius=25, width=2)

            elif ball==(i,j) and( i!=0 and i!=13):

                p.draw.circle(screen, color=ball_color, center=(58 + ((i-1) * 102), 48 + (j * 78)), radius=25,width=8)
            elif ball[0]==13 :
                p.draw.rect(screen, color=ball_color, rect=p.Rect(dimension[0] - 20, 180 + (ball[1]-2) * squareleny, 20, 60))
            elif ball[0]==0:
                p.draw.rect(screen, color=ball_color,rect=p.Rect(0, 180 + (ball[1] - 2) * squareleny, 20, 60))
            elif ball[0] != 13 and i==13 and j in (2,3,4):
                p.draw.rect(screen, color=(40, 40, 40),
                            rect=p.Rect(dimension[0] - 20, 180 + (j - 2) * squareleny, 20, 60))
            elif ball[0] != 0 and i==0 and j in (2,3,4):
                p.draw.rect(screen, color=(40, 40, 40), rect=p.Rect(0, 180 + (j - 2) * squareleny, 20, 60))

            x = board[i][j]
            if x != 0:
                screen.blit(images[x], p.Rect(39 + ((i - 1) * 102), 29 + (j * 78), 30, 30))

            # arcs and small circles

    PI=math.pi
    p.draw.arc(screen, border_orange, (16 , 0, 50, 50),(3*PI/2)-.6, 2*PI+.6, width=3)#top left corner
    p.draw.arc(screen, border_orange, (1190, 0, 50, 50),   PI/2+.8,0-1.2, width=3)  # top right corner

    p.draw.arc(screen, border_orange, (16, dimension[1] - 48,50,50), 3*PI/2+.8 ,PI-.8, width=3)  # top bottom left corner
    p.draw.arc(screen, border_orange, (1190, dimension[1] - 48, 50, 50),2*PI+1.2,3*PI/2-.8,  width=3)  # top bottom right corner

def highlighter(gs,validmoves,selected,movetype):
    if selected!=():
        r,c=selected
        if gs.board[r][c]*(-1 if gs.bluetomove else 1)>0:#if its same team

            p.draw.circle(screen, (0,0,255,100), center=(58 + ((r-1) * 102), 48 + (c * 78)), radius=28,width=2)

        #highlight possible moves
        for move in validmoves:

           if move.srow==r and move.scol==c :
               if movetype in  ['p','c','r','t'] and move.movetype in ['p','c','r','t']:

                    p.draw.circle(screen, (0, 255, 255, 100), center=(58 + ((move.erow - 1) * 102), 48 + (move.ecol * 78)), radius=28, width=2)
               elif move.movetype==movetype:
                   p.draw.circle(screen, (0, 255, 255, 100),
                                 center=(58 + ((move.erow - 1) * 102), 48 + (move.ecol * 78)), radius=28, width=2)

def loadimages():
    positions=[2,6,3,1,8,7,9,10,-2,-6,-3,-1,-8,-7,-9,-10]

    otherimages['pitch']=p.transform.rotate(p.transform.smoothscale(p.image.load('images/pitch1.jpeg'),(550,400)),90).convert()
    otherimages['scebg'] = p.transform.flip(p.transform.smoothscale(p.image.load('images/scebg.jpeg'), (1300, 800)),True,False).convert()
    otherimages['arsene']= p.transform.smoothscale(p.image.load('images/arsene.jpg'),(1300,600)).convert()
    otherimages['pep']= p.transform.flip(p.transform.smoothscale(p.image.load('images/pep.jpg'),(1300, 700)),True,False).convert()
    otherimages['forbg']= p.transform.smoothscale(p.image.load('images/forbg.jpeg'), (1300, 800)).convert()
    otherimages['backbutton']=p.transform.smoothscale(p.image.load('images/back.png'),(75,75)).convert()
    otherimages['windowicon']=p.image.load('images/strategy.png')
    scenarioimages.append(p.transform.smoothscale(p.image.load('images/matchbg0.jpg'),(1300,700)).convert())
    scenarioimages.append(p.transform.smoothscale(p.image.load('images/matchbg0.jpg'), (1300, 700)).convert())
    scenarioimages.append(p.transform.smoothscale(p.image.load('images/matchbg2.jpeg'), (1300, 700)).convert())
    scenarioimages.append(p.transform.smoothscale(p.image.load('images/matchbg0.jpg'), (1300, 700)).convert())
    scenarioimages.append(p.transform.smoothscale(p.image.load('images/matchbg4.jpeg'), (1300, 700)).convert())

    for i in positions:
        key='a'+str(abs(i)) if i>0 else 'b'+str(abs(i))
        images[i]=p.transform.smoothscale(p.image.load('images/{}.png'.format(key)),(35,35)).convert_alpha()
        if abs(i)!=1 and i>0:
            lineupimages[i] = p.transform.smoothscale(p.image.load('images/{}.png'.format('l'+str(i))), (55, 55)).convert_alpha()
            selectedlineupimages[i] = p.transform.smoothscale(p.image.load('images/{}.png'.format('sl' + str(i))), (55, 55)).convert_alpha()
            rolesimages[i] = p.transform.smoothscale(p.image.load('images/{}.png'.format('f'+str(i))), (55, 65)).convert_alpha()
            activatedrolesimages[i] = p.transform.smoothscale(p.image.load('images/{}.png'.format('af'+str(i))), (55, 65)).convert_alpha()



#def drawmenu(font,):

def main():
    global screen
    screen = p.display.set_mode((dimension[0], dimension[1] + panelheight), 8)
    loadimages()
    p.init()
    clock=p.time.Clock()

    infofont = p.font.Font(ucd, 80)
    p.display.set_icon(otherimages['windowicon'])
    p.display.set_caption("Total Football")

    running=True
    click=True
    while running:
        screen.fill((0,0,0))
        screen.blit(otherimages['arsene'],(0,0))
        mx, my = p.mouse.get_pos()
        txtobj5 = infofont.render('TOTAL FOOTBALL', 0, p.Color('black'))
        txtloc5 = p.Rect(300,10, 390, 200)
        txtobj2 = menufont.render('MATCH', 0, menucolor)
        txtloc2 = p.Rect(940, 300, 90, 60)
        txtobj1 = menufont.render('RULES', 0, menucolor)
        txtloc1 = p.Rect(940, 400, 90, 60)
        txtobj3 = menufont.render('SCENARIOS', 0, menucolor)
        txtloc3 = p.Rect(940, 500, 150, 60)
        txtobj4 = menufont.render('SETTING', 0, menucolor)
        txtloc4 = p.Rect(940, 600, 120, 60)
        screen.blit(txtobj1, txtloc1)
        screen.blit(txtobj2, txtloc2)
        screen.blit(txtobj3, txtloc3)
        screen.blit(txtobj4, txtloc4)
        screen.blit(txtobj5, txtloc5)

        if txtloc2.collidepoint((mx, my)):

            screen.blit(menufont.render('MATCH', 0, highlighter_color), txtloc2)
            if click:
                menus.play_click()
                playmenu(screen)
        elif txtloc1.collidepoint((mx, my)):
            screen.blit(menufont.render('RULES', 0, highlighter_color), txtloc1)
            if click:
                menus.play_click()
                rules(screen)
        elif txtloc3.collidepoint((mx, my)):

            screen.blit(menufont.render('SCENARIOS', 0, highlighter_color), txtloc3)
            if click:
                menus.play_click()
                scenarios(screen)
        elif txtloc4.collidepoint((mx, my)):
            screen.blit(menufont.render('SETTING', 0, highlighter_color), txtloc4)
            if click:
                menus.play_click()
                setting(screen)
        click=False
        for k in p.event.get():
            if k.type==p.QUIT:
                running=False
            elif k.type==p.MOUSEBUTTONDOWN:
                if k.button ==1:
                    click=True
        clock.tick(60)
        p.display.flip()
def scenarios(screen):
    global MUSIC, TURNS, TIMER, MAXGOAL
    p.init()
    clock = p.time.Clock()
    running = True
    click = True


    while running:
        screen.fill((0, 0, 0))
        screen.blit(otherimages['scebg'], (0, 0))
        screen.blit(otherimages['backbutton'], (1150, 25))
        mx, my = p.mouse.get_pos()

        txtobj2 = menufont.render('RMA  VS  BAR ', 0,menucolor)
        txtloc2 = p.Rect(60, 200, 250, 60)
        txtobj3 = menufont.render('JUV  VS  MUN ', 0,menucolor)
        txtloc3 = p.Rect(60, 300, 250, 60)
        txtobj4 = menufont.render('JUV  VS  ARS ', 0,menucolor)
        txtloc4 = p.Rect(60, 400, 250, 60)
        txtobj5 = menufont.render('RMA  VS  BAY ', 0,menucolor)
        txtloc5 = p.Rect(60, 500, 250, 60)
        txtobj6 = menufont.render('LIV  VS  MCI ', 0,menucolor)
        txtloc6 = p.Rect(60, 600, 250, 60)

        txtobj1 = headerfontfilled.render('SCENARIOS', 0, p.Color('white'))
        txtloc1 = p.Rect(500, 60, 150, 100)

        screen.blit(txtobj1, txtloc1)
        screen.blit(txtobj2, txtloc2)
        screen.blit(txtobj3, txtloc3)
        screen.blit(txtobj4, txtloc4)
        screen.blit(txtobj5, txtloc5)
        screen.blit(txtobj6, txtloc6)


        if txtloc2.collidepoint((mx, my)):
            screen.blit(menufont.render('RMA  VS  BAR ', 0, (222,240,122)), txtloc2)
            p.draw.rect(screen, highlighter_color, (48, 200, 250, 48), 4)
            if click:
                menus.play_click()
                scenariossecond(screen,0)
        elif txtloc3.collidepoint((mx, my)):
            screen.blit(menufont.render('JUV  VS  MUN ', 0, (222,240,122)), txtloc3)
            p.draw.rect(screen, highlighter_color, (48, 300, 250, 48), 4)
            if click:
                menus.play_click()
                scenariossecond(screen,0)
        elif txtloc4.collidepoint((mx, my)):
            screen.blit(menufont.render('JUV  VS  ARS ', 0, (222,240,122)), txtloc4)
            p.draw.rect(screen, highlighter_color, (48, 400, 250, 48), 4)
            if click:
                menus.play_click()
                scenariossecond(screen,2)
        elif txtloc5.collidepoint((mx, my)):
            screen.blit(menufont.render('RMA  VS  BAY ', 0, (222,240,122)), txtloc5)
            p.draw.rect(screen, highlighter_color, (48, 500, 250, 48), 4)
            if click:
                menus.play_click()
                scenariossecond(screen,0)
        elif txtloc6.collidepoint((mx, my)):
            screen.blit(menufont.render('LIV  VS  MCI ', 0, (222,240,122)), txtloc6)
            p.draw.rect(screen, highlighter_color, (48, 600, 250, 48), 4)
            if click:
                menus.play_click()
                scenariossecond(screen,4)
        if mx>1150 and my>25 and mx<1225 and my<100 and click:
           running=False
           break
        click = False
        for k in p.event.get():
            if k.type == p.QUIT:
                running = False
                break
            elif k.type == p.MOUSEBUTTONDOWN:
                if k.button == 1:
                    click = True
        clock.tick(60)
        p.display.flip()

def setting(screen):
    global MUSIC,TURNS,TIMER,MAXGOAL
    p.init()
    timerindex=1
    clock = p.time.Clock()
    running=True
    click=True

    infofont = p.font.SysFont('monospace', 32, True, False)

    while running:
        screen.fill((0, 0, 0))

        screen.blit(otherimages['backbutton'], (1150, 25))
        mx, my = p.mouse.get_pos()

        txtobj2 = infofont.render('MUSIC'+('   ON' if MUSIC else '   OFF'), 0, p.Color('white'))
        txtloc2 = p.Rect(400, 250, 90, 60)
        txtobj1 = headerfontfilled.render('SETTINGS', 0, p.Color('white'))
        txtloc1 = p.Rect(400, 100, 150, 100)
        txtobj3 = infofont.render('TIMER   '+'10 20 30 40 50 60 ', 0, p.Color('white'))
        txtloc3 = p.Rect(400, 350, 650, 60)
        txtobj4 = infofont.render('TOTAL TURNS  + -  '+str(TURNS ), 0, p.Color('white'))
        txtloc4 = p.Rect(400, 450, 500, 60)
        txtobj5 = infofont.render('MAX    GOAL  + -  ' + str(MAXGOAL), 0, p.Color('white'))
        txtloc5 = p.Rect(400, 550, 500, 60)
        screen.blit(txtobj1, txtloc1)
        screen.blit(txtobj2, txtloc2)
        screen.blit(txtobj3, txtloc3)
        screen.blit(txtobj4, txtloc4)
        screen.blit(txtobj5, txtloc5)

        if txtloc2.collidepoint((mx, my)):

            screen.blit(infofont.render('MUSIC'+('   ON' if MUSIC else '   OFF'), 0, highlighter_color), txtloc2)
            if click:
                menus.play_click()

                MUSIC=not MUSIC

        elif mx>550 and mx<970 and my>350 and my<380:
            #str(((mx - 450) / 4) * 10)
            #screen.blit(infofont.render(str(math.floor((mx-550)/40)*10), 0, highlighter_color), p.Rect(math.floor((mx-550)/40)*40+550, 350, 700, 60))
            if click:
                menus.play_click()
                timerindex=(math.floor((mx-550)/60))
        elif my>450and my<490 and mx>644 and mx<674 and TURNS<100:

            screen.blit(infofont.render('+', 0, highlighter_color), p.Rect(647, 450, 500, 60))
            if click  :
                menus.play_click()
                TURNS+=5


        elif my>450and my<490 and mx>680 and mx<720 and TURNS>5:

            screen.blit(infofont.render('-', 0, highlighter_color), p.Rect(685, 450, 500, 60))


            if click  :
                menus.play_click()
                TURNS -= 5
        elif my>550and my<590 and mx>644 and mx<674 and MAXGOAL<10:

            screen.blit(infofont.render('+', 0, highlighter_color), p.Rect(648, 550, 500, 60))
            if click  :
                menus.play_click()
                MAXGOAL +=1


        elif my>550and my<590 and mx>680 and mx<720 and MAXGOAL>0:

            screen.blit(infofont.render('-', 0, highlighter_color), p.Rect(686, 550, 500, 60))


            if click  :
                menus.play_click()
                MAXGOAL -= 1

        if mx>1150 and my>25 and mx<1225 and my<100 and click:
           running=False
           break
        p.draw.rect(screen, highlighter_color, ((timerindex * 60 + 550)-timerindex-5, 345, 42, 40), 3)
        click = False
        for k in p.event.get():
            if k.type == p.QUIT:
                running = False
                break
            elif k.type == p.MOUSEBUTTONDOWN:
                if k.button == 1:
                    click = True
        clock.tick(60)
        p.display.flip()
def scenariossecond(screen,matchno):
    p.init()
    clock = p.time.Clock()
    infofont_h = p.font.SysFont('Helvitca', 64, True, True)

    running=True
    click=False
    while running:
        screen.fill((0, 0, 0))

        screen.blit(scenarioimages[matchno],(0,0))
        screen.blit(otherimages['backbutton'], (1150, 25))
        mx, my = p.mouse.get_pos()
        txtobj2 = desfont.render(menus.MATCHDES[matchno], 0, p.Color('white'))
        txtloc2 = p.Rect(40, 250, 90, 60)
        txtobj1 = headerfontfilled.render(menus.MATCH_H[matchno], 0, menucolor)
        txtloc1 = p.Rect(450, 10, 150, 100)
        txtobj3 = desfont.render(menus.MATCHFORMATION[matchno], 0, p.Color('white'))
        txtloc3 = p.Rect(700, 350, 650, 60)
        txtobj4 = desfont.render(menus.MATCHSIDES[matchno], 0, p.Color('white'))
        txtloc4 = p.Rect(700, 450, 500, 60)
        txtobj5 = infofont_h.render('PLAY', 0, p.Color('red'))
        txtloc5 = p.Rect(700, 550, 500, 100)
        screen.blit(txtobj1, txtloc1)
        screen.blit(txtobj2, txtloc2)
        screen.blit(txtobj3, txtloc3)
        screen.blit(txtobj4, txtloc4)
        screen.blit(txtobj5, txtloc5)

        if txtloc5.collidepoint((mx, my)):

            screen.blit(infofont_h.render('PLAY', 0, highlighter_color), txtloc5)
            if click:
                menus.play_click()
                game(clock,blue=True,red=False,whosfirst=1,matchno=matchno,redname=menus.MATCH_H[matchno][:3],bluename=menus.MATCH_H[matchno][7:])

        if mx>1150 and my>25 and mx<1225 and my<100 and click:
           running=False
           break
        click = False

        for k in p.event.get():
            if k.type == p.QUIT:
                running = False
                break
            elif k.type == p.MOUSEBUTTONDOWN:
                if k.button == 1:
                    click = True
        clock.tick(60)
        p.display.flip()
def movesdescription(screen):
    p.init()
    clock = p.time.Clock()
    click = False
    while True:
        screen.fill((1, 1, 1))
        screen.blit(otherimages['backbutton'], (1150, 25))
        mx, my = p.mouse.get_pos()
        txtobj1 = headerfontfilled.render('RULES', 0, p.Color('white'))
        txtloc1 = p.Rect(550, 10, 150, 100)
        screen.blit(txtobj1, txtloc1)
        txtobj3 = menufont.render('PASSING:', 0, menucolor)
        txtloc3 = p.Rect(10, 100, 40, 40)
        screen.blit(txtobj3,txtloc3)

        if mx > 1150 and my > 25 and mx < 1225 and my < 100 and click:
            break
        for i in range(0,4):
            txtobj2=desfont2.render(RULES.PASSINGSTYLES[i],0,menucolor)
            txtloc2=p.Rect(10,200+i*40,40,40)
            screen.blit(txtobj2, txtloc2)
            txtobj2=desfont2.render(RULES.PASSINGSTYLESDES[i],0,p.Color('white'))
            txtloc2=p.Rect(170,200+i*40,80,40)
            screen.blit(txtobj2,txtloc2)


        click = False
        for k in p.event.get():
            if k.type == p.QUIT:
                return
            elif k.type == p.MOUSEBUTTONDOWN:
                click = True

        clock.tick(60)
        p.display.flip()


def playerpower(screen):
    p.init()
    clock = p.time.Clock()
    click = False
    while True:
        screen.fill((1, 1, 1))
        screen.blit(otherimages['backbutton'], (1150, 25))
        mx, my = p.mouse.get_pos()
        txtobj1 = headerfontfilled.render('RULES', 0, p.Color('white'))
        txtloc1 = p.Rect(550, 10, 150, 100)
        txtobj5 = menufont.render('NEXT', 0, menucolor)
        txtloc5 = p.Rect(1150, 600, 60, 60)
        screen.blit(txtobj5,txtloc5)
        screen.blit(txtobj1,txtloc1)

        if mx > 1150 and my > 25 and mx < 1225 and my < 100 and click:
            break
        elif txtloc5.collidepoint((mx,my)):
          screen.blit(menufont.render('NEXT', 0, highlighter_color), txtloc5)
          if click:
            movesdescription(screen)
        for i in range(0,len(RULES.ROLE)):
            font,color=(desfont2,p.Color('white')) if i!=0 else (menufont,menucolor)
            txtobj2=font.render(RULES.ROLE[i],0,color)
            txtloc2=p.Rect(10,70+i*70,40,40)
            screen.blit(txtobj2,txtloc2)
            txtobj2=font.render(RULES.PASS[i],0,color)
            txtloc2 = p.Rect(140, 70 + i * 70, 40, 40)
            screen.blit(txtobj2, txtloc2)
            txtobj2 = font.render(RULES.RUN[i], 0, color)
            txtloc2 = p.Rect(550, 70 + i * 70, 40, 40)
            screen.blit(txtobj2, txtloc2)
            font=arrowsfont if font!=menufont else font
            txtobj2 = font.render(RULES.TACKLE[i], 0, color)
            txtloc2 = p.Rect(920, 70 + i * 70, 40, 40)
            screen.blit(txtobj2, txtloc2)


        click = False
        for k in p.event.get():
            if k.type == p.QUIT:
                return
            elif k.type == p.MOUSEBUTTONDOWN:
                click = True

        clock.tick(60)
        p.display.flip()


def rules(screen):
    p.init()
    clock = p.time.Clock()
    click=False
    while True:
        screen.fill((1,1,1))
        screen.blit(otherimages['backbutton'], (1150, 25))
        mx, my = p.mouse.get_pos()
        txtobj1 = headerfontfilled.render('RULES', 0, p.Color('white'))
        txtloc1 = p.Rect(550, 10, 150, 100)
        txtobj4=desfont2.render('This game is a variation of chess that incorporates principles of football',0,p.Color('white'))
        txtloc4=p.Rect(10,100,40,40)
        txtobj3=menufont.render('IMPORTANT KEYS:',0,menucolor)
        txtloc3=p.Rect(10,450,40,40)
        txtobj5=menufont.render('NEXT',0,menucolor)
        txtloc5=p.Rect(1150,600,60,60)
        for i in range(0, 2):
            txtobj2=menufont.render(RULES.SUBHEADS[i],0,menucolor)
            txtloc2=p.Rect(10,120+i*120,50,50)
            screen.blit(txtobj2, txtloc2)

        for i in range(0,2):
            txtobj2=desfont2.render(RULES.TURNS[i],0,p.Color('white'))
            txtloc2=p.Rect(30,170+i*40,40,40)
            screen.blit(txtobj2, txtloc2)
        for i in range(0,4):
            txtobj2=desfont2.render(RULES.PLAYINGSTYLES[i],0,menucolor)
            txtloc2=p.Rect(10,300+i*40,40,40)
            screen.blit(txtobj2, txtloc2)
            txtobj2=desfont2.render(RULES.PLAYINGSTYLESDES[i],0,p.Color('white'))
            txtloc2=p.Rect(170,300+i*40,80,40)
            screen.blit(txtobj2,txtloc2)
        for i in range(0,5):
            txtobj2=desfont2.render(RULES.IMPORTANTKEYS[i],0,p.Color('white'))
            txtloc2=p.Rect(30,500+i*35,80,40)
            screen.blit(txtobj2,txtloc2)
        screen.blit(txtobj1,txtloc1)
        screen.blit(txtobj4, txtloc4)
        screen.blit(txtobj3,txtloc3)
        screen.blit(txtobj5,txtloc5)


        if mx>1150 and my>25 and mx<1225 and my<100 and click:
            break
        elif txtloc5.collidepoint((mx,my)):
            screen.blit(menufont.render('NEXT', 0, highlighter_color), txtloc5)
            if click:
                playerpower(screen)

        click=False
        for k in p.event.get():
            if k.type==p.QUIT:
                return
            elif k.type == p.MOUSEBUTTONDOWN:
                click = True

        clock.tick(60)
        p.display.flip()

def setformation(screen,formation,lineup):
    p.init()
    clock = p.time.Clock()
    activated=0
    selected=(10,10)

    #denoted indices in lineup array so 10 is chosen instead of 0
    click=False

    while True:

        screen.fill((0,0,0))

        mx, my = p.mouse.get_pos()
        screen.blit(otherimages['forbg'], (0, 0))
        screen.blit(otherimages['backbutton'], p.Rect(1150, 25,75,75))
        #player formation

        topheadingobj1=menufont.render("FORMATION",0,p.Color((255, 96, 0)))
        topheadingloc1 = p.Rect(170, 30 , 90, 60)
        screen.blit(topheadingobj1, topheadingloc1)

        topheadingobj2 = menufont.render("PLAYER ROLES", 0,  p.Color((255, 96, 0)))
        topheadingloc2 = p.Rect(720, 70, 90, 60)
        screen.blit(topheadingobj2, topheadingloc2)
        screen.blit(otherimages['pitch'],p.Rect(100,100,500,500))
        #player roles

        positions=np.array([[2,3,0],[6,8,10],[7,9,0]])
        #drawing formation
        for j in range(0,3):
            for i in range(0,5):
                key=lineup[j][i]
                if key!=0:

                    if  selected[0]==j and selected[1]==i :

                            screen.blit(selectedlineupimages[key], p.Rect(130 + (i * 70), 150 + (j * 120), 55, 55))
                    else:
                            screen.blit(lineupimages[key],p.Rect(130+(i*70),150+(j*120),55,55))
        roleheading=["DEF","MID","ATT"]
        for j in range(0, 3):
            headobj2 = nsemiboldfont.render(roleheading[j], 0,
                                         p.Color((101, 174, 241)))
            headloc2 = p.Rect(725, 140+ (j * 70), 90, 60)

            screen.blit(headobj2, headloc2)

            for i in range(0,3 if j==1 else 2):
                key = positions[j][i]
                if key==activated:

                    screen.blit(activatedrolesimages[key],p.Rect(795+(i*70),130+(j*70),55,55))
                else:
                    screen.blit(rolesimages[key], p.Rect(795 + (i * 70), 130 + (j * 70), 55, 55))
        click=False
        for k in p.event.get():
            if k.type==p.QUIT or(mx>1150 and my>25 and mx<1225 and my<100 and click):
                for j in range(2, -1,-1):
                    noofnonzeros=0
                    for i in range(4, -1,-1):
                        if lineup[j][i]!=0:
                            noofnonzeros+=1
                    formation=formation[:4-2*j]+str(noofnonzeros)+formation[(4-2*j)+1:]

                return (formation,lineup)
            elif k.type==p.MOUSEBUTTONDOWN:
                click=True
                location = p.mouse.get_pos()

                if location[0]>795 and location[0]<925 and location[1]>130 and location[1]<340:
                    key=positions[(location[1]-120)//70][(location[0]-795)//70]

                    if key==activated:#unclick
                        activated=0
                    elif key!=activated:#click
                        activated=key
                elif location[0]>925 and location[0]<995 and location[1]>200 and location[1]<270:
                    key = positions[1][2]

                    if key == activated:  # unclick
                        activated = 0
                    elif key != activated:  # click
                        activated = key
                elif location[0]>130 and location[0]<465 and location[1]>150 and location[1]<440:
                    lineupposition=[(location[1]-150)//95,(location[0]-130)//70]
                    if activated!=0 :
                        if lineup[lineupposition[0]][lineupposition[1]]!=0:
                            lineup[lineupposition[0]][lineupposition[1]]=activated
                            activated=0
                    else:
                        if selected==(10,10):
                            selected=lineupposition
                        else:
                            temp=lineup[selected[0]][selected[1]]
                            lineup[selected[0]][selected[1]] = lineup[lineupposition[0]][lineupposition[1]]
                            lineup[lineupposition[0]][lineupposition[1]]=temp
                            selected=(10,10)
                else:
                    selected=(10,10)
                    activated=0

        clock.tick(60)
        p.display.flip()

def playmenu(screen):
    #global screen
    p.init()
    endfont=p.font.SysFont('Helvitca',64,True,False)
    infofont=p.font.SysFont('monospace',32,True,False)

    #screen = p.display.set_mode((dimension[0],dimension[1]+panelheight))
    whosfirst=0
    clock=p.time.Clock()
    running=False
    blue=True
    red=True
    battstyle1=True
    bdefstyle1=True
    battstyle2=True
    bdefstyle2=True
    attstyle = ['Positional','Direct']
    defstyle=[ 'Sitback','Highpress']
    click=False
    redformationstr='4-3-3'
    blueformationstr='4-3-3'
    redlineup=np.array([[7,0,9,0,7],[0,10,6,8,0],[0,2,3,3,2]])
    bluelineup = np.array([[7,0,10,0,7],[0,8,6,8,0],[0,2,3,3,2]])

    while not running:


        screen.fill((0,0,0))
        screen.blit(otherimages['pep'], (0, 0))
        screen.blit(otherimages['backbutton'], (1150, 25))
        mx, my = p.mouse.get_pos()

        txtobj2 = menufont.render('RED: '+ ' PLAYER ' if red else 'RED: '+' CPU', 0, menucolor)
        txtloc2 = p.Rect(600, 220, 90, 60)
        addtxtobj1=nsemiboldfont.render('Att:'+attstyle[0] if battstyle1 else 'Att:'+attstyle[1], 0, p.Color('grey'))
        addtxtloc1 = p.Rect(580, 300, 150, 60)
        addtxtobj3= nsemiboldfont.render('Def:' + defstyle[0] if bdefstyle1 else 'Def:' + defstyle[1], 0, p.Color('grey'))
        addtxtloc3 = p.Rect(580, 360, 150, 60)
        screen.blit(txtobj2, txtloc2)
        if not red:
            screen.blit(addtxtobj1, addtxtloc1)
            screen.blit(addtxtobj3, addtxtloc3)
        txtobj3 = menufont.render('BLUE: '+ 'PLAYER ' if blue else 'BLUE: '+' CPU', 0, menucolor)
        txtloc3 = p.Rect(900, 220, 90, 60)

        addtxtobj2=nsemiboldfont.render('Att:'+attstyle[0] if battstyle2 else 'Att:'+attstyle[1], 0, p.Color('grey'))
        addtxtloc2 = p.Rect(900, 300, 150, 60)
        addtxtobj4 = nsemiboldfont.render('Def:' + defstyle[0] if bdefstyle2 else 'Def:' + defstyle[1], 0, p.Color('grey'))
        addtxtloc4 = p.Rect(900, 360, 150, 60)
        screen.blit(txtobj3, txtloc3)
        txtobj4 = menufont.render('In Possession', 0,
                                     menucolor)
        txtloc4 = p.Rect(600+(whosfirst*300), 500, 250, 60)

        screen.blit(txtobj4, txtloc4)
        if not blue:
            screen.blit(addtxtobj2, addtxtloc2)
            screen.blit(addtxtobj4, addtxtloc4)
        txtobj = endfont.render('PLAY ', 0, p.Color((189, 6, 14)))
        txtloc = p.Rect(800, 620, 90, 60)
        screen.blit(txtobj, txtloc)
        redformationobj=menufont.render('Shape: '+redformationstr,0,menucolor)
        redformationloc=p.Rect(600,430,90,60)
        screen.blit(redformationobj,redformationloc)
        blueformationobj = menufont.render('Shape: '+blueformationstr, 0, menucolor)
        blueformationloc = p.Rect(900, 430, 90, 60)
        screen.blit(blueformationobj,blueformationloc)
        if txtloc.collidepoint((mx,my)):
          screen.blit(endfont.render('PLAY ', 0, highlighter_color), txtloc)
          if click:
            menus.play_click()
            dattstyle={1:POSITIONAL if battstyle1 else DIRECT,-1:POSITIONAL if battstyle2 else DIRECT}
            ddefstyle = {1:SITBACK if bdefstyle1 else  HIGHPRESS, -1:SITBACK if bdefstyle2 else  HIGHPRESS}
            game(clock,blue,red,bluelineup,redlineup,whosfirst,dattstyle,ddefstyle)
        elif txtloc2.collidepoint((mx,my)):
           screen.blit(menufont.render('RED: '+ ' PLAYER ' if red else 'RED: '+' CPU', 0, highlighter_color), txtloc2)
           if click:
               menus.play_click()
               red=not red
        elif txtloc3.collidepoint((mx, my)):
            screen.blit(menufont.render('BLUE: '+ 'PLAYER ' if blue else 'BLUE: '+' CPU', 0, highlighter_color), txtloc3)
            if click:
                menus.play_click()
                blue=not blue
        elif txtloc4.collidepoint((mx, my)):
            if click:
                menus.play_click()
                whosfirst=1-whosfirst
        elif addtxtloc1.collidepoint((mx, my)) and not red:
            screen.blit(nsemiboldfont.render('Att:'+attstyle[0] if battstyle1 else 'Att:'+attstyle[1], 0, highlighter_color),addtxtloc1)
            if click:
                menus.play_click()
                battstyle1=not battstyle1
        elif addtxtloc2.collidepoint((mx, my)) and not blue :
            screen.blit(nsemiboldfont.render('Att:' + attstyle[0] if battstyle2 else 'Att:' + attstyle[1], 0,
                                        highlighter_color), addtxtloc2)
            if click:
                menus.play_click()
                battstyle2=not battstyle2
        elif addtxtloc3.collidepoint((mx, my)) and not red:
            screen.blit(nsemiboldfont.render('Def:'+defstyle[0] if bdefstyle1 else 'Def:'+defstyle[1], 0, highlighter_color),addtxtloc3)
            if click:
                menus.play_click()
                bdefstyle1=not bdefstyle1
        elif addtxtloc4.collidepoint((mx, my)) and not blue :
            screen.blit(nsemiboldfont.render('Def:' + defstyle[0] if bdefstyle2 else 'Def:' + defstyle[1], 0,
                                        highlighter_color), addtxtloc4)
            if click:
                menus.play_click()
                bdefstyle2=not bdefstyle2
        elif redformationloc.collidepoint((mx, my)):
            screen.blit(menufont.render('Shape: ' + redformationstr, 0, highlighter_color), redformationloc)
            if click:
                menus.play_click()
                redformationstr,redlineup=setformation(screen,redformationstr,redlineup)
        elif blueformationloc.collidepoint((mx, my)):
            screen.blit(menufont.render('Shape: '+blueformationstr, 0, highlighter_color),blueformationloc)
            if click:
                menus.play_click()
                blueformationstr,bluelineup=setformation(screen,blueformationstr,bluelineup)
        if mx>1150 and my>25 and mx<1225 and my<100 and click:
           running=False
           break

        click=False
        for k in p.event.get():
            if k.type==p.QUIT:
                return
            elif k.type==p.MOUSEBUTTONDOWN:
                if k.button ==1:
                    click=True
        clock.tick(60)
        p.display.flip()


def game(clock,blue,red,bluelineup=np.array([[7,0,10,0,7],[0,8,6,8,0],[0,2,3,3,2]]),redlineup=np.array([[7,0,9,0,7],[0,10,6,8,0],[0,2,3,3,2]]),whosfirst=0,dattstyle=None,ddefstyle=None,matchno=-1,redname='RED',bluename="BLUE"):
    global turnsleft
    running=False
    turnsleft = TURNS
    maxgoal = MAXGOAL
    timer = TIMER

    if matchno==-1:
        gs = ce.GameState(bluelineup,redlineup,whosfirst,dattstyle,ddefstyle)

    else:
        gs = ce.GameState(bluelineup, redlineup, menus.MWHOSTARTS[matchno], menus.MATTSTYLE[matchno], menus.MDEFSTYLE[matchno])

        gs.restart(menus.MBOARD[matchno],menus.MBALL[matchno])
        maxgoal = menus.MOTHERINFO[matchno]['maxgoal']
        turnsleft=menus.MOTHERINFO[matchno]['turns']
        print(gs.bluetomove,gs.movesperturn)


    validmoves=gs.getvalidmoves()
    animate=False

    mademove=False #flag to update the listonly when a valid move is made and not for every fps
    #functionality flags
    movetype = 'c'#flag indicates whether to pass,flag to regain posseion,flag to shoot spl for strikers ,default player try to carry ball
    selected = ()
    selectedlist = []

    drawgamestate(gs, validmoves, selected, movetype,menufont,redname,bluename)
    time.sleep(5)
    menus.play_start()
    matchend=False
    playerone=blue#true if human plays blue
    playertwo=red#true if human plays red
    aithinking=False
    movefinderprocess=None
    moveundone=False
    #initialzing timer
    if (gs.bluetomove and playerone) or (not gs.bluetomove and playertwo):
        lastrec=time.time()
    while not running:
        humanturn=(gs.bluetomove and playerone) or (not gs.bluetomove and playertwo)
        for e in p.event.get():
            if e.type==p.QUIT:
                running=not running
            #mouse captures
            elif e.type==p.MOUSEBUTTONDOWN:
                if not matchend :
                    location=p.mouse.get_pos()

                    if location[0]<30:
                        row=0
                    elif location[0]>dimension[0]-30:
                        row=13
                    else:
                        row=(location[0]//102)+1
                    col=location[1]//78



                    if selected==(row,col) or col>=7:
                        selected=()
                        selectedlist=[]
                    else:
                        selected = (row,col)
                        enemycolor=1 if gs.bluetomove else -1
                        allycolor=-1 if gs.bluetomove else 1

                        #print('check', gs.ball, selected,movetype,enemycolor,gs.board[row][col][0])
                        if movetype in ['c' ,'r','t','p'] and len(selectedlist)==1 :#not allowing shoot and spl pass
                            #print('testing for ally color')
                            if gs.board[selectedlist[0][0]][selectedlist[0][1]]*allycolor>0:#not allowing any case whose 1st touch is not same team player

                                if (gs.board[row][col]==0) and row not in (0,13):
                                    #print('r or c',gs.ball,selected)
                                    movetype='c'if gs.ball==selectedlist[0] else 'r'
                                elif  selectedlist[0]== gs.ball and (gs.board[row][col]*allycolor>0 or (row in (0,13) and col in (2,3,4))):
                                    #print('pass selected')
                                    movetype='p'
                                elif  (gs.board[row][col]*enemycolor>0) and gs.ball==selected:
                                    #print('here')
                                    movetype='t'

                        selectedlist.append(selected)

                    if len(selectedlist)==2 and humanturn:
                        move=ce.Move(selectedlist[0],selectedlist[1],gs.board,movetype,gs.ball)

                        if move in validmoves:
                            flag=gs.bluetomove
                            gs.makemove(move)
                            print("human move information", move.piecemoved, move.moveId, gs.movesperturn, gs.bluetomove)
                            turnsleft = turnsleft - 1 if flag!=gs.bluetomove else turnsleft

                            #for func checking
                            #smf.scoreboard(gs, move, checking=True)#need to be removed
                            mademove=True
                            animate=True
                            selectedlist = []
                            selected = ()

                        else:
                            #label=myfont.render('wrong move',1,(255,0,0))
                            #screen.blit(label, label.get_rect(center=(200, dimension[1] - 20)))
                            selectedlist=[selected]
                            print('wrong move')


            #keyboard captures
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undomove()

                    mademove=True
                    animate=False
                    matchend=False
                    if aithinking:
                        movefinderprocess.terminate()
                        aithinking=False
                    moveundone=True
                #recording functionalty flags

                if e.key==p.K_k :#k as through ball in fifa 19
                    movetype='k'

                elif e.key==p.K_s :
                    movetype = 's'

                elif e.key==p.K_c:#can determine type only before selecting the 1st piece
                    movetype = 'c'
                elif e.key==p.K_r:
                    gs=ce.GameState(bluelineup,redlineup,whosfirst)
                    turnsleft=100
                    validmoves=gs.getvalidmoves()
                    mademove=False
                    animate=False
                    matchend=False
                    selectedlist=[]
                    selected=()
                    movetype='c'
                    if aithinking:
                        movefinderprocess.terminate()
                        aithinking=False
                    moveundone=True
        #ai turn
        if not matchend and not humanturn and not moveundone :
            if not aithinking:
                aithinking=True
                returnqueue=Queue()
                movefinderprocess=Process(target=smf.findbestmove,args=(gs,returnqueue))
                movefinderprocess.start()
                print('AI THINKING')
                    #move=smf.findbestmove(gs,validmoves)

                if  movefinderprocess.is_alive():
                    aimovelist=returnqueue.get()#list of successive moves for ai
                    print('DONE THINKING')
                    #if aimovelist[0]==None or aimovelist[1]==None:
                    #    aimovelist=[smf.randommove(validmoves),smf.randommove(validmoves)]
                    #prev=gs.possession
                        #aimovelist[1] =
                    if aimovelist[0]!=None:
                        inturn=gs.bluetomove
                        for aimove in aimovelist:#making suitable for any no of moves
                            if gs.bluetomove==inturn:
                                #print("no of moves and whos turn",gs.movesperturn,gs.bluetomove)
                                gs.makemove(aimove)

                                #print("move information",aimove.piecemoved,aimove.moveId)
                        turnsleft-=1
                    #gs.makemove(aimovelist[1])
                    #smf.scoreboard(gs,aimovelist[-1],checking=True)
                    mademove=True
                    animate=True
                    aithinking=False
                if turnsleft==0:
                    movefinderprocess.terminate()

        if mademove:
            if animate:
                animation(gs.log[-1],clock,gs.board,gs.ball)
            validmoves=gs.getvalidmoves()
            mademove=False
            animate=False
            moveundone=False
        drawgamestate(gs, validmoves, selected, movetype,menufont,redname,bluename)
        #if round(time.time()-lastrec,2)>timer and humanturn:

        #    lastrec=time.time()

        #displaying result
        if (gs.redscore==maxgoal or gs.bluescore==maxgoal) :
            winner = redname+' won ' if gs.redscore==maxgoal else redname+' won '
            drawendtext(winner,p.font.Font(sablonblack,80))
            matchend = True
            gs.goalallowed = ''
        elif gs.goalallowed !='' and (gs.redscore<maxgoal and gs.bluescore<maxgoal) :

            gs.restart(ce.GameState(bluelineup,redlineup,1 if gs.goalallowed=='-1' else 0,dattstyle,ddefstyle).board,(8,3) if gs.goalallowed=='-1' else (5,3))
            gs.goalallowed=''
        if turnsleft==0 :
          if gs.redscore==gs.bluescore:
            drawendtext("draw",p.font.Font(sablonblack,80))
            matchend=True
          else:
              matchend=True
              winner = redname+' won ' if gs.redscore >gs.bluescore else redname+' won '

              drawendtext(winner,p.font.Font(sablonblack,80))
        clock.tick(60)
        p.display.flip()
def drawinfo(gs,movetype,font,redname,bluename):
    global turnsleft
    turn=bluename if gs.bluetomove else redname
    #font = p.font.SysFont('Helvitca', 64, True, False)
    txtobj = font.render('TURN :'+turn, 0, p.Color('black'))
    txtloc = p.Rect(20,dimension[1], 90, 60)
    screen.blit(txtobj, txtloc)

    txtobj = font.render('TURNS LEFT :'+str(turnsleft), 0, p.Color('black'))
    txtloc = p.Rect(260, dimension[1], 90, 60)
    screen.blit(txtobj, txtloc)
    txtobj = ledboardfont.render(str(gs.bluescore)+' : ' + str(gs.redscore), 0, p.Color('black'))
    txtloc = p.Rect(660, dimension[1], 90, 60)
    screen.blit(txtobj, txtloc)
    txtobj = font.render('MODE :'+movetype, 0, p.Color('black'))
    txtloc = p.Rect(880, dimension[1], 90, 60)
    screen.blit(txtobj, txtloc)
    #txtobj = font.render('TIMER :' + str(round(time.time()-lastrec,2)), 0, p.Color('black'))
    #txtloc = p.Rect(1050, dimension[1], 90, 60)
    #screen.blit(txtobj, txtloc)

def drawendtext(winner,font):

    txtobj=font.render(winner,0,p.Color('grey'))
    txtloc=p.Rect(dimension[0]/2-txtobj.get_width(),dimension[1]/2-txtobj.get_height(),900,400)
    screen.blit(txtobj,txtloc)
    txtobj = font.render(winner, 0, p.Color('black'))
    txtloc = p.Rect(dimension[0] / 2 - txtobj.get_width()+2, dimension[1] / 2 - txtobj.get_height()+2, 900, 400)
    screen.blit(txtobj, txtloc)

def animation(move,clock,board,ball):

    if move.movetype in ('k','p','s'):
        menus.play_move()
    if move.movetype == 't':
        dr = -move.erow + move.srow
        dc = -move.ecol + move.scol
    else:
        dr=move.erow-move.srow
        dc=move.ecol-move.scol
    if ball[0] in (0,13):
        menus.play_end()
    framesper=20
    framescount=(abs(dr)+abs(dc))*framesper

    for frame in range(framescount+1):
        if move.movetype == 't':
            r,c=(move.erow+dr*frame/framescount,move.ecol+dc*frame/framescount)
        else:
            r,c=(move.srow+dr*frame/framescount,move.scol+dc*frame/framescount)

        drawboard(ball,board)

           #draw images
        if move.movetype  == 'c':
            # erase the piece in starting pos
            p.draw.circle(screen, color=background_color, center=(58 + ((move.erow - 1) * 102), 48 + (move.ecol * 78)),
                          radius=25)
            p.draw.circle(screen, color=(158, 158, 159), center=(58 + ((move.erow - 1) * 102), 48 + (move.ecol * 78)), radius=25,
                          width=2)
            # erasing ball circle movement all ready done

            # moving ball
            p.draw.circle(screen, color=ball_color, center=(58 + ((r - 1) * 102), 48 + (c * 78)), radius=25, width=8)

            screen.blit(images[move.piecemoved], p.Rect(39 + ((r - 1) * 102), 29 + (c * 78), 30, 30))
        elif move.movetype == 'r':
            # erase the piece in starting pos
            p.draw.circle(screen, color=background_color, center=(58 + ((move.erow - 1) * 102), 48 + (move.ecol * 78)),
                          radius=25)
            p.draw.circle(screen, color=(158, 158, 159), center=(58 + ((move.erow - 1) * 102), 48 + (move.ecol * 78)), radius=25,
                          width=2)

            screen.blit(images[move.piecemoved], p.Rect(39 + ((r - 1) * 102), 29 + (c * 78), 30, 30))

        elif move.movetype in ('k','p'):
            #erasing original
            p.draw.circle(screen, color=background_color, center=(58 + ((move.erow - 1) * 102), 48 + (move.ecol * 78)),
                          radius=25)
            p.draw.circle(screen, color=(158, 158, 159), center=(58 + ((move.erow - 1) * 102), 48 + (move.ecol * 78)), radius=25,
                          width=2)
            if move.piececaptured!=0:
                screen.blit(images[move.piececaptured], p.Rect(39 + ((move.erow - 1) * 102), 29 + (move.ecol* 78), 30, 30))

            #moving
            p.draw.circle(screen, color=ball_color, center=(58 + ((r - 1) * 102), 48 + (c * 78)), radius=25, width=8)
        elif move.movetype =='t':
            # erasing original
            p.draw.circle(screen, color=background_color, center=(58 + ((move.srow - 1) * 102), 48 + (move.scol * 78)),
                          radius=25)
            p.draw.circle(screen, color=(158, 158, 159), center=(58 + ((move.srow - 1) * 102), 48 + (move.scol * 78)),
                          radius=25,
                          width=2)
            if move.piecemoved!=0:
                screen.blit(images[move.piecemoved], p.Rect(39 + ((move.srow - 1) * 102), 29 + (move.scol* 78), 30, 30))

            # moving
            p.draw.circle(screen, color=ball_color, center=(58 + (((r) - 1) * 102), 48 + (c) * 78), radius=25, width=8)

        p.display.flip()
        clock.tick(60)


if __name__=='__main__':
    main()