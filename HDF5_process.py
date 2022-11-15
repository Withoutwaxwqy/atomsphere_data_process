# import h5py
# import os
# from mpl_toolkits.basemap import Basemap as Basemap
# import matplotlib.pyplot as plt
# import numpy as np
# def AMSR_reader(path):
#     path_list_all = os.listdir(path)
#     path_list_h5 = []
#     for each in path_list_all:
#         if os.path.splitext(each)[1] == ".h5":
#             path_list_h5.append(each)
#     for each in path_list_h5:
#         f= h5py.File(path+each, 'r')
#         kh5 = f.keys()
#         for key in kh5:
#             print(f[key], key, f[key].name)

#         latA0 = f["Latitude of Observation Point for 89A"][()]
#         lonA0 = f["Longitude of Observation Point for 89A"][()]
#         latB0 = f["Latitude of Observation Point for 89B"][()]
#         lonB0 = f["Longitude of Observation Point for 89B"][()]

#         BR_238_H = f["Brightness Temperature (res06,23.8GHz,H)"][()]
#         BR_238_V = f["Brightness Temperature (res06,23.8GHz,V)"][()]
#         BR_89_AH = f["Brightness Temperature (original,89GHz-A,H)"][()]
#         BR_89_AV = f["Brightness Temperature (original,89GHz-A,V)"][()]

#         f.close()

#     # 绘图
#     m = Basemap(llcrnrlon=-130., llcrnrlat=0., urcrnrlon=-40., urcrnrlat=60.,
#                 projection='cyl', lat_1=20., lat_2=40., lon_0=-60.,
#                 resolution='l', area_thresh=1000.)
#     plt.figure()
#     m.drawcoastlines()
#     m.drawcountries()
#     m.drawmapboundary()
#     # m.fillcontinents(color='#cc9966', lake_color='#99ffff')
#     m.drawparallels(np.arange(10, 70, 20), labels=[1, 1, 0, 0])
#     m.drawmeridians(np.arange(-100, 0, 20), labels=[0, 0, 0, 1])

#     num=latA0.shape[0]*latA0.shape[1]

#     latA = latA0.reshape((1, num))
#     latB = latB0.reshape((1, num))
#     lonA = lonA0.reshape((1, num))
#     lonB = lonB0.reshape((1, num))
#     # BR_238_H = BR_238_H.reshape((1, num))
#     # BR_238_V = BR_238_V.reshape((1, num))
#     BR_89_AH = BR_89_AH.reshape((1, num))
#     xA,yA=m(lonA, latA)
#     m.scatterm(xA, yA ,marker = '.')
#     # plt.xticks([-100, -95, -90, -85, -80, -75, -70], ['-100', '-95', '-90', '-85', '-80', '-75', '-70'])
#     # plt.xlim((-100, -70))
#     # plt.yticks([15, 20, 25, 30, 35, 40, 45], ['15', '20', '25', '30', '35', '40', '45'])
#     # plt.ylim((15, 45))
#     plt.colorbar()
#     plt.show()

