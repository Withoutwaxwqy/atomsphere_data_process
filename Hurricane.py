'''
定义台风class

'''

import matplotlib.pyplot as plt
import re
from itertools import islice
import numpy as np
import os
import wget
import siteprocess as sp
import shapefile
import echartsplot as es
import pwv_to_littleR as ptl
from pwv_to_littleR import *
from mpl_toolkits.basemap import Basemap as Basemap
from scipy import interpolate as ipl
from coordinateconvert import *
from scipy.interpolate import interp1d  # 引入scipy中的一维插值库
from scipy.interpolate import griddata  # 引入scipy中的二维插值库
import datetime as dt
import matplotlib.path as mpath

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False

class Hurricane():
    '''
    飓风类
    '''
    def __init__(self, name: str, ID: str, year: int, duration: tuple, field: tuple,
                 site_all,
                 isdataexist=False,
                 pwvinterval='hourly'):
        self.name           = name
        self.ID             = ID
        self.duration       = duration
        self.year           = year
        self.pwvinterval    = pwvinterval
        self.isdataexist    = isdataexist
        self.point1         = field[0]
        self.point2         = field[1]
        self.site_all       = site_all
        self.site_a         = sp.site_select(self.site_all, self.point1, self.point2)
        self.pc_dir         = 'E:\\论文\\毕业论文\\PWVDATA\\hurricane_' + self.name + '_PWV_Hour\\'
        self.pwv_path       = 'E:\\论文\\毕业论文\\PWVDATA\\hurricane_' + self.name + '_PWV_Hour\\' + 'pwv_data_hourly\\'
        self.site_qc1       = []
        self.pw_qc1         = []
        self.track          = []
        self.amsr           = 'E:\\论文\\毕业论文\\AMSRDATA\\hurricane_'+self.name + '_amsr\\'

    # TODO 加入轨迹信息，需要下载的数据信息，实现自动下载和数据处理
    # TODO 把函数全都移植到这个类里面

    def Hurrican_data_dl(self):
        '''
        默认下载至 'E:\\论文\\毕业论文\\PWVDATA\\hurricane_<hurricane_name>_PWV_Hour'
        :param urllistpath:
        :return:

        '''
        pc_dir = self.pc_dir
        if not os.path.exists(pc_dir):
            os.makedirs(pc_dir)
        if not os.path.exists(self.pwv_path):
            os.makedirs(self.pwv_path)

        # 生成urls.txt
        suominet_dl_url = "https://www.suominet.ucar.edu/data/pwvConusHourly/"
        # 设置下载路径

        if self.isdataexist == True:
            print("名为 " + self.name + " 的台风数据已经存在！！！\n")
        else:
            pwv_dl_list = []
            with open(pc_dir + "urls.txt", 'w') as f:
                if self.year == 2019 and self.duration[0] < 300 and self.duration[1] > 300:
                    print('无法使用该命令下载，请分两次下载！\n')
                else:  # 根据suominet官网文件目录确定下载目录
                    if self.year == 2019 and self.duration[0] >= 300:
                        suominetdir = suominet_dl_url
                    if self.year == 2020:
                        suominetdir = suominet_dl_url
                    if self.year <= 2019 and self.year >= 2008:
                        suominetdir = suominet_dl_url + "y" + str(self.year) + "/"
                # 写 urls.txt
                for i in range(self.duration[0], self.duration[1] + 1):
                    if self.pwvinterval == 'hourly':
                        for j in range(24):
                            url = "SUOh_{}.{}.{}.00.PWV".format(self.year, str(i).zfill(3), str(j).zfill(2))
                            f.write(suominetdir + url + '\n')
                            pwv_dl_list.append([suominetdir + url, url])
                print(self.name + "台风数据正在下载！！！目标文件夹->" + pc_dir + '\n')
            for each in pwv_dl_list:
                if not os.path.exists(self.pwv_path+each[1]):
                    wget.download(each[0], out=self.pwv_path + each[1])
        return 0

    def plot_pwv(self):
        '''
            绘制pw的时间序列图和pw error的时间序列图
            :param site_a: 需要绘图的site
            :param pwv_info_path:
            :param pwv_err_info_path:
            :return: None
            '''

        pw, pwerr = [], []
        with open(self.pwv_path+"sitepwvtimeordered.txt", 'r') as f:
            for line in islice(f, 0, None):
                pw.append(re.split(',', line)[1:-1])
        with open(self.pwv_path+"sitepwverrtimeordered.txt", 'r') as f:
            for line in islice(f, 0, None):
                pwerr.append(re.split(',', line)[1:-1])
        pw = np.array(pw, dtype=float)
        pwerr = np.array(pwerr, dtype=float)
        index_a = [int(i[4]) for i in self.site_a]
        pw_a = pw[index_a][:]
        pwerr_a = pwerr[index_a][:]
        x = [i for i in range(np.shape(pw_a)[1])]
        legend = []
        # 画site的pwv时间序列图
        plt.figure()
        for i in range(np.shape(pw_a)[0]):
            plt.scatter(x, pw_a[i][:], marker='.')
            legend.append(self.site_all[index_a[i]][3])
        plt.title(str(self.year)+" "+str(self.duration[0])+"-"+str(self.duration[1])+" Hurricane " + self.name + " PWV time series")
        plt.xlabel("time(interval:30min)")
        plt.ylabel("PW(mm)")
        plt.legend(legend, fontsize=5, loc='best')
        plt.savefig(self.pc_dir + "PW of sites.png", dpi=500)

        # 画site的pwv-error时间序列图
        plt.figure()
        for i in range(np.shape(pw_a)[0]):
            plt.scatter(x, pwerr_a[i][:], marker='.')
            legend.append(self.site_all[index_a[i]][3])
        plt.title(str(self.year) +" "+ str(self.duration[0]) + "-" + str(
            self.duration[1]) + " Hurricane " + self.name + " PWV error time series")
        plt.xlabel("time(interval:30min)")
        plt.ylabel("PW error(mm)")
        plt.legend(legend, fontsize=5, loc='best')

        # plt.show()
        plt.savefig(self.pc_dir+"PW error of sites.png", dpi = 500)
        return 0

    def plot_eharts(self):
        es.draw_usa_map1(self.site_a, self.pc_dir)

    def pwv2littleR(self):
        ptl.pwv_to_little_r(self.pwv_path, self.site_all)

    def site_QC1(self):
        # QC1 检测-将出线过少的self.site_a
        #STEP 1: 先选出site_a 的
        # vprint
        pwv_number_site = np.zeros(shape=(np.shape(self.site_a)[0],2), dtype=None)
        pw, pwerr = [], []
        with open(self.pwv_path + "sitepwvtimeordered.txt", 'r') as f:
            for line in islice(f, 0, None):
                pw.append(re.split(',', line)[1:-1])
        with open(self.pwv_path + "sitepwverrtimeordered.txt", 'r') as f:
            for line in islice(f, 0, None):
                pwerr.append(re.split(',', line)[1:-1])
        pw = np.array(pw, dtype=float)
        pwerr = np.array(pwerr, dtype=float)
        index_a = [int(i[4]) for i in self.site_a]
        pw_a = pw[index_a][:]
        pwerr_a = pwerr[index_a][:]
        # 统计每个测站有效观测值个数
        vaild_pw_number_a   = np.count_nonzero(pw_a > 0, axis=1)
        # 统计中位数
        max_pw_site_a       = np.max(vaild_pw_number_a)
        index_QC1_site_a    = np.where(vaild_pw_number_a >  max_pw_site_a/3)
        index_not_QC1_site_a= np.where(vaild_pw_number_a <= max_pw_site_a/3)

        QC1_pw_num_site_a          = vaild_pw_number_a[index_QC1_site_a]
        not_QC1_pw_num_site_a      = vaild_pw_number_a[index_not_QC1_site_a]
        plt.figure()
        plt.stem(index_QC1_site_a[0],      QC1_pw_num_site_a,     linefmt='b-', markerfmt='o', basefmt='--', label='accepted by QC1')
        plt.stem(index_not_QC1_site_a[0],  not_QC1_pw_num_site_a, linefmt='r-', markerfmt='o', basefmt='--', label='not accepted by QC1')
        plt.ylabel("Sample Number",fontsize=14)
        plt.ylim(-10, 400)
        plt.xlabel("Station ID", fontsize=14)
        plt.legend(loc="upper center")
        # plt.show()
        plt.savefig(self.pc_dir+"QC1_result.png", dpi=600)

        # 取得QC1 之后的测站每历元观测值
        self.site_qc1 = self.site_a[index_QC1_site_a,:]
        pw_QC1 = pw_a[list(index_QC1_site_a[0])][:]
        self.pw_qc1 = pw_QC1
        index_a = np.array(index_a)
        index_QC1_site_all = index_a[list(index_QC1_site_a[0])]
        # 生成画图所需的x轴序列
        x = [i for i in range(np.shape(pw_QC1)[1])]
        # 开始对QC1 结果绘图
        plt.figure()
        legend = []
        for i in range(np.shape(pw_QC1)[0]):
            plt.scatter(x, pw_QC1[i][:], marker='.')
            legend.append(self.site_all[index_QC1_site_all[i]][3])
        plt.title(str(self.year) + " " + str(self.duration[0]) + "-" + str(
            self.duration[1]) + " Hurricane " + self.name + " PWV time series")
        plt.xlabel("time(interval:30min)")
        plt.ylabel("PW(mm)")

        plt.legend(legend, fontsize=5, loc='best')

        # plt.show()
        plt.savefig(self.pc_dir+"PW of sites after QC1.png", dpi=500)

        # 将QC1 运行后筛选的测站输出为 out文件
        QC1_out = self.pc_dir+"out_after_QC1\\"
        if not os.path.exists(QC1_out):
            os.makedirs(self.pc_dir+"out_after_QC1\\")
        #
        path_list_all = os.listdir(self.pwv_path)
        path_list_pwv = []
        for each in path_list_all:
            if os.path.splitext(each)[1] == ".PWV":
                path_list_pwv.append(each)
        for each in path_list_pwv:
            fin = ptl.load_PWV(self.pwv_path + each)
            tt = dt.datetime.strptime(each,'SUOh_%Y.%j.%H.00.PWV')
            if not os.path.exists(QC1_out+ 'be\\'):
                os.makedirs(QC1_out+ 'be\\')
            fout = open(QC1_out+ 'be\\' + 'obs.' + dt.datetime.strftime(tt, "%Y%m%d%H"), 'w')

            # outline = np.zeros(shape=(1,52))
            for i in range(fin.shape[0]):
                pwvinfo = fin[i]
                LL = sp.site_info(pwvinfo[0], self.site_all)
                if LL == None or pwvinfo[0] not in self.site_all[index_QC1_site_all,3]:
                    pass
                else:
                    # 将PWV数据录入sitepwv
                    # sitepwvindex = np.where(self.site_all == pwvinfo[0])
                    # if sitepwvindex[0].size != 0:
                    #     rawindex = sitepwvindex[0][0]
                    #     if pwvinfo[1][11:13] == '15':
                    #         sitepwv[rawindex][filenum * 2 + 1] = pwvinfo[3]
                    #         sitepwverr[rawindex][filenum * 2 + 1] = pwvinfo[4]
                    #     if pwvinfo[1][11:13] == '45':
                    #         sitepwv[rawindex][filenum * 2 + 2] = pwvinfo[3]
                    #         sitepwverr[rawindex][filenum * 2 + 1] = pwvinfo[4]
                    fout.write(str(format(float(LL[1]), '20.5f')) +  # Lat
                               str(format(float(LL[0]), '20.5f')) +  # Lon
                               ' ' * 40 + # ID
                               fin[i][0] + ' ' * 36 + # Name
                               'FM-111' + ' ' * 34 +  # 类型
                               ' ' * 40 + str(format(float(LL[2]), '20.5f')) +
                               str(format(0, '10d')) * 5 +
                               F_str * 3 +
                               str(format(0, '10d')) + str(format(36, '10d')) +
                               ' ' * 6 + pwvinfo[1][0:8] + pwvinfo[1][9:13] + '00' +  # Date
                               HeaderInVaildStr * 13 +
                               # PW
                               str(format(float(pwvinfo[3])*0.1, '13.5f')) +
                               str(format(int(float(pwvinfo[4])*10), '7d')) +
                               HeaderInVaildStr + '\n' +
                               # Data
                               str(format(float(pwvinfo[9]) * 100, '13.5f')) + str(format(0, '7d')) +  # Pressure
                               str(format(float(LL[2]), '13.5f')) + str(format(0, '7d')) +  # Height
                               str(format(float(pwvinfo[10]) + TEM_K, '13.5f')) + str(format(0, '7d')) +  # Temperature
                               DataInVaildStr * 7 + '\n' +
                               # EndingRecord + TailIntegers
                               EndingRecordStr + '\n' +
                               TailIntegers + '\n'
                               )
            fout.close()
            #filenum = filenum + 1

    def site_plot_basemap(self):
        pass

    def hurricane_track_plot(self):
        shapepath   = self.pc_dir + "shp\\"
        shapefile   = self.pc_dir + "shp\\" + self.ID + "_lin"
        if not os.path.exists(shapepath):
            os.makedirs(shapepath)
            print("\n waring <1> hurricane_track_plot终止， 因为没有shp文件夹并且无shp数据, 请将台风"+self.name+"的数据下载至：\n"+
                  shapepath+"\n")
            return 1
        path_list_all = os.listdir(shapepath)
        if len(path_list_all) == 0:
            print("\n waring <2> hurricane_track_plot终止， 因为有shp文件夹但是无shp数据, 请将台风" + self.name + "的数据下载至：\n" +
                  shapepath + "\n")
            return 2

        m = Basemap(llcrnrlon=-100.,llcrnrlat=15.,urcrnrlon=-70.,urcrnrlat=45.,
                    projection='lcc',lat_1=20.,lat_2=40.,lon_0=-60.,
                    resolution ='l',area_thresh=1000.)
        fig         = plt.figure()
        shp_info    = m.readshapefile(shapefile, "Gordon", drawbounds=False)

        names = []
        for shapedict in m.Gordon_info:
            cat = shapedict['STORMTYPE']
        # STROMTYPE注释：
        # TD: tropical depression
        # TS: tropical strom
        #
        #

        # print(names)
        # print(len(names))
        # print("\n")
        # 根据属性，在地图上画图
        # stromtype_color = {"LO":"r", "TD":"g", "TS":"b", "HU":"m", "TS":"y", "EX":"cyan"}
        stromtype_trans = {
            "TD": "Tropical cyclone of tropical depression intensity",
            "TS": "Tropical cyclone of tropical storm intensity",
            "HU": "Tropical cyclone of hurricane intensity",
            "EX": "Extratropical cyclone",
            "SD": "Subtropical cyclone of subtropical depression intensity",
            "SS": "Subtropical cyclone of subtropical storm intensity",
            "LO": "Low-pressure cyclones",
            "WV": "Tropical Wave",
            "DB": "Disturbance"
        }
        i = 0
        for shapedict, shape in zip(m.Gordon_info, m.Gordon):
            # name = shapedict['NAME']
            cat = shapedict['STORMTYPE']
            xx, yy = zip(*shape)
            # plot为在地图上画图
            # 有颜色的绘制
            # m.plot(xx, yy, linewidth=1.5, color=stromtype_color[cat], label='DOY'+str(i+245) +' '+ cat)
            # 无颜色绘制轨迹
            m.plot(xx, yy, linewidth =1.5, label = stromtype_trans[cat])
            # m.scatter(xx[-1], yy[-1], c='none', s=100, edgecolors='r')
            i = i+1
        # 在地图上画其他辅助要素，国界，经纬度线等
        #
        s = self.site_qc1[0]
        x = s[:, 0]
        y = s[:, 1]
        sitename = s[:, 3]
        fx = list(x.astype(np.float64))
        fy = list(y.astype(np.float64))
        xs, ys = m(fx, fy)

        m.drawcoastlines()
        m.drawcountries()
        # # -------------有颜色边界------------------------
        # m.drawmapboundary(fill_color='#99ffff')
        # m.fillcontinents(color='#cc9966', lake_color='#99ffff')
        # -------------无颜色边界-------------------------
        m.drawmapboundary(fill_color=None)
        # m.fillcontinents(color=None, lake_color=None)
        m.drawparallels(np.arange(10, 70, 20), labels=[1, 1, 0, 0])
        m.drawmeridians(np.arange(-100, 0, 20), labels=[0, 0, 0, 1])
        for x, y, sn in zip(xs, ys, sitename):
        #    plt.scatter(x, y, marker='v', color=None, edgecolors='b', s=20, zorder=10)
            plt.annotate(sn, xy=(x,y), xytext=(x, y), fontsize = 5)

        # 画从PDF中复制下来的台风点轨迹
        temp1 = np.loadtxt(self.pc_dir + 'shp\\'+self.name+'_track.txt', dtype=str)
        temp2 = temp1[:, 3:5].astype(float)  # 此时经度还没改过来 ， 需要加个符号
        temp2[:, 1] = -temp2[:, 1]
        track_ll = temp2
        # 让它稀释一点

        track_x, track_y = m(track_ll[:, 1],track_ll[:, 0])
        index = [i for i in range(len(track_x)) if i % 2 == 0]

        # 6 9 叠加形成台风符号
        # plt.scatter(track_x, track_y, s=50, marker='$6$',
        #            edgecolors='k', facecolor=None, linewidths=0.5)
        # plt.scatter(track_x, track_y, s=50, marker='$9$',
        #            edgecolors='k', facecolor=None, linewidths=0.5)
        # plt.scatter(track_x, track_y, s=50, marker='o',
        #            edgecolors='grey', facecolor='white')



        plt.scatter(track_x[index], track_y[index], s=200, marker= self.get_hurricane_marker(),
                  edgecolors='r', facecolors='none', linewidth=1, label = "Hurricane Track")
        # 设置图的标题
        plt.title('Hurricane ' + self.name + ' Tracks (Hurricane ID: ' + self.ID + ')')
        # plt.legend(loc= "upper right")

        plt.savefig(self.pc_dir+self.name+"_best_track.png", dpi=600)


    def   interpolate_2d_plot(self, flag):
        '''
        对每一天的测站pwv在空间上进行差值
        :return:
        '''
        # 使用self.site_qc1
        data = self.pw_qc1
        site_info = self.site_qc1[0]

        s = self.site_qc1[0]
        # 测站的XY坐标
        x = s[:, 0]
        y = s[:, 1]
        sitename = s[:, 3]
        fx = x.astype(np.float64)
        fy = y.astype(np.float64)
        # 初始化basemap
        m = Basemap(llcrnrlon=-100., llcrnrlat=15., urcrnrlon=-70., urcrnrlat=45.,
                    projection='cyl', lat_1=20., lat_2=40., lon_0=-60.,
                    resolution='l', area_thresh=1000.)
        fig = plt.figure()
        # xs, ys = m(fx, fy)
        zz  = np.zeros(shape=(np.shape(x)[0],7), dtype=float)
        # 取七天零点的数据进行差值
        index = [i*48 for i in range(7)]
        for i in range(7):
            zz[:,i]=data[:,i*48]
        # test 先算第一天的
        # z0 = z[:, 0]
        # 剔除 0的 测站

        # plt.figure()
        # plt.subplots()
        m.drawcoastlines()
        m.drawcountries()
        m.drawmapboundary()
        #m.fillcontinents(color='#cc9966', lake_color='#99ffff')
        m.drawparallels(np.arange(10, 70, 20), labels=[1, 1, 0, 0])
        m.drawmeridians(np.arange(-100, 0, 20), labels=[0, 0, 0, 1])
        # for _x, _y, _sn in zip(xs, ys, sitename):
        #     p = plt.scatter(x, y, marker='v', color='b',edgecolors='y', s=40, zorder=10)
        #     # plt.annotate(_sn, xy=(_x, _y), xytext=(_x + 100, _y), fontsize=5)
        #
        # for i in range(7):


        z = data[:, flag*48]
        index_not_zero = np.where(z>30)
        x0=fx[index_not_zero]
        y0=fy[index_not_zero]
        z0=z[index_not_zero]

        func = ipl.Rbf(x0, y0, z0, function='multiquadric')
        # 栅格化
        xnew, ynew = np.mgrid[-100:-70:100j, 15:45:100j]
        # 计算由差值函数计算得到的新的z值
        znew = func(xnew, ynew)
        xx, yy = m(xnew, ynew)
        # plt.figure()
        # vplt.cm.get_cmap('cmap')
        color_list = plt.cm.YlGnBu(np.linspace(0, 1, 21))
        jieti = np.linspace(30, 80, 21)
        cj = np.linspace(0,1,21)
        CS =plt.contourf(xx, yy, znew, alpha = 0.5, levels = jieti, colors=color_list)
        CX = plt.contour(xx, yy, znew, alpha = 0.7) #color='balck', linewidth = 1)
        plt.xticks([-100, -95, -90, -85, -80, -75,-70],['-100', '-95', '-90', '-85', '-80', '-75','-70'])
        plt.xlim((-100,-70))
        plt.yticks([15,20,25,30,35,40,45], ['15','20','25','30','35','40','45'])
        plt.ylim((15,45))
        plt.clabel(CX, inline=True, fontsize=10)
        plt.title("DOY " + str(flag+self.duration[0]) + " pwv 测站二维插值图 ")
        plt.colorbar()
        plt.savefig(self.pc_dir+"plot\\"+self.name+" counter "+str(flag)+"new.png", dpi=600)

    def get_hurricane_marker(self):
        u = np.array([[2.444, 7.553],
                      [0.513, 7.046],
                      [-1.243, 5.433],
                      [-2.353, 2.975],
                      [-2.578, 0.092],
                      [-2.075, -1.795],
                      [-0.336, -2.870],
                      [2.609, -2.016]])
        u[:, 0] -= 0.098
        codes = [1] + [2] * (len(u) - 2) + [2]
        u = np.append(u, -u[::-1], axis=0)
        codes += codes
        return mpath.Path(3 * u, codes, closed=False)

    def counterf_plot(self):
        data = self.pw_qc1
        site_info = self.site_qc1[0]

        s = self.site_qc1[0]
        # 测站的XY坐标
        x = s[:, 0]
        y = s[:, 1]
        sitename = s[:, 3]
        fx = x.astype(np.float64)
        fy = y.astype(np.float64)
        # 初始化basemap
        # m = Basemap(llcrnrlon=-100., llcrnrlat=15., urcrnrlon=-70., urcrnrlat=45.,
        #             projection='lcc', lat_1=20., lat_2=40., lon_0=-60.,
        #             resolution='l', area_thresh=1000.)
        # xs, ys = m(fx, fy)
        zz = np.zeros(shape=(np.shape(x)[0], 7), dtype=float)
        # 取七天零点的数据进行差值
        index = [i * 48 for i in range(7)]
        for i in range(7):
            zz[:, i] = data[:, i * 48]
        grid_x, grid_y = np.mgrid[-100:-70:500j, 15:45:500j]
        # x方向在0-1上均匀生成200个数，y方向在0-1上均匀生成500个数
        i = 0
        z = data[:, 4 * 48]
        index_not_zero = np.where(z > 30)
        x0 = fx[index_not_zero]
        y0 = fy[index_not_zero]
        z0 = z[index_not_zero]
        points0 = np.vstack((x0, y0))
        # 随机生成（200，2）的矩阵，即200个点坐标
        points = points0.T
        values = z0

        # 初始化basemap
        m = Basemap(llcrnrlon=-100., llcrnrlat=15., urcrnrlon=-70., urcrnrlat=45.,
                    projection='lcc', lat_1=20., lat_2=40., lon_0=-60.,
                    resolution='l', area_thresh=1000.)
        xs, ys = m(fx, fy)


    def func2(self):
        plt.rcParams.update({"font.size": 10})
        data = self.pw_qc1
        site_info = self.site_qc1[0]


        s = self.site_qc1[0]
        # 测站的XY坐标
        x = s[:, 0]
        y = s[:, 1]
        sitename = s[:, 3]
        fx = x.astype(np.float64)
        fy = y.astype(np.float64)
        #计算插值后的差值
        pwv_after_interpolate = np.zeros(shape=(100,100,6))
        pwv_in = np.zeros(shape=(100,100,5))

        xnew, ynew = np.mgrid[-100:-70:100j, 15:45:100j]
        for flag in range(6):
            z = data[:, flag * 48]
            index_not_zero = np.where(z > 30)
            x0 = fx[index_not_zero]
            y0 = fy[index_not_zero]
            z0 = z[index_not_zero]
            func = ipl.Rbf(x0, y0, z0, function='multiquadric')

            # 计算由差值函数计算得到的新的z值
            znew = func(xnew, ynew)
            pwv_after_interpolate[:, :, flag] = znew

        for i in range(5):
            pwv_in[:, :, i] = pwv_after_interpolate[:, :, i+1]-pwv_after_interpolate[:, :, i]
        plt.figure()
        m = Basemap(llcrnrlon=-100., llcrnrlat=15., urcrnrlon=-70., urcrnrlat=45.,
                    projection='cyl', lat_1=20., lat_2=40., lon_0=-60.,
                    resolution='l', area_thresh=1000.)
        m.drawcoastlines()
        m.drawcountries()
        # # -------------有颜色边界------------------------
        # m.drawmapboundary(fill_color='#99ffff')
        # m.fillcontinents(color='#cc9966', lake_color='#99ffff')
        # -------------无颜色边界-------------------------
        m.drawmapboundary(fill_color=None)
        # m.fillcontinents(color=None, lake_color=None)
        m.drawparallels(np.arange(10, 70, 20), labels=[1, 1, 0, 0])
        m.drawmeridians(np.arange(-100, 0, 20), labels=[0, 0, 0, 1])

        x, y = m(xnew, ynew)
        color_list = plt.cm.bwr(np.linspace(0, 1, 15))
        level = np.linspace(-30, 30, 15)

        fff, axes = plt.subplots(nrows=2, ncols=2)
        i = 0
        for e in axes.flat:
            CF = e.contourf(x, y, pwv_in[:, :, i], alpha=0.5, levels=level, colors=color_list)
            CX = e.contour(x, y, pwv_in[:, :, i], alpha = 0.5, colors='k', linewidths=0.2)
            # e.set_title('fig'+str(i))
            i = i + 1

        plt.xticks([-100, -95, -90, -85, -80, -75, -70], ['-100', '-95', '-90', '-85', '-80', '-75', '-70'])
        plt.xlim((-100, -70))
        plt.yticks([15, 20, 25, 30, 35, 40, 45], ['15', '20', '25', '30', '35', '40', '45'])
        plt.ylim((15, 45))
        c = plt.colorbar(CF, ax=axes.ravel().tolist())
        c.set_label('GPS/PWV插值结果隔历元作差（mm）')
        c.set_ticks([-25,-20,-15,-10,-5,0,5,10,15,20,25])
        c.ax.tick_params(labelsize=8)
        plt.savefig(self.pc_dir + "pwvw二维平面作差结果.png", dpi=600)
        plt.show()

        pass





