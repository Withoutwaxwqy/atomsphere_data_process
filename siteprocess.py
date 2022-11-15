# 目的：对测站进行一些处理；选择合适的测站
import numpy as np
import os

def site_info(siteName, siteTable):
    site_index = np.where(siteTable == siteName)
    if site_index[0].size == 0:
        return None
    raw = siteTable[site_index[0]][0]
    LL = [raw[0], raw[1], raw[2]]
    return LL


def site_select(site_tabel, point1, point2):
    # 根据左下角 point1 和右上角的 point2 筛选出合适的站点 (反过来也没关系)
    # point 的 type 应该为tuple (latitude,longitude) (不能反过来)
    # site_tabel 类型为 numpy.array

    site_list = []
    for i in range(np.shape(site_tabel)[0]):
        site_lat = float(site_tabel[i][1])
        site_lon = float(site_tabel[i][0])
        if (site_lat - point1[0])*(site_lat - point2[0])<0 and (site_lon - point1[1])*(site_lon - point2[1])<0:
            site_list.append([site_tabel[i][0],site_tabel[i][1],site_tabel[i][2],site_tabel[i][3], i])
    return np.array(site_list, dtype=None)

def site_write_for_pyecharts_add(site_list, savepath):
    '''
    把站点信息输出为pyecharts可以使用的Geo()下的.add_coordinates命令(保存为txt以便于复制)\n
    把(lat, lon, sitename)-->.add_coordinates(name, lon, lat)
    example : .add_coordinate('WA',-120.04,47.56)
    :param site_list:使用numpy.loadtxt('site_list.txt')之后的 site矩阵
    :param savepath: txt file保存路径
    :return: None
    '''
    with open(savepath, 'w') as f:
        f.write("###这个文件是来自于E:\\论文\\atomsphere_data_process\\siteprocess.py"+
                "的函数 site_write_for_pyecharts_add\n"+
                "###目的是为了生成echart绘图所需要的插入点的命令\n")
        for i in range(np.shape(site_list)[0]):
            line = ".add_coordinate('{}',{},{})\n".format(site_list[i][3],site_list[i][0],site_list[i][1])
            f.write(line)
    return 0
#
# def site_quantity_test(sitelist:tuple, year:int):
#
#     SUOd_dir = "D:\\acdemic\\毕业论文\\PWVDATA\\SUOd_" + str(year)+"\\"
#     path_list_all = os.listdir(SUOd_dir)
#     path_list_pwv = []
#     for each in path_list_all:
#         if os.path.splitext(each)[1] == ".PWV":
#             path_list_pwv.append(each)
#     for each in sitelist:
#         for eachfile in
