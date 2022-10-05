import json

def cargar_json(guanyador, perdedor , empat = False):
    file = open("vic.json")
    c = file.read()
    js = json.loads(c)

    if empat == True:
        js[guanyador]["E"] += 1
        js[perdedor]["E"] += 1
        print("\n")
        print(f"IA :  {js['IA']['v']} \n ")
        print("··························· \n")
        print(f"HUMÀ : {js['H']['v']} \n")
        print("··························· \n")
        
        print("\n")

    else:
        js[guanyador]["v"] +=1
        js[perdedor]["d"] +=1



        s= json.dumps(js)
        file.close()
        f = open("vic.json", "w")
        f.write(s)
        f.close()
        print("\n")
        print(f"IA :  {js['IA']['v']} \n ")
        print("··························· \n")
        print(f"HUMÀ : {js['H']['v']} \n")
        print("··························· \n")
        print("\n")




def evaluate(player):
    if player == 1:
        return "H"
    return "IA"

def other(player):
    if player == 1:
        return "IA"
    return "H"
