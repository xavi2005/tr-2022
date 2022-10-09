""" 
EL quatre en ratlla serà una matriu M (6*7) on serà l'espai de partida. Si Mij = 1, implicà fitxa de l'IA. Si Mij = -1 , implicà fitxa de l'Humà. On Mij = 0,
casella buida.

L'intel·ligència artificial maximitzarà i, per tant, interarà orientar-se cap a aquelles situacions on li donin més puntuació. 
La complexitat temporal es veu afectada per la quantitat de possibles desencadenacions. És per això, que definirem una profunditat màxima K.

"""



#importa l'arxiu de constants defines per les parts gràfiques i més.
import constantes
from constantes import *

#paquet per sortir de l'execució del programa
import sys
from sys import exit

#això serveix per la creació senzilla de matrius
import numpy as np

#paquet de pygame, motor de la nostra part gràfica
import pygame

#random per decidir aleatòriament quin serà l'usuari que tirarà primer
import random

#paquet per crear aquelles matrius temporals NM de l'algorisme de minimax
import copy
from copy import deepcopy

#math servirà per crear el conepte d'infinit en alpha-beta
import math

pygame.init() #incizialitzar pygame
screen = pygame.display.set_mode(SCREEN) #crear una pantalla
pygame.display.set_caption('CUATRE EN RATLLA HUMÀ VS IA') #definir un títol
font = pygame.font.Font('freesansbold.ttf', 64) #establir la font
screen.fill(BLUE)#pintar el fons
pygame.display.update()#actualitzar els canvis


#Igual que el tres en ratlla, la classe matriu(BOARD) servirà per interactuar amb la matriu.

class Board:
    def __init__(self):
        self.board = BOARD
        self.win = False

        #funció que assigna a un jugador a una posició ij
    def put_piece(self, row, col, player):
        self.board[row][col] = player
        
        #funció que rep una columna i troba la fila on li correspon dispondre la peça.
        #si una columna ja està plena retorna false

    def matrix_move(self, col, player):
        if self.is_full_col(col) == False:
            row = self.view_row(col)
            self.put_piece(row, col, player)
            return row
        else:
            return False
        
        #funció que determina si hi ha taules. En el cas que Mij != 0, retorna False. Cas contrari retorna True 

    def board_tie(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == 0:
                    return False

        return True

        #funció que determina si ens trobem en un estat final. Quan les columnes estiguin totes plenes o quan apareixi un guanyador
    def is_terminal_position(self):
        if len(self.check_possible_colums()) == 0 or self.check_win() is not None:
            return True
        
        #funció que retorna les possibles columnes on encara es pot tirar. 
    def check_possible_colums(self):
        colums_posibles = []
        for i in range(COLS):
            if not self.is_full_col(i):
                colums_posibles.append(i)
        return colums_posibles
    
        #funció que determina si una columna està plena. Si M6j != 0 retorna True.Cas contari , false

    def is_full_col(self, col):
        return self.board[ROWS - 1][col] != 0

        #funció utilitzada anteriorment per veure la Mi donada j
    def view_row(self, col):
        for i in range(ROWS):
            if self.board[i][col] == 0:
                return i

    def revers_matrix(self):
        print(np.flip(self.board, 0))
       
    
    #analitzar en la matriu si existeix un guanyador. El que fa és verificar si hi ha 4 caselles que siguin iguals i diferents a 0.

    def check_win(self):
        # mirar si existeix una jugada guanyadora vertical
        for i in range(ROWS - 3):
            for j in range(COLS):
                if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j] != 0:

                    self.win = True
                    return self.board[i][j] , ((i, j), (i+3, j))

        # mirar si existeix una jugada guanyadora horitzontal
        for i in range(ROWS):
            for j in range(COLS - 3):
                if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3] != 0:
                    self.win = True

                    return self.board[i][j] , ((i, j), (i, j+3))
                    
        # revisar per les daigonals de esquerre a dreta

        for i in range(COLS - 3):
            for j in range(ROWS - 3):
                if self.board[j][i] == self.board[j+1][i+1] == self.board[j+2][i+2] == self.board[j+3][i+3] != 0:
                    self.win = True

                    return self.board[j][i] , ((j, i), (j+3, i+3))
        # revisar les diagonals de dreta a esquerra

        for i in range(COLS - 3):
            for j in range(3, ROWS):
                if self.board[j][i] == self.board[j-1][i+1] == self.board[j-2][i+2] == self.board[j-3][i+3] != 0:
                    self.win = True

                    return self.board[j][i], ((j, i), (j-3, i+3))
         
        #retorna None si encara no hi ha cap guanyador

        return None


#la classe joc s'encarrega de les parts gràfiques i de canviar de torn de tirada.
    
class Game:
    def __init__(self, player):
        self.board = Board()
        self.actual_player = player
        self.moves = []
        

        self.draw_table()
        #funció que dibuixa el taulell
        
    def draw_table(self):
        for i in range(ROWS):
            for j in range(COLS):
                pygame.draw.circle(
                    screen, BLACK, (j*COL_P + COL_P_M, i*ROW_P + ROW_P_M), (ROW_P_M - D_C))

        #funció que dibuixa la linea quan es guanya
    def draw_line(self, r1, c1, r2, c2):
        pygame.draw.line(screen, BLACK, (c1*COL_P + COL_P_M, r1*ROW_P -
                         ROW_P_M), (c2*COL_P + COL_P_M, r2*ROW_P - ROW_P_M), ANCH)

        #funció que marca el moviment, tant a la matriu com gràficament. Després, s'encarrega d'avaluar si hi ha un guanyador. En el cas de que no, canvïa de torn.
    def mark_move(self, col):
        if self.board.is_full_col(col) == False:
            color = evaluate_player(self.actual_player)

            row = self.board.matrix_move(col, self.actual_player)
            curr_row = ROWS-row
            pygame.draw.circle(screen, color, (col*COL_P + COL_P_M, curr_row*ROW_P - ROW_P_M), (ROW_P_M - D_C))
            
            self.add_colum_move(col)
            
            if self.board.check_win() is not None:
                print("\n")
                

                tup = self.board.check_win()[1]
                row1 = ROWS - tup[0][0]
                col1 = tup[0][1]
                row2 = ROWS - tup[1][0]
                col2 = tup[1][1]

                self.draw_line(row1, col1, row2, col2)
                text = font.render(f'{eval(self.board.check_win()[0])} WINS!', True, GREEN)
                textrect = text.get_rect()
                textrect.center = (WIDTH / 2, HEIGHT / 2)
                screen.blit(text, textrect)
                print(f"Historial de les columnes on has mogut :  {self.moves}")

                self.board.win = True

            if self.board.board_tie() == True:
                return TIE

            else:
                self.change_player()

    def change_player(self):
        self.actual_player *= -1
    
    def add_colum_move(self,col):
        if self.actual_player == -1:
            self.moves.append(col+1)
    

    
    
    
    
#funció que atribueix una puntuació donades 4 posicions adjuntes de la matriu.

# En el cas d'haver-hi 3 fitxes iguals i diferents a 0 i una buida. Suma 6.
# En el cas d'haver-hi 4 fitxes iguals i diferents a 0. Suma 100.
# En el cas d'haver-hi 2 fitxes iguals i diferents a 0 i dos buides. Suma 3.
# En el cas d'haver-hi 3 fitxes iguals i diferents a 0 i una buida però són del contari. Resta 5.

def evaluate_part(part_to_eval , player):
    score = 0
    other_player = BOY
    if player == BOY:
        other_player = IA
    
    if part_to_eval.count(player) == 4:
        score += 100
    

    elif part_to_eval.count(player) == 3 and part_to_eval.count(EMPTY) == 1:
        score += 6

    elif part_to_eval.count(player) == 2 and part_to_eval.count(EMPTY) == 2:
        score += 3

    if part_to_eval.count(other_player) == 3 and part_to_eval.count(EMPTY) == 1:
        score -= 5
    return score 

# Aquesta funció s'encarrega de trobar totes les submatrius de 4 caselles de M tal que siguin adjuntes entre si, tan horitzontalment,verticalment o en diagonal
# Per a cada submatriu és l'entrada a la funció de dalt que la puntuarà.

def score_pos(board, player):
    score = 0

    center_array = [int(i) for i in list(board[:, COLS//2])]
    center_count = center_array.count(player)
    score += center_count * 3

    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3 ):
            part_to_eval = row_array[c:c+4]
            score += evaluate_part(part_to_eval , player)
    
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS - 3 ):
            part_to_eval = col_array[r:r+4]
            score += evaluate_part(part_to_eval , player)
    
    for r in range(ROWS -3):
        for c in range(COLS -3):
            part_to_eval = [board[r+i][c+i] for i in range(4)]
            score += evaluate_part(part_to_eval , player)
    
    for r in range(ROWS -3):
        for c in range(COLS -3):
            part_to_eval = [board[r+3 - i][c+i] for i in range(4)]
            score += evaluate_part(part_to_eval , player)
    
    return score


#algorisme de minimax amb la variant alpha-beta.
#La profunditat de l'arbre és de K=6. En el cas de que ens trobem en una situació terminal (retornarà 10000000 si IA és guayadora o -10000000 si humà és guanyador). 
#Si s'arriba a al profunditat K, aleshores es puntua la matriu a través de les dues funcions de dalt.
#Finalment, la columna escollida per l'algorisme serà aquella que més puntuació li doni.

def minimax(board, depth, alpha, beta  , maximizing_player):
    get_cols = board.check_possible_colums()
    if board.is_terminal_position() or depth == 0:
        
        if board.is_terminal_position():
            if board.check_win()[0] == IA:
                return None, WINS_AI
            elif board.check_win()[0] == BOY:
                return None, WINS_BOY
            else:
                return None, TIE
        else:
            return None, score_pos(board.board, IA)
            
    if maximizing_player:
        best_score = -math.inf
        best_column = random.choice(get_cols)
        for col in get_cols:
            row = board.view_row(col)
            tempt_board = deepcopy(board)
            tempt_board.put_piece(row, col, IA)
            # tempt_board.revers_matrix()
            curr_score = minimax(tempt_board, depth - 1, alpha , beta, False)[1]
            
            if curr_score > best_score:
                best_score = curr_score
                best_column = col
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_column, best_score
    else:
        best_score = math.inf
        best_column = random.choice(get_cols)
        for col in get_cols:
            row = board.view_row(col)
            tempt_board = deepcopy(board)
            tempt_board.put_piece(row, col, BOY)
            curr_score = minimax(tempt_board, depth - 1, alpha , beta, True)[1]
            if curr_score < best_score:
                best_score = curr_score
                best_column = col
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return best_column, best_score


    
#funció main que recull les dinàmiques del joc i es reuneix tot el que s'ha programat anteriorment.
#Consta de condicionals per verificar el torn de la partida.
#Quan li toqui l'humà es registrarà la columna on es vol tirar i es marcarà el moviment
#Quan li toqui a l'IA, utilitzarà minimax per trobar la millor jugada

def main():
    run = True
    firts = random.choice([-1, 1]) #s'escull jugador d'inici
    print(eval(firts))
    print("\n")
   

    game = Game(firts)
    

    board = game.board
    
  

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit(0)
             
            

            if board.win == False and board.board_tie() == False:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    col = int(pos[0] // COL_P)
                    game.mark_move(col)
                    
                    pygame.display.update()
        
        pygame.display.update()

        if game.actual_player == IA and board.win == False and board.board_tie() == False:
            best_col, best_score = minimax(board, 6, -math.inf, math.inf , True)

            print(best_col,best_score)
            

            game.mark_move(best_col)
            

        pygame.display.update()
    


#Executa el main()
if __name__ == "__main__":
    
    main()
    



 
