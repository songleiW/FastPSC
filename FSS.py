import numpy as np
import random
import string
LAMBDA = 128
import math
N=32
UN=math.pow(2,32)

def DPFGen(alpha,beta):
    key0=[]
    key1=[]
    alpha=num2Bool(alpha)

    s0=random01(LAMBDA,'00')
    s1=random01(LAMBDA,'01')

    key0.append(s0)
    key1.append(s1)

    t0=False
    t1=True

    for i in range(N):
        G=random01(2*LAMBDA+2,s0)
        sL0=G[:LAMBDA]
        tL0=G[LAMBDA:LAMBDA+1]
        sR0 = G[LAMBDA+1:2*LAMBDA+1]
        tR0 = G[2*LAMBDA+1]

        G=random01(2*LAMBDA+2,s1)
        sL1 = G[:LAMBDA]
        tL1 = G[LAMBDA :LAMBDA + 1]
        sR1 = G[LAMBDA + 1 :2 * LAMBDA + 1]
        tR1 = G[2 * LAMBDA + 1]

        if alpha[i]:
            sLose0=sL0
            sLose1=sL1
            sKeep0=sR0
            sKeep1=sR1
        else:
            sLose0 = sR0
            sLose1 = sR1
            sKeep0 = sL0
            sKeep1 = sL1
        sCW=Bool2Str(str2Bool(sLose0) ^ str2Bool(sLose1))
        tLCW=str2Bool(tL0)^str2Bool(tL1)^alpha[i]^True
        tRCW=str2Bool(tR0)^str2Bool(tR1)^alpha[i]

        if alpha[i] :
            tKeep0=tR0
            tKeep1=tR1
            tKeepCW=tRCW
        else:
            tKeep0 = tL0
            tKeep1 = tL1
            tKeepCW = tLCW

        key0.append(sCW+Bool2Str(tLCW)+Bool2Str(tRCW))
        key1.append(sCW+Bool2Str(tLCW)+Bool2Str(tRCW))

        s0=Bool2Str(str2Bool(sKeep0)^t0 & str2Bool(sCW))
        s1=Bool2Str(str2Bool(sKeep1)^t1 & str2Bool(sCW))

        t0=str2Bool(tKeep0)^t0 & tKeepCW
        t1=str2Bool(tKeep1)^t1 & tKeepCW


    random.seed(s0)
    c1=random.randint(0,134545)

    random.seed(s1)
    c2 = random.randint(0, 134545)

    key0.append((-2*t1+1)*(beta-c1+c2))
    key1.append((-2*t1+1)*(beta-c1+c2))

    return key0,key1

def DPFEval(b,key,x):
    s=key[0]
    t=True if b==1 else False
    x=num2Bool(x)
    for i in range(N):
        CW=key[i+1]
        sCW=CW[:LAMBDA]
        tLCW=CW[LAMBDA]
        tRCW=CW[LAMBDA+1]
        T=Bool2Str(str2Bool(random01(2*LAMBDA+2,s))^(t&str2Bool(sCW+tLCW+sCW+tRCW)))
        sL=T[:LAMBDA]
        tL=str2Bool(T[LAMBDA])
        sR=T[LAMBDA+1:2*LAMBDA+1]
        tR=str2Bool(T[-1])
        if ~x[i]:
            s=sL
            t=tL
        else:
            s = sR
            t = tR
    random.seed(s)
    return (-2*b+1)*(random.randint(0, 134545)+int(Bool2Str(t))*key[-1])

def DCFGen(alpha,beta):

    alpha = num2Bool(alpha)[::-1]

    key0 = []
    key1 = []

    s0 = random01(LAMBDA, '00')
    s1 = random01(LAMBDA, '01')

    key0.append(s0)
    key1.append(s1)

    Valpha = 0


    t0 = False
    t1 = True

    for i in range(N) :
        skey=[]

        G = random01(4 * LAMBDA + 2, s0)

        sL0 = G[:LAMBDA]
        vL0 = G[LAMBDA :2 * LAMBDA]
        tL0 = str2Bool(G[2 * LAMBDA])
        sR0 = G[2 * LAMBDA + 1:3 * LAMBDA + 1]
        vR0 = G[3 * LAMBDA + 1 :4 * LAMBDA + 1]
        tR0 = str2Bool(G[4 * LAMBDA + 1])

        G = random01(4 * LAMBDA + 2, s1)

        sL1 = G[:LAMBDA]
        vL1 = G[LAMBDA :2 * LAMBDA]
        tL1 = str2Bool(G[2 * LAMBDA])
        sR1 = G[2 * LAMBDA + 1:3 * LAMBDA + 1]
        vR1 = G[3 * LAMBDA + 1 :4 * LAMBDA + 1]
        tR1 = str2Bool(G[4 * LAMBDA + 1])


        if alpha[i] :
            sLose0 = sL0
            sLose1 = sL1
            sKeep0 = sR0
            sKeep1 = sR1
            vLose0=vL0
            vLose1=vL1
            vKeep0=vR0
            vKeep1=vR1
            tKeep0=tR0
            tKeep1=tR1

        else :
            sLose0 = sR0
            sLose1 = sR1
            sKeep0 = sL0
            sKeep1 = sL1
            vLose0=vR0
            vLose1=vR1
            vKeep0=vL0
            vKeep1=vL1
            tKeep0 = tL0
            tKeep1 = tL1

        sCW=Bool2Str(str2Bool(sLose0) ^ str2Bool(sLose1))

        random.seed(vLose0)
        c1 = random.randint(0, 134545)

        random.seed(vLose1)
        c2 = random.randint(0, 134545)

        vCW=(-2*t1+1)*(c2-c1-Valpha)

        if alpha[i] :
            vCW=vCW+(-2*t1+1)*beta

        random.seed(vKeep1)

        Valpha=Valpha-random.randint(0, 134545)

        random.seed(vKeep0)
        Valpha=Valpha+random.randint(0, 134545)+(-2*t1+1)*vCW

        tLCW=tL0^tL1^alpha[i]^True
        tRCW=tR0^tR1^alpha[i]

        skey.append(sCW)
        skey.append(vCW)
        skey.append(tLCW)
        skey.append(tRCW)

        key0.append(skey)
        key1.append(skey)


        s0=Bool2Str(str2Bool(sKeep0)^t0&str2Bool(sCW))
        s1=Bool2Str(str2Bool(sKeep1)^t1&str2Bool(sCW))

        if alpha[i] :
            t0=tKeep0^t0&tRCW
            t1=tKeep1^t1&tRCW

        else:
            t0=tKeep0^t0&tLCW
            t1=tKeep1^t1&tLCW

    random.seed(s0)
    c1 = random.randint(0, 134545)

    random.seed(s1)
    c2 = random.randint(0, 134545)


    CW=(-2*t1+1)*(c2-c1-Valpha)

    key0.append(CW)
    key1.append(CW)

    return key0,key1

def DCFEval(b,key,x):
    s=key[0]
    V=0
    t=True if b==1 else False
    x=num2Bool(x)[::-1]
    for i in range(N):
        CW=key[i+1]
        sCW=CW[0]
        vCW=CW[1]
        tLCW=CW[2]
        tRCW=CW[3]

        G = random01(4 * LAMBDA + 2, s)

        s_L = G[:LAMBDA]
        v_L = G[LAMBDA :2 * LAMBDA]
        t_L = str2Bool(G[2 * LAMBDA])
        s_R = G[2 * LAMBDA + 1:3 * LAMBDA + 1]
        v_R = G[3 * LAMBDA + 1 :4 * LAMBDA + 1]
        t_R = str2Bool(G[4 * LAMBDA + 1])

        str1=s_L+Bool2Str(t_L)+s_R+Bool2Str(t_R)
        str2=sCW+Bool2Str(tLCW)+sCW+Bool2Str(tRCW)

        T=Bool2Str(str2Bool(str1)^(t&str2Bool(str2)))

        sL=T[:LAMBDA]
        tL=str2Bool(T[LAMBDA])
        sR=T[LAMBDA+1:2*LAMBDA+1]
        tR=str2Bool(T[2*LAMBDA+1])

        if not x[i]:
            random.seed(v_L)
            V=V+(-2*b+1)*(random.randint(0, 134545)+t*vCW)
            s=sL
            t=tL
        else:
            random.seed(v_R)
            V = V + (-2 * b + 1) * (random.randint(0, 134545) + t * vCW)
            s = sR
            t = tR
    random.seed(s)
    return V+(-2 * b + 1)*(random.randint(0, 134545)+t*key[-1])



def DICGen(r_in,r_out,p,q):
    gamma=int((UN-1+r_in)%UN)
    k0,k1=DCFGen(gamma,1)
    Q=int((q+1)%UN)
    alphaP=int((p+r_in)%UN)
    alphaQ=int((q+r_in)%UN)
    alphaQq=int((q+1+r_in)%UN)
    z0=random.randint(1,UN)
    z1=int(int(r_out+int(alphaP>alphaQ)-int(alphaP>p)+int(alphaQq>Q)+int(alphaQ==(UN-1))-z0)%UN)

    k0.append(z0)
    k1.append(z1)


    return k0,k1

def DICEval(b,key,x,p,q):
    Q=int((q+1)%UN)
    xP=int((x+(UN-1-p))%UN)
    xQ=int((x+(N-1-Q))%UN)
    sP=DCFEval(b,key[:-1],xP)
    sQ=DCFEval(b,key[:-1],xQ)

    return b*(int(x>p)-int(x>Q))-sP+sQ+key[-1]


def num2Bool(alpha):
    a = bin(2**8+alpha).replace('0b', '')[::-1] #取补码
    alpha = np.zeros(N, dtype=bool)
    for i in range(len(a)):
        if a[i]=='1':
            alpha[i]=True
    return alpha



def random01(length,seed):
    res=''
    for i in range(int(length/32)):
        random.seed(seed)
        res=res+bin(random.randint(44444444410, 54444444410))[2:2+32]
    if not len(res)==length:
        res = res + bin(random.randint(0, 44444444410))[2:2+length-len(res)]
    return res

def str2Bool(str):
    res=np.zeros(len(str), dtype=bool)
    for i in range(len(str)) :
        if str[i]=='1':
            res[i]=True
    return res

def Bool2Str(Boolean):
    res=''
    for i in range(len(Boolean)):
        if Boolean[i]:
            res=res+'1'
        else:
            res=res+'0'
    return res

def mpcMSB(x,y): #测试性能
    x=num2BoolCom(x)

    G1=np.zeros(32, dtype=bool)
    P1=np.zeros(32, dtype=bool)
    G1[0]=False
    for i in range(0,len(x)-1):
        G1[i+1],G1[i+1]=mpcMultiBool(x[i],False,False,x[i])
        P1[i+1]=x[i]
    l=len(x)
    for i in range(0,int(math.log(len(x),2))):
        r1,r2=mpcMultiBool(P1[1],G1[0],P1[1],G1[0])
        G1[0]=r1^G1[1]
        n=1
        for j in np.arange(2,l,2):
            r1,r2=mpcMultiBool(P1[j+1],G1[j],P1[j+1],G1[j])
            G1[n]=r1^G1[j+1]
            #P1[n],P1[n]=mpcMultiBool(P1[j+1],P1[j],P1[j+1],P1[j])
            n=n+1
        l=int(l/2)

    return x[-1]^G1[0],x[-1]^G1[0]

# def mpcMSB(x,y): #这个才是对的
#     x=num2BoolCom(x)
#     y=num2BoolCom(y)
#
#     G1=np.zeros(32, dtype=bool)
#     G2=np.zeros(32, dtype=bool)
#     P1=np.zeros(32, dtype=bool)
#     P2=np.zeros(32, dtype=bool)
#     G1[0]=False
#     G2[0]=False
#     for i in range(0,len(x)-1):
#         G1[i+1],G2[i+1]=mpcMultiBool(x[i],False,False,y[i])
#         P1[i+1]=x[i]
#         P2[i+1]=y[i]
#     l=len(x)
#     for i in range(0,int(math.log(len(x),2))):
#         r1,r2=mpcMultiBool(P1[1],G1[0],P2[1],G2[0])
#         G1[0]=r1^G1[1]
#         G2[0]=r2^G2[1]
#         n=1
#         for j in np.arange(2,l,2):
#             r1,r2=mpcMultiBool(P1[j+1],G1[j],P2[j+1],G2[j])
#             G1[n]=r1^G1[j+1]
#             G2[n]=r2^G2[j+1]
#             P1[n],P2[n]=mpcMultiBool(P1[j+1],P1[j],P2[j+1],P2[j])
#             n=n+1
#         l=int(l/2)
#
#     return x[-1]^G1[0],y[-1]^G2[0]


def mpcMultiBool(x1, y1, x2, y2) :

    # 生乘triple
    u = False  # np.random.randint(0, math.sqrt(MAX))
    v = True  ##np.random.randint(0, math.sqrt(MAX))
    w = u & v
    a1 = True  # np.random.randint(0, math.sqrt(MAX))
    a2 = u ^ a1
    b1 = True  # np.random.randint(0, math.sqrt(MAX))
    b2 = v ^ b1
    c1 = True  # np.random.randint(0, math.sqrt(MAX))
    c2 = w ^ c1

    e = x1 ^ a1 ^ x2 ^ a2
    f = y1 ^ b1 ^ y2 ^ b2
    res1 = e & f ^ f & a1 ^ e & b1 ^ c1
    res2 = f & a2 ^ e & b2 ^ c2
    return res1, res2


def num2BoolCom(alpha):
    a = bin(alpha& 0xffffffff).replace('0b', '')[::-1]
    alpha = np.zeros(N, dtype=bool)
    for i in range(len(a)):
        if a[i]=='1':
            alpha[i]=True
    #print(alpha)
    return alpha