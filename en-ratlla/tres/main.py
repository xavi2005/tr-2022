""" 
L'idea del tres en ratlla és cear una matriu M d'ordre 3 en la qual, si Mij = 0 siginificarà no s'hi troben elements, si Mij = 1 serà fitxa del jugador humà,
si Mij = -1 , fitxa de la intel·ligència artificial. A través de pygame graficarem aquesta matriu i renderitzarem els canvis quan es s'efectüin les jugades.
1 = creu i -1 = rodona.
A través de minimax, es trobarà el resultat òptim per a -1.


"""


#importar el mòdul de pygame que ens permetrà expressar la matriu gràficament i totes les altres coses que es veruàn en pantalla
import pygame

#importar sys ens servirà per poguer parar l'execució d'un programa.
import sys

#el paquet random servirà per triar un jugador incial aleatori
import random

#json ens servirà com a base de dades per apuntar les partides guanyades de la màquina i jugador
import json

#copy ens seveix per l'algorisme de minimax. Permet replicar possibles situacions sense alterar el resultat de la variable a analitzar
import copy
from copy import deepcopy


#finalment aquí importem els paquets que han estat progrmats per mi i es troben a altres documents

#cargarJson és una funció que servirà per apuntar els resultats al json(vic.json)
import cargarJson
from cargarJson import *

#aquest paquet s'hi troben les constants utlitzades continuament en aquest document.
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
    #definim els atributs de la classe gràcies a la funció __init__
    def __init__(self):
        self.board = Board() 
        self.actual_player = 1
        self.ia = IA(self.actual_player * -1)
        self.draw_struct()
        self.run = True
        
    def stop(self):
        self.run = False

    #funció per canviar de jugador. Com que cada jugador té el valor de -1 o 1 , al multiplicar per -1 , sempre retornà l'altre. 
    #aquest es guardarà en l'atribut de jugador actual.
    def change_player (self ):
        self.actual_player = self.actual_player* -1
    
    #la funció check win del joc s'encarga de definir si algun judor a guanyat
    #s'aprofita del taulell que li proporciona la class Board
    #si retorna 0, el joc ha acabat en taules , si None, encara no hi ha guanyador, else , retorna el jugador que ha guanyat
    #el que fa és comprovar si en les diagonals, files i columnes de la matriu 3*3, existeix tres -1 o tres 1. Si això passa, retorna el número que ho compleix 
    def check_win(self):
        
        board = self.board.board
        
        #revisa les files. Per fer veure si exeisteix guanyador, Mi0 = Mi1 = Mi2.
        for i in range(len(board)):
            if board[i][0] == board[i][1] == board[i][2] != 0:
                return board[i][0]
        
        #revisa les columnes. Per veure si existeix guanyador , M0j = M1j = M2j
        for j in range(len(board)):
            if board[0][j] == board[1][j] == board[2][j] != 0:
                return board[0][j]
        
        
        #revisa les diagonals. Per veure si existeix guanyador, M00 = M11 = M22 o M02 = M11 = M20
        
        if board[0][0] == board[1][1] == board[2][2] != 0:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != 0:
            return board[0][2]
        if self.board.is_full() == True:
            return 0
        return None
    
    #aquesta funció analitza el resultat de check_win(), si és NULL , aleshores canvia de jugador , si és igual al jugador actual, aleshores para el joc i ho anota al json.
    #si és 0, para igualment 
    def check(self):
        if self.check_win() == None:
                        
            self.change_player()
                        
        if self.check_win() == self.actual_player:
                self.stop()
                cargar_json(evaluate(self.actual_player),  other(self.actual_player))
                
                    
        if self.check_win == 0:
            cargar_json("H" , "IA" , True)
            self.stop()
            
            
    #funció que rep com a pràmetre la fila i la columa. El que fa és anotar-ho a la matriu. Després ho dibuixa gràficament.
    #Finalment fa un check().
    def mark_move(self , row, col):
        self.board.move(row, col, self.actual_player)
        self.draw_move(row, col, self.actual_player)
        self.check()
    
   #funció de la classe game que s'encarga de dibiuxar la estrucura, les files i columnes.

    def draw_struct(self):
        #diubuixa les ratlles horitzontals
        
        pygame.draw.line(screen , BLUE , ( 0, ROW_P) , (WIDTH,ROW_P) ,ANCH)
        pygame.draw.line(screen , BLUE , (0 , ROW_P*2) ,  ( WIDTH , ROW_P*2) , ANCH)
        
        #dibuixa les ratlles verticals
        
        pygame.draw.line(screen , BLUE , ( COL_P , 0) , (COL_P, HEIGHT), ANCH)
        pygame.draw.line(screen , BLUE , (COL_P*2, 0 ) , (COL_P*2, HEIGHT) , ANCH)
    
    
    #funció que rep una fila , una columna i un jugador. Si el jugador = -1 , dibuixa un cercle en  M[fila][columna]. Si el jugador = 1 , dibuixa una creu en M[fila][columna]
    def draw_move(self , row, col, player):
        if player == -1:
            self.draw_circle(row, col)
        elif player == 1:
            self.draw_cross(row, col)
        else:
            return False
        
    #funció que dibuixa una creu en funció de la fila i columna.

    def draw_cross(self, row, col):
        pygame.draw.line(screen , BLUE , (COL_P*col + K , ROW_P*row + K ) , (COL_P*(col+1) - K , ROW_P*(row+1) -K) , ANCH )
        pygame.draw.line(screen , BLUE , (COL_P * col + K  , ROW_P* (row + 1) - K ) , (COL_P* (col+1) -K , ROW_P*row +K ), ANCH)
    
    
    #funció que dibuixa un cercle en funció de la fila i columna.
    
    def draw_circle(self, row, col):
        pygame.draw.circle(screen, BLUE , (COL_P*col + COL_P/2 , ROW_P*row + ROW_P /2 ) , ROW_P/2 - K, ANCH)
    
    

#Classe que s'ocupa de extruere varies funcionalitats del tauell, com per exemple sapiguer les posicions de les caselles buides.
#d'afegir els moviments al taullel i de comprovar si està ple 
    
class Board:
    def __init__(self):
        self.board = BOARD
    
    #funció per marcar cada canvi que es faci en la matriu.
    # Com a paràmetres rep la fila, la columna i el jugador que fa la jugada. ( M[fila][columna] = jugador)
    
    def move(self, row , col, player):
        self.board[row][col] = player
    
    
    #funció que verifica si M[fila][columna] = 0. Si és verdader, es podrà afegir una fitxa , cas contrari retorarà fals. 
    def is_empty(self , row , col):
        if self.board[row][col] == 0:
            return True
        return False
    
    #funció per comprovar si la matriu està plena. Es a dir si es compleix que Mij != 0, retornarà verdader, si Mij = 0, fals. 
    
    def is_full(self):
        
        for i in range(ROW):
            for j in range(COL):
                if self.board[i][j] == 0:
                    return False
        return True
    
    #Definim una varaible k = 0
    #El que fa la funció d'abaix és analitzar si Mij = 0. Si això es compleix , k = k +1 i, s'afageix en una altre Matriu la "i" i la "j".
    #Per tant tindrem finalment una matriu M2 de k files i 2 columnes on  Mi0 i  Mi1 seràn les files i les columnes encara no omplertes
    
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
    
    
    #funció que li entrà la M del estat actual. El que fa és retornar la millor jugada per -1
    
    def play_IA( self , board ):
        minimize , move = self.minimax(board , False)
        
        print( f" La ia ha decitit amb la evaluació de {minimize} moure a {move}")
        
        return move
    
    
    #l'algorisme de minimax. Rep com a entrades , la Matriu i si es maximitza o minimitza. En aquest cas com l'algorisme vol que guanyi -1, es minimitza.
    #no hi ha una profunditat K màxima d'exploració
    #D'alguna manera intenta trobar aquella jugada que més li orienti a jugades guanyadores.


    def minimax( self ,game , maximizing = False ):
        #si detecta que M es troba en un estat final, es a dir , si hi ha un guanyador o si s'ha arribat a les taules. Retorna -1 si es compleix que ha guanyat IA.
        # 1 si es compleix que ha guanyat l'HUMÀ. Si hi ha taules, retorna 0. 
        #el que retorna és la puntuació de la matriu.
        final_state = game.check_win()
        if final_state == 1:
            return 1, None
        if final_state == -1:
            return -1 ,None
        elif game.board.is_full():
            return 0 , None
        
        #cas contrari , quan no hi ha estat final.
        
        #si es troba maximitzant, es crearant k(número de Mij = 0) matrius NM on en cada una d'aquetes, copies de M , es subtuirà NVi[M2[i][0]][M2[i][1]] = 1.
        #La iéssima fila de M2 s'anirà colocant a la i-èssima matriu NM.
        
        
        """ Per exemple si tenim la matriu M :
        M = [
        [0,0,1],
        [0,0,1],
        [-1,1,-1]]
        
        M2 serà una altre matriu k*2, on k = 4(Les ij on Mij = 0).
        M2 = [
        [0,0],
        [0,1],
        [1,0],
        [1,1]]
        
        Per tant es crearant k matrius NM, on k = 4:
        
        NM1 = [
        [1,0,1],
        [0,0,1],
        [-1,1,-1]]
        
        NM2 = [
        [0,1,1],
        [0,0,1],
        [-1,1,-1]]
        
        NM3 = [
        [0,0,1],
        [1,0,1],
        [-1,1,-1]]
        
        NM4 = [
        [0,0,1],
        [0,1,1],
        [-1,1,-1]]
        
        
        """
        #Cada una d'aquestes matrius passarà per la funció minimax recursivament i l'altre paràmetre maximazing serà False, ja que les altres k*(k-1) matrius se li atribuirà el valor de -1. 
        
       
        
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
        
        
        #Si l'algorisme es troba minimitzant es farà el mateix procés però es col·locarà a les k matrius NVi[M2[i][0]][M2[i][1]] = -1
        #Després per cada NVi serà l'entrada recursivament de minimax juntament amb maximitzant = True.
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
                
                #detecta la casella on s'ha produït un click amb el ratolí
                pos = event.pos
                row = int(pos[1] // ROW_P)
                col = int(pos[0] // ROW_P)
                
              #en el cas de que el torn sigui humà marcarà el moviment. Introduïnt-lo a la matriu, dibuixant-lo etc..
                
                if game.actual_player == human_player and  board.is_empty(row, col ) == True:
                    game.mark_move(row, col)
             
            #si el totn és de la màquina buscarà la millor solució i ho marcarà
                    
             if game.actual_player == -1:
               pygame.display.update()
               row , col = ia.play_IA(game)
               game.mark_move(row, col)
               




                    
                
                    

        pygame.display.update()


#executa el main() 

if __name__ == "__main__":
    main()
    


