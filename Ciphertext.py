import random
import numpy as np
import pickle
import copy
import FSS
from time import time
DELAY=2

NETWORK=0
CommSize=0
numDCF=0
import warnings
warnings.filterwarnings('ignore')

MAX = 100000  # 空白值

def reFreshDB(DB) :
    newDB = []
    for i in range(len(DB)) :
        newDB.append([[i]])
        id = 0
        for j in range(1, len(DB[i]) + 1) :
            newDB[i].append([[id]])
            newDB[i][j].append([DB[i][j - 1][0]])
            for r in range(1, len(DB[i][j - 1])) :
                newDB[i][j].append(DB[i][j - 1][r])

            id = id + 1
    return newDB


def kIsomorp(DB, k) :
    DB.sort(key=lambda i : len(i), reverse=True)  #根据图的大小进行排序
    for i in range(len(DB)) :
        DB[i].sort(key=lambda j : len(j), reverse=False) #根据节点的degree进行排序

    for i in range(int(len(DB) / k)) :

        for j in range(i * k + 1, (i + 1) * k) :  # 首先吧节点数量设为一致的
            for r in range(len(DB[i * k]) - len(DB[j])) :
                DB[j].append([[len(DB[j])-2], [MAX]])

        for j in range(len(DB[i * k])) :  # 泛化每一个节点的degree
            maxDegree = 0
            for s in range(i * k, (i + 1) * k) :  # 求最大的degree
                if len(DB[s][j]) > maxDegree :  # 求最大的degree
                    maxDegree = len(DB[s][j])
            for s in range(i * k, (i + 1) * k) :  # 泛化每个节点的degree
                for r in range(maxDegree - len(DB[s][j])) :
                    DB[s][j].append([0, MAX])   #所有的假邻居都指向第一个节点，只是类型设置成无效值，这样也不影响匹配精度

    return DB

def encDB(oDB, k,flag) :

    DB = reFreshDB(oDB)  # 给图编号

    DB = kIsomorp(DB, k)  # 构建k-同构图

    if flag :  # AIDS数据集
        lenVTyp = 62
        lenETyp = 3
    else :  #MED数据集
        lenVTyp = 10
        lenETyp = 3

    eDB1 = []
    eDB2 = []

    for i in range(len(DB)):
        graph1=[i] #明文的graph ID
        graph2=[i]


        for j in range(1, len(DB[i])) :
            oneHot = getOneHot(DB[i][j][0][0], len(DB[i])-1)  # 获得节点ID的one-hot encoding 形式




            oneHot1 = getRandBits(len(DB[i]))   #多一位是为了存储假的ID
            oneHot2 = oneHot1 ^ oneHot

            graph1.append([oneHot1])    #节点的ID
            graph2.append([oneHot2])


            oneHot = getOneHot(DB[i][j][1][0]-1, lenVTyp)  # 获得节点类型的one-hot encoding 形式
            oneHot1 = getRandBits(lenVTyp+1)
            oneHot2 = oneHot1 ^ oneHot
            graph1[j].append(oneHot1)
            graph2[j].append(oneHot2)



            for r in range(2, len(DB[i][j])) :
                oneHotID = getOneHot(DB[i][j][r][0], len(DB[i])-1)  # 获得邻居节点ID的one-hot encoding 形式
                oneHotID1 = getRandBits(len(DB[i]))
                oneHotID2 = oneHotID1 ^ oneHotID



                oneHotEdg = getOneHot(DB[i][j][r][1]-1, lenETyp)  # 获得邻居边的one-hot encoding 形式
                oneHotEdg1 = getRandBits(lenETyp+1)
                oneHotEdg2 = oneHotEdg1 ^ oneHotEdg


                graph1[j].append([oneHotID1,oneHotEdg1])
                graph2[j].append([oneHotID2,oneHotEdg2])

        eDB1.append(graph1)
        eDB2.append(graph2)
    # file = open('encDB1.txt', 'wb')
    # pickle.dump(eDB1, file)
    # file.close()
    #
    # file = open('encDB2.txt', 'wb')
    # pickle.dump(eDB2, file)
    # file.close()


    return eDB1,eDB2

def CipherSearch(eDB1,eDB2,eQ1,eQ2,tau1,tau2):
    Res1 = []
    Res2 = []
    [candiGraph1,candiGraph2] = genCandi(eDB1,eDB2,eQ1,eQ2,tau1,tau2)  # 生成候选图

    for i in range(len(candiGraph1)):
        [GED1,GED2]=secGED(eQ1,eQ2, candiGraph1[i],candiGraph2[i], tau1,tau2)

        if sum(mpcComp(GED1, tau1,GED2,tau2)):
            Res1.append(candiGraph1[i])
            Res2.append(candiGraph2[i])


def secGED(eQ1,eQ2, candiGraph1,candiGraph2, tau1,tau2):
    GED1=0
    GED2=0

    diffSize=len(eQ1) - len(candiGraph1)

    if diffSize>0:
        for i in range(diffSize):
            candiGraph1.append([MAX])
            candiGraph2.append([0])

    elif diffSize<0:
        for i in range(-diffSize):
            eQ1.append([MAX])
            eQ2.append([0])

    QUEUE=queue.LifoQueue()
    m=[]
    [encLBM1,encLBM2]=secgetLBM(eQ1, eQ2, candiGraph1, candiGraph2, m, tau1, tau2)



    if sum(mpcComp(encLBM1, tau1,encLBM2,tau2)):
        QUEUE.put(m)


    while not QUEUE.empty():
        m=QUEUE.get()
        if len(m)==len(eQ1):
            return 0,0



        diffSet=list(set(range(len(candiGraph1))).difference(set(m)))


        for i in diffSet:
            mNew=m.copy()

            mNew.append(i)

            [encLBM1,encLBM2]=secgetLBM(eQ1, eQ2,candiGraph1, candiGraph2,mNew,tau1, tau2)

            if sum(mpcComp(encLBM1, tau1, encLBM2, tau2)) :
                QUEUE.put(mNew)

    return MAX


def secgetLBM(eQ1, eQ2,candiGraph1, candiGraph2,m,tau1, tau2):

    [EC1,EC2]=secgetEC(eQ1, eQ2,candiGraph1, candiGraph2,m)

    if sum(mpcComp(EC1, tau1, EC2, tau2)) :
        return MAX

    [BM1,BM2] = secgetBM(eQ1, eQ2, candiGraph1, candiGraph2, m)


    if sum(mpcComp(EC1+BM1, tau1, EC2+BM2, tau2)) :
        return MAX

    [LBL1,LBL2] = secgetLBL(eQ1, eQ2, candiGraph1, candiGraph2, m)


    if sum(mpcComp(EC1+BM1+LBL1, tau1, EC2+BM2+LBL2, tau2)) :
        return MAX

    return EC1+BM1+LBL1,EC2+BM2+LBL2


def secgetEC(eQ1, eQ2,candiGraph1, candiGraph2,m):
    EC1=0
    EC2=0

    for i in range(len(m)):

        [a,b]=pcMultiBool2Bool(eQ1[i][0],candiGraph1[m[i]][0],eQ2[i][0],candiGraph2[m[i]][0])

        EC1 = EC1+a
        EC2 = EC2+b




        for j in range (i+1,len(m)):

            labelQ1 = MAX
            labelQ2 = MAX

            labelG1 = MAX
            labelG2 = MAX

            for id in range(1,len(eQ1[i])):

                labelQ1=eQ1[i][id][1]
                labelQ2=eQ2[i][id][1]


            for id in range(1,len(candiGraph1[m[i]])):
                if candiGraph1[m[i]][id][0]+candiGraph2[m[i]][id][0]==m[j]:
                    labelG1=candiGraph1[m[i]][id][1]
                    labelG2=candiGraph2[m[i]][id][1]
                    break

    return EC1,EC2


def secgetBM(eQ1, eQ2,eG1,eG2,m):

    BM1=0
    BM2=0

    for i in range(len(m)):
        labelQ1 = []
        labelQ2 = []

        labelG1 = []
        labelG2 = []

        for j in range(1,len(eQ1[i])):
            if eQ1[i][j][0]+eQ2[i][j][0] not in range(len(m)) :
                labelQ1.append(eQ1[i][j][1])
                labelQ2.append(eQ2[i][j][1])

        for j in range(1,len(eG1[m[i]])):
            if eG1[m[i]][j][0]+eG2[m[i]][j][0] not in m:
                labelG1.append(eG1[m[i]][j][1])
                labelG2.append(eG2[m[i]][j][1])

        [a,b]=setInsec(labelQ1, labelG1, labelQ2, labelG2)


        BM1=BM1+a
        BM2=BM2+b

    return BM1,BM2



def secgetLBL(eQ1, eQ2,eG1,eG2,m):
    labelEdgeQ1=[]
    labelVertQ1=[]
    labelEdgeG1 = []
    labelVertG1 = []

    labelEdgeQ2 = []
    labelVertQ2 = []
    labelEdgeG2 = []
    labelVertG2 = []

    for i in range(len(m),len(eQ1)):

        labelVertQ1.append(eQ1[i][0])
        labelVertQ2.append(eQ2[i][0])



        for j in range(1,len(eQ1[i])):
            if eQ1[i][j][0]+eQ2[i][j][0] not in range(len(m)) :
                labelEdgeQ1.append(eQ1[i][j][1])
                labelEdgeQ2.append(eQ2[i][j][1])


    for i in range(len(eG1)):
        if i not in m:

            labelVertG1.append(eG1[i][0])
            labelVertG2.append(eG2[i][0])

            for j in range(1, len(eG1[i])) :
                if eG1[m[i]][j][0] + eG2[m[i]][j][0] not in m :
                    labelEdgeG1.append(eG1[i][j][1])
                    labelEdgeG2.append(eG2[i][j][1])


    l1,l2=setInsec(labelVertQ1, labelVertG1, labelVertQ2, labelVertG2)

    diff1= max(len(labelVertQ1), len(labelVertG1)- l1)
    diff2= max(len(labelVertQ2), len(labelVertG2)- l2)



    return diff1,diff2



def genCandi(eDB1,eDB2,eQ1,eQ2,tau1,tau2):
    candiGraph1 = []  # 候选图1
    candiGraph2 = []  # 候选图2

    QVertexTyp1 = []
    QVertexTyp2 = []

    QEdgeTyp1 = []
    QEdgeTyp2 = []

    for i in range(1,len(eQ1)): #因为第一个是ID所以需要跳过
        QVertexTyp1.append(eQ1[i][1])
        QVertexTyp2.append(eQ2[i][1])


    for i in range(1,len(eQ1)): #因为第一个是ID所以需要跳过
        for j in range(2,len(eQ1[i])):
            QEdgeTyp1.append(eQ1[i][j][1])
            QEdgeTyp2.append(eQ2[i][j][1])





    for index in range(len(eDB1)) :
        #print(int(index*100/len(eDB1)))


        GVertexTyp1 = []
        GVertexTyp2 = []

        GEdgeTyp1 = []
        GEdgeTyp2 = []

        for i in range(1,len(eDB1[index])) :
            GVertexTyp1.append(eDB1[index][i][1])
            GVertexTyp2.append(eDB2[index][i][1])


        for i in range(1,len(eDB1[index])) :
            for j in range(2, len(eDB1[index][i])) :
                GEdgeTyp1.append(eDB1[index][i][j][1])
                GEdgeTyp2.append(eDB2[index][i][j][1])


        [diff1,diff2]=diff2Set(QVertexTyp1, GVertexTyp1,QVertexTyp2, GVertexTyp2)


        [a,b]=diff2Set(QEdgeTyp1, GEdgeTyp1, QEdgeTyp2, GEdgeTyp2)


        [select1,select2]=mpcComp(diff1+a,tau1,diff2+b,tau2)

        if select1^select2:
            candiGraph1.append(eDB1[index])
            candiGraph2.append(eDB2[index])


    return candiGraph1,candiGraph2


def diff2Set(setA1, setB1,setA2, setB2):

    [lengthA1,lengthA2]=getRealLenSet(setA1,setA2)
    [lengthB1,lengthB2]=getRealLenSet(setB1,setB2)


    [diff1,diff2]=mpcMax(lengthA1,lengthB1,lengthA2,lengthB2)


    [a,b]=setInsec(setA1, setB1,setA2, setB2)



    return diff1-a,diff2-b



def getRealLenSet(set1, set2):    #获得真实的集合大小，即过滤假的类型
    res1=0
    res2=0
    global NETWORK
    NETWORK = NETWORK + 1
    for i in range(len(set1)):
        [a1, a2] = mpcMultiBool2Aith(not set1[i][-1], 1, set2[i][-1], 0)

        res1=res1+a1
        res2=res2+a2

    return res1,res2


def mpcMax(A1,B1,A2,B2):



    [b1,b2]=mpcComp(A1,B1,A2,B2)
    global NETWORK
    NETWORK = NETWORK + 1
    [res11,res21]=mpcMultiBool2Aith(not b1,A1,b2,A2)
    [res12,res22]=mpcMultiBool2Aith(b1, B1, b2, B2)


    return res11+res12,res21+res22


def mpcComp(a1, b1, a2, b2) :

    random_integer = random.randint(-2147483648, 2147483647)
    key0,key1=FSS.DCFGen(random_integer, 1)

    r1=FSS.DCFEval(0, key0, a1+b1+a2+b2+random_integer)
    r2=FSS.DCFEval(1, key1, a1+b1+a2+b2+random_integer)

    return r1,r2


    #return a1 + a2 <= b1 + b2, False


def setInsec(setA1, setB1, setA2, setB2) :  #普通的协议

    res1 = 0
    res2 = 0
    flagA1 = np.ones(len(setA1), dtype=bool)
    flagA2 = np.zeros(len(setA1), dtype=bool)

    flagB1 = np.ones(len(setB1), dtype=bool)
    flagB2 = np.zeros(len(setB1), dtype=bool)

    for i in range(len(setA1)) :
        for j in range(len(setB1)) :
            global NETWORK
            NETWORK = NETWORK + 4
            [t1, t2] = mpcMultiBoolist2Boolist(setA1[i][:-1], setB1[j][:-1], setA2[i][:-1], setB2[j][:-1])

            b1 = bool(sum(t1) % 2)
            b2 = bool(sum(t2) % 2)

            [b1, b2] = mpcMultiBool2Bool(b1, flagA1[i], b2, flagA2[i])
            [b1, b2] = mpcMultiBool2Bool(b1, flagB1[j], b2, flagB2[j])

            [flagA1[i], flagA2[i]] = mpcMultiBool2Bool(flagA1[i], not b1, flagA2[i], b2)
            [flagB1[j], flagB2[j]] = mpcMultiBool2Bool(flagB1[j], not b1, flagB2[j], b2)

            [a1, a2] = mpcMultiBool2Aith(b1, 1, b2, 0)

            res1 = res1 + a1
            res2 = res2 + a2

    return res1, res2





# def setInsec(A1, B1,A2, B2):
#     setA1 = A1.copy()
#     setA2 = A2.copy()
#     setB1 = B1.copy()
#     setB2 = B2.copy()
#
#     res=0
#
#     for i in range(len(setA1)):
#         a = setA1[i] ^ setA1[i]
#     pi=np.arange(len(setA1))
#     for i in range(len(setA1)):
#         a = setA1[i] ^ setA1[i]
#     for i in range(len(setA1)) :
#         a = setA1[i] ^ setA1[i]
#
#     for i in range(len(setA1)) :
#         a = setA1[i] ^ setA1[i]
#     pi = np.arange(len(setA1))
#     for i in range(len(setA1)) :
#         a = setA1[i] ^ setA1[i]
#     for i in range(len(setA1)) :
#         a = setA1[i] ^ setA1[i]
#
#
#     for i in range(len(setB1)):
#         a = setB1[i] ^ setB1[i]
#     pi=np.arange(len(setB1))
#     for i in range(len(setB1)):
#         a = setB1[i] ^ setB1[i]
#     for i in range(len(setB1)) :
#         a = setB1[i] ^ setB1[i]
#
#     for i in range(len(setB1)) :
#         a = setB1[i] ^ setB1[i]
#     pi = np.arange(len(setB1))
#     for i in range(len(setB1)) :
#         a = setB1[i] ^ setB1[i]
#     for i in range(len(setB1)) :
#         a = setB1[i] ^ setB1[i]
#
#
#
#     i=0
#     while i<len(setA1):
#         for j in range(len(setB1)):
#             global NETWORK
#             NETWORK = NETWORK + 4
#             #print(i,j,len(setA1),len(setB1))
#             #if i>=len(setA1):
#                 #break
#             [t1,t2]=mpcMultiBoolist2Boolist(setA1[i][:-1],setB1[j][:-1],setA2[i][:-1],setB2[j][:-1])
#
#
#             b1=bool(sum(t1) % 2)
#             b2=bool(sum(t2) % 2)
#
#             if b1^b2:
#                 res = res + 1
#                 del setA1[i]
#                 del setA2[i]
#                 del setB1[j]
#                 del setB2[j]
#                 i=i-1
#                 break
#         i = i + 1
#
#         #if len(setB1)==0:
#             #break
#
#     return 0,res
#

def getRandBits(length) :
    res = ''
    for i in range(int(length / 32)) :
        res = res + bin(random.randint(44444444410, 54444444410))[2 :2 + 32]
    if not len(res) == length :
        res = res + bin(random.randint(44444444410, 54444444410))[2 :2 + length - len(res)]
    return str2Bool(res)



def str2Bool(str):
    res=np.zeros(len(str), dtype=bool)
    for i in range(len(str)) :
        if str[i]=='1':
            res[i]=True
    return res


def getOneHot(val, length) :
    oneHot = np.zeros(length+1, dtype=bool)
    if val<length:
        oneHot[val] = True
    else:
        oneHot[-1] = True


    return oneHot



def mpcMultiBool2Aith(b1,A1,b2,A2):
    global CommSize

    CommSize = CommSize+2*16

    r=random.randint(0,64)

    if b1:
        m1 =  A1 - r
        m2 =  - r
    else:
        m1 = - r
        m2 = A1 - r


    res1=r

    if b2:
        res2=m2
    else:
        res2=m1

    r = random.randint(0,64)

    if b2 :
        m1 = A2 - r
        m2 = - r
    else :
        m1 = - r
        m2 = A2 - r

    if b1 :
        res1 = res1+m2
    else :
        res1 = res1+m1

    res2 = res2 + r



    return res1,res2

def mpcMultiBool2Bool(x1, y1, x2, y2) :

    u = False
    v = False
    w = u & v
    a1 = True
    a2 = u ^ a1
    b1 = True
    b2 = v ^ b1
    c1 = True
    c2 = w ^ c1

    e = x1 ^ a1 ^ x2 ^ a2
    f = y1 ^ b1 ^ y2 ^ b2
    res1 = e & f ^ f & a1 ^ e & b1 ^ c1
    res2 = f & a2 ^ e & b2 ^ c2
    return res1, res2






def mpcMultiBool2Boolist(x1, y1, x2, y2) :

    global CommSize

    CommSize = CommSize + len(x1) * 4


    # 生乘triple
    u = np.zeros(1, dtype=bool)
    v = np.zeros(len(y1), dtype=bool)
    w = u & v
    a1 = np.ones(1, dtype=bool)
    a2 = u ^ a1
    b1 = np.ones(len(y1), dtype=bool)
    b2 = v ^ b1
    c1 = np.ones(len(y1), dtype=bool)
    c2 = w ^ c1

    e = x1 ^ a1 ^ x2 ^ a2
    f = y1 ^ b1 ^ y2 ^ b2
    res1 = e & f ^ f & a1 ^ e & b1 ^ c1
    res2 = f & a2 ^ e & b2 ^ c2
    return res1, res2



def mpcMultiBoolist2Boolist(x1, y1, x2, y2) :


    # 生乘triple
    u = np.zeros(len(x1), dtype=bool)
    v = np.zeros(len(y1), dtype=bool)
    w = u & v
    a1 = np.ones(len(x1), dtype=bool)
    a2 = u ^ a1
    b1 = np.ones(len(y1), dtype=bool)
    b2 = v ^ b1
    c1 = np.ones(len(y1), dtype=bool)
    c2 = w ^ c1

    e = x1 ^ a1 ^ x2 ^ a2
    f = y1 ^ b1 ^ y2 ^ b2
    res1 = e & f ^ f & a1 ^ e & b1 ^ c1
    res2 = f & a2 ^ e & b2 ^ c2
    return res1, res2