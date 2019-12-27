import collections
f=open('input.txt','r')
a=f.readline()
if a[0]=='S':
    First='SINGLE'
else:
    First='GAME'
a = f.readline()
if a[0]=='B':
    piece1='B'
    piece2='W'
else:
    piece1='W'
    piece2='B'
a=f.readline()
a=a[:-1]
time=float(a)
endPlace1={(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(4,0),(4,1)}
endPlace2={(15,15),(15,14),(15,13),(15,12),(15,11),(14,15),(14,14),(14,13),(14,12),(14,11),(14,15),(13,15),(13,14),(13,13),(13,12),(12,15),(12,14),(12,13),(11,15),(11,14)}

matrix = [[0] * 16 for _ in range(16)]
for k in range(16):
    a = str(f.readline())
    res=''
    for i in a:
        if i!='\n':
            res+=i
    for j in range(16):
        matrix[k][j]=res[j]
def isEmpty(i,j,pos):
    if not check(i,j,pos):
        return False
    if pos[i][j]=='.':
        return True
    else:
        return False
f.close()
#检查x，y是否出边界
def check(x, y,pos):
    if (0 <= x < 16) and (0 <= y < 16):
        return True

    return False


#点往周围走的情况
def adjacentPositons(i,j,pos):
    if pos[i][j]=='B':
        if (i,j)in endPlace1 or (i,j) in endPlace2:
            result = []
            directions=[(1, 0), (1, 1), (0, 1)]
            for x, y in directions:
                ni = i + x
                nj = j + y
                if isEmpty(ni, nj, pos) and check(ni, nj, pos):
                    result.append((ni, nj))
            return result
        else:
            result = []
            directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
            for x, y in directions:
                ni = i + x
                nj = j + y
                if isEmpty(ni, nj, pos) and check(ni, nj, pos):
                    if (ni,nj) not in endPlace1:
                        result.append((ni, nj))
            return result
    else:
        if (i,j)in endPlace2 or (i,j) in endPlace1:
            result = []
            directions=[(-1, 0), (-1, -1), (0, -1)]
            for x, y in directions:
                ni = i + x
                nj = j + y
                if isEmpty(ni, nj, pos) and check(ni, nj, pos):
                    result.append((ni, nj))
            return result
        else:
            result = []
            directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
            for x, y in directions:
                ni = i + x
                nj = j + y
                if isEmpty(ni, nj, pos) and check(ni, nj, pos):
                    if (ni, nj) not in endPlace2:
                        result.append((ni, nj))
            return result
#一次跳跃
def getOneHopPositions(i,j,pos):
    result=[]
    directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    for x, y in directions:
        ni = i + x
        nj = j + y
        if check(ni,nj,pos) and not isEmpty(ni,nj,pos):
            ni=ni+x
            nj=nj+y
            if check(ni,nj,pos) and isEmpty(ni,nj,pos):
                result.append((ni,nj))
    return result
def getAllHopPositions(i,j,pos):
    xxx=i
    yyy=j
    visit=[]
    result=[]
    visit.append((i,j))
    parent={}
    queue=collections.deque()
    queue.append((i,j))
    while queue:
        (x,y)=queue.popleft()
        for a in getOneHopPositions(x,y,pos):
            if a not in  visit:
                parent[(a[0],a[1])]=(x,y)
                visit.append((a[0],a[1]))
                queue.append((a[0],a[1]))
                result.append((a[0],a[1]))
    res=[[] for _ in range(len(result))]
    index=0
    if parent:
        for i in result:
            while i in parent.keys():
                res[index].append((i[0],i[1]))
                i = parent[i]
            res[index].append((xxx,yyy))
            res[index]=res[index][::-1]
            index += 1
    ress=[]
    if pos[xxx][yyy]=='B':
        for xx in res:
            if xx[0] in endPlace1:
                if (xx[-1][0]>=xxx and xx[-1][1]>yyy) or (xx[-1][0]>xxx and xx[-1][1]>=yyy):
                    ress.append(xx)
            elif xx[0] in endPlace2:
                if (xx[-1][0],xx[-1][1]) in endPlace2:
                    ress.append(xx)
            else:
                if (xx[-1][0],xx[-1][1]) not in endPlace1:
                    ress.append(xx)
        return ress
    else:
        for xx in res:
            if xx[0] in endPlace2:
                if (xx[-1][0]<=xxx and xx[-1][1]<yyy) or (xx[-1][0]<xxx and xx[-1][1]<=yyy):
                    ress.append(xx)
            elif xx[0] in endPlace1:
                if (xx[-1][0], xx[-1][1]) in endPlace1:
                    ress.append(xx)
            else:
                if (xx[-1][0],xx[-1][1]) not in endPlace2:
                    ress.append(xx)
        return ress

#输出player棋盘的位置
def getPlayerPositions(player,pos):
    result=[]
    for i in range(16):
        for j in range(16):
            if pos[i][j] == player:
                result.append((i,j))
    return result
def isEnd(player,pos):
    position=getPlayerPositions(player,pos)
    if player=='B':
        if set(position)==endPlace2:
            return True
    else:
        if set(position)==endPlace1:
            return True
    return False

def actions(player,pos):
    res=[]
    for i in range(16):
        for j in range(16):
            if pos[i][j]==player:
                res.append((i,j))
    camp=[]
    if player=='B':
        for xx in res:
            if xx in endPlace1:
                camp.append(xx)
        if not camp:
            ress = []
            for i, j in res:
                lvl1 = adjacentPositons(i, j, pos)
                for x in lvl1:
                    if ((i, j), x) not in ress:
                        ress.append([(i, j), x])
                lvl2 = getAllHopPositions(i, j, pos)
                for xx in lvl2:
                    if xx not in ress:
                        ress.append(xx)
            return ress
        else:
            ress = []
            for i, j in camp:
                lvl1 = adjacentPositons(i, j, pos)
                for x in lvl1:
                    if ((i, j), x) not in ress:
                        ress.append([(i, j), x])
                lvl2 = getAllHopPositions(i, j, pos)
                for xx in lvl2:
                    if xx not in ress:
                        ress.append(xx)
            if not ress:
                for i, j in res:
                    lvl1 = adjacentPositons(i, j, pos)
                    for x in lvl1:
                        if ((i, j), x) not in ress:
                            ress.append([(i, j), x])
                    lvl2 = getAllHopPositions(i, j, pos)
                    for xx in lvl2:
                        if xx not in ress:
                            ress.append(xx)
                return ress
            else:
                return ress
    else:
        for xx in res:
            if xx in endPlace2:
                camp.append(xx)
        if not camp:
            ress = []
            for i, j in res:
                lvl1 = adjacentPositons(i, j, pos)
                for x in lvl1:
                    if ((i, j), x) not in ress:
                        ress.append([(i, j), x])
                lvl2 = getAllHopPositions(i, j, pos)
                for xx in lvl2:
                    if xx not in ress:
                        ress.append(xx)
            return ress
        else:
            ress = []
            for i, j in camp:
                lvl1 = adjacentPositons(i, j, pos)
                for x in lvl1:
                    if ((i, j), x) not in ress:
                        ress.append([(i, j), x])
                lvl2 = getAllHopPositions(i, j, pos)
                for xx in lvl2:
                    if xx not in ress:
                        ress.append(xx)
            if not ress:
                for i, j in res:
                    lvl1 = adjacentPositons(i, j, pos)
                    for x in lvl1:
                        if ((i, j), x) not in ress:
                            ress.append([(i, j), x])
                    lvl2 = getAllHopPositions(i, j, pos)
                    for xx in lvl2:
                        if xx not in ress:
                            ress.append(xx)
                return ress
            else:
                return ress
import copy
import random
# action 当前棋盘所有可走的情况
def succ(state,action):
    player=state[0]
    mat=copy.deepcopy(state[1])
    mat[action[0][0]][action[0][1]]='.'
    mat[action[-1][0]][action[-1][1]]=player
    if player=='B':
        new='W'
    else:
        new='B'
    return (new,mat)

def evalFunction(state):
    board=state[1]
    player1=piece1
    if state[0]=='B':
        player2='W'
    else:
        player2='B'
    p1pos=getPlayerPositions(player1,board)
    p2pos=getPlayerPositions(player2,board)
    p1score=0
    p2score=0
    if player1=='B':
        if set(p1pos)==endPlace2:
            return 2**32
        for p in p1pos:
            p1score+=(abs(p[0]-15)+abs(p[1]-15))
        for p in p2pos:
            p2score+=(abs(p[0]-0)+abs(p[1]-0))
    else:
        if set(p1pos)==endPlace1:
            return 2**32
        for p in p1pos:
            p1score += (abs(p[0]-0)+abs(p[1]-0))
        for p in p2pos:
            p2score += (abs(p[0]-15)+abs(p[1]-15))
    return p2score-p1score

def prune(state,depth,alpha,beta):
    if depth==0:
        return evalFunction(state)
    if isEnd(state[0],state[1]):
        return evalFunction(state)
    if state[0]==piece1:
        value=float('-inf')
        allActions=actions(state[0],state[1])
        for action in allActions:
            value=max(value,prune(succ(state,action),depth-1,alpha,beta))
            alpha=max(alpha,value)
            if beta<=alpha:
                break
        return value
    else:
        value = float('inf')
        legal_actions = actions(state[0],state[1])
        for action in legal_actions:
            value = min(value, prune(succ(state, action), depth - 1, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value
def MinMaxValue(state,depth):
    allActions=actions(state[0],state[1])
    if not allActions:
        return None
    beta = float('inf')
    player=state[0]
    alpha=-float('inf')
    score=[prune(succ(state,action),depth-1,alpha,beta) for action in allActions]
    if player==piece1:
        max_score=max(score)
        max_actions=[]
        for index in range(len(score)):
            if score[index]==max_score:
                max_actions.append(allActions[index])
        action = random.choice(max_actions)
    else:
        min_score = min(score)
        min_actions = []
        for index in range(len(score)):
            if score[index] == min_score:
                min_actions.append(allActions[index])
        action = random.choice(min_actions)
    return action


ff = open('output.txt','w')
if First=='SINGLE':
    action = MinMaxValue((piece1, matrix), 1)
    if abs(action[-1][0] - action[0][0]) >= 2 or abs(action[-1][1] - action[0][1]) >= 2:
        move = 'J'
    else:
        move = 'E'

    for act in range(1, len(action)):
        ff.write(move + ' ' + str(action[act - 1][1]) + ',' + str(action[act - 1][0]) + ' ' + str(
            action[act][1]) + ',' + str(action[act][0]))
        if act != len(action) - 1:
            ff.write('\n')
    ff.close()
else:
    count1=0
    count2=0
    for index in getPlayerPositions(piece1,matrix):
        if index in endPlace1 or index in endPlace2:
            count1+=1
    for index in getPlayerPositions(piece2,matrix):
        if index in endPlace1 or index in endPlace2:
            count2+=1
    if time >500:
        if count1 >=14 and count2>=14:
            action = MinMaxValue((piece1, matrix), 3)
            if abs(action[-1][0] - action[0][0]) >= 2 or abs(action[-1][1] - action[0][1]) >= 2:
                move = 'J'
            else:
                move = 'E'

            for act in range(1, len(action)):
                ff.write(move + ' ' + str(action[act - 1][1]) + ',' + str(action[act - 1][0]) + ' ' + str(
                    action[act][1]) + ',' + str(action[act][0]))
                if act != len(action) - 1:
                    ff.write('\n')
            ff.close()
        else:
            action = MinMaxValue((piece1, matrix), 2)
            if abs(action[-1][0] - action[0][0]) >= 2 or abs(action[-1][1] - action[0][1]) >= 2:
                move = 'J'
            else:
                move = 'E'

            for act in range(1, len(action)):
                ff.write(move + ' ' + str(action[act - 1][1]) + ',' + str(action[act - 1][0]) + ' ' + str(
                    action[act][1]) + ',' + str(action[act][0]))
                if act != len(action) - 1:
                    ff.write('\n')
            ff.close()
    elif time<42:
        action = MinMaxValue((piece1, matrix), 1)
        if abs(action[-1][0] - action[0][0]) >= 2 or abs(action[-1][1] - action[0][1]) >= 2:
            move = 'J'
        else:
            move = 'E'

        for act in range(1, len(action)):
            ff.write(move + ' ' + str(action[act - 1][1]) + ',' + str(action[act - 1][0]) + ' ' + str(
                action[act][1]) + ',' + str(action[act][0]))
            if act != len(action) - 1:
                ff.write('\n')
        ff.close()
    else:
        if count1>=14 or count2>=14:
            action = MinMaxValue((piece1, matrix), 3)
            if abs(action[-1][0] - action[0][0]) >= 2 or abs(action[-1][1] - action[0][1]) >= 2:
                move = 'J'
            else:
                move = 'E'

            for act in range(1, len(action)):
                ff.write(move + ' ' + str(action[act - 1][1]) + ',' + str(action[act - 1][0]) + ' ' + str(
                    action[act][1]) + ',' + str(action[act][0]))
                if act != len(action) - 1:
                    ff.write('\n')
            ff.close()
        elif count2>10 or count1>10:
            action = MinMaxValue((piece1, matrix), 2)
            if abs(action[-1][0] - action[0][0]) >= 2 or abs(action[-1][1] - action[0][1]) >= 2:
                move = 'J'
            else:
                move = 'E'

            for act in range(1, len(action)):
                ff.write(move + ' ' + str(action[act - 1][1]) + ',' + str(action[act - 1][0]) + ' ' + str(
                    action[act][1]) + ',' + str(action[act][0]))
                if act != len(action) - 1:
                    ff.write('\n')
            ff.close()
        else:
            action = MinMaxValue((piece1, matrix), 1)
            if abs(action[-1][0] - action[0][0]) >= 2 or abs(action[-1][1] - action[0][1]) >= 2:
                move = 'J'
            else:
                move = 'E'

            for act in range(1, len(action)):
                ff.write(move + ' ' + str(action[act - 1][1]) + ',' + str(action[act - 1][0]) + ' ' + str(
                    action[act][1]) + ',' + str(action[act][0]))
                if act != len(action) - 1:
                    ff.write('\n')
            ff.close()