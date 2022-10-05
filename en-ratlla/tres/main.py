import pygame
import sys
import random
import json
import copy
from copy import deepcopy

import cargarJson
from cargarJson import *
import constantes
from constantes import *

#imprimeix el taulell a la CLI

def print_board( board):
    s = ""
    for i in range(len(board)):
        for j in range(len(board[i])):
            s+= f" {board[i][j]} "
        
        s += "\n"
    
    print(s)

pygame.init() #incizializa el modul de python
screen = pygame.display.set_mode(SCREEN) #crea una pantalla de les amplades donades
pygame.display.set_caption('TRES EN RATLLA HUMÀ vs IA') #posa el títol determinat al joc
screen.fill(S_COLOR) #afageix el color de la pantalla
  

#Classe joc que s'encarga de canviar de jugador, de verificar quan s'acaba la partida , de dibuixar en les estructures en pygame i
# de cargar el resultats al json 

class Game:
    def __init__(self):
        self.board = Board()
        self.actual_player = 1
        self.ia = IA(self.actual_player * -1)
        self.draw_struct()
        self.run = True
        
    def stop(self):
        self.run = False


    def change_player (self ):
        self.actual_player = self.actual_player* -1
    
    #la funcio check win del joc s'encarga de definir si algun judor a gunnyat
    #s'aprofita del taulell que li proporciona la class Board
    #si retorna 0, el joc acabat en taules , si None, encara no hi ha guanyador, else , retorna el judor que ha guanyat
    def check_win(self):
        board = self.board.board
        #revisa les hosritzontals
        for i in range(len(board)):
            if board[i][0] == board[i][1] == board[i][2] != 0:
                return board[i][0]
        for j in range(len(board)):
            if board[0][j] == board[1][j] == board[2][j] != 0:
                return board[0][j]
        
        if board[0][0] == board[1][1] == board[2][2] != 0:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != 0:
            return board[0][2]
        if self.board.is_full() == True:
            return 0
        return None
    
    def check(self):
        if self.check_win() == None:
                        
            self.change_player()
                        
        if self.check_win() == self.actual_player:
                self.stop()
                cargar_json(evaluate(self.actual_player),  other(self.actual_player))
                
                    
        if self.check_win == 0:
            cargar_json("H" , "IA" , True)
            self.stop()
            
            
    
    def mark_move(self , row, col):
        self.board.move(row, col, self.actual_player)
        self.draw_move(row, col, self.actual_player)
        self.check()
    
   #funcio de la classe game que s'encarga de dibiuxar la estrucura, les files i columnes 

    def draw_struct(self):
        #diubuixa les ratlles horitzontals
        
        pygame.draw.line(screen , BLUE , ( 0, ROW_P) , (WIDTH,ROW_P) ,ANCH)
        pygame.draw.line(screen , BLUE , (0 , ROW_P*2) ,  ( WIDTH , ROW_P*2) , ANCH)
        #dibuixa les ratlles verticals
        pygame.draw.line(screen , BLUE , ( COL_P , 0) , (COL_P, HEIGHT), ANCH)
        pygame.draw.line(screen , BLUE , (COL_P*2, 0 ) , (COL_P*2, HEIGHT) , ANCH)
    
    def draw_move(self , row, col, player):
        if player == -1:
            self.draw_circle(row, col)
        elif player == 1:
            self.draw_cross(row, col)
        else:
            return False
    

    def draw_cross(self, row, col):
        pygame.draw.line(screen , BLUE , (COL_P*col + K , ROW_P*row + K ) , (COL_P*(col+1) - K , ROW_P*(row+1) -K) , ANCH )
        pygame.draw.line(screen , BLUE , (COL_P * col + K  , ROW_P* (row + 1) - K ) , (COL_P* (col+1) -K , ROW_P*row +K ), ANCH)
    
    def draw_circle(self, row, col):
        pygame.draw.circle(screen, BLUE , (COL_P*col + COL_P/2 , ROW_P*row + ROW_P /2 ) , ROW_P/2 - K, ANCH)
    
    def restart(self):
        self.__init__()


#Classe que s'ocupa de extruere varies funcionalitats del tauell, com per exemple sapiguer les posicions de les caselles buides,
#d'afegir els moviments al taullel i de comprovar si està ple 
    
class Board:
    def __init__(self):
        self.board = BOARD
    
    #funcio per marcar cada canvi que es faci en el taulell.
    # Com a paràmetres rep la fila i la columna i el judor que fa la jugada
    
    def move(self, row , col, player):
        self.board[row][col] = player
    
    def is_empty(self , row , col):
        if self.board[row][col] == 0:
            return True
        return False
    
    #funcio per comprovar si encara quden elements no omplerts en el taulell
    def is_full(self):
        
        for i in range(ROW):
            for j in range(COL):
                if self.board[i][j] == 0:
                    return False
        return True
    
    #funcio per determinar si els elements per omplir d'una llista
    
    def list_empty(self):
        empty_list = []
        for i in range( ROW):
            for j in range(COL):
                if self.board[i][j] == 0:
                    empty_list.append((i , j))
        return empty_list

#Finalment tenim la classe de la inteligència artificial que extreu el moviment òptim gràcies el algorisme de minimax, que posteriorment ,
#es marcarà al tauell


class IA:
    def __init__(self, player = -1):
        self.player = player
    
    def play_IA( self , board ):
        minimize , move = self.minimax(board , False)
        
        print( f" La ia ha decitit amb la evaluació de {minimize} moure a {move}")
        
        return move


    def minimax( self ,game , maximizing = False ):
        final_state = game.check_win()
        if final_state == 1:
            return 1, None
        if final_state == -1:
            return -1 ,None
        elif game.board.is_full():
            return 0 , None
        else:
          if maximizing:

            maximize = -10
            best_move = None
            emptys = game.board.list_empty()
            for (row, col) in emptys:
                copy_game = copy.deepcopy(game)
                copy_game.board.move(row, col , self.player * -1)
                play_IA = self.minimax(copy_game, False)[0]
                if play_IA > maximize:
                    maximize = play_IA
                    best_move = (row, col)
            return maximize , best_move
        
          elif not maximizing:
            minimize = 10
            best_move = None
            emptys = game.board.list_empty()
            for (row, col) in emptys:
                copy_game = copy.deepcopy(game)
                copy_game.board.move(row, col , self.player)
                play_IA = self.minimax(copy_game, True)[0]
                if play_IA < minimize:
                    minimize = play_IA
                    best_move = (row, col)
            return minimize , best_move

#funció main del joc que dona dinàmica al joc i recull totes les classes posteriors per començar la interacció

def main():
    #definim la instancia joc perquè inicialitzi el joc
    #L'elecció per la possibilitat del primer llançament és aleatoria

    game = Game()
    board = game.board
    ia = game.ia
    game.draw_struct()
    actual_player = game.actual_player
    human_player = 1
    ai_player = -1

    run = True #definin l'estat correr
    while run: #mentre estigui corrent
        for event in pygame.event.get(): #captar el 'events'.
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() #surt del joc
                sys.exit(0) #surt del programa
            
            # si el joc està corrent
            if game.run == True:
             if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = int(pos[1] // ROW_P)
                col = int(pos[0] // ROW_P)
                
                
                if game.actual_player == human_player and  board.is_empty(row, col ) == True:
                    game.mark_move(row, col)
                    
                    
             if game.actual_player == -1:
               pygame.display.update()
               row , col = ia.play_IA(game)
               game.mark_move(row, col)
               




                    
                
                    

        pygame.display.update()


if __name__ == "__main__":
    main()
    


