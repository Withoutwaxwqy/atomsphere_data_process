import matplotlib.pyplot as plt
import re
from itertools import islice
import numpy as np
import os
from Hurricane import Hurricane


def pw_and_error_plot(site_globel, site_a, pwv_info_path, pwv_err_info_path):
    '''
    绘制pw的时间序列图和pw error的时间序列图
    :param site_a: 需要绘图的site
    :param pwv_info_path:
    :param pwv_err_info_path:
    :return: None
    '''
    plt.figure(figsize=(500,500))
    pw, pwerr = [],[]
    with open(pwv_info_path, 'r') as f:
        for line in islice(f, 0, None):
            pw.append(re.split(',', line)[1:-1])
    with open(pwv_err_info_path, 'r') as f:
        for line in islice(f, 0, None):
            pwerr.append(re.split(',', line)[1:-1])
    pw      = np.array(pw,    dtype=float)
    pwerr   = np.array(pwerr, dtype=float)
    index_a = [int(i[4]) for i in site_a]
    pw_a    = pw[index_a][:]
    pwerr_a = pwerr[index_a][:]
    x = [i for i in range(np.shape(pw_a)[1])]
    legend = []
    for i in range(np.shape(pw_a)[0]):
        plt.scatter(x, pw_a[i][:], marker='.')
        legend.append(site_globel[index_a[i]][3])
    plt.title("2020 205-208 Hurricane HANNA PWV time series")
    plt.xlabel("time(interval:30min)")
    plt.ylabel("PW(mm)")
    plt.legend(legend, fontsize=5, loc='best')
    plt.show()

    return 0

def series_site_pwv_plot(h:Hurricane, sitenames:list):
    pw, pwerr = [], []
    with open(h.pwv_path + "sitepwvtimeordered.txt", 'r') as f:
        for line in islice(f, 0, None):
            pw.append(re.split(',', line)[1:-1])
    with open(h.pwv_path + "sitepwverrtimeordered.txt", 'r') as f:
        for line in islice(f, 0, None):
            pwerr.append(re.split(',', line)[1:-1])
    pw = np.array(pw, dtype=float)
    # pwerr = np.array(pwerr, dtype=float)
    index_a = [int(i[4]) for i in h.site_a]
    pw_a = pw[index_a][:]
    # pwerr_a = pwerr[index_a][:]
    x0 = np.array([i for i in range(np.shape(pw_a)[1])])
    x = x0.reshape((1,len(x0)))

    # 画site的pwv时间序列图
    plt.figure(figsize=(6, 12))
    i = 1
    colors = ['r', 'g' ,'b', 'y', 'm', 'r']
    for each in sitenames:# TODO - 2021 04 11 待修改
        plt.subplot(len(sitenames),1,i)
        index = np.where(h.site_a==each)[0]
        if len(index)==0:
            print(each + ' 找不到！\n')
        plt.scatter(x, pw_a[index][:], marker='.', s=10,color = 'b', label = each)
        if i != len(sitenames):
            plt.xticks([])
        else:
            doy = [str(dd) for dd in range(h.duration[0]-1, h.duration[1])]
            ll = [i * 2 * 24 for i in range(len(doy))]
            plt.xticks(ll, doy)
        plt.xlim((0*48, 6*48))
        plt.ylim((10, 65))
        plt.legend(loc = 'upper right')
        i = i+1

    # plt.title(str(h.year) + " " + str(h.duration[0]) + "-" + str(
    #     h.duration[1]) + " Hurricane " + h.name + " PWV time series ()")
    # plt.xlabel("time(interval:30min)")
    # plt.ylabel("PW(mm)")
    # plt.legend(legend, fontsize=5, loc='best')
    plt.savefig(h.pc_dir + 'plot\\' + "PW of series (selected) sites.png", dpi=500)


def single_site_pwv_plot(h:Hurricane):
    '''
    单独画每个测站的图
    :param h: 飓风类
    :return:
    '''
    path = h.pc_dir+'single_site_pwv_plot\\'
    if not os.path.exists(path):
        os.makedirs(path)

    pw, pwerr = [], []
    with open(h.pwv_path + "sitepwvtimeordered.txt", 'r') as f:
        for line in islice(f, 0, None):
            pw.append(re.split(',', line)[1:-1])
    with open(h.pwv_path + "sitepwverrtimeordered.txt", 'r') as f:
        for line in islice(f, 0, None):
            pwerr.append(re.split(',', line)[1:-1])
    pw = np.array(pw, dtype=float)
    # pwerr = np.array(pwerr, dtype=float)
    index_a = [int(i[4]) for i in h.site_a]
    pw_a = pw[index_a][:]
    # pwerr_a = pwerr[index_a][:]
    x0 = np.array([i for i in range(np.shape(pw_a)[1])])
    x = x0.reshape((1, len(x0)))

    doy = [str(dd) for dd in range(h.duration[0] - 1, h.duration[1])]
    ll = [i * 2 * 24 for i in range(len(doy))]
    sites = h.site_qc1[0]
    for i in range(np.shape(sites)[0]):
        each = sites[i][3]
        plt.figure()
        index = np.where(h.site_a == each)[0]
        plt.scatter(x, pw_a[index][:], marker='.', s=20, color='b')
        plt.xticks(ll, doy)
        plt.xlim((0 * 48, len(doy) * 48))
        plt.ylim((10, 70))
        plt.title(each+" PWV ")
        plt.savefig(path+each+"_pwv.png", dpi=500)
