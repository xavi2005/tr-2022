import random
N = 10 #qunatitat de nodes que té el graf
M = [[0 for i in range(0,N)] for x in range(0,N)] # es crea un vector per cada node i s'inicialitzen les nou posicions a 0 

llista_conexions = [0,1,2,1,3,4,5,6] #aquesta és la llista de connexions que pateix el graf, és només diracional, no hi ha intercanvi mutuo. 
for i in range(0, len(llista_conexions) , 2): # El recorregut del for es fa de dos en dos, es a dir M[i] = node i M[i+1] = node a conectar 
    M[llista_conexions[i]][llista_conexions[i+1]] = 1

#Imprimeix totes les conexions del graf

def print_visual(M):
    s = ""
    for i in range(0, len(M)):
        for j in range(0,len(M[i])):
            if M[i][j] == 1:
              s+= f" In node {i} we have a connexion with node {j} \n "
    print(s)

#imprimeix la matriu

def print_matrix(M):
    m = ""
    for i in range(0, len(M)):
        for j in range(0,len(M[i])):
            if j == 0:
                m+= f"[ {M[i][j]} , "
            if j == 9:
                m+= f" {M[i][j]} ]"
            else:
                m+= f" {M[i][j]} , "
        m += "\n"
    print(m)
    

print("MATRIX")
print_visual(M)
print_matrix(M)


