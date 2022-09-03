

def main():
 

 def es_tocan(v, currentNode): #funció per comprovar si la reina a aqgregar es toca amb les anteriors. True si no es troquen , false si es toquen
    for i in range(0,currentNode):
        if v[i] == v[currentNode] or abs(currentNode - i) == abs(v[currentNode] - v[i]):
            return False
    return True
    

 def backtrak( v , metadepth , currentdepth): #comença l'execució del backtraking on es té en compte la profunditat on es vol arribar, Metadepth = nreinas a colocar, i la profunditat actual del arbre, currentdepth = nreias agreades
    if metadepth   == currentdepth: #cas base de la recursivitat, que el meta sigui igual al current
        
        print_board(v)
        #print(v)
    
    #en cas contrari , farà un recorregut de totes les possibilitats per colocar la reina(i). La funció tornarà a ser trucada, quan la funció es_tocan = True , es a dir passa el filtre de comporvacions.
    
    else:
        for i in range( 0, metadepth ):
            v[currentdepth] = i
            if es_tocan(v , currentdepth) == True:
                backtrak( v ,metadepth , currentdepth +1 )

    #crea el taulell de n files * n columnes
 
 def crear_taulell(mida):
    taulell = [["*" for x in range(0,mida)] for x in range(0,mida)]
    
    return taulell

    #en cas de que es trobi una combinació_guanyadora = j, s'imprimirà el taulell amb les posicions de les reinas de la combinació(j) 
 
 def print_board(v):
    taulell_incial = crear_taulell(len(v))
    for i in range( 0 , len(v)):
        taulell_incial[v[i]][i] = "Q"
    s = ""
    for i in range(0,len(taulell_incial)):
        for j in range(0,len(taulell_incial[i])):
            
            s+= f" {taulell_incial[i][j]}  "
        
        s+= "\n\n"
        
    print(s)

#es defineix la profunditat incial del arbre

 depth = 0 
 #es pregunta la profunditat meta 
 metadepth = int(input( " -> Quantes n reines vols posar en un taulell n*n :  " ))
 #es crea el taullel amb la profunditat meta
 reinas = [-1 for x in range(0,metadepth)]

 backtrak(reinas , metadepth, depth)



if __name__ == "__main__":
    main() #executem la funció main que realitzarà el càlcul de les n-reinas



        