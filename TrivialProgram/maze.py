import copy

def move_algo(map: list, id: int, size_m: int, size_n: int)->int:
    ml = []
    fpos1 = []
    fpos2 = []
    dis = []
    open1 = []
    count1 = []
    count2 = []
    dicst = {}
    minimum_cost = {}
    is_visited = {}

    for m in range(size_m): #m=0~14
        ml.append(map[m*size_n:(m+1)*size_n])

    for x in range(size_m):#有问题
        for y in range(size_n):
            if ml[x][y] == 2*id:
                head = (x,y)                
                open1.append(head) #open1=[[x,y]]

    if open1 == []:
        return -1            

    for fi in range(size_m): #x=head[0],y=head[1]  先记录下所有食物位置
        for fj in range(size_n):
            if ml[fi][fj] == -1:
                food = [fi,fj]
                fpos1.append(food)

    if fpos1 == []: #wrong answer了 t7
        if len(ml) > 1:
            if head[0] == 0:
                if head[1] == 0:                    
                    if ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    elif ml[head[0]+1][head[1]] == 0:
                        ANS = 2
                        return ANS
                    else:
                        return -1
                if head[1] == size_n -1:                                   
                    if ml[head[0]+1][head[1]] == 0:
                        ANS = 2
                        return ANS
                    elif ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1
                else:
                    if ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    elif ml[head[0]+1][head[1]] == 0:
                        ANS = 2
                        return ANS
                    elif ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1
            elif head[0] == size_m - 1:
                if head[1] == 0:                    
                    if ml[head[0]-1][head[1]] == 0:
                        ANS = 0
                        return ANS
                    elif ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    else:
                        return -1
                if head[1] == size_n -1:
                    if ml[head[0]-1][head[1]] == 0:
                        ANS = 0
                        return ANS                    
                    elif ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1
                else:
                    if ml[head[0]-1][head[1]] == 0:
                        ANS = 0
                        return ANS
                    elif ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    elif ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1
            elif head[1] == 0:
                if head[0] == 0:
                    if ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    elif ml[head[0]+1][head[1]] == 0:
                        ANS = 2
                        return ANS
                    else:
                        return -1
                elif head[0] == size_m - 1:
                    if ml[head[0]-1][head[1]] == 0:
                        ANS = 0
                        return ANS
                    elif ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    else:
                        return -1
                else:
                    if ml[head[0]-1][head[1]] == 0:
                        ANS = 0
                        return ANS
                    elif ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    elif ml[head[0]+1][head[1]] == 0:
                        ANS = 2
                        return ANS
                    else:
                        return -1
            elif head[1] == size_n -1:
                if head[0] == 0:
                    if ml[head[0]+1][head[1]] == 0:
                        ANS = 2
                        return ANS
                    elif ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1
                elif head[0] == size_m - 1:
                    if ml[head[0]-1][head[1]] == 0:
                        ANS = 0
                        return ANS
                    elif ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1
                else:
                    if ml[head[0]-1][head[1]] == 0:
                        ANS = 0
                        return ANS                    
                    elif ml[head[0]+1][head[1]] == 0:
                        ANS = 2
                        return ANS
                    elif ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1
            else:
                if ml[head[0]-1][head[1]] == 0:
                    ANS = 0
                    return ANS
                elif ml[head[0]][head[1]+1] == 0:
                    ANS = 1
                    return ANS
                elif ml[head[0]+1][head[1]] == 0:
                    ANS = 2
                    return ANS
                elif ml[head[0]][head[1]-1] == 0:
                    ANS = 3
                    return ANS
                else:
                    return -1
        if len(ml) == 1:
            if head[1] == 0:
                if ml[head[0]][head[1]+1] == 0:
                    ANS = 1
                    return ANS
                else:
                    return -1
            elif head[1] == size_n -1:
                if ml[head[0]][head[1]-1] == 0:
                    ANS = 3
                    return ANS
                else:
                    return -1
            else:
                if ml[head[0]][head[1]+1] == 0:
                    ANS = 1
                    return ANS
                elif ml[head[0]][head[1]-1] == 0:
                    ANS = 3
                    return ANS
                else:
                    return -1

    if fpos1 != []:
        for i in range(size_m): #计算距离时，是否需要+1  #计算每一个点到fpos中的每一个food的hm距离，然后取最小的
            for j in range(size_n):#fpos[n][0]是food的x
                for n in range(len(fpos1)):
                    heuristic = abs(fpos1[n][0] - i) + abs(fpos1[n][1] - j)
                    dis.append(heuristic)#这个距离要干啥用呢,怎么再后续存储时继续调用，不被覆盖？
                    heuristic_dist = min(dis) #需不需要return？ 记得清空dis
                    dicst[(i,j)] = heuristic_dist #字典
                dis = []

        for i in range(size_m):
            for j in range(size_n):
                minimum_cost[(i,j)] = 0
                is_visited[(i,j)] = False

        prev_point = copy.deepcopy(ml)
        for ii in range(len(prev_point)):
            for jj in range(len(prev_point[0])):
                prev_point[ii][jj] = ()

        while open1 != []:
            if len(open1) == 1: 
                P = (open1[0][0],open1[0][1])
                if ml[P[0]][P[1]] == -1:                                      
                    fpos2.append(P)#food的坐标
                    break
                is_visited[P] = True
                open1.remove(P)
                for Q in [(P[0]-1,P[1]),(P[0],P[1]+1),(P[0]+1,P[1]),(P[0],P[1]-1)]:
                    if (Q[0] >= 0) and (Q[1] >= 0) and (Q[0] < size_m) and (Q[1] < size_n) and (ml[Q[0]][Q[1]] == -1 or ml[Q[0]][Q[1]] == 0) and (is_visited[Q] == False or minimum_cost[P] + 1 < minimum_cost[Q]):
                        open1.append(Q)
                        minimum_cost[Q] = minimum_cost[P] + 1
                        prev_point[Q[0]][Q[1]] = P
            if len(open1) > 1:
                open1 = list(set(open1))
                open1.sort(key = lambda x:((minimum_cost[x] + dicst[x]),x[0],x[1]))
                P = open1[0]
                if ml[P[0]][P[1]] == -1:                                      
                    fpos2.append(P)#food的坐标
                    break
                is_visited[P] = True
                open1.remove(P)                             
                for Q in [(P[0]-1,P[1]),(P[0],P[1]+1),(P[0]+1,P[1]),(P[0],P[1]-1)]:
                    if (Q[0] >= 0) and (Q[1] >= 0) and (Q[0] < size_m) and (Q[1] < size_n) and (ml[Q[0]][Q[1]] == -1 or ml[Q[0]][Q[1]] == 0) and (is_visited[Q] == False or minimum_cost[P] + 1 < minimum_cost[Q]):
                        open1.append(Q)
                        minimum_cost[Q] = minimum_cost[P] + 1
                        prev_point[Q[0]][Q[1]] = P


        if fpos2 == []:#open1=[[x,y]] x=head[0],y=head[1]
            if len(ml) > 1:
                if head[0] == 0:
                    if head[1] == 0:                    
                        if ml[head[0]][head[1]+1] == 0:
                            ANS = 1
                            return ANS
                        elif ml[head[0]+1][head[1]] == 0:
                            ANS = 2
                            return ANS
                        else:
                            return -1
                    if head[1] == size_n -1:                                   
                        if ml[head[0]+1][head[1]] == 0:
                            ANS = 2
                            return ANS
                        elif ml[head[0]][head[1]-1] == 0:
                            ANS = 3
                            return ANS
                        else:
                            return -1
                    else:
                        if ml[head[0]][head[1]+1] == 0:
                            ANS = 1
                            return ANS
                        elif ml[head[0]+1][head[1]] == 0:
                            ANS = 2
                            return ANS
                        elif ml[head[0]][head[1]-1] == 0:
                            ANS = 3
                            return ANS
                        else:
                            return -1
                elif head[0] == size_m - 1:
                    if head[1] == 0:                    
                        if ml[head[0]-1][head[1]] == 0:
                            ANS = 0
                            return ANS
                        elif ml[head[0]][head[1]+1] == 0:
                            ANS = 1
                            return ANS
                        else:
                            return -1
                    if head[1] == size_n -1:
                        if ml[head[0]-1][head[1]] == 0:
                            ANS = 0
                            return ANS                    
                        elif ml[head[0]][head[1]-1] == 0:
                            ANS = 3
                            return ANS
                        else:
                            return -1
                    else:
                        if ml[head[0]-1][head[1]] == 0:
                            ANS = 0
                            return ANS
                        elif ml[head[0]][head[1]+1] == 0:
                            ANS = 1
                            return ANS
                        elif ml[head[0]][head[1]-1] == 0:
                            ANS = 3
                            return ANS
                        else:
                            return -1
                elif head[1] == 0:
                    if head[0] == 0:
                        if ml[head[0]][head[1]+1] == 0:
                            ANS = 1
                            return ANS
                        elif ml[head[0]+1][head[1]] == 0:
                            ANS = 2
                            return ANS
                        else:
                            return -1
                    elif head[0] == size_m - 1:
                        if ml[head[0]-1][head[1]] == 0:
                            ANS = 0
                            return ANS
                        elif ml[head[0]][head[1]+1] == 0:
                            ANS = 1
                            return ANS
                        else:
                            return -1
                    else:
                        if ml[head[0]-1][head[1]] == 0:
                            ANS = 0
                            return ANS
                        elif ml[head[0]][head[1]+1] == 0:
                            ANS = 1
                            return ANS
                        elif ml[head[0]+1][head[1]] == 0:
                            ANS = 2
                            return ANS
                        else:
                            return -1
                elif head[1] == size_n -1:
                    if head[0] == 0:
                        if ml[head[0]+1][head[1]] == 0:
                            ANS = 2
                            return ANS
                        elif ml[head[0]][head[1]-1] == 0:
                            ANS = 3
                            return ANS
                        else:
                            return -1
                    elif head[0] == size_m - 1:
                        if ml[head[0]-1][head[1]] == 0:
                            ANS = 0
                            return ANS
                        elif ml[head[0]][head[1]-1] == 0:
                            ANS = 3
                            return ANS
                        else:
                            return -1
                    else:
                        if ml[head[0]-1][head[1]] == 0:
                            ANS = 0
                            return ANS                    
                        elif ml[head[0]+1][head[1]] == 0:
                            ANS = 2
                            return ANS
                        elif ml[head[0]][head[1]-1] == 0:
                            ANS = 3
                            return ANS
                        else:
                            return -1
                else:
                    if ml[head[0]-1][head[1]] == 0:
                        ANS = 0
                        return ANS
                    elif ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    elif ml[head[0]+1][head[1]] == 0:
                        ANS = 2
                        return ANS
                    elif ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1
            if len(ml) == 1:
                if head[1] == 0:
                    if ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    else:
                        return -1
                elif head[1] == size_n -1:
                    if ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1
                else:
                    if ml[head[0]][head[1]+1] == 0:
                        ANS = 1
                        return ANS
                    elif ml[head[0]][head[1]-1] == 0:
                        ANS = 3
                        return ANS
                    else:
                        return -1

        if fpos2 != []:#这边可能会有问题
            xi = fpos2[0][0]
            yi = fpos2[0][1]
            while (xi,yi) != head:
                pp = (xi,yi)
                (xi,yi) = (prev_point[xi][yi][0],prev_point[xi][yi][1])
            if (pp[0] - head[0] == -1) and (pp[1] - head[1] == 0):
                ANS = 0
                return ANS
            if (pp[0] - head[0] == 0) and (pp[1] - head[1] == 1):
                ANS = 1
                return ANS
            if (pp[0] - head[0] == 1) and (pp[1] - head[1] == 0):
                ANS = 2
                return ANS
            if (pp[0] - head[0] == 0) and (pp[1] - head[1] == -1):
                ANS = 3
                return ANS




if __name__ == "__main__":
    demoMapDir='demoMap/'
    field_image = []
    info=None
    with open(demoMapDir+"0"+".txt", "r") as f:
        info = eval(f.readline().strip())
        for line in f:
            field_image.append(eval(line.strip()))
    flat_image = [item for sublist in field_image for item in sublist]
    assert info[4] == move_algo(flat_image, info[0], info[1], info[2])
    
    for i in range(1,info[3]):
        field_image = []
        with open(demoMapDir+str(i)+".txt", "r") as f:
            moveAns = eval(f.readline().strip())
            for line in f:
                field_image.append(eval(line.strip()))
        flat_image = [item for sublist in field_image for item in sublist]
        assert moveAns == move_algo(flat_image, info[0], info[1], info[2])
