class TaulaHash:
  def __init__(self):
    self.taulahash = [None] * 127

#Funció per interactuar amb les respostes del programa(És per donar-hi més funcionalitat)
  def maneig_respostes(self,res):
    if res == "n_element":
      return "no hi ha aquest valor dins de la taula hash"
    if res == "true":
      return "Acció completada correctament"
  
#Primera funcionalitat, definir la funció hash de la classe
#La funció hash no és molt important, perquè simplement és una transformació d'un valor a un altre, que funciona com a index
  
  def __funcio_hash__(self,value):
    key = 0 #Inicialitzem la clau en un valor null
    for i in range(0, len(value)):
      key += ord(value[i])
    return key % 127

#Segona funcionalitat, la funció d'introduir valors dins de la taula hash.

  def Introduir_valors(self,value):
    hash = self.__funcio_hash__(value)
    if self.taulahash[hash] is None:
      self.taulahash[hash] = value
      return self.maneig_respostes("true")

#Segona funcionalitat de la taula hash, buscar si el valor existeix dintre de la taula hash. O per altre banda, 
#buscar a través de l'index
  
  def Buscar_valors_existens(self,value):
    hash = self.__funcio_hash__(value)
    if self.taulahash[hash] is None:
      return self.maneig_respostes("n_element")
    else:
      return self.maneig_respostes("true")
  
  def Buscar_valors_index(self,index):
    if self.taulahash[index] is None:
      self.maneig_respostes("n_element")
    
    else:
      return self.maneig_respostes("true")

#treure elements d'una taula hash accedint a l'index i substituint per None. 
  def Treure_elements(self,value):
    hash = self.__funcio_hash__(value)
    if self.taulahash[hash] is None:
      return self.maneig_respostes("n_element")
    else:
      self.taulahash[hash] = None
      return self.maneig_respostes("n_element")

#Finalement, funció per visualitzar la taula hash

  def visualitzacio_taula(self):
    return self.taulahash



      
