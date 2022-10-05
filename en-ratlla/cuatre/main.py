import constantes
from constantes import *
import sys
from sys import exit
import numpy as np
import pygame
import random
import copy
from copy import deepcopy
import math

pygame.init()
screen = pygame.display.set_mode(SCREEN)
pygame.display.set_caption('CUATRE EN RATLLA HUMÀ VS IA')
font = pygame.font.Font('freesansbold.ttf', 64)
screen.fill(BLUE)
pygame.display.update()


class Board:
    def __init__(self):
        self.board = BOARD
        self.win = False

    def put_piece(self, row, col, player):
        self.board[row][col] = player

    def matrix_move(self, col, player):
        if self.is_full_col(col) == False:
            row = self.view_row(col)
            self.put_piece(row, col, player)
            return row
        else:
            return False

    def board_tie(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == 0:
                    return False

        return True

    def is_terminal_position(self):
        if len(self.check_possible_colums()) == 0 or self.check_win() is not None:
            return True

    def check_possible_colums(self):
        colums_posibles = []
        for i in range(COLS):
            if not self.is_full_col(i):
                colums_posibles.append(i)
        return colums_posibles

    def is_full_col(self, col):
        return self.board[ROWS - 1][col] != 0

    def view_row(self, col):
        for i in range(ROWS):
            if self.board[i][col] == 0:
                return i

    def revers_matrix(self):
        print(np.flip(self.board, 0))

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

        return None


class Game:
    def __init__(self, player):
        self.board = Board()
        self.actual_player = player
        self.moves = []
        

        self.draw_table()

    def draw_table(self):
        for i in range(ROWS):
            for j in range(COLS):
                pygame.draw.circle(
                    screen, BLACK, (j*COL_P + COL_P_M, i*ROW_P + ROW_P_M), (ROW_P_M - D_C))

    def draw_line(self, r1, c1, r2, c2):
        pygame.draw.line(screen, BLACK, (c1*COL_P + COL_P_M, r1*ROW_P -
                         ROW_P_M), (c2*COL_P + COL_P_M, r2*ROW_P - ROW_P_M), ANCH)

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
    

def evaluate_part(part_to_eval , player):
    score = 0
    other_player = BOY
    if player == BOY:
        other_player = IA
    
    if part_to_eval.count(player) == 4:
        score += 100
    

    elif part_to_eval.count(player) == 3 and part_to_eval.count(EMPTY) == 1:
        score += 5

    elif part_to_eval.count(player) == 2 and part_to_eval.count(EMPTY) == 2:
        score += 2

    if part_to_eval.count(other_player) == 3 and part_to_eval.count(EMPTY) == 1:
        score -= 4
    return score 


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


def main():
    run = True
    firts = random.choice([-1, 1])
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
    


if __name__ == "__main__":
    
    main()
    



 