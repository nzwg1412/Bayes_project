import GPyOpt
import numpy as np
import pandas as pd
import os

def exeact():
    # 改变工作目录
    os.chdir("D:/work2019/优化压裂/Multistage-optimization-final-AI3-BOPT/Multistage-optimization-final/multistage-optimization")

    path_01 = "multistage_optimization.exe"

    # r_v = os.system(path_01)

    # print(r_v)

def func(X):
    #完成数据覆盖，物理仿真模型调用，以及得到结果输出
    f = open("input/temp/initial.dat", "wt")
    f.seek(0)
    #####把x_next保存到文件中，每行一个数据

    # print(X)
    print(X[0][1])
    for i in range(5):
        f.write(str(X[0][i])+'\n')
    f.close
    ####
    exeact()
    f = open("output/xxx.dat", "rt")
    AllVector = f.readlines()
    f.close()
    Y = AllVector[5]
    return Y


domain =[{'P1': 'var1', 'type': 'continuous', 'domain': (22,30)}, {'P2': 'var2', 'type': 'continuous', 'domain': (22,30)},{'V1': 'var3', 'type': 'continuous', 'domain': (2000,4000)},{'V2': 'var4', 'type': 'continuous', 'domain': (2000,4000)},{'Spacing': 'var5', 'type': 'continuous', 'domain': (10,40)}]
X_init = pd.read_csv('input/temp/initial.dat',header=None, engine='python')
# 修改类型
# X_init = X_init.values.tolist()
X_init = np.array(X_init).reshape(1,5)
Y_init = np.array(10396200).reshape(1,1)

iter_count = 10
current_iter = 0
X_step = X_init
Y_step = Y_init

while current_iter < iter_count:
    bo_step = GPyOpt.methods.BayesianOptimization(f = None, domain = domain, X = X_step, Y = Y_step)
    x_next = bo_step.suggest_next_locations()
    # x_next = sum(x_next, [])
    print(x_next)


    y_next = func(x_next)
    X_step = np.vstack((X_step, x_next))
    Y_step = np.vstack((Y_step, y_next))
    current_iter += 1

print(X_step)
print(Y_step)