from os import system
from random import randint
from time import sleep
import colorama # pip install colorama

mat = [] # matrice di gioco
vuoto, gioc, avv = "( )", "o", "(\33[1;31mo\33[0m)" # valori delle caselle
start = True # dice se si tratta della tua prima partita
end = "" # dice chi vince alla fine
extMin, extMax = 0, 0 # estremi d'azione per la diffioltà media

# inizializza la matrice per la prima volta
def init():
    colorama.init()
    global start
    start = False
    for i in range(6):
        a = []
        for j in range(7):
            a.append(vuoto)
        mat.append(a)

# rappresenta la matrice
def display():
    system("cls")
    print("   0   1   2   3   4   5   6")
    for i in range(6):
        print("|", end=" ")
        for j in range(7):
            print(mat[i][j], end=" ")
        print("|")
    print("   0   1   2   3   4   5   6\n")

# funzione per il giocatore
def insertGioc():
    display()
    j = input("Inserisci colonna: ")
    while j == '' or not j.isdigit() or int(j)<0 or int(j)>6 or mat[0][int(j)] != vuoto:
        display()
        print("Colonna non valida")
        sleep(1)
        display()
        j = input("Inserisci colonna: ")
    j = int(j)
    for i in range(5,-1,-1):
        if mat[i][j] == vuoto:
            mat[i][j] = gioc
            break
    display()

# evidenzia la sequenza di 4 caselle che ha portato alla vittoria
def evidenzia(player, mode, i, j):
    # colora di bianco le caselle
    for z in range(6):
        for k in range(7):
            if mat[z][k] != vuoto:
                mat[z][k]= "(\33[1;37mo\33[0m)" # bianco
    if mode == "orizzontale":
        for z in range(4):
            mat[i][j-z] = gioc if player == gioc else avv
    if mode == "verticale":
        for z in range(4):
            mat[i-z][j] = gioc if player == gioc else avv
    if mode == "ascendente":
        for z in range(4):
            mat[i+z][j-z] = gioc if player == gioc else avv
    if mode == "discendente":
        for z in range(4):
            mat[i-z][j-z] = gioc if player == gioc else avv
    

# controlla se ha vinto qualcuno
def check():
    global end    
    # parte orizzontale
    for i in range(6):
        countA, countB = 0, 0
        for j in range(7):
            if mat[i][j] == gioc:
                countB = 0
                countA = countA + 1
                if countA >= 4:
                    end = gioc
                    evidenzia(gioc, "orizzontale", i, j)
                    return False
            elif mat[i][j] == avv:
                countA = 0
                countB = countB + 1
                if countB >= 4:
                    end = avv
                    evidenzia(avv, "orizzontale", i, j)
                    return False
            else:
                countA = countB = 0
    
    # parte verticale
    for j in range(7):
        countA, countB = 0, 0
        for i in range(6):
            if mat[i][j] == gioc:
                countB = 0
                countA = countA + 1
                if countA >= 4:
                    end = gioc
                    evidenzia(gioc, "verticale", i, j)
                    return False
            elif mat[i][j] == avv:
                countA = 0
                countB = countB + 1
                if countB >= 4:
                    end = avv
                    evidenzia(avv, "verticale", i, j)
                    return False
            else:
                countA = countB = 0
    
    # parte diagonale disc
    for i in range(3):
        for j in range(4):
            countA, countB = 0, 0
            for z in range(4):
                if mat[i+z][j+z] == gioc:
                    countB = 0
                    countA = countA + 1
                elif mat[i+z][j+z] == avv:
                    countA = 0
                    countB = countB + 1
            if countA >= 4:
                end = gioc
                evidenzia(gioc, "discendente", i+z, j+z)
                return False
            elif countB >= 4:
                end = avv
                evidenzia(avv, "discendente", i+z, j+z)
                return False
    
    # parte diagonale asc
    for i in range(3,6):
        for j in range(4):
            countA, countB = 0, 0
            for z in range(4):
                if mat[i-z][j+z] == gioc:
                    countB = 0
                    countA = countA + 1
                elif mat[i-z][j+z] == avv:
                    countA = 0
                    countB = countB + 1
            if countA >= 4:
                end = gioc
                evidenzia(gioc, "ascendente", i-z, j+z)
                return False
            elif countB >= 4:
                end = avv
                evidenzia(avv, "ascendente", i-z, j+z)
                return False
                
    # controllo pareggio
    par = 0
    for j in range(7):
        if mat[0][j] == vuoto: break
        else: par = par + 1
    if par == 7:
        end = "par"
        return False
           
    return True # con True il gioco va avanti (vedi while check() nel main)

# reinizializza la matrice a partire dalla rivincita
def reInit():
    global end, extMax, gioc
    extMax = 0
    end, gioc = "", "o"
    system("cls")
    for i in range(6):
        for j in range(7):
            mat[i][j] = vuoto

# dice chi ha vinto e propone una rivincita
def endGame():
    display()
    if end == "par":
        print("Siete arrivati ad un pareggio")
    elif end == gioc:
        print("\33[1;32mCongratulazioni, hai vinto!\33[0m")
    elif end == avv:
        print("\33[1;31mChe peccato, hai perso\33[0m")
    ans = input("Vuoi riprovare? (Y/N): ")
    while len(ans) != 1 or (ans.upper() != 'Y' and ans.upper() != 'N'):
        display()
        print("Risposta non valida")
        sleep(1)
        display()
        if end == "par":
            print("Siete arrivati ad un pareggio")
        elif end == gioc:
            print("\33[1;32mCongratulazioni, hai vinto!\33[0m")
        elif end == avv:
            print("\33[1;31mChe peccato, hai perso\33[0m")
        ans = input("Vuoi riprovare? (Y/N): ")
    if ans.upper() == 'Y':
        return main()
    else: return

def diffMedia(): # strategia difensiva
    global extMin, extMax
    if extMax == 0: # concentra gli attacchi su di un'area specifica
        extMin = randint(0,3) # setta i valori solo una volta
        extMax = extMin + 3
    
    # attacco
    for j in range(7): # si tratta di un controllo in verticale
        if mat[0][j] != vuoto: continue
        count = 0
        for i in range(5, -1, -1):
            if mat[i][j] == avv:
                count = count + 1
                if count >= 3 and i>=0 and mat[i-1][j] == vuoto:
                    return j
            else: count = 0
    
    for i in range(6): # controllo in orizzontale sx-dx
        count = 0
        for j in range(7):
            if mat[i][j] == avv:
                count = count + 1
                if count >= 3:
                    if i==5 and j<6:
                        if mat[i][j+1] == vuoto:
                            return j+1
                    elif i<5 and j<6:
                        if mat[i+1][j+1] != vuoto and mat[i][j+1] == vuoto:
                            return j+1
            else: count = 0
    
    for i in range(6): # controllo in orizzontale dx-sx
        count = 0
        for j in range(6,-1,-1):
            if mat[i][j] == avv:
                count = count + 1
                if count >= 3:
                    if i==5 and j>0:
                        if mat[i][j-1] == vuoto:
                            return j-1
                    elif i<5 and j>0:
                        if mat[i+1][j-1] != vuoto and mat[i][j-1] == vuoto:
                            return j-1
            else: count = 0
    
    # difesa
    for j in range(7): # si tratta di un controllo in verticale
        if mat[0][j] != vuoto: continue
        count = 0
        for i in range(5, -1, -1):
            if mat[i][j] == gioc:
                count = count + 1
                if count >= 3  and i>=0 and mat[i-1][j] == vuoto:
                    return j
            else: count = 0
    
    for i in range(6): # controllo in orizzontale sx-dx
        count = 0
        for j in range(7):
            if mat[i][j] == gioc:
                count = count + 1
                if count >= 3:
                    if i==5 and j<6:
                        if mat[i][j+1] == vuoto:
                            return j+1
                    elif i<5 and j<6:
                        if mat[i+1][j+1] != vuoto and mat[i][j+1] == vuoto:
                            return j+1
            else: count = 0
    
    for i in range(6): # controllo in orizzontale dx-sx
        count = 0
        for j in range(6,-1,-1):
            if mat[i][j] == gioc:
                count = count + 1
                if count >= 3:
                    if i==5 and j>0:
                        if mat[i][j-1] == vuoto:
                            return j-1
                    elif i<5 and j>0:
                        if mat[i+1][j-1] != vuoto and mat[i][j-1] == vuoto:
                            return j-1
            else: count = 0
    
    return randint(extMin, extMax) # colpisce nell'area

def diffDifficile(): # strategia mista-offensiva
    global extMin, extMax
    if extMax == 0: # concentra gli attacchi su di un'area specifica
        extMin = randint(0,3) # setta i valori solo una volta
        extMax = extMin + 3
    
    # attacco vincente
    for j in range(7): # si tratta di un controllo in verticale
        if mat[0][j] != vuoto: continue
        count = 0
        for i in range(5, -1, -1):
            if mat[i][j] == avv:
                count = count + 1
                if count >= 3 and i>=0 and mat[i-1][j] == vuoto:
                    return j
            else: count = 0
    
    for i in range(6): # controllo in orizzontale sx-dx
        count = 0
        for j in range(7):
            if mat[i][j] == avv:
                count = count + 1
                if count >= 3:
                    if i==5 and j<6:
                        if mat[i][j+1] == vuoto:
                            return j+1
                    elif i<5 and j<6:
                        if mat[i+1][j+1] != vuoto and mat[i][j+1] == vuoto:
                            return j+1
            else: count = 0
    
    for i in range(6): # controllo in orizzontale dx-sx
        count = 0
        for j in range(6,-1,-1):
            if mat[i][j] == avv:
                count = count + 1
                if count >= 3:
                    if i==5 and j>0:
                        if mat[i][j-1] == vuoto:
                            return j-1
                    elif i<5 and j>0:
                        if mat[i+1][j-1] != vuoto and mat[i][j-1] == vuoto:
                            return j-1
            else: count = 0
    
    for i in range(6): # controllo del caso orizzontale OXOO
        count = 0
        for j in range(6,1,-1):
            if mat[i][j] == avv:
                count = count + 1
                if count == 2 and mat[i][j-1] == vuoto and mat[i][j-2] == avv:
                    if i==5:
                        return j-1
                    elif i<5:
                        if mat[i+1][j-1] != vuoto:
                            return j-1
            else: count = 0
            
    for i in range(6): # controllo del caso orizzontale OOXO
        count = 0
        for j in range(5):
            if mat[i][j] == avv:
                count = count + 1
                if count == 2 and mat[i][j+1] == vuoto and mat[i][j+2] == avv:
                    if i==5:
                        return j+1
                    elif i<5:
                        if mat[i+1][j+1] != vuoto:
                            return j+1
            else: count = 0
    
    for i in range(3): # controllo in diagonale disc sx-dx
        for j in range(4):
            count = 0
            for z in range(3):
                if mat[i+z][j+z] == avv:
                    count = count + 1
                    if count == 3:
                        if i+z+1 == 5 and mat[i+z+1][j+z+1] == vuoto:
                            return j+z+1
                        elif i+z+1 < 5 and mat[i+z+2][j+z+1] != vuoto and mat[i+z+1][j+z+1] == vuoto:
                            return j+z+1
                else: count = 0
                
    for i in range(3): # controllo in diagonale disc dx-sx
        for j in range(3,7):
            count = 0
            for z in range(3):
                if mat[i+z][j-z] == avv:
                    count = count + 1
                    if count == 3:
                        if i+z+1 == 5 and mat[i+z+1][j-z-1] == vuoto:
                            return j-z-1
                        elif i+z+1 < 5 and mat[i+z+2][j-z-1] != vuoto and mat[i+z+1][j-z-1] == vuoto:
                            return j-z-1
                else: count = 0
                
    for i in range(3,6): # controllo in diagonale asc sx-dx
        for j in range(4):
            count = 0
            for z in range(3):
                if mat[i-z][j+z] == avv:
                    count = count + 1
                    if count == 3:
                        if i-z-1 == 0 and mat[i-z-1][j+z+1] == vuoto:
                            return j+z+1
                        elif i-z-1 > 0 and mat[i-z][j+z+1] != vuoto and mat[i-z-1][j+z+1] == vuoto:
                            return j+z+1
                else: count = 0
    
    for i in range(3,6): # controllo in diagonale asc dx-sx
        for j in range(3,7):
            count = 0
            for z in range(3):
                if mat[i-z][j-z] == avv:
                    count = count + 1
                    if count == 3:
                        if i-z-1 == 0 and mat[i-z-1][j-z-1] == vuoto:
                            return j-z-1
                        elif i-z-1 > 0 and mat[i-z][j-z-1] != vuoto and mat[i-z-1][j-z-1] == vuoto:
                            return j-z-1
                else: count = 0
    
    for i in range(3): # controllo in diagonale disc sx-dx OOXO
        for j in range(4):
            count = 0
            for z in range(2):
                if mat[i+z][j+z] == avv:
                    count = count + 1
                    if count == 2 and mat[i+z+1][j+z+1] == vuoto and mat[i+z+2][j+z+2] == avv:
                        if i+z+1 == 5:
                            return j+z+1
                        elif i+z+1 < 5 and mat[i+z+2][j+z+1] != vuoto:
                            return j+z+1
                else: count = 0
                
    for i in range(3): # controllo in diagonale disc dx-sx OXOO
        for j in range(3,7):
            count = 0
            for z in range(2):
                if mat[i+z][j-z] == avv:
                    count = count + 1
                    if count == 2 and mat[i+z+1][j-z-1] == vuoto and mat[i+z+2][j-z-2] == avv:
                        if i+z+1 == 5:
                            return j-z-1
                        elif i+z+1 < 5 and mat[i+z+2][j-z-1] != vuoto:
                            return j-z-1
                else: count = 0
                
    for i in range(3,6): # controllo in diagonale asc sx-dx OOXO
        for j in range(4):
            count = 0
            for z in range(2):
                if mat[i-z][j+z] == avv:
                    count = count + 1
                    if count == 2 and mat[i-z-1][j+z+1] == vuoto and mat[i-z-2][j+z+2] == avv:
                        if i-z-1 == 0:
                            return j+z+1
                        elif i-z-1 > 0 and mat[i-z][j+z+1] != vuoto:
                            return j+z+1
                else: count = 0
    
    for i in range(3,6): # controllo in diagonale asc dx-sx OXOO
        for j in range(3,7):
            count = 0
            for z in range(2):
                if mat[i-z][j-z] == avv:
                    count = count + 1
                    if count == 2 and mat[i-z-1][j-z-1] == vuoto and mat[i-z-2][j-z-2] == avv:
                        if i-z-1 == 0:
                            return j-z-1
                        elif i-z-1 > 0 and mat[i-z][j-z-1] != vuoto:
                            return j-z-1
                else: count = 0
    
    # contrattacco di emergenza
    for j in range(7): # si tratta di un controllo in verticale
        if mat[0][j] != vuoto: continue
        count = 0
        for i in range(5, -1, -1):
            if mat[i][j] == gioc:
                count = count + 1
                if count >= 3  and i>=0 and mat[i-1][j] == vuoto:
                    return j
            else: count = 0
    
    for i in range(6): # controllo in orizzontale sx-dx
        count = 0
        for j in range(7):
            if mat[i][j] == gioc:
                count = count + 1
                if count >= 3:
                    if i==5 and j<6:
                        if mat[i][j+1] == vuoto:
                            return j+1
                    elif i<5 and j<6:
                        if mat[i+1][j+1] != vuoto and mat[i][j+1] == vuoto:
                            return j+1
            else: count = 0
    
    for i in range(6): # controllo in orizzontale dx-sx
        count = 0
        for j in range(6,-1,-1):
            if mat[i][j] == gioc:
                count = count + 1
                if count >= 3:
                    if i==5 and j>0:
                        if mat[i][j-1] == vuoto:
                            return j-1
                    elif i<5 and j>0:
                        if mat[i+1][j-1] != vuoto and mat[i][j-1] == vuoto:
                            return j-1
            else: count = 0
            
    for i in range(6): # controllo del caso orizzontale OXOO
        count = 0
        for j in range(6,1,-1):
            if mat[i][j] == gioc:
                count = count + 1
                if count == 2 and mat[i][j-1] == vuoto and mat[i][j-2] == gioc:
                    if i==5:
                        return j-1
                    elif i<5:
                        if mat[i+1][j-1] != vuoto:
                            return j-1
            else: count = 0
            
    for i in range(6): # controllo del caso orizzontale OOXO
        count = 0
        for j in range(5):
            if mat[i][j] == gioc:
                count = count + 1
                if count == 2 and mat[i][j+1] == vuoto and mat[i][j+2] == gioc:
                    if i==5:
                        return j+1
                    elif i<5:
                        if mat[i+1][j+1] != vuoto:
                            return j+1
            else: count = 0
    
    for i in range(3): # controllo in diagonale disc sx-dx
        for j in range(4):
            count = 0
            for z in range(3):
                if mat[i+z][j+z] == gioc:
                    count = count + 1
                    if count >= 3:
                        if i+z+1 == 5 and mat[i+z+1][j+z+1] == vuoto:
                            return j+z+1
                        elif i+z+1 < 5 and mat[i+z+2][j+z+1] != vuoto and mat[i+z+1][j+z+1] == vuoto:
                            return j+z+1
                else: count = 0
                
    for i in range(3): # controllo in diagonale disc dx-sx
        for j in range(3,7):
            count = 0
            for z in range(3):
                if mat[i+z][j-z] == gioc:
                    count = count + 1
                    if count >= 3:
                        if i+z+1 == 5 and mat[i+z+1][j-z-1] == vuoto:
                            return j-z-1
                        elif i+z+1 < 5 and mat[i+z+2][j-z-1] != vuoto and mat[i+z+1][j-z-1] == vuoto:
                            return j-z-1
                else: count = 0
                
    for i in range(3,6): # controllo in diagonale asc sx-dx
        for j in range(4):
            count = 0
            for z in range(3):
                if mat[i-z][j+z] == gioc:
                    count = count + 1
                    if count >= 3:
                        if i-z-1 == 0 and mat[i-z-1][j+z+1] == vuoto:
                            return j+z+1
                        elif i-z-1 > 0 and mat[i-z][j+z+1] != vuoto and mat[i-z-1][j+z+1] == vuoto:
                            return j+z+1
                else: count = 0
    
    for i in range(3,6): # controllo in diagonale asc dx-sx
        for j in range(3,7):
            count = 0
            for z in range(3):
                if mat[i-z][j-z] == gioc:
                    count = count + 1
                    if count >= 3:
                        if i-z-1 == 0 and mat[i-z-1][j-z-1] == vuoto:
                            return j-z-1
                        elif i-z-1 > 0 and mat[i-z][j-z-1] != vuoto and mat[i-z-1][j-z-1] == vuoto:
                            return j-z-1
                else: count = 0
                
    for i in range(3): # controllo in diagonale disc sx-dx OOXO
        for j in range(4):
            count = 0
            for z in range(2):
                if mat[i+z][j+z] == gioc:
                    count = count + 1
                    if count == 2 and mat[i+z+1][j+z+1] == vuoto and mat[i+z+2][j+z+2] == gioc:
                        if i+z+1 == 5:
                            return j+z+1
                        elif i+z+1 < 5 and mat[i+z+2][j+z+1] != vuoto:
                            return j+z+1
                else: count = 0
                
    for i in range(3): # controllo in diagonale disc dx-sx OXOO
        for j in range(3,7):
            count = 0
            for z in range(2):
                if mat[i+z][j-z] == gioc:
                    count = count + 1
                    if count == 2 and mat[i+z+1][j-z-1] == vuoto and mat[i+z+2][j-z-2] == gioc:
                        if i+z+1 == 5:
                            return j-z-1
                        elif i+z+1 < 5 and mat[i+z+2][j-z-1] != vuoto:
                            return j-z-1
                else: count = 0
                
    for i in range(3,6): # controllo in diagonale asc sx-dx OOXO
        for j in range(4):
            count = 0
            for z in range(2):
                if mat[i-z][j+z] == gioc:
                    count = count + 1
                    if count == 2 and mat[i-z-1][j+z+1] == vuoto and mat[i-z-2][j+z+2] == gioc:
                        if i-z-1 == 0:
                            return j+z+1
                        elif i-z-1 > 0 and mat[i-z][j+z+1] != vuoto:
                            return j+z+1
                else: count = 0
    
    for i in range(3,6): # controllo in diagonale asc dx-sx OXOO
        for j in range(3,7):
            count = 0
            for z in range(2):
                if mat[i-z][j-z] == gioc:
                    count = count + 1
                    if count == 2 and mat[i-z-1][j-z-1] == vuoto and mat[i-z-2][j-z-2] == gioc:
                        if i-z-1 == 0:
                            return j-z-1
                        elif i-z-1 > 0 and mat[i-z][j-z-1] != vuoto:
                            return j-z-1
                else: count = 0
    
    # contrattacco di disturbo        
    for i in range(6): # controllo in orizzontale sx-dx
        count = 0
        for j in range(7):
            if mat[i][j] == gioc:
                count = count + 1
                if count >= 2:
                    if j == 5 and count < 3: continue # se il contrattacco è inutile
                    if i==5 and j<6:
                        if mat[i][j+1] == vuoto:
                            return j+1
                    elif i<5 and j<6:
                        if mat[i+1][j+1] != vuoto and mat[i][j+1] == vuoto:
                            return j+1
            else: count = 0
    
    for i in range(6): # controllo in orizzontale dx-sx
        count = 0
        for j in range(6,-1,-1):
            if mat[i][j] == gioc:
                count = count + 1
                if count >= 2:
                    if j == 1 and count < 3: continue # se il contrattacco è inutile
                    if i==5 and j>0:
                        if mat[i][j-1] == vuoto:
                            return j-1
                    elif i<5 and j>0:
                        if mat[i+1][j-1] != vuoto and mat[i][j-1] == vuoto:
                            return j-1
            else: count = 0
    
    for j in range(7): # si tratta di un controllo in verticale
        if mat[0][j] != vuoto: continue
        count = 0
        for i in range(5, -1, -1):
            if mat[i][j] == gioc:
                count = count + 1
                if count >= 2  and i>=0 and mat[i-1][j] == vuoto:
                    return j
            else: count = 0
    
    for i in range(3): # controllo in diagonale disc sx-dx
        for j in range(4):
            count = 0
            for z in range(3):
                if mat[i+z][j+z] == gioc:
                    count = count + 1
                    if count >= 2:
                        if i+z+1 == 5 and mat[i+z+1][j+z+1] == vuoto:
                            return j+z+1
                        elif i+z+1 < 5 and mat[i+z+2][j+z+1] != vuoto and mat[i+z+1][j+z+1] == vuoto:
                            return j+z+1
                else: count = 0
                
    for i in range(3): # controllo in diagonale disc dx-sx
        for j in range(3,7):
            count = 0
            for z in range(3):
                if mat[i+z][j-z] == gioc:
                    count = count + 1
                    if count >= 2:
                        if i+z+1 == 5 and mat[i+z+1][j-z-1] == vuoto:
                            return j-z-1
                        elif i+z+1 < 5 and mat[i+z+2][j-z-1] != vuoto and mat[i+z+1][j-z-1] == vuoto:
                            return j-z-1
                else: count = 0
                
    for i in range(3,6): # controllo in diagonale asc sx-dx
        for j in range(4):
            count = 0
            for z in range(3):
                if mat[i-z][j+z] == gioc:
                    count = count + 1
                    if count >= 2:
                        if i-z-1 == 0 and mat[i-z-1][j+z+1] == vuoto:
                            return j+z+1
                        elif i-z-1 > 0 and mat[i-z][j+z+1] != vuoto and mat[i-z-1][j+z+1] == vuoto:
                            return j+z+1
                else: count = 0
    
    for i in range(3,6): # controllo in diagonale asc dx-sx
        for j in range(3,7):
            count = 0
            for z in range(3):
                if mat[i-z][j-z] == gioc:
                    count = count + 1
                    if count >= 2:
                        if i-z-1 == 0 and mat[i-z-1][j-z-1] == vuoto:
                            return j-z-1
                        elif i-z-1 > 0 and mat[i-z][j-z-1] != vuoto and mat[i-z-1][j-z-1] == vuoto:
                            return j-z-1
                else: count = 0
    
    # attacco normale
    for j in range(7): # si tratta di un controllo in verticale
        if mat[0][j] != vuoto: continue
        count = 0
        for i in range(5, -1, -1):
            if mat[i][j] == avv:
                count = count + 1
                if count >= 2 and i>=0 and mat[i-1][j] == vuoto:
                    return j
            else: count = 0
    
    for i in range(6): # controllo in orizzontale sx-dx
        count = 0
        for j in range(7):
            if mat[i][j] == avv:
                count = count + 1
                if count >= 2:
                    if i==5 and j<6:
                        if mat[i][j+1] == vuoto:
                            return j+1
                    elif i<5 and j<6:
                        if mat[i+1][j+1] != vuoto and mat[i][j+1] == vuoto:
                            return j+1
            else: count = 0
    
    for i in range(6): # controllo in orizzontale dx-sx
        count = 0
        for j in range(6,-1,-1):
            if mat[i][j] == avv:
                count = count + 1
                if count >= 2:
                    if i==5 and j>0:
                        if mat[i][j-1] == vuoto:
                            return j-1
                    elif i<5 and j>0:
                        if mat[i+1][j-1] != vuoto and mat[i][j-1] == vuoto:
                            return j-1
            else: count = 0
    
    for i in range(3): # controllo in diagonale disc sx-dx
        for j in range(4):
            count = 0
            for z in range(3):
                if mat[i+z][j+z] == avv:
                    count = count + 1
                    if count >= 2:
                        if i+z+1 == 5 and mat[i+z+1][j+z+1] == vuoto:
                            return j+z+1
                        elif i+z+1 < 5 and mat[i+z+2][j+z+1] != vuoto and mat[i+z+1][j+z+1] == vuoto:
                            return j+z+1
                else: count = 0
                
    for i in range(3): # controllo in diagonale disc dx-sx
        for j in range(3,7):
            count = 0
            for z in range(3):
                if mat[i+z][j-z] == avv:
                    count = count + 1
                    if count >= 2:
                        if i+z+1 == 5 and mat[i+z+1][j-z-1] == vuoto:
                            return j-z-1
                        elif i+z+1 < 5 and mat[i+z+2][j-z-1] != vuoto and mat[i+z+1][j-z-1] == vuoto:
                            return j-z-1
                else: count = 0
                
    for i in range(3,6): # controllo in diagonale asc sx-dx
        for j in range(4):
            count = 0
            for z in range(3):
                if mat[i-z][j+z] == avv:
                    count = count + 1
                    if count >= 2:
                        if i-z-1 == 0 and mat[i-z-1][j+z+1] == vuoto:
                            return j+z+1
                        elif i-z-1 > 0 and mat[i-z][j+z+1] != vuoto and mat[i-z-1][j+z+1] == vuoto:
                            return j+z+1
                else: count = 0
    
    for i in range(3,6): # controllo in diagonale asc dx-sx
        for j in range(3,7):
            count = 0
            for z in range(3):
                if mat[i-z][j-z] == avv:
                    count = count + 1
                    if count >= 2:
                        if i-z-1 == 0 and mat[i-z-1][j-z-1] == vuoto:
                            return j-z-1
                        elif i-z-1 > 0 and mat[i-z][j-z-1] != vuoto and mat[i-z-1][j-z-1] == vuoto:
                            return j-z-1
                else: count = 0
    return randint(extMin, extMax) # colpisce nell'area

# IA avversaria pensata su 3 difficolta'
def insertAvv(difficulty):
    display()
    # Difficoltà Facile
    if difficulty == 1:
        n = randint(0,6) # scelta casuale della colonna
        while mat[0][n] != vuoto: # se la colonna e' piena ne sceglie un'altra
            n = randint(0,6)
        for i in range(5,-1,-1): # inserisce il disco nella prima cella vuota
            if mat[i][n] == vuoto:
                mat[i][n] = avv
                break
    # Difficoltà Media
    elif difficulty == 2:
        n = diffMedia()
        while mat[0][n] != vuoto: # se la colonna e' piena ne sceglie un'altra
            n = randint(0, 6)
        for i in range(5,-1,-1): # inserisce il disco nella prima cella vuota
            if mat[i][n] == vuoto:
                mat[i][n] = avv
                break
    # Difficoltà Difficile
    elif difficulty == 3:
        n = diffDifficile()
        while mat[0][n] != vuoto: # se la colonna e' piena ne sceglie un'altra
            n = randint(0, 6)
        for i in range(5,-1,-1): # inserisce il disco nella prima cella vuota
            if mat[i][n] == vuoto:
                mat[i][n] = avv
                break
    display()
    print("L'avversario ha inserito un disco nella colonna \33[1;31m" + str(n) + "\33[0m")
    system("pause")
    
def getCoin():
    system("cls")
    coin = input("Testa o Croce? (T/C): ")
    while len(coin) != 1 or (coin.upper() != 'T' and coin.upper() != 'C'):
        print("\nCarattere non valido")
        sleep(1)
        system("cls")
        coin = input("Testa o Croce? (T/C): ")
    rnd = ""
    if randint(0, 1): rnd = 'T'
    else: rnd = 'C'
    print("Ecco... è uscita " + ("\33[1;37mTesta\33[0m" if rnd == 'T' else "\33[1;37mCroce\33[0m")) # operatore ternario
    coin = coin.upper()
    if coin == rnd:
        print("\nInizi tu")
        system("pause")
        return True
    else:
        print("\nInizia il tuo avversario")
        system("pause")
        return False
    
def game(difficulty):
    coin = getCoin()
    if coin:
        while check(): # il gioco va avanti
            insertGioc()
            if check():
                insertAvv(difficulty)
            else: break
    else:
        while check(): # il gioco va avanti
            insertAvv(difficulty)
            if check():
                insertGioc()
            else: break
                
def selectDiff():
    system("cls")
    diff = ["\33[1;32mFacile\33[0m", "\33[1;33mNormale\33[0m", "\33[1;31mDifficile\33[0m"]
    if start: init()
    else: reInit()
    # selezione difficolta'
    print("Seleziona difficolta':")
    for i in range(3):
        print("--" + str(i+1) + "-- " + diff[i])
    d = input("--> ")
    while d == '' or not d.isdigit() or int(d)<1 or int(d)>3:
        print("\nDifficolta' non valida")
        sleep(1)
        system("cls")
        print("Seleziona difficolta':")
        for i in range(3):
            print("--" + str(i+1) + "-- " + diff[i])
        d = input("--> ")
    d = int(d)
    print("\nHai scelto: " + diff[d-1])
    system("pause")
    return d

def setColor():
    global gioc
    system("cls")
    colorsCode = ["\33[1;34m", "\33[1;32m", "\33[1;33m", "\33[1;35m", "\33[1;36m"]
    colors = ["Blu", "Verde", "Giallo", "Magenta", "Ciano"]
    colReset = "\33[0m" # resetta il colore
    print("Seleziona il colore del tuo disco:")
    for i in range(5):
        print("--" + str(i+1) + "-- " + colorsCode[i] + colors[i] + colReset)
    c = input("--> ")
    while c == '' or not c.isdigit() or int(c)<1 or int(c)>5:
        print("\nColore non valido")
        sleep(1)
        system("cls")
        print("Seleziona il colore del tuo disco:")
        for i in range(5):
            print("--" + str(i+1) + "-- " + colorsCode[i] + colors[i] + colReset)
        c = input("--> ")
    c = int(c)
    gioc = "(" + colorsCode[c-1] + gioc + colReset + ")"
    print("\nHai scelto: " + colorsCode[c-1] + colors[c-1] + colReset)
    system("pause")
        
# main del programma
def main():
    d = selectDiff()
    setColor()
    game(d)
    endGame()

main()