import GPyOpt
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


def exeact():
    # 改变工作目录
    os.chdir("D:/wb/two_stages/Multistage-optimization-final-AI3-BOPT/Multistage-optimization-final/multistage-optimization")

    path_01 = "multistage_optimization.exe"

    r_v = os.system(path_01)

    # print(r_v)

def func(X):
    #完成数据覆盖，物理仿真模型调用，以及得到结果输出
    f = open("input/temp/initial.dat", "r+")
    f.seek(0)
    #####把x_next保存到文件中，每行一个数据

    # print(X)
    #print(X[0][1])
    for i in range(5):
        f.write(str(X[0][i])+'\n')
    f.close
    ####
    #exeact()
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
Y_init = np.array(7740090).reshape(1,1)
NPV_max = np.array(7740090).reshape(1,1)

#27.702153694446768
#26.71222309897869
#3683.3762320792357
#2279.563934971128
#18.041868414485904
iter_count = 50
current_iter = 0
X_step = X_init
Y_step = Y_init
y_max = 7740090
p1 = X_step[0][0]
p2 = X_step[0][1]
times = 0
#for each iteration: npv_max=目前已知的最大值，if 新观测到的点npv_new>npv_max，则npv_max=npv_new；else pass。画出npv_max和iteration的趋势图看看
while current_iter < iter_count:
    bo_step = GPyOpt.methods.BayesianOptimization(f = None, domain = domain, X = X_step, Y = Y_step)
    x_next = bo_step.suggest_next_locations()
    # x_next = sum(x_next, [])
    print(x_next)
    y_next = float(func(x_next))
    p1 = np.hstack((p1,x_next[0][0]))
    print(p1)
    print(p1.shape)
    p2 = np.hstack((p2,x_next[0][1]))
    print(p2)
    print(p2.shape)
    X_step = np.vstack((X_step, x_next))
    if y_next >= y_max:
        y_max = y_next
    else:
        pass

    NPV_max = np.vstack((NPV_max, y_max))
    Y_step = np.vstack((Y_step, y_next))
    current_iter += 1
    times = np.hstack((times,current_iter))
    print(times.shape)
    print(y_next)

print(X_step)
print(Y_step[0])
print(Y_step.shape)
input_values = times

#plot根据列表绘制出有意义的图形，linewidth是图形线宽，可省略
plt.figure()
plt.plot(input_values,p1,'r-D',linewidth=2,linestyle='--', label="Stage 1")
plt.plot(input_values,p2,'g-s',linewidth=2, label="Stage 2")

plt.legend(loc="upper right",fontsize = 14)   # 与plt.legend(loc=1)等价
# #设置图标标题
# plt.title("Square Numbers",fontsize = 24)
#设置坐标轴标签
plt.xlabel("Iteration",fontsize = 18)
plt.ylabel("Treatment Pressure (MPa)",fontsize = 18)
#设置刻度标记的大小
plt.tick_params(axis='both',labelsize = 18)
plt.savefig('figure/Pressure.png', bbox_inches='tight')
#打开matplotlib查看器，并显示绘制图形
Y = np.zeros((iter_count+1,1))
input_values = input_values.reshape(iter_count+1,1)
for i in range(iter_count+1):
    Y[i] = Y_step[i]
print(Y)

plt.figure()
plt.plot(input_values,Y,'r-D', linewidth=2)
plt.xlabel("Iteration", fontsize = 18)
plt.ylabel("NPV (USD)",fontsize = 18)
#设置刻度标记的大小
plt.tick_params(axis='both',labelsize = 18)
plt.savefig('figure/NPV.png', bbox_inches='tight')

Ys = np.zeros((iter_count+1,1))
input_values = input_values.reshape(iter_count+1,1)
for i in range(iter_count+1):
    Ys[i] = NPV_max[i]
print(Ys)

plt.figure()
plt.plot(input_values,Ys,'r-D', linewidth=2)
plt.xlabel("Iteration", fontsize = 18)
plt.ylabel("NPV (USD)",fontsize = 18)
#设置刻度标记的大小
plt.tick_params(axis='both',labelsize = 18)
plt.savefig('figure/NPV.png', bbox_inches='tight')

plt.show()
