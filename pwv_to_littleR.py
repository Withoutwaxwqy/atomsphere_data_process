import os
# convert pwv&ztd to little_r
import numpy as np
import re
from itertools import islice
from siteprocess import *
import matplotlib.pyplot as plt

inVaildNum = -888888
HeaderInVaildStr = str(format(inVaildNum, '13.5f')) + str(format(inVaildNum, '7d'))
DataInVaildStr = str(format(inVaildNum, '13.5f')) + str(format(0, '7d'))
EndingRecordStr = '-777777.00000      0-777777.00000      0      1.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
TailIntegers = '     39      0      0'
TEM_K = 273.15
F_str = '         F'

def pwv_to_little_r(path, siteTable):


    path_list_all = os.listdir(path)
    path_list_pwv = []
    for each in path_list_all:
        if os.path.splitext(each)[1] == ".PWV":
            path_list_pwv.append(each)
    # ---------------------------- PWV format ----------------------------------
    # Site PWVmidTim    Duration PW   FMerr Wdelay Mdelay Tdelay  KFAC  Press  Temp  Rhum Ddelay Mf Kf
    # SSSS YYYMMDD/HHMM   MIN   [mm]   [mm]  [mm]  [mm]   [mm]   d.ddd  [mbar]  [c]   [%]   [mm]  C C

    #---------------------------- LITTLE_R format ------------------------------
    # Lat.	Lon.	ID	Name	Platform	Source	Elevation	Valid fields	Num. errors	Num. warn.	Seq. number	Num. dup.	sound	bogus	Discard?	Unix time	Jul. day	Date	SLP, QC	Ref Pres., QC	Ground Temp, QC	SST, QC	SFC Pres, QC	Precip, QC	Dly Max T, QC	Dly Min T, QC	Ngt Min T, QC	3hr Pres Chg, QC	24hr Pres Chg, QC	Cld cvr, QC	Ceil, QC	Zenith Total Delay, QC
    # Pressure (Pa)	QC	Height (m)	QC	Temperature (K)	QC	Dew point (K)	QC	Wind speed (m/s)	QC	Wind direction (deg)	QC	Wind U (m/s)	QC	Wind V (m/s)	QC	Relative humidity (%)	QC	Thickness (m)	QC
    # Lat Lon Platform 日期字串 是必选项
    # 顺便整理一下质量控制所需要的数据
    sitepwvlist = [([0] * (len(path_list_pwv)*2+1)) for i in range(siteTable.shape[0])]
    sitepwverrlist = [([0] * (len(path_list_pwv)*2+1)) for i in range(siteTable.shape[0])]
    for i in range(siteTable.shape[0]):
        sitepwvlist[i][0] = siteTable[i][3]
        sitepwverrlist[i][0] = siteTable[i][3]
    sitepwv = np.array(sitepwvlist)
    sitepwverr = np.array(sitepwverrlist)
    # s =    np.array(shape=(siteTable.shape[0], len(path_list_pwv)), dtype=str)
    filenum = 0
    for each in path_list_pwv:
        fin = load_PWV(path+'\\'+each)
        fout = open(path+'\\'+os.path.splitext(each)[0]+'.out','w')

        # outline = np.zeros(shape=(1,52))
        for i in range(fin.shape[0]):
            pwvinfo = fin[i]
            LL = site_info(pwvinfo[0],siteTable)
            if LL == None:
                pass
            else:
                # 将PWV数据录入sitepwv
                sitepwvindex = np.where(siteTable == pwvinfo[0])
                if sitepwvindex[0].size != 0:
                    rawindex = sitepwvindex[0][0]
                    if pwvinfo[1][11:13] == '15':
                        sitepwv[rawindex][filenum*2+1] = pwvinfo[3]
                        sitepwverr[rawindex][filenum * 2 + 1] = pwvinfo[4]
                    if pwvinfo[1][11:13] == '45':
                        sitepwv[rawindex][filenum*2+2] = pwvinfo[3]
                        sitepwverr[rawindex][filenum * 2 + 1] = pwvinfo[4]
                fout.write(str(format(float(LL[1]), '20.5f')) + #Header
                           str(format(float(LL[0]), '20.5f')) +
                           ' '*40 +
                           fin[i][0]+' '*36 +
                           'FM-111'+' '*34 +
                           ' '*40+str(format(float(LL[2]), '20.5f')) +
                           str(format(0,'10d'))*10+
                           ' '*6+pwvinfo[1][0:8]+pwvinfo[1][9:13]+'00'+ # Date
                           HeaderInVaildStr*13+
                           # PW
                           str(format(float(pwvinfo[3]), '13.5f')) +str(format(0, '7d'))+
                           HeaderInVaildStr+'\n'+
                           # Data
                           str(format(float(pwvinfo[9])*100, '13.5f'))+str(format(0, '7d')) + # Pressure
                           str(format(float(LL[2]), '13.5f'))+str(format(0, '7d')) + # Height
                           str(format(float(pwvinfo[10])+TEM_K, '13.5f'))+str(format(0, '7d')) + # Temperature
                           DataInVaildStr * 7 + '\n' +
                           # EndingRecord + TailIntegers
                           EndingRecordStr + '\n' +
                           TailIntegers + '\n'
                           )
        fout.close()
        filenum = filenum + 1

    # np.savetxt(path+"\\sitepwvtimeordered.txt" ,sitepwv, delimiter=',')
    with open(path+'\\sitepwvtimeordered.txt', 'w') as fp:
        for i in range(siteTable.shape[0]):
            #fp.write(sitepwv[i][0]+'\t')
            for j in range(len(path_list_pwv)*2+1):
                fp.write(sitepwv[i][j]+',')
            fp.write('\n')
    with open(path+'\\sitepwverrtimeordered.txt', 'w') as fp:
        for i in range(siteTable.shape[0]):
            for j in range(len(path_list_pwv)*2+1):
                fp.write(sitepwverr[i][j]+',')
            fp.write('\n')








def ztd_to_little_r(path,siteTable):
    path_list_all = os.listdir(path)
    path_list_ztd = []
    for each in path_list_all:
        if os.path.splitext(each)[1] == ".PWV":
            path_list_ztd.append(each)
    # ---------------------------- PWV format ----------------------------------
    # Site PWVmidTim    Duration PW   FMerr Wdelay Mdelay Tdelay  KFAC  Press  Temp  Rhum Ddelay Mf Kf
    # SSSS YYYMMDD/HHMM   MIN   [mm]   [mm]  [mm]  [mm]   [mm]   d.ddd  [mbar]  [c]   [%]   [mm]  C C

    # ---------------------------- LITTLE_R format ------------------------------
    # Lat.	Lon.	ID	Name	Platform	Source	Elevation	Valid fields	Num. errors	Num. warn.	Seq. number	Num. dup.	sound	bogus	Discard?	Unix time	Jul. day	Date	SLP, QC	Ref Pres., QC	Ground Temp, QC	SST, QC	SFC Pres, QC	Precip, QC	Dly Max T, QC	Dly Min T, QC	Ngt Min T, QC	3hr Pres Chg, QC	24hr Pres Chg, QC	Cld cvr, QC	Ceil, QC	Zenith Total Delay, QC
    # Pressure (Pa)	QC	Height (m)	QC	Temperature (K)	QC	Dew point (K)	QC	Wind speed (m/s)	QC	Wind direction (deg)	QC	Wind U (m/s)	QC	Wind V (m/s)	QC	Relative humidity (%)	QC	Thickness (m)	QC
    # Lat Lon Platform 日期字串 是必选项
    # 顺便整理一下质量控制所需要的数据
    siteztdlist = [([0] * (len(path_list_ztd) * 2 + 1)) for i in range(siteTable.shape[0])]
    siteztderrlist = [([0] * (len(path_list_ztd) * 2 + 1)) for i in range(siteTable.shape[0])]
    for i in range(siteTable.shape[0]):
        siteztdlist[i][0] = siteTable[i][3]
        siteztderrlist[i][0] = siteTable[i][3]
    siteztd = np.array(siteztdlist)
    siteztderr = np.array(siteztderrlist)
    # s =    np.array(shape=(siteTable.shape[0], len(path_list_pwv)), dtype=str)
    filenum = 0
    for each in path_list_ztd:
        fin = load_ztd(path + '\\' + each)
        fout = open(path + '\\' + os.path.splitext(each)[0] + '.out', 'w')

        # outline = np.zeros(shape=(1,52))
        # for i in range(fin.shape[0]):
        #     # pwvinfo = fin[i]
        #     # LL = site_info(pwvinfo[0], siteTable)
        #     if LL == None:
        #         pass
        #     else:
        #         # 将PWV数据录入sitepwv
        #         siteztdindex = np.where(siteTable == pwvinfo[0])
        #         if siteztdindex[0].size != 0:
        #             rawindex = siteztdindex[0][0]
        #             if pwvinfo[1][11:13] == '15':
        #                 pass
        #             if pwvinfo[1][11:13] == '45':
        #                 pass
        fout.write(' \n')
        fout.close()
        filenum = filenum + 1

    # np.savetxt(path+"\\sitepwvtimeordered.txt" ,sitepwv, delimiter=',')
    with open(path + '\\siteztdtimeordered.txt', 'w') as fp:
        for i in range(siteTable.shape[0]):
            # fp.write(sitepwv[i][0]+'\t')
            for j in range(len(path_list_ztd) * 2 + 1):
                fp.write(siteztd[i][j] + ',')
            fp.write('\n')
    with open(path + '\\siteztderrtimeordered.txt', 'w') as fp:
        for i in range(siteTable.shape[0]):
            for j in range(len(path_list_ztd) * 2 + 1):
                fp.write(siteztderr[i][j] + ',')
            fp.write('\n')


def load_PWV(pwvfilepath):
    f = open(pwvfilepath, 'r')
    i = 0
    reTable = []
    for line in islice(f, 2, None):
        reTable.append(re.split(r'[ ]+', line))
    return np.array(reTable)

def load_ztd(ztdfilepath):
    f= open(ztdfilepath, 'r')
    i = 0
    reTable =[]
    for line in islice(f, 1, None):
        reTable.append(re.split(r'[ ]+', line))
    return np.array(reTable)
