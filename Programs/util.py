import numpy as np
import random
DOMAIN=100000000



p = 4294967311  # mod of the finite field



def ParsePSI(Set):
    zero_indices = np.where(Set == 0)[0]
    Set=Set*DOMAIN-Set

def ParsePSU(Set):
    zero_indices = np.where(Set != 0)[0]
    Set=Set*DOMAIN-Set

def genSetsNew2(M, N, r):
    # 通过几何分布生成每个集合的随机增量大小
    random_increments = np.random.geometric(p=r, size=M)

    # 生成每个集合
    random_sets = [
        set(random.sample(range(1, DOMAIN), N) + random.choices(range(1, DOMAIN), k=increment)) for increment in
        random_increments
    ]
    # 计算集合的交集并转换为 NumPy 数组
    intersection_result = np.array(list(set.union(*random_sets)))
    return intersection_result





def genSetsNew1(M, N, r):
    # 通过几何分布生成每个集合的随机增量大小
    random_increments = np.random.geometric(p=r, size=M)

    # 生成每个集合
    random_sets = [
        set(random.sample(range(1, DOMAIN), N) + random.choices(range(1, DOMAIN), k=increment)) for increment in
        random_increments
    ]
    # 计算集合的交集并转换为 NumPy 数组
    intersection_result = np.array(list(set.intersection(*random_sets)))
    return intersection_result


def testEnc(N,r):
    sampled_values_N = np.random.choice(DOMAIN, N, replace=False)
    flag_N = np.ones(N, dtype=int)


    X = np.random.geometric(p=r)
    sampled_values_X = np.random.choice(DOMAIN, X, replace=True)
    flag_X = np.zeros(X, dtype=int)

    result_array = np.concatenate([sampled_values_N, sampled_values_X])
    result_flags = np.concatenate([flag_N, flag_X])

    result_array1 = np.random.randint(1, p, size=result_array.shape)
    result_array2 = np.random.randint(1, p, size=result_array.shape)
    result_array=result_array-result_array1-result_array2

    result_flags1 = np.random.randint(1, p, size=result_array.shape)
    result_flags2 = np.random.randint(1, p, size=result_array.shape)
    result_flags=result_flags-result_flags1-result_flags2

    return len(result_flags)


def testEncMRR(N):
    sampled_values_N = np.random.choice(DOMAIN, N, replace=False)


    result_array1 = np.random.randint(1, p, size=sampled_values_N.shape)
    result_array2 = np.random.randint(1, p, size=sampled_values_N.shape)
    result_array=sampled_values_N-result_array1-result_array2



def testEncPRISM():
    sampled_values_N = np.random.choice(DOMAIN, DOMAIN-1, replace=False)
    result_array1 = np.random.randint(1, p, size=sampled_values_N.shape)

    result_array=sampled_values_N-result_array1


def genSetsNew(M, N, r) :  # N is the size of the set held by each data owner; M is the number of users, r is the probability

    # 从几何分布中采样 M 次
    X_values = np.random.geometric(p=r, size=M)

    # 从1到N中随机采样 X1+X2+...+XM 次，并追加到一维随机列表 A

    s=np.sum(X_values)

    A = np.random.randint(1, DOMAIN,size=int((M * N+s)*3/4))

    return A



def genSets(M, N) :  # N is the size of the set held by each data owner; M is the number of users

    random_matrix = np.empty((M, N), dtype=int)

    for i in range(M) :
        row_values = np.random.choice(DOMAIN + 1, N, replace=False)
        random_matrix[i, :] = row_values

    return random_matrix


def encSet(Sets):

    ciperSet1= np.empty(Sets.shape,dtype=int)
    for i in range(Sets.shape[0]) :
        row_values = np.random.choice(p + 1, Sets.shape[1])
        ciperSet1[i, :] = row_values

    ciperSet2 = np.empty(Sets.shape, dtype=int)
    for i in range(Sets.shape[0]) :
        row_values = np.random.choice(p + 1, Sets.shape[1])
        ciperSet2[i, :] = row_values


    ciperSet3=Sets-ciperSet1-ciperSet2


    ciperFlagSet1 = np.empty(Sets.shape, dtype=int)
    for i in range(Sets.shape[0]) :
        row_values = np.random.choice(p + 1, Sets.shape[1])
        ciperFlagSet1[i, :] = row_values

    ciperFlagSet2 = np.empty(Sets.shape, dtype=int)
    for i in range(Sets.shape[0]) :
        row_values = np.random.choice(p + 1, Sets.shape[1])
        ciperFlagSet2[i, :] = row_values

    ciperFlagSet2 = 1 - ciperFlagSet1 - ciperFlagSet2


    return ciperSet1,ciperSet2,ciperSet3,ciperFlagSet1,ciperFlagSet2,ciperFlagSet3


def getTimePSU(Sets):

    dic1 = np.zeros(DOMAIN, dtype=int)
    dic2 = np.zeros(DOMAIN, dtype=int)

    for key in Sets :
        dic1[key] += key
        dic2[key] += key
    random_factors = np.random.uniform(1, p, size=dic1.shape)
    dic1=dic1*random_factors*random_factors
    dic2=dic2*random_factors



    Sets=Sets+Sets
    Sets=np.random.permutation(Sets)
    Sets=Sets+Sets
    Sets=np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets=Sets+Sets
    Sets=np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets

    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets

    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets

    random_factors = np.random.uniform(1, p, size=len(Sets))

    Sets =np.sum(Sets*random_factors)




def getTimePSI(N,Sets):

    dic1 = np.zeros(DOMAIN, dtype=int)
    dic2 = np.zeros(DOMAIN, dtype=int)

    for key in Sets :
        dic1[key] += key
        dic2[key] += key
    random_factors = np.random.uniform(1, p, size=dic1.shape)
    dic1=(N-dic1)*random_factors*random_factors
    dic2=(N-dic2)*random_factors


    Sets=Sets+Sets
    Sets=np.random.permutation(Sets)
    Sets=Sets+Sets
    Sets=np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets=Sets+Sets
    Sets=np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets

    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets

    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets
    Sets = Sets + Sets
    Sets = np.random.permutation(Sets)
    Sets = Sets + Sets

    random_factors = np.random.uniform(1, p, size=len(Sets))

    Sets =np.sum(Sets*random_factors)










# size=80000000
#
# # 生成四个随机数组
# array1 = np.random.rand(size)
# array2 = np.random.rand(size)
# array3 = np.random.rand(size)
# array4 = np.random.rand(size)
#
#
# start_time = time.time()
#
# array=array1+array2+array3 + array4
# array=array1+array2+array3 + array4
# nonzero_indices = np.nonzero(array-array*1231233)
#
# nonzero_indices = np.where(array == 0)
#
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(elapsed_time)
#
#
#
# start_time = time.time()
#
# array=array1+array2+array3 + array4
# array=array1+array2+array3 + array4
# nonzero_indices = np.nonzero(array-array*1231233)
#
# nonzero_indices = np.nonzero(array)
#
#
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(elapsed_time)
