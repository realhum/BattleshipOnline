from __future__ import print_function
import zmq
import time
import random
import msvcrt
import os
import numpy as np

columns = np.array(['A','B','C','D','E','F','G','H','I','J'])
lines = np.array(['1','2','3','4','5','6','7','8','9','10'])

def draw_battlefield_for_shipsetting(battlefield, posi, posj, vertically, shipsize):
    if shipsize!=0:
        print("Place the ship length " + str(shipsize) )
    print("  ", end = "    ")
    for j in range(10):
        print(" "+columns[j], end = "    ")
    print ('\n')
    for i in range(10):
        
        if i<9:
            print(" "+lines[i], end = "    ")
        else:
            print(lines[i], end = "    ")
            
        for j in range(10):            
            if (i>=posi and i<=posi+(shipsize-1)*vertically) and (j>=posj and j<=posj+(shipsize-1)*(not vertically)):
                print('|?|', end = "   ")
            else:
                if battlefield[i][j]==0:
                    print('|_|', end = "   ")  
                if battlefield[i][j]==1:
                    print('|X|', end = "   ")
                    
        print ('\n')
    print ('w, a, s, d - moving')
    print ('r - rotating')
    print ('e - accept')
    return True

def set_ship(battlefield, posi, posj, vertically, ship): 
    for i in range(ship):
        if vertically:
            battlefield[posi+i][posj]=1
        else:
            battlefield[posi][posj+i]=1
    return True

def check_correct_position(battlefield, posi, posj, vertically, ship):
    if posi+(ship-1)*vertically>9 or posj+(ship-1)*(not vertically)>9:
        return False
    if posi!=0: 
        check_posi=posi-1
    else: 
        check_posi=posi
    if posj!=0:
        check_posj=posj-1;
    else: 
        check_posj=posj
    for i in range((ship-1)*vertically+3):
        if (posi == 0 or posi+(ship-1)*vertically==9) and i == (ship-1)*vertically+2:
            break
        for j in range((ship-1)*(not vertically)+3):
            if (posj == 0 or posj+(ship-1)*(not vertically) == 9) and j == (ship-1)*(not vertically)+2:
                break
            #print (str(i)+' '+str(j) + '-'+ str(battlefield[check_posi+i][check_posj+j]))
            if battlefield[check_posi+i][check_posj+j]==1:
                return False
    return True

def placing_ships(battlefield):
    
    
    ships_to_set = np.array([4,3,3,2,2,2,1,1,1,1])
    posi=0
    posj=0
    vertically=True
    os.system('cls')
    draw_battlefield_for_shipsetting(battlefield,0,0,vertically,ships_to_set[0])

    while len(ships_to_set)!=0:    
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch == 's':
                if posi + (ships_to_set[0]-1) * vertically != 9:
                    posi=posi+1
                    os.system('cls')
                    draw_battlefield_for_shipsetting(battlefield,posi,posj,vertically,ships_to_set[0])
            elif ch == 'w':
                if posi!=0:
                    posi=posi-1
                    os.system('cls')
                    draw_battlefield_for_shipsetting(battlefield,posi,posj,vertically,ships_to_set[0])
            elif ch == 'a':
                if posj!=0:
                    posj=posj-1
                    os.system('cls')
                    draw_battlefield_for_shipsetting(battlefield,posi,posj,vertically,ships_to_set[0])
            elif ch == 'd':
                if posj + (ships_to_set[0]-1) * (not vertically)!=9:
                    posj=posj+1
                    os.system('cls')
                    draw_battlefield_for_shipsetting(battlefield,posi,posj,vertically,ships_to_set[0])
            elif ch == 'r':
                vertically = not vertically
                os.system('cls')
                draw_battlefield_for_shipsetting(battlefield,posi,posj,vertically,ships_to_set[0])
            elif ch == 'e':
                if check_correct_position(battlefield,posi,posj,vertically,ships_to_set[0]):
                    set_ship(battlefield,posi,posj,vertically,ships_to_set[0])
                    os.system('cls')
                    draw_battlefield_for_shipsetting(battlefield,posi,posj,vertically,ships_to_set[0])
                    ships_to_set = np.delete(ships_to_set,0,0)
                else:
                    os.system('cls')
                    draw_battlefield_for_shipsetting(battlefield,posi,posj,vertically,ships_to_set[0])
                    print ('\nError:\tInvalid position, try again')
    os.system('cls')  
    print("Your final battlefield.")
    draw_battlefield_for_shipsetting(battlefield,10,10,vertically,0)
    return True

def check_chotted_battle(battlefield, posi1, posj1, posi2, posj2):
    global killed
    if posi1==posi2:
        posi=posi1
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            #print('checking'+str(posj1+k))
            if posj1+k==10:
                end_of_ship=True
            else:
                if battlefield[posi][posj1+k]==0 or battlefield[posi][posj1+k]==4:
                    end_of_ship=True
                elif battlefield[posi][posj1+k]==1:
                    return False
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            #print('checking'+str(posj1-k))
            if posj1-k==-1:
                end_of_ship=True
            else:
                if battlefield[posi][posj1-k]==0 or battlefield[posi][posj1-k]==4:
                    end_of_ship=True
                elif battlefield[posi][posj1-k]==1:
                    return False
                
        end_of_ship=False
        k=0
        while not end_of_ship:
            if posj1+k==10:
                end_of_ship=True
            elif battlefield[posi][posj1+k]==0 or battlefield[posi][posj1+k]==4:
                end_of_ship=True
            else:
                battlefield[posi][posj1+k]=3
                killed = True
            k=k+1
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            if posj1-k==-1:
                end_of_ship=True
            elif battlefield[posi][posj1-k]==0 or battlefield[posi][posj1-k]==4:
                end_of_ship=True
            else:
                battlefield[posi][posj1-k]=3
                killed = True
                
    elif posj1==posj2:
        posj=posj1
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            #print('checking'+str(posi1+k))
            if posi1+k==10:
                end_of_ship=True
            else:
                if battlefield[posi1+k][posj]==0 or battlefield[posi1+k][posj]==4:
                    end_of_ship=True
                elif battlefield[posi1+k][posj]==1:
                    return False
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            #print('checking'+str(posi1-k))
            if posi1-k==-1:
                end_of_ship=True
            else:
                if battlefield[posi1-k][posj]==0 or battlefield[posi1-k][posj]==4:
                    end_of_ship=True
                elif battlefield[posi1-k][posj]==1:
                    return False
                
        end_of_ship=False
        k=0
        while not end_of_ship:
            if posi1+k==10:
                end_of_ship=True
            elif battlefield[posi1+k][posj]==0 or battlefield[posi1+k][posj]==4:
                end_of_ship=True
            else:
                battlefield[posi1+k][posj]=3
                killed = True
            k=k+1
            
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            if posi1-k==-1:
                end_of_ship=True
            elif battlefield[posi1-k][posj]==0 or battlefield[posi1-k][posj]==4:
                end_of_ship=True
            else:
                battlefield[posi1-k][posj]=3
                killed = True
    return True

def draw_battlefields(mybattlefield, enemybattlefield, posi, posj):
    print("  ", end = "   ")
    for j in range(10):
        print(" "+columns[j], end = "   ")
    print("  ", end = "   ")
    print("  ", end = "   ")
    for j in range(10):
        print(" "+columns[j], end = "   ")        
    print ('\n')
    
    for i in range(10):        
        if i<9:
            print(" "+lines[i], end = "   ")
        else:
            print(lines[i], end = "   ")
            
        for j in range(10):            
            if mybattlefield[i][j]==0: #ïóñòî
                print('|_|', end = "  ")  
            elif mybattlefield[i][j]==1: #öåëûé êîðàáëü
                print('|X|', end = "  ")
            elif mybattlefield[i][j]==2: #ïîäáèò
                print('|/|', end = "  ")
            elif mybattlefield[i][j]==3: #óáèò
                print('|0|', end = "  ")
            elif mybattlefield[i][j]==4: #ïðîìàõ
                print('|.|', end = "  ")
                    
        print("  ", end = "   ")
        if i<9:
            print(" "+lines[i], end = "   ")
        else:
            print(lines[i], end = "   ")
            
        for j in range(10):            
            if i==posi and j==posj:
                print('|?|', end = "  ")
            else:
                if enemybattlefield[i][j]==0: #ïóñòî
                    print('|_|', end = "  ")  
                elif enemybattlefield[i][j]==1: #öåëûé êîðàáëü
                    print('|X|', end = "  ")
                elif enemybattlefield[i][j]==2: #ïîäáèò
                    print('|/|', end = "  ")
                elif enemybattlefield[i][j]==3: #óáèò
                    print('|0|', end = "  ")
                elif enemybattlefield[i][j]==4: #ïðîìàõ
                    print('|.|', end = "  ")                    
        print ('\n')  
    print ('\t\t\tYour Field\t\t\t\t\t\t    Enemys Field')
    print ('w, a, s, d - moving')
    print ('e - shot')
    return True

def check_correct_shot(enemybattlefield,posi,posj):
    if enemybattlefield[posi][posj]==3 or enemybattlefield[posi][posj]==4 or enemybattlefield[posi][posj]==2:
        return False
    else:
        return True
    
def shot(enemybattlefield,posi,posj,id):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://46.32.79.43:5000")
    socket.send("%i Shot %i %i" % (id, posi, posj))
    reply = socket.recv()
    return reply

def walk_on_battlefield(mybattlefield, enemybattlefield, id):    
    posi=0
    posj=0
    os.system('cls')
    draw_battlefields(mybattlefield, enemybattlefield, 0, 0)

    while True:    #íàïèñàòü óñëîâèå âûõîäà
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch == 's':
                if posi != 9:
                    posi=posi+1
                    os.system('cls')
                    draw_battlefields(mybattlefield, enemybattlefield, posi, posj)
            elif ch == 'w':
                if posi!=0:
                    posi=posi-1
                    os.system('cls')
                    draw_battlefields(mybattlefield, enemybattlefield, posi, posj)
            elif ch == 'a':
                if posj!=0:
                    posj=posj-1
                    os.system('cls')
                    draw_battlefields(mybattlefield, enemybattlefield, posi, posj)
            elif ch == 'd':
                if posj!=9:
                    posj=posj+1
                    os.system('cls')
                    draw_battlefields(mybattlefield, enemybattlefield, posi, posj)
            elif ch == 'e':
                if check_correct_shot(enemybattlefield,posi,posj):
                    check = shot(enemybattlefield,posi,posj, id)
                    if(check!="Win" and check!="Lose"):
                            enemy_battlefield[posi][posj] = int(check)
                            if(check == "3"):
                                
                                if posi!=0:
                                    if enemy_battlefield[posi-1][posj]==1 or enemy_battlefield[posi-1][posj]==2:
                                        enemy_battlefield[posi][posj]=2 #ðàíåí
                                        #print('check '+str(posi)+'-'+str(posi-1)+' '+str(posj))
                                        check_chotted_battle(enemy_battlefield, posi, posj, posi-1, posj)
                                        check = True
                            
                                if posi!=9:
                                    if enemy_battlefield[posi+1][posj]==1 or enemy_battlefield[posi+1][posj]==2:
                                        enemy_battlefield[posi][posj]=2 #ðàíåí
                                        #print('check '+str(posi)+'-'+str(posi+1)+' '+str(posj))
                                        check_chotted_battle(enemy_battlefield, posi, posj, posi+1, posj)
                                        check = True
                                if posj!=0:
                                    if enemy_battlefield[posi][posj-1]==1 or enemy_battlefield[posi][posj-1]==2:
                                        enemy_battlefield[posi][posj]=2 #ðàíåí
                                        #print('check '+str(posi)+' '+str(posj)+'-'+str(posj-1))
                                        check_chotted_battle(enemy_battlefield, posi, posj, posi, posj-1)
                                        check = True
                
                                if posj!=9:
                                    if enemy_battlefield[posi][posj+1]==1 or enemy_battlefield[posi][posj+1]==2:
                                        enemy_battlefield[posi][posj]=2 #ðàíåí
                                        #print('check '+str(posi)+' '+str(posj)+'-'+str(posj+1))
                                        check_chotted_battle(enemy_battlefield, posi, posj, posi, posj+1)
                                        check = True
                    
                            os.system('cls')
                            draw_battlefields(mybattlefield, enemybattlefield, 10, 10)
                            return "No"
                    else:
                        enemy_battlefield[posi][posj] = 2
                        os.system('cls')
                        draw_battlefields(mybattlefield, enemybattlefield, 10, 10)
                        return check
                    os.system('cls')
                    draw_battlefields(mybattlefield, enemybattlefield, posi, posj)
                else:
                    os.system('cls')
                    draw_battlefields(mybattlefield, enemybattlefield, posi, posj)
                    print ('\nError:\tInvalid position, try again')
    return True

if __name__ == "__main__":
    context = zmq.Context()
    #  Socket to talk to server
    print("Connecting to server")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://46.32.79.43:5000")
    
    print("Press 1 if you want to play vs player")
    print("Press 2 if you want to play vs bot")
    ch = msvcrt.getch()
    if(ch == '1'): 
        message = "0 Connection"
        socket.send(str(message))
        reply = socket.recv()
    else:
        message = "0 Bot"
        socket.send(str(message))
        reply = socket.recv()
    print(reply)
    id = int(reply)
    if(ch == '1'):
        while (reply!="Start"):
            socket.send("%i Wait" % id)
            reply = socket.recv()
            print(reply)
            time.sleep(1)
    else:
        socket.send("%i Wait" % id)
        reply = socket.recv()
        print(reply)
    my_battlefield = np.zeros((10,10))
    placing_ships(my_battlefield)
    board_str = ''
    for i in range(10):
        for j in range(10):
            board_str = board_str + str(int(my_battlefield[i][j]))
    board_str = str(id) + " Upload " + board_str
    socket.send(board_str)
    reply = socket.recv()
    print(reply)
    
    enemy_battlefield = np.zeros((10,10))
    #draw_battlefields(my_battlefield, enemy_battlefield, 1, 1)
    socket.send("%i Turn" % id)
    reply = socket.recv()
    while(reply!="Win" and reply!="Lose"):
        if(reply != "No"):
            c = 0
            for i in range(10):
                for j in range(10):
                    my_battlefield[i][j] = int(reply[c])
                    c = c + 1
            reply = walk_on_battlefield(my_battlefield, enemy_battlefield, id)
        else:
            socket.send("%i Turn" % id)
            reply = socket.recv()
        time.sleep(0.5)
    os.system('cls')
    draw_battlefields(my_battlefield, enemy_battlefield, 10, 10)
    if(reply == "Win"):
        print ("YOU WON!!!")
    else:
        print ("YOU LOSE!!!")
        
    '''
    reply = "Nothing"
    while (reply == "Nothing"):
        socket.send("%i Get" % id)
        reply = socket.recv()
        time.sleep(1)
    print(reply)    
    c = 0
    for i in range(10):
        for j in range(10):
            enemy_battlefield[i][j] = int(reply[c])
            c = c + 1
    '''
    
