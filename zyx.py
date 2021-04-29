import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d #引入scipy中的一维插值库
from scipy.interpolate import griddata#引入scipy中的二维插值库


'''''
def func(x, y):
    return x**2+y**2
'''''
grid_x, grid_y = np.mgrid[1:10:200j, 1:10:500j]
#x方向在0-1上均匀生成200个数，y方向在0-1上均匀生成500个数

points = np.random.randint(1,10,(200, 2))
#随机生成（200，2）的矩阵，即200个点坐标

values = np.arange(0,200)#func(points[:,0], points[:,1])
#规定坐标值的值


grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
print(grid_z0[0][1])
#由于griddata返回的值是nddarry的格式的，所以可以读取他的数据，这里就是读取第[0][1]个数值的数

grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear',fill_value=5)
print(grid_z1[0][1])

grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic',fill_value=5)
print(grid_z1[0][1])
'''
plt.subplot(221)
plt.imshow(func(grid_x, grid_y).T, extent=(1,10,1,10), origin='lower')
plt.plot(points[:,0], points[:,1], 'k.', ms=1)

plt.title('Original')
'''
plt.subplot(222)
plt.imshow(grid_z0.T, extent=(1,10,1,10), origin='lower')

plt.title('Nearest')
plt.subplot(223)
plt.imshow(grid_z1.T, extent=(1,10,1,10), origin='lower')

plt.title('Linear')
plt.subplot(224)
plt.imshow(grid_z2.T, extent=(1,10,1,10), origin='lower')

plt.title('Cubic')
plt.gcf().set_size_inches(8, 8)
plt.show()