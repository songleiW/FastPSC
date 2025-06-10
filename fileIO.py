import numpy as np
import random
ratio=80
maxGraph=227*ratio
def readFile(flag):
    print(ratio)
    QDB=[]
    DB=[]     #每个节点的第一的数字表示节点类型，后面的每个元组表示一个邻居节点的ID和边的类型
    if flag==1:
        fileName="./AIDS"
    if flag==2:
        fileName="./CHEM"
    file = open(fileName)
    line = file.readline()
    line = file.readline()
    while line :
        graph=[]
        while True :
            text = line.strip().split(' ')
            if text[0]=='e':
                break
            graph.append([int(text[2])])
            line = file.readline()
        while True :
            text = line.strip().split(' ')
            if text[0]!='e':
                line = file.readline()
                break
            graph[int(text[1])].append([int(text[2]),int(text[3])])
            graph[int(text[2])].append([int(text[1]),int(text[3])])
            line = file.readline()
        DB.append(graph)
       # if len(DB)>=maxGraph:
           # break
    for i in range(30):
        index=i#random.randint(0,len(DB)-1)
        QDB.append(DB[index])
        #del DB[index]
    return QDB,DB