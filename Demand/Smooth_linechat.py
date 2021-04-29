import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# 通过微分方法，将散点折线图变平滑

# 横纵坐标，T横坐标
X = np.array([5, 19, 35, 77, 108])
Y = np.array([320, 560, 774, 890, 1320])

plt.plot(X, Y)


# 第三个变量，可以理解为平滑程度，越高越smooth
X_new = np.linspace(X.min(), X.max(), 20) 
 
smooth = make_interp_spline(X, Y)(X_new)
 
plt.plot(X_new, smooth)
plt.show()