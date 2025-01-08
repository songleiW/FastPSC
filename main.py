import math
import random

import numpy as np
import util
import Server
import time
from math import comb
r=0.00001




for M in [60]:
    for N in [2**16,2**18,2**20,2**22,2**24]:
        Set=util.genSetsNew(M, N, r)
        start_time = time.time()
        util.getTimePSI(M,Set)
        end_time = time.time()
        elapsed_time= end_time - start_time
        set_size=len(Set)
        LANtime=elapsed_time+set_size*32*7/8/1024/1024/1024/1.25/4000
        WANTime=elapsed_time+set_size*32*7/8/1024/1024/12.5/25
        print(r,M,N, round(LANtime,1),round(WANTime,1),round(set_size*32*20/8/1024/1024/1024,1))


for M in [20,40,60,80,100]:
    for N in [2**20]:
        Set=util.genSetsNew(M, N, r)
        start_time = time.time()
        util.getTimePSI(M,Set)
        end_time = time.time()
        elapsed_time= end_time - start_time
        set_size=len(Set)
        LANtime=elapsed_time+set_size*32*7/8/1024/1024/1024/1.25/4000
        WANTime=elapsed_time+set_size*32*7/8/1024/1024/12.5/25
        print(r,M,N, round(LANtime,1),round(WANTime,1),round(set_size*32*20/8/1024/1024/1024,1))



exit(11)


for r in [0.0001,0.00005,0.00001]: #0.0001,0.00005,0.00001
    for M in [20,40,60,80,100]: #20,40,60,80,100
        for N in [2**20]: #2**16,2**18,2**20,2**22,2**24
            Set=util.genSetsNew2(M, N, r)
            start_time = time.time()
            util.ParsePSU(Set)
            end_time = time.time()
            elapsed_time= end_time - start_time
            print(r,M,N, elapsed_time, len(Set))


exit(11)




for M in [20,40,60,80,100]:
    for N in [2**16,2**18,2**20,2**22,2**24]:
        Set=util.genSetsNew1(M, N, r)
        start_time = time.time()
        util.ParsePSI(Set)
        end_time = time.time()
        elapsed_time= end_time - start_time
        print(r,M,N, elapsed_time, len(Set))


exit(11)


for M in [60]:
    for N in [2**16,2**18,2**20,2**22,2**24]:
        Set=util.genSetsNew(M, N, r)
        start_time = time.time()
        util.getTimePSU(Set)
        end_time = time.time()
        elapsed_time= end_time - start_time
        set_size=len(Set)
        print(r,M,N, elapsed_time,set_size)


exit(11)


for M in [2**16,2**18,2**20,2**22,2**24]:
    start_time = time.time()
    for i in range(10):
        util.testEncPRISM()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(M, elapsed_time/10)


exit(11)


for M in [2**16,2**18,2**20,2**22,2**24]:
    start_time = time.time()
    for i in range(10):
        util.testEncMRR(M)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(M, elapsed_time/10)



for M in [2**16,2**18,2**20,2**22,2**24]:
    start_time = time.time()
    size=0
    for i in range(10):
        l=util.testEnc(M, r)/10
    size=size+l
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(M, elapsed_time/10,size*12*32/8/1024/1024)


