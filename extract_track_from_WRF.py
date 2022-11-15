# -*- encoding: utf-8 -*-
'''
@File    :   extract_track_from_WRF.py.py
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author    @Version    @Desciption
------------       -------     --------    -----------
2021/10/20 11:39   WangQiuyi      1.0         None
'''


import numpy as np
import netCDF4 as nc
import datetime
from wrf import getvar, ALL_TIMES, to_np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import pandas as pd

def nearest_position( stn_lat, stn_lon, lat2d, lon2d):
    """获取最临近格点坐标索引
    stn_lat  : 站点纬度
    stn_lon  : 站点经度
    lat2d    : numpy.ndarray网格二维经度坐标
    lon2d    : numpy.ndarray网格二维纬度坐标
    Return: y_index, x_index
    """
    difflat = stn_lat - lat2d;
    difflon = stn_lon - lon2d;
    rad = np.multiply(difflat,difflat)+np.multiply(difflon , difflon)
    aa=np.where(rad==np.min(rad))
    ind=np.squeeze(np.array(aa))
    return tuple(ind)

if __name__  == "__main__":
    # setting
    wrfout_dir  = r"F:\WRF\Michael_V1\VAR1_06h\2018101112\wrf\wrfout_d01_2018-10-11_12_00_00.nc"
    lonTC0, latTC0 = -85.4, 30.2
    wrfout      = nc.Dataset(wrfout_dir, mode="r")
    lat2D       = to_np(getvar(wrfout, "lat"  ))  # units: decimal degrees
    lon2D       = to_np(getvar(wrfout, "lon"  ))  # units: decimal degrees
    times       = to_np(getvar(wrfout, "times", timeidx=ALL_TIMES))  #
    nt = len(times)
    ny, nx = np.shape(lat2D)

    date0 = datetime.datetime.strptime(str(times[0])[0:19], "%Y-%m-%dT%H:%M:%S")
    date1 = datetime.datetime.strptime(str(times[1])[0:19], "%Y-%m-%dT%H:%M:%S")
    history_interval = (date1 - date0).total_seconds()/3600  #hours

    lonMax = np.max(lon2D)
    lonMin = np.min(lon2D)
    latMax = np.max(lat2D)
    latMin = np.min(lat2D)

    date = [] # 2020-07-20T00
    lons = [] # degree
    lats = [] # degree
    pmin = [] # hPa
    vmax = [] # m/s

    lonTC = lonTC0
    latTC = latTC0

    for it in range(nt):
        slp         = to_np(getvar(wrfout ,"slp"         ,units="hPa"   ,timeidx=it))
        wspd_wdir10 = to_np(getvar(wrfout ,"wspd_wdir10" ,units="m s-1" ,timeidx=it))
        wspd10      = wspd_wdir10[0]

        if it==0 :
            # 如果给定了初始时刻的TC位置，则使用给定的TC位置
            # 未给定初始时刻TC位置，则取全场slp最小的位置为TC中心
            if latTC0 > -60.0 :
                latTC = latTC0
                lonTC = lonTC0
                #lons.append(round(lonTC,2))
                #lats.append(round(latTC,2))
                #continue
            else:
                slpMin = np.min(slp[:,:])
                indexMin = np.argwhere(slp[:,:] == slpMin)
                jTC = indexMin[0][0]
                iTC = indexMin[0][1]
                lonTC = lon2D[jTC,iTC]
                latTC = lat2D[jTC,iTC]

        ### 1 找到TC中心(lonTC, latTC)的索引(iTC, jTC)
        indexTC = nearest_position(latTC, lonTC, lat2D, lon2D)
        jTC = indexTC[0]
        iTC = indexTC[1]
        # 避免台风中心选在边界点
        jTC = np.max((1,jTC))    # jTC [1,ny-2]
        jTC = np.min((jTC,ny-2))
        iTC = np.max((1,iTC))    # iTC [1,nx-2]
        iTC = np.min((iTC,nx-2))

        ### 2 计算TC center附近的网格分辨率dAvg，
        dLat = lat2D[jTC+1,iTC] - lat2D[jTC,iTC]
        dLon = lon2D[jTC,iTC+1] - lon2D[jTC,iTC]
        dAvg = (dLat + dLon)/2.0

        ### 3 根据移速计算台风中心最大可能半径，根据这个
        if latTC < 30.0 : # 纬度30°以南，台风移速每小时0.5°
           radius = 0.5*history_interval  # 0.5 degree/hour
        else:             # 纬度30°以北，台风移速每小时1.0°
           radius = 1.0*history_interval  # 1.0 degree/hour
           radius = 0.5*history_interval  # 0.5 degree/hour
        radius = 1.0*history_interval  # 1.0 degree/hour
        if it==0 :
           radius = 0.5
        indexRadius = int(radius/dAvg) + 1

        ### 找到最大可能半径内，slp最小值及其位置索引
        iStart = iTC - indexRadius
        iEnd   = iTC + indexRadius
        jStart = jTC - indexRadius
        jEnd   = jTC + indexRadius
        jStart = np.max((1,jStart))
        jEnd   = np.min((jEnd,ny-2))
        iStart = np.max((1,iStart))
        iEnd   = np.min((iEnd,nx-2))

        slpMin = np.min(slp[jStart:jEnd,iStart:iEnd])
        w10Max = np.max(wspd10[jStart:jEnd,iStart:iEnd])
        indexMin = np.argwhere(slp[jStart:jEnd,iStart:iEnd] == slpMin)
        jTC = indexMin[0][0] + jStart
        iTC = indexMin[0][1] + iStart
        lonTC = lon2D[jTC,iTC]
        latTC = lat2D[jTC,iTC]
        print("date:", str(times[it])[0:19],"TC center:",round(lonTC,2), round(latTC,2)," p min:",round(slpMin,2), " vmax:",round(w10Max,2))
        date.append(str(times[it])[0:19])
        lons.append(round(lonTC,2))
        lats.append(round(latTC,2))
        pmin.append(round(slpMin,2))
        vmax.append(round(w10Max,2))

    #read CMA-STI best track
    f_Con = 'cma_bst_hato.txt'
    col_names =['date','grade','lat', 'lon', 'pres', 'vmax']
    widths = [10,2,4,5,4,3]
    df = pd.read_fwf(f_Con,usecols=[0,1,2,3,4,5],widths=widths,names=col_names)
    latObs  = df['lat'].values[:]
    lonObs  = df['lon'].values[:]
    latObs  = np.array(latObs)/10
    lonObs  = np.array(lonObs)/10

    ### plot track
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([lonMin, lonMax, latMin, latMax],crs=ccrs.PlateCarree())
    xticks = np.linspace(lonMin, lonMax, 6, endpoint=True)
    yticks = np.linspace(latMin, latMax, 6, endpoint=True)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.gridlines()
    ax.coastlines()
    for it in range(1,len(lons)):
        if it == 1:
           plt.plot((lons[it-1],lons[it]), (lats[it-1],lats[it]),color='red',linewidth=1.5,transform=ccrs.PlateCarree(), label="wrf")
        else:
           plt.plot((lons[it-1],lons[it]), (lats[it-1],lats[it]),color='red',linewidth=1.5,transform=ccrs.PlateCarree())
    for it in range(1,len(lonObs)):
        if it == 1:
            plt.plot((lonObs[it-1],lon   Obs[it]), (latObs[it-1],latObs[it]),color='black',linewidth=2,transform=ccrs.PlateCarree(), label="obs")
        else:
            plt.plot((lonObs[it-1],lonObs[it]), (latObs[it-1],latObs[it]),color='black',linewidth=2,transform=ccrs.PlateCarree())
    plt.legend()
    plt.show()