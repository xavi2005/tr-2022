


#crear els dos vectors G i W en funció dels nodes i les connexions
def procesar_input(con,nodes):
    W = [[] for x in range(nodes)]
    G = [[] for x in range(nodes)]
    for i in range(0 , len(con) ):
        pes = con[i][2]
        node_pare = con[i][0]
        node_conectar = con[i][1]
        G[node_pare].append(node_conectar)
        G[node_conectar].append(node_pare)
        W[node_pare].append(pes)
        W[node_conectar].append(pes)
    return G , W



#algorisme de dijkstra per trobar el mínim pes d'un node incial fins un altre

def dijkstra(G , W ,I , F ):
    diccionari_cerca = []
    visitados = [False for i in range(len(G))]
    
    diccionari_cerca.append((0 , I))
    
    while len(diccionari_cerca)  > 0:
        diccionari_cerca.sort(reverse = True)
        menor = diccionari_cerca.pop()
        vertex = menor[1]
        pes = menor[0]

        if vertex == F:
            return pes
        
        if visitados[vertex] == False:
            visitados[vertex] = True
            for i in range(0, len(G[vertex])):
                vertex_a_visitar = G[vertex][i]
                pes_afegir = W[vertex][i]
                diccionari_cerca.append([ pes_afegir + pes , vertex_a_visitar])
    
    return None


def main():
    #exemple de l´ús de dijkstra en un graf

    #Vèrtexs
    nodes = 6

    #node per começar 
    inicial = 0

    #node objectiu
    final = 5

    #connexions d'una matriu M on , M[i] = [u,v,w] , on u i v es connecten amb un pes de w.
    connexions = [[0 , 1 , 7], [1 ,3 ,8]  , [3 ,5, 4] ,[5 , 4 ,1] ,[4 ,2 ,4], [0,2 ,2] ,[2 ,3 ,8] ,[0,5,20] ]
    
    G , W = procesar_input(connexions , nodes)
    pes = dijkstra(G,W,I = inicial ,F = final )
    print(f" El pes mínim és de {pes}")





if __name__ == "__main__":
    main()


