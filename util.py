import numpy as np
DOMAIN=10000000



p = 4294967311  # mod of the finite field

def genSets(M, N) :  # N is the size of the set held by each data owner; M is the number of users
    #np.save('Sets_'+str(M)+'_'+str(N)+'.npy', np.random.randint(0, DOMAIN, size=(M, N)))

    # 创建包含0到DOMAIN-1的数组
    unique_numbers = np.arange(DOMAIN)
    # 对每一行进行处理
    random_matrix = np.empty((M, N), dtype=np.int32)
    for i in range(M) :
        np.random.shuffle(unique_numbers)  # 打乱数组顺序
        random_matrix[i] = unique_numbers[:N]  # 取前N个随机数作为该行的元素

    return random_matrix

    #return np.random.randint(0, DOMAIN, size=(M, N))

def encSet(Sets,M,N,P):

    ciperSet=np.zeros((M, DOMAIN),dtype=np.int32)

    for i in range(M):
        ciperSet[i,Sets[i,:]]=np.random.randint(0, p, N)


    random_numbers = np.random.rand(*ciperSet.shape)  # 生成与 arr 相同大小的随机数数组
    mask = (ciperSet == 0) & (random_numbers < P*3/4)  # 找到为0的元素并根据概率 p 进行判断
    ciperSet[mask] = np.random.randint(1, p, size=mask.sum())  # 将符合条件的元素设置成随机数

    #np.save('enc_Sets_'+str(M)+'_'+str(N)+'.npy', ciperSet)
    return ciperSet