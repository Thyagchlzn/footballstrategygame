import pygame as p
import os
p.font.init()
ucd = os.path.join("tools", "ucd.ttf")
sablonblack = os.path.join("tools", "sblackalt.otf")
sablonwhite = os.path.join("tools", "swhitealt.otf")
ledboard=os.path.join("tools", "scoreboard.ttf")
nsemibold=os.path.join("tools", "cfsans.ttf")
premier=os.path.join("tools", "Premier2019.ttf")
teamjersey=os.path.join("tools", "TeamJersey96.ttf")
sportsspirit=os.path.join("tools", "sportsspirit.ttf")
arrows=os.path.join("tools", "arrows.ttf")
menucolor=p.Color((224, 62, 40))
menufont=p.font.Font(premier, 44)
nsemiboldfont=p.font.Font(nsemibold,32)
desfont=p.font.Font(sportsspirit,36)
headerfont=p.font.Font(sablonwhite,64)
headerfontfilled=p.font.Font(sablonblack,64)
ledboardfont=p.font.Font(ledboard,44)
desfont2=p.font.Font(sportsspirit,28)
arrowsfont=p.font.Font(arrows,28)
ball_color=(1,1,1)#(255,102,0)
highlighter_color=(252, 5, 108)
border_orange= (236,100,17) #(255,255,255)
background_color =(56, 57, 59)#(56,65,75)#(169, 169, 169)
dimension=(1050+98*2,578)

class RULES:
    SUBHEADS=['TURNS:','PLAYING STYLES:']
    TURNS=["In possession 2 moves per turn, out of possession 1 move per turn ","If ball regained in 1st move then another move is awarded"]
    PLAYINGSTYLES=['POSITIONAL: ','DIRECT: ','HIGHPRESS: ','SITBACK: ']
    PLAYINGSTYLESDES=['Plays as defined by Rinus Michels','Plays based on low no of passes,long passes to score goals','goes man to man with the aim of winning ball high up','compact shape, no space between lines, forces oppn to wings']
    IMPORTANTKEYS=['c: moves with or without ball','k: through pass for 10 and 8','s: shoots even when an oppn non gk payer blocking goal inside d box','z: undo  moves [ not to use when AI is moving ]','r: resets the board']
    ROLE=['ROLE','1(GK)','2(FB)','3(CB)','6(CDM)','8(CM)','10(CAM)','7(W)','9(ST)']
    PASS=['PASS','NP','NP ,LOB PASS','NP','NP ,LOB PASS','NP ,LOB PASS, THROUGH PASS','NP ,LOB PASS, SPECIAL PASS','NP','NP ,SHOOT']
    PASSINGSTYLES=['NP: ','LOB: ','THROUGH: ','SPECIAL: ']
    PASSINGSTYLESDES=['No oppn player in  between them','No oppn player one step ahead of passer and behind receiver','Only applicable if the region is empty with k mode on','Through and NP applicable for 2 spaces in any direction']
    RUN=['RUN(WITH BALL)','1','2 [ 1 ]','1','1','1','1','2 [ 1 ]','1']
    TACKLE=['TACKLE [In Dir]','','4','485+976-','6-5+4','6-4','4','4','4']
