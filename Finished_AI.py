#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import msvcrt
import os
import zmq
from __future__ import print_function
import numpy as np
import random
import time

mybattlefield = np.zeros((10, 10, 50))
enemybattlefields = np.zeros((10, 10, 50))


def set_ship(battlefield, posi, posj,player_id, vertically, ship): 
    for i in range(ship):
        if vertically:
            battlefield[posi+i][posj][player_id]=1
        else:
            battlefield[posi][posj+i][player_id]=1
    return True

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
        if check_correct_position(mybattlefield,posi,posj,player_id,vertically,ships_to_set[0]):
            set_ship(mybattlefield,posi,posj,player_id,vertically,ships_to_set[0])
            ships_to_set = np.delete(ships_to_set,0,0)
    return True

def check_correct_shot(enemybattlefield,posi,posj, player_id):
    if enemybattlefield[posi][posj][player_id]==3 or enemybattlefield[posi][posj][player_id]==4:
        return False
    else:
        return True
    
def shot(enemybattlefield,posi,posj,player_id):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://46.32.79.43:5000")
    socket.send("%i BotShot %i %i" % (player_id, posi, posj))
    reply = socket.recv()
    return reply
    
def step_in_game(player_id):
    '''
    list_to_shot_i=[]
    list_to_shot_j=[]
    for i in range(10):     
        for j in range(10):
            if enemybattlefields[i][j][player_id]==2:
                if i!=9:
                    list_to_shot_i.append(i+1)
                    list_to_shot_j.append(j)
                if i!=0:
                    list_to_shot_i.append(i-1)
                    list_to_shot_j.append(j)                    
                if j!=9:
                    list_to_shot_i.append(i)
                    list_to_shot_j.append(j+1)
                if j!=0:
                    list_to_shot_i.append(i)
                    list_to_shot_j.append(j-1)
    shot_is_done=False
    while len(list_to_shot_i)!=0 and not shot_is_done:
        if check_correct_shot(enemybattlefields, list_to_shot_i[0], list_to_shot_j[0], player_id):
            #print('shot from list pos: '+str(list_to_shot_i[0])+' '+str(list_to_shot_j[0])+':'+str(enemybattlefields[list_to_shot_i[0]][list_to_shot_j[0]][player_id]))
            check = shot(enemybattlefields,list_to_shot_i[0],list_to_shot_j[0], player_id)
            posi = list_to_shot_i[0]
            posj = list_to_shot_j[0]
            enemybattlefields[posi][posj][player_id] = int(check)
            if(check == "3"):           
                if posi!=0:
                    if enemybattlefields[posi-1][posj][player_id]==1 or enemybattlefields[posi-1][posj][player_id]==2:
                        
                        #print('check '+str(posi)+'-'+str(posi-1)+' '+str(posj))
                        check_chotted_battle(enemybattlefields, posi, posj, posi-1, posj, player_id)
                        
                            
                if posi!=9:
                    if enemybattlefields[posi+1][posj][player_id]==1 or enemybattlefields[posi+1][posj][player_id]==2:
                        
                        #print('check '+str(posi)+'-'+str(posi+1)+' '+str(posj))
                        check_chotted_battle(enemybattlefields, posi, posj, posi+1, posj, player_id)
                        
                if posj!=0:
                    if enemybattlefields[posi][posj-1][player_id]==1 or enemybattlefields[posi][posj-1][player_id]==2:
                        
                        #print('check '+str(posi)+' '+str(posj)+'-'+str(posj-1))
                        check_chotted_battle(enemybattlefields, posi, posj, posi, posj-1, player_id)
                        
                
                if posj!=9:
                    if enemybattlefields[posi][posj+1][player_id]==1 or enemybattlefields[posi][posj+1][player_id]==2:
                        
                        #print('check '+str(posi)+' '+str(posj)+'-'+str(posj+1))
                        check_chotted_battle(enemybattlefields, posi, posj, posi, posj+1, player_id)
            
            shot_is_done=True
            #draw_battlefield_for_shipsetting(enemybattlefields, player_id)
        else:
            list_to_shot_i.pop(0)
            list_to_shot_j.pop(0)
    '''
    shot_is_done=False
    while not shot_is_done:
        posi=random.randint(0,9)
        posj=random.randint(0,9)
        #print('shot pos: '+str(posi)+' '+str(posj)+':'+str(enemybattlefields[posi][posj][player_id]))
        if check_correct_shot(enemybattlefields, posi, posj, player_id):
            #print('shot pos: '+str(posi)+' '+str(posj))
            check = shot(enemybattlefields, posi, posj, player_id)
            enemybattlefields[posi][posj][player_id] = int(check)
            '''
            if(check == "3"):           
                if posi!=0:
                    if enemybattlefields[posi-1][posj][player_id]==1 or enemybattlefields[posi-1][posj][player_id]==2:
                        #enemybattlefields[posi][posj][player_id]=2 #ранен
                        #print('check '+str(posi)+'-'+str(posi-1)+' '+str(posj))
                        check_chotted_battle(enemybattlefields, posi, posj, posi-1, posj, player_id)
                        
                            
                if posi!=9:
                    if enemybattlefields[posi+1][posj][player_id]==1 or enemybattlefields[posi+1][posj][player_id]==2:
                        #enemybattlefields[posi][posj][player_id]=2 #ранен
                        #print('check '+str(posi)+'-'+str(posi+1)+' '+str(posj))
                        check_chotted_battle(enemybattlefields, posi, posj, posi+1, posj, player_id)
                        
                if posj!=0:
                    if enemybattlefields[posi][posj-1][player_id]==1 or enemybattlefields[posi][posj-1][player_id]==2:
                        #enemybattlefields[posi][posj][player_id]=2 #ранен
                        #print('check '+str(posi)+' '+str(posj)+'-'+str(posj-1))
                        check_chotted_battle(enemybattlefields, posi, posj, posi, posj-1, player_id)
                        
                
                if posj!=9:
                    if enemybattlefields[posi][posj+1][player_id]==1 or enemybattlefields[posi][posj+1][player_id]==2:
                        #enemybattlefields[posi][posj][player_id]=2 #ранен
                        #print('check '+str(posi)+' '+str(posj)+'-'+str(posj+1))
                        check_chotted_battle(enemybattlefields, posi, posj, posi, posj+1, player_id)
            '''            
            shot_is_done=True
    #draw_battlefield_for_shipsetting(enemybattlefields, player_id)        
    return True

context = zmq.Context()
#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://46.32.79.43:5000")
while (True):
    socket.send("0 BotPlay")
    reply = socket.recv()
    if(reply!="No"):
        player_id = int(reply)
        step_in_game(player_id)

    time.sleep(0.5)



# In[ ]:





# In[ ]:




