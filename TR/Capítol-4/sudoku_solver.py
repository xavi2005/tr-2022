#el sudoku solver



#funció cota per veure si explorar el node
def is_valid(sudoku , n , i , j):
    fila = sudoku[i]
    col = [f[j] for f in sudoku]
    bloque = [sudoku[a][b] for a in range(9) for b in range(9) if i// 3 == a//3 and j//3 == b//3]

    return n not in fila and n not in col and n not in bloque

#funció de backtrak per solucionar el sudoku
def sudoku_solver(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                for n in range(1 , 10):
                    if is_valid(sudoku , n , i, j):
                        
                        sudoku[i][j] = n
                        if sudoku_solver(sudoku):
                            return True
                        else:
                            sudoku[i][j] = 0
                return False
    return True

#imprimir el sudoku d'una forma més visual
def print_sudoku(SUDOKU):
  s= "\n\n\n\n\t\t\t\t\t\t"
  for i in range(9):
      for j in range(9):
          if j == 0 :
              s+= "| "
          if j == 3:
              s+= " | "
          if j == 6:
              s+= "| "
          
          s+= f" {SUDOKU[i][j]} "
          if j == 8:
              s+= " |"
      s+= "\n\t\t\t\t\t\t ----------------------------------- \n\t\t\t\t\t\t"
  print(s)



#introduir el sudoku a solucionar en la matriu

SUDOKU = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]]


print_sudoku(SUDOKU)

print("\nRESOLGUENT EL SUDOKU ...")
sudoku_solver(SUDOKU)


print_sudoku(SUDOKU)
