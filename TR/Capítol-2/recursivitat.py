

def factorial(n , curr):
  if n == 0 or n ==1 :
    return curr
  else:
    curr*= n
    factorial(n-1 , curr)
   

def sumatori(n , curr):
  if n == 0: return curr
  else:
    curr += n
    sumatori(n-1 , curr)

    
numero = input(int ( "numero per fer el sumatori: "))
if numero >= 0:
  print(f"factorial : {factorial(numero , 1)}")
  print(f"sumatori : {sumatori(numero , 0)}")
  
else:
  print("Números negatius no!)
 
