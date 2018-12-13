#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
import zmq
import msvcrt
import os
from __future__ import print_function
import numpy as np
import random

bot_arr = np.zeros((10,10,50))
shot_arr = np.zeros(50)
killed = False

class Player(object):
    def __init__(self, id_player, id_duo, isPlaying, isWaiting, placement, isUploaded, myTurn, niceShot, winner, vsBot, getShot):
        self.id_player = id_player
        self.id_duo = id_duo
        self.isPlaying = isPlaying
        self.isWaiting = isWaiting
        self.placement = placement
        self.isUploaded = isUploaded
        self.myTurn = myTurn
        self.niceShot = niceShot
        self.winner = winner
        self.vsBot = vsBot
        self.getShot = getShot

def check_chotted_battle(battlefield, posi1, posj1, posi2, posj2, player_id):
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
                if battlefield[posi][posj1+k][player_id]==0 or battlefield[posi][posj1+k][player_id]==4:
                    end_of_ship=True
                elif battlefield[posi][posj1+k][player_id]==1:
                    return False
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            #print('checking'+str(posj1-k))
            if posj1-k==-1:
                end_of_ship=True
            else:
                if battlefield[posi][posj1-k][player_id]==0 or battlefield[posi][posj1-k][player_id]==4:
                    end_of_ship=True
                elif battlefield[posi][posj1-k][player_id]==1:
                    return False
                
        end_of_ship=False
        k=0
        while not end_of_ship:
            if posj1+k==10:
                end_of_ship=True
            elif battlefield[posi][posj1+k][player_id]==0 or battlefield[posi][posj1+k][player_id]==4:
                end_of_ship=True
            else:
                battlefield[posi][posj1+k][player_id]=3
                killed = True
            k=k+1
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            if posj1-k==-1:
                end_of_ship=True
            elif battlefield[posi][posj1-k][player_id]==0 or battlefield[posi][posj1-k][player_id]==4:
                end_of_ship=True
            else:
                battlefield[posi][posj1-k][player_id]=3
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
                if battlefield[posi1+k][posj][player_id]==0 or battlefield[posi1+k][posj][player_id]==4:
                    end_of_ship=True
                elif battlefield[posi1+k][posj][player_id]==1:
                    return False
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            #print('checking'+str(posi1-k))
            if posi1-k==-1:
                end_of_ship=True
            else:
                if battlefield[posi1-k][posj][player_id]==0 or battlefield[posi1-k][posj][player_id]==4:
                    end_of_ship=True
                elif battlefield[posi1-k][posj][player_id]==1:
                    return False
                
        end_of_ship=False
        k=0
        while not end_of_ship:
            if posi1+k==10:
                end_of_ship=True
            elif battlefield[posi1+k][posj][player_id]==0 or battlefield[posi1+k][posj][player_id]==4:
                end_of_ship=True
            else:
                battlefield[posi1+k][posj][player_id]=3
                killed = True
            k=k+1
            
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            if posi1-k==-1:
                end_of_ship=True
            elif battlefield[posi1-k][posj][player_id]==0 or battlefield[posi1-k][posj][player_id]==4:
                end_of_ship=True
            else:
                battlefield[posi1-k][posj][player_id]=3
                killed = True
    return True
        
def set_ship(battlefield, posi, posj,player_id, vertically, ship): 
    for i in range(ship):
        if vertically:
            battlefield[posi+i][posj][player_id]=1
        else:
            battlefield[posi][posj+i][player_id]=1
    return True

def check_correct_position(battlefield, posi, posj, player_id, vertically, ship):
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
            if battlefield[check_posi+i][check_posj+j][player_id]==1:
                return False
    return True

def placing_ships(player_id):  
    ships_to_set = np.array([4,3,3,2,2,2,1,1,1,1])
    while len(ships_to_set)!=0:  
        posi=random.randint(0,9)
        posj=random.randint(0,9)
        vertically=random.choice([True,False])
        if check_correct_position(bot_arr,posi,posj,player_id,vertically,ships_to_set[0]):
            set_ship(bot_arr,posi,posj,player_id,vertically,ships_to_set[0])
            ships_to_set = np.delete(ships_to_set,0,0)
    return True
        
if __name__ == "__main__":
    boards_arr = np.zeros((10, 10, 50))
    for i in range(50):
        placing_ships(i)
    context = zmq.Context()
    socket_connect = context.socket(zmq.REP)
    socket_connect.bind("tcp://*:5000")
    players_arr = []
    count = 0
    for i in range(0, 50):
        players_arr.append(Player(i, -1, False, False, "Last", False, False, 0, "No", False, 0))
    while True:
        message = socket_connect.recv()
        print(message)
        split_mes = message.split()
        id_player = int(split_mes[0])
        command = split_mes[1]
        if(command == "Connection"):
            count = count + 1
            players_arr[count].isWaiting = True
            socket_connect.send(str(count))
        if(command == "Bot"):
            count = count + 1
            players_arr[count].vsBot = True
            players_arr[count].isWaiting = True
            socket_connect.send(str(count))
       

        elif(command == "Wait"):
            if(not players_arr[id_player].vsBot):
                if(players_arr[id_player].id_duo == -1):
                    for i in range(1, 50):
                        if(i!=id_player and players_arr[i].isWaiting):
                            players_arr[id_player].id_duo = i
                            players_arr[id_player].isWaiting = False
                            players_arr[id_player].isPlaying = True
                            players_arr[id_player].placement = "First"
                            players_arr[i].id_duo = id_player
                            players_arr[i].isWaiting = False
                            players_arr[i].isPlaying = True
                            players_arr[i].placement = "Second"
                            socket_connect.send("Start")
                            break
                else:
                    socket_connect.send("Start")
                if(players_arr[id_player].id_duo == -1):
                    socket_connect.send("Not found yet")
            else:
                players_arr[id_player].isWaiting = False
                players_arr[id_player].isPlaying = True
                players_arr[id_player].placement = "First"
                socket_connect.send("Start")
        elif(command == "Upload"):
            arr = split_mes[2]
            c = 0
            for i in range(10):
                for j in range(10):
                    boards_arr[i][j][id_player] = int(arr[c])
                    c = c + 1
            print (boards_arr)
            players_arr[id_player].isUploaded = True
            socket_connect.send("Ok")
        
        elif(command == "Place"):
            if (players_arr[id_player].placement == "First"):
                players_arr[id_player].myTurn = True
            socket_connect.send(players_arr[id_player].placement)
        elif(command == "Turn"):
            if(not players_arr[id_player].vsBot):
                duo_id = players_arr[id_player].id_duo
                if(players_arr[duo_id].isUploaded):
                    if(players_arr[id_player].placement == "Second"):
                        if(players_arr[id_player].winner == "Lose"):
                            socket_connect.send("Lose")
                        else: 
                            socket_connect.send("No")
                    else:
                        board_str = ''
                        for i in range(10):
                            for j in range(10):
                                board_str = board_str + str(int(boards_arr[i][j][id_player]))
                        socket_connect.send(board_str)
                else:
                    socket_connect.send("No")
            else:
                if(players_arr[id_player].placement == "Second"):
                    if(players_arr[id_player].winner == "Lose"):
                        socket_connect.send("Lose")
                    else: 
                        socket_connect.send("No")
                else:
                    board_str = ''
                    for i in range(10):
                        for j in range(10):
                            board_str = board_str + str(int(boards_arr[i][j][id_player]))
                    socket_connect.send(board_str)
        elif(command == "Shot"):
            posi = int(split_mes[2])
            posj = int(split_mes[3])
            if(not players_arr[id_player].vsBot):
                duo_id = players_arr[id_player].id_duo
                global killed
                killed = False
                check = False
                if(boards_arr[posi][posj][duo_id] == 1):
                    if posi!=0:
                        if boards_arr[posi-1][posj][duo_id]==1 or boards_arr[posi-1][posj][duo_id]==2:
                            boards_arr[posi][posj][duo_id]=2 #ранен
                            #print('check '+str(posi)+'-'+str(posi-1)+' '+str(posj))
                            check_chotted_battle(boards_arr, posi, posj, posi-1, posj, duo_id)
                            check = True
                            
                    if posi!=9:
                        if boards_arr[posi+1][posj][duo_id]==1 or boards_arr[posi+1][posj][duo_id]==2:
                            boards_arr[posi][posj][duo_id]=2 #ранен
                            #print('check '+str(posi)+'-'+str(posi+1)+' '+str(posj))
                            check_chotted_battle(boards_arr, posi, posj, posi+1, posj, duo_id)
                            check = True
                    if posj!=0:
                        if boards_arr[posi][posj-1][duo_id]==1 or boards_arr[posi][posj-1][duo_id]==2:
                            boards_arr[posi][posj][duo_id]=2 #ранен
                            #print('check '+str(posi)+' '+str(posj)+'-'+str(posj-1))
                            check_chotted_battle(boards_arr, posi, posj, posi, posj-1, duo_id)
                            check = True
                
                    if posj!=9:
                        if boards_arr[posi][posj+1][duo_id]==1 or boards_arr[posi][posj+1][duo_id]==2:
                            boards_arr[posi][posj][duo_id]=2 #ранен
                            #print('check '+str(posi)+' '+str(posj)+'-'+str(posj+1))
                            check_chotted_battle(boards_arr, posi, posj, posi, posj+1, duo_id)
                            check = True
                    
                    players_arr[id_player].niceShot += 1
                    if(players_arr[id_player].niceShot == 20):
                        players_arr[id_player].winner = "Win"
                        players_arr[duo_id].winner = "Lose"
                        socket_connect.send("Win")
                    else:
                        players_arr[id_player].placement = "Second"
                        players_arr[duo_id].placement = "First"
                        if(check and not killed):
                            #boards_arr[posi][posj][duo_id] = 3
                            socket_connect.send("2")
                        #elif(not check):
                        #    socket_connect.send("3")
                            #boards_arr[posi][posj][duo_id] = 3
                        else:
                            boards_arr[posi][posj][duo_id] = 3
                            socket_connect.send("3")
                elif(boards_arr[posi][posj][duo_id] == 0):
                    boards_arr[posi][posj][duo_id] = 4
                    players_arr[id_player].placement = "Second"
                    players_arr[duo_id].placement = "First"
                    socket_connect.send("4")
            else:
                global killed
                killed = False
                check = False
                if(bot_arr[posi][posj][id_player] == 1):
                    if posi!=0:
                        if bot_arr[posi-1][posj][id_player]==1 or bot_arr[posi-1][posj][id_player]==2:
                            bot_arr[posi][posj][id_player]=2 #ранен
                            #print('check '+str(posi)+'-'+str(posi-1)+' '+str(posj))
                            check_chotted_battle(bot_arr, posi, posj, posi-1, posj, id_player)
                            check = True
                            
                    if posi!=9:
                        if bot_arr[posi+1][posj][id_player]==1 or bot_arr[posi+1][posj][id_player]==2:
                            bot_arr[posi][posj][id_player]=2 #ранен
                            #print('check '+str(posi)+'-'+str(posi+1)+' '+str(posj))
                            check_chotted_battle(bot_arr, posi, posj, posi+1, posj, id_player)
                            check = True
                    if posj!=0:
                        if bot_arr[posi][posj-1][id_player]==1 or bot_arr[posi][posj-1][id_player]==2:
                            bot_arr[posi][posj][id_player]=2 #ранен
                            #print('check '+str(posi)+' '+str(posj)+'-'+str(posj-1))
                            check_chotted_battle(bot_arr, posi, posj, posi, posj-1, id_player)
                            check = True
                
                    if posj!=9:
                        if bot_arr[posi][posj+1][id_player]==1 or bot_arr[posi][posj+1][id_player]==2:
                            bot_arr[posi][posj][id_player]=2 #ранен
                            #print('check '+str(posi)+' '+str(posj)+'-'+str(posj+1))
                            check_chotted_battle(bot_arr, posi, posj, posi, posj+1, id_player)
                            check = True
                    players_arr[id_player].niceShot += 1
                    if(players_arr[id_player].niceShot == 20):
                        players_arr[id_player].winner = "Win"
                        socket_connect.send("Win")
                    else:
                        players_arr[id_player].placement = "Second"
                        if(check and not killed):
                            #boards_arr[posi][posj][duo_id] = 3
                            socket_connect.send("2")
                        #elif(not check):
                        #    socket_connect.send("3")
                            #boards_arr[posi][posj][duo_id] = 3
                        else:
                            bot_arr[posi][posj][id_player] = 3
                            socket_connect.send("3")
                elif(bot_arr[posi][posj][id_player] == 0):
                    bot_arr[posi][posj][id_player] = 4
                    players_arr[id_player].placement = "Second"
                    socket_connect.send("4")
        elif(command == "BotPlay"):
            found = False
            for i in range(50):
                if(players_arr[i].vsBot and players_arr[i].isUploaded and players_arr[i].placement == "Second" and players_arr[i].winner == "No"):
                    found = True
                    socket_connect.send("%i" %i)
                    break
            if(not found):
                socket_connect.send("No")
        elif(command == "BotShot"):
            posi = int(split_mes[2])
            posj = int(split_mes[3])
            global killed
            killed = False
            check = False
            if(boards_arr[posi][posj][id_player] == 1):
                '''
                if posi!=0:
                    if boards_arr[posi-1][posj][id_player]==1 or boards_arr[posi-1][posj][id_player]==2:
                        boards_arr[posi][posj][id_player]=2 #ранен
                        #print('check '+str(posi)+'-'+str(posi-1)+' '+str(posj))
                        check_chotted_battle(boards_arr, posi, posj, posi-1, posj, id_player)
                        check = True
                            
                if posi!=9:
                    if boards_arr[posi+1][posj][id_player]==1 or boards_arr[posi+1][posj][id_player]==2:
                        boards_arr[posi][posj][id_player]=2 #ранен
                        #print('check '+str(posi)+'-'+str(posi+1)+' '+str(posj))
                        check_chotted_battle(boards_arr, posi, posj, posi+1, posj, id_player)
                        check = True
                if posj!=0:
                    if boards_arr[posi][posj-1][id_player]==1 or boards_arr[posi][posj-1][id_player]==2:
                        boards_arr[posi][posj][id_player]=2 #ранен
                        #print('check '+str(posi)+' '+str(posj)+'-'+str(posj-1))
                        check_chotted_battle(boards_arr, posi, posj, posi, posj-1, id_player)
                        check = True
                
                if posj!=9:
                    if boards_arr[posi][posj+1][id_player]==1 or boards_arr[posi][posj+1][id_player]==2:
                        boards_arr[posi][posj][id_player]=2 #ранен
                        #print('check '+str(posi)+' '+str(posj)+'-'+str(posj+1))
                        check_chotted_battle(boards_arr, posi, posj, posi, posj+1, id_player)
                        check = True
                 '''   
                shot_arr[id_player] += 1
                if(shot_arr[id_player] == 20):
                    players_arr[id_player].winner = "Lose"
                    socket_connect.send("No")
                else:
                    players_arr[id_player].placement = "First"
                    if(check and not killed):
                        #boards_arr[posi][posj][duo_id] = 3
                        socket_connect.send("2")
                    #elif(not check):
                    #    socket_connect.send("3")
                        #boards_arr[posi][posj][duo_id] = 3
                    else:
                        boards_arr[posi][posj][id_player] = 3
                        socket_connect.send("3")
            elif(boards_arr[posi][posj][id_player] == 0):
                boards_arr[posi][posj][id_player] = 4
                players_arr[id_player].placement = "First"
                socket_connect.send("4")


# In[ ]:




