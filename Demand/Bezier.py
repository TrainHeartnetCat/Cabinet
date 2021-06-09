import matplotlib.pyplot as plt
import numpy as np
import math

# n次贝塞尔曲线
# 用于拟合非函数图形曲线
# 插值时默认在0~1区间插值，根据公式是0~1，而且从数学定义上，如果超出1应该也没有意义
# parameter equation: bezier = sum(C(n,i) * Point[i] * (1-t)**(n-i) * t**i) -> t∈[0, 1]
# combinatorial number: C(n,m) = n! / ((n-m)!*m!) -> m<=n

# 是否在画布上保留原始的数据点，是则为True
keep_origin_point = True
# 数据组的lsit
points = [np.array([(1.2, 0.3), (1.3, 0.3), (1.4, 0.3), (1.5, 0.4), (1.6, 0.4),
                    (1.6, 0.9), (1.5, 1.6), (1.4, 2), (1.3, 2), (1.2, 2)]),
          np.array([(1.5, 1.7), (1.6, 1), (1.7, 0.5), (1.8, 0.5), (1.9, 0.5),
                   (2  , 0.5), (2.1, 0.4), (2.2, 0.4), (2.3, 0.3), (2.4, 0.2),
                   (2.5, 0.2), (2.6, 0.1), (2.7, 0.1), (2.8, 0.1), (2.9, 0.2),
                   (3  , 0.2), (3.1, 0.3), (3.2, 0.4), (3.3, 0.4), (3.4, 0.5),
                   (3.5, 0.5), (3.6, 0.6), (3.7, 0.7), (3.8, 1), (1.5, 2),
                   (1.6, 2), (1.7, 2), (1.8, 2), (1.9, 2), (2  , 2),
                   (2.1, 2), (2.2, 2), (2.3, 2), (2.4, 2), (2.5, 2),
                   (2.6, 2), (2.7, 2), (2.8, 2), (2.9, 2), (3  , 2),
                   (3.1, 2), (3.2, 2), (3.3, 2), (3.4, 2), (3.5, 2),
                   (3.6, 2), (3.7, 1.9), (3.8, 1.7)]),
                    ]
# 如果不同的点组想要用不同的插值个数，得自行添加参数。同位置点组与参数相互对应，因此必须保证数量也对应
interpolation = [100, 100]

if len(points) != len(interpolation):
    print('Error! Please check the number of element in list points and list interpolation!')
    exit(0)

def combinatorial_number(n, m):
    func = math.factorial(n) / (math.factorial(n-m) * math.factorial(m))
    return func

def plot_bezier(point, interpolation):
    n = len(point) - 1

    # origin
    # work = []
    # for t in np.linspace(0, 1, interpolation):
    #     result = combinatorial_number(n, 0) * point[0] * (1 - t)**(n - 0) * t**0
    #     for i in range(1, n + 1):
    #         result = result + combinatorial_number(n, i) * point[i] * (1 - t)**(n - i) * t**i
    #     work.append(result)

    # simplification
    para = lambda t: sum(combinatorial_number(n, i) * point[i] * (1 - t)**(n - i) * t**i 
                    for i in range(n + 1))
    fit = np.array([para(t) 
                    for t in np.linspace(0, 1, interpolation)])

    X = fit[:, 0]# array中的x坐标array
    Y = fit[:, 1]
    return X, Y

for i in range(len(points)):
    new_x, new_y = plot_bezier(points[i], interpolation[i])
    plt.plot(new_x, new_y, 'red')
    if keep_origin_point == True:
        origin_x, origin_y = points[i][:, 0], points[i][:, 1]
        plt.plot(origin_x, origin_y)

plt.show()
