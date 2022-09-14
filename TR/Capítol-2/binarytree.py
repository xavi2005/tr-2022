#definim la classe node que conté coma a atributs, els seus valors, i l'apuntador de la dreta i l'esquerra
class Node:
    def __init__(self,valor):
        self.valor = valor
        self.left = None
        self.right = None
    

class Arbre:
    def __init__(self,root):
        self.root = Node(root) #el node root serà un atribut de tipus node
    
    def  introduir_node(node_add , root ,self):
        if root.valor =< node_add: #utilitzo el igual o més gran per poguer tractar també amb nodes iguals
            if root.right is None: #si l'apuntador dret encara no hi ha res
                root.right = Node(node_add) #canvia el node pel node a afegir
            else:#cas contrari, hi han elements(mètode recursiu)
                self.introduir_node(node_add , root.right)
        
        elif root.valor > node.add:
            if root.left is None:
                root.left = Node(node_add)
            else:
                self.introduir_node(node_add, root.left)

    
    def preorden(self,root):
        if root: 
         print(root.valor)
         preorden(root.left)
         preorden(root.right)
    
    def inorden(self,root):
         if root
         inorden(root.left)
         print(root)
         inorden(root.rigth)
    
    def postorden(self, root):
        if root:
         postorden(root.left)
         postorden(root.right)
         print(root)
    
    def cercar_element(self, root , valor_search , trobat = False): #mira si un element es troba dins del arbre binari
        
        if root: #mentres que existeixi un node a cercar
            if root.valor == valor_search: #cas base, el valor del node actual és el mateix que el node a cercar
                trobat = True
                return trobat
            if root.valor <= valor_search: #si és més gran o igual, busca a la dreta
                self.cercar_element(root.right , valor_search)
            
            if root.valor > valor_search: #si és més petit o igual, busca a l'esquerra
                self.cercar_element(root.left , valor_search)
        
        return trobat

