import os.path
import time
from chessengine import POSITIONAL,SITBACK,HIGHPRESS,DIRECT

try:
    import pygame.mixer

    pygame.mixer.init()

    SUCCESS = pygame.mixer.get_init() is not None

except (ImportError, RuntimeError):
    SUCCESS = False

if SUCCESS:
    click = pygame.mixer.Sound(os.path.join( "sounds", "click.ogg"))
    move = pygame.mixer.Sound(os.path.join( "sounds", "kick.mp3"))
    start = pygame.mixer.Sound(os.path.join( "sounds", "endwhist.mp3"))
    end = pygame.mixer.Sound(os.path.join( "sounds", "endwhist.mp3"))

    #background = pygame.mixer.Sound(os.path.join("res", "sounds", "background.ogg"))

"""
class Music:
    def __init__(self):
        self.playing = False

    def play(self, load):
        if SUCCESS and load["sounds"]:
            background.play(-1)
            self.playing = True

    def stop(self):
        if SUCCESS:
            background.stop()
        self.playing = False

    def is_playing(self):
        return self.playing
"""
MATCHDES=["With 25 moves to go BAR need a goal to win against 10 men RMA","With 20 moves to go BAR need a goal to win against 10 men RMA","With 20 moves to go ARS need a goal to qualify for semi-final","With 15 moves to go BAR need a goal to win against 10 men RMA","With 40 moves to go can LIV comeback against MCI?"]
MATCHFORMATION=['3-4-2   4-3-1-2','3-4-2   4-3-1-2','4-4-2   4-4-1-1','3-4-2   4-3-1-2','4-3-3   4-3-3',]
MATCHSIDES=['RMA:Cmp    BAR:Plyr','RMA:Cmp    BAR:Plyr','JUVE:Cmp    ARS:Plyr','RMA:Cmp    BAR:Plyr','MCI:Cmp    LIV:Plyr']
MATCH_H=["RMA VS BAR","RMA VS BAR","JUV VS ARS","RMA VS BAR","MCI VS LIV"]
MATTSTYLE=[{1:DIRECT,-1:DIRECT},{1:DIRECT,-1:DIRECT},{1:POSITIONAL,-1:DIRECT},{1:DIRECT,-1:DIRECT},{1:POSITIONAL,-1:POSITIONAL}]#EACH ENTRY IS A DICT KEYS BE 1,-1
MDEFSTYLE=[{1:HIGHPRESS,-1:HIGHPRESS},{1:HIGHPRESS,-1:HIGHPRESS},{1:HIGHPRESS,-1:HIGHPRESS},{1:HIGHPRESS,-1:HIGHPRESS},{1:HIGHPRESS,-1:HIGHPRESS}]#EACH ENTRY IS A DICT      1,-1
MBOARD=[[ [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 8,3,2, 0, 0],
          [0, -10, 0, 0, -9, 0, 0],
          [-8, 2, 0, 0, 0, -8, 0],
        [7, 0, 0, 0, 0, 0, -2],
          [0, -6, 0, 10, 0, 0, 0],
          [10, 0, 0, -10, 0, 8, 0],
          [-2, 9, 0, 0, 0, 0, 0],
          [0, -3, 0, 0, -3, 0, 0],
          [0, 0, 0, -1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
        ],
        [ [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 8,3,2, 0, 0],
          [0, -10, 0, 0, -9, 0, 0],
          [-8, 2, 0, 0, 0, -8, 0],
        [7, 0, 0, 0, 0, 0, -2],
          [0, -6, 0, 10, 0, 0, 0],
          [10, 0, 0, -10, 0, 8, 0],
          [-2, 9, 0, 0, 0, 0, 0],
          [0, -3, 0, 0, -3, 0, 0],
          [0, 0, 0, -1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
        ],
        [ [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 2, 3, 3, 0, 2, 0],
          [0, 0, -9, 0, 0, 0, -7],
          [0, -8, 0, 0, 0, 0, 0],
          [0, 7, -10, 6, 0, 8, 0],
          [0, 0, 0, -7, 7, 0, 0],
        [0, -2, 9, -6, 0, 0, 0],
          [0, 0, 0, -3, -3, -2, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, -1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
        ],
        [ [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 8,3,2, 0, 0],
          [0, -10, 0, 0, -9, 0, 0],
          [-8, 2, 0, 0, 0, -8, 0],
        [7, 0, 0, 0, 0, 0, -2],
          [0, -6, 0, 10, 0, 0, 0],
          [10, 0, 0, -10, 0, 8, 0],
          [-2, 9, 0, 0, 0, 0, 0],
          [0, -3, 0, 0, -3, 0, 0],
          [0, 0, 0, -1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
        ],
        [ [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 2, 3, 3, 3, -10],
          [0, 0, -7, 6, 0, 0, 0],
          [0, 0, 0, -8, 0, -7, 0],
          [-2, 7, 0, 0, 0, 10, -8],
        [0, 0, 0, 8, -6, 0, 7],
          [0, 0, 0, 0, 9, -2, 0],
          [0, 0, -3, 0, -3, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, -1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
        ]]
MBALL=[(8,1),(8,1),(7,3),(8,1),(8,5)]#ball position in tuple
MWHOSTARTS=[-1,-1,-1,-1,-1]
MOTHERINFO=[{"turns":25,"maxgoal":1},{"turns":20,"maxgoal":1},{"turns":20,"maxgoal":1},{"turns":20,"maxgoal":1},{"turns":40,"maxgoal":1}]#now noofmoves only cn xpanded to dict for multiple attr

def play_click():
    if SUCCESS :
        click.play()
        time.sleep(0.1)


def play_start():
    if SUCCESS :
        start.play()


def play_move():
    if SUCCESS :
        move.play()
        time.sleep(0.1)


def play_end():
    if SUCCESS :
        end.play()



if SUCCESS:
    pygame.mixer.quit()
