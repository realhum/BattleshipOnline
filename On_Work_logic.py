def check_chotted_battle(battlefield, posi1, posj1, posi2, posj2, player_id):
    if posi1==posi2:
        posi=posi1
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            print('checking'+str(posj1+k))
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
            print('checking'+str(posj1-k))
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
                
    elif posj1==posj2:
        posj=posj1
        end_of_ship=False
        k=0
        while not end_of_ship:
            k=k+1
            print('checking'+str(posi1+k))
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
            print('checking'+str(posi1-k))
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
    return True

def shot(battlefield,posi,posj,player_id):
    if battlefield[posi][posj][player_id]==0: #ïóñòî
        battlefield[posi][posj][player_id]=4
    elif battlefield[posi][posj][player_id]==1: #íåòðîíóòûé êîðàáëü
        global shotted
        shotted=shotted+1
        if posi!=0:
            if battlefield[posi-1][posj][player_id]==1 or battlefield[posi-1][posj][player_id]==2:
                battlefield[posi][posj][player_id]=2 #ðàíåí
                print('check '+str(posi)+'-'+str(posi-1)+' '+str(posj))
                check_chotted_battle(battlefield, posi, posj, posi-1, posj, player_id)
                return True            
        if posi!=9:
            if battlefield[posi+1][posj][player_id]==1 or battlefield[posi+1][posj][player_id]==2:
                battlefield[posi][posj][player_id]=2 #ðàíåí
                print('check '+str(posi)+'-'+str(posi+1)+' '+str(posj))
                check_chotted_battle(battlefield, posi, posj, posi+1, posj, player_id)
                return True
        if posj!=0:
            if battlefield[posi][posj-1][player_id]==1 or battlefield[posi][posj-1][player_id]==2:
                battlefield[posi][posj][player_id]=2 #ðàíåí
                print('check '+str(posi)+' '+str(posj)+'-'+str(posj-1))
                check_chotted_battle(battlefield, posi, posj, posi, posj-1, player_id)
                return True
        if posj!=9:
            if battlefield[posi][posj+1][player_id]==1 or battlefield[posi][posj+1][player_id]==2:
                battlefield[posi][posj][player_id]=2 #ðàíåí
                print('check '+str(posi)+' '+str(posj)+'-'+str(posj+1))
                check_chotted_battle(battlefield, posi, posj, posi, posj+1, player_id)
                return True
        battlefield[posi][posj][player_id]=3 #óáèò
    return True
    
