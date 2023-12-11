import numpy as np
import util
import Server
import time

P=0.5
num_threads=1



for M in range(500,10001,1000):
    for N in range(int(util.DOMAIN/10), int(util.DOMAIN+1), int(util.DOMAIN/10)) :
        #start_time = time.time()
        #util.genSets(M,N)
        #end_time = time.time()
        #elapsed_time = end_time - start_time
        #print(f"Generation: {M,N,elapsed_time}s")



        #Sets = util.genSets(M,N) #np.load('Sets_'+str(M)+'_'+str(N)+'.npy')


        #start_time = time.time()

        #end_time = time.time()
        #elapsed_time = end_time - start_time
        #print(f"Encryption: {M,N,elapsed_time}s")



        #encSets = np.load('enc_Sets_'+str(M)+'_'+str(N)+'.npy')

        encSets=util.encSet(util.genSets(M, N), M, N, P)

        start_time = time.time()
        Server.PSI(encSets,M,N)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"PSI: {M,N,elapsed_time/num_threads}s")
