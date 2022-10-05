import numpy as np

#les files i les columnes del taulell
ROWS = 6
COLS = 7



#Taullel de el joc inicialitzat en una matru de 6*7 on Mij = 0

BOARD = np.zeros((ROWS,COLS))

#MIDES PER PYGAME

WIDTH = 1150
HEIGHT = 800

ANCH = 10 

ROW_P = HEIGHT / ROWS 
COL_P = WIDTH / COLS 

COL_P_M = COL_P / 2
ROW_P_M = ROW_P / 2
D_C = 5

SCREEN = (WIDTH , HEIGHT)


#COLORS

BLACK = (0,0,0)
BLUE = (0 , 0, 255)
RED = (255,0,0)
YELLOW = (255 , 255 ,0)
GREEN = (0, 255 , 0)


#funcions addicionals

def evaluate_player(player):
    if player == 1:
        return RED
    return YELLOW

def eval(player):
    if player == 1:
        return "RED"
    return "YELLOW"



#JUGADORS
IA = 1
BOY = -1
EMPTY = 0


#PUNTUACIONS GUANYADORES

WINS_AI = 10000000000
WINS_BOY = -10000000000
TIE = 0
