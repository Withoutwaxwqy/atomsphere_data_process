import os
import numpy as np
from pwv_to_littleR import *
from siteprocess import *
from rawurlgener import pwv_raw_urllist_gen
from itertools import islice
from pw_plot import *
# from echartsplot import draw_usa_map1
from Hurricane import Hurricane
from pw_plot import *
import datetime as dt

from PDFconvert import HourlyPrecip
# import HDF5_process as hp


if __name__ == "__main__":
    #
    # 测站信息txt 录入
    site = np.loadtxt('D:\\acdemic\\毕业论文\\PWVDATA\\NorthAmericanSiteCoordinate.txt', str)

    # V_0.1 使用台风Gordon但是效果一般， 所以换成
    # pw_and_error_plot(site, site_avail, site_pwv_matrix_path, site_pwverr_matrix_path)
    #----------------------------------------------------------------------------------------------------
    # 初始化台风类
    # Gordon = Hurricane("Gordon", "AL072018", 2018, (245,251),((15.00, -100.00),(45.00, -77.00)), site, isdataexist=True, pwvinterval='hourly')
    # # Gordon.Hurrican_data_dl()
    # Gordon.pwv2littleR()
    #
    # # site_write_for_pyecharts_add(Gordon.site_a, Gordon.pc_dir+"add.txt")
    # Gordon.site_QC1()
    # Gordon.hurricane_track_plot()
    # 
    # 
    # Gordon.plot3(['CN16','FLC6','AL90','MSME','MSOX'],[5,14,12,13,9])
    # Gordon.func2()
    # # Gordon.hurricane_track_plot()
    # # 选择的五个时期的不同测站初步确定为
    # site1 = ['CN16', 'FLC6', 'AL90', 'MCD6', 'MSME', 'MSOX']
    # site2 = ['CN16', 'CCV6', 'CNC0', 'AL50', 'ALTA', 'MSOX']
    # # 但是上述测站选择画出来的图效果并不是很好， 因此决定缩短时间窗
    # # site1= ['BVHS', 'AL90', '1LSU', 'MSME', 'MSOX']
    # single_site_pwv_plot(Gordon)
    # series_site_pwv_plot(Gordon, site2)
    # # Gordon.plot_pwv()
    # Gordon.interpolate_2d_plot(0)

    # --------------------------------------------------------------------------------------------------
    # 读取同化的AMSR2 H5格式的数据
    # hp.AMSR_reader("D:\\acdemic\\毕业论文\\PWVDATA\\hurricane_Gordon_PWV_Hour\\amsr2\\")




    # rpdf = HourlyPrecip(Gordon.pc_dir+"探空降水量\\2562092.pdf", None, None)
    # rpdf.ReadPDFFile()


    #------------------------------------------------------------------------------------------------------
    # pwv 空间差值图
    # Gordon.zyx_interp()
    # 先画第一天的


    # TODO List
    # 1 ASMR数据下载绘图（pwv） ()
    # 2 pwv沿着路径站点选点（趋势） (1)
    # 3 pwv空间差值图 (1)
    # 4 ECMWF 分析对比 ()
    # 5 统计QC前后统计量 （比较简单） ()
    # 6 数据同化 ()

    # Gordon.plot_eharts()
    # Gordon.site_QC1()
    # 实验了几个不同的台风，效果都一般
    # Florence = Hurricane("Florence" , 2018, (256,260), ((31.5,-73.2),(41.3,-85)), site,
    #                      isdataexist=True,
    #                      pwvinterval="hourly"
    #                      )
    # Florence.Hurrican_data_dl()
    # Florence.pwv2littleR()
    # Florence.plot_pwv()

    # Delta = Hurricane("Delta", 2020, (282,286),((25,-80.0),(35,-95)),site,
    #                   isdataexist=False,
    #                   pwvinterval="hourly")
    # Delta.Hurrican_data_dl()
    # Delta.pwv2littleR()
    # Delta.plot_pwv()

    # v_0.2 还是是使用Micheal
    Ida_duration  = (dt.date(2021, 8, 27), dt.date(2018, 9, 1))
    Ida_duration_DOY = (int(dt.datetime.strftime(Ida_duration[0],'%j')),
                        int(dt.datetime.strftime(Ida_duration[1],'%j')))
    # Micheal = Hurricane('MichealPro', "AL142018", 2018, Micheal_duration_DOY,((15,-100),(45,-70)),site,
    #                     isdataexist=True)
    Ida = Hurricane('Ida', "AL092021", 2021, Ida_duration_DOY, ((10, -130), (60, -60)), site,
                       isdataexist=True)
    #Ida.Hurrican_data_dl()
    # Ida.pwv2littleR()
    #
    # site1 = []
    # series_site_pwv_plot(Micheal, site1)
    #
    Ida.site_QC1()
    single_site_pwv_plot(Ida)
    # Ida.plot2()
    # # Ida.hurricane_track_plot()
    # Ida.plot_pwv()
    # rpdf = HourlyPrecip(Micheal.pc_dir + "NCEI precipitation\\2757793.pdf", None, None)
    # rpdf.ReadPDFFile()
    # Micheal.hurricane_track_plot()
    # Micheal.plot_pwv()
    # Micheal.interpolate_2d_plot()
    # for i in range(4):
    #     Micheal.interpolate_2d_plot(i)
    #
    # site1 = ['GRIS', 'BVHS', 'AL90', 'ALTA', 'AL60', 'NCRD']
    # series_site_pwv_plot(Micheal, site1)
    # plot_many_site_in_one_fig(Micheal, site1)
    # ['DUNN'
    # '1ULM','CN13', 'CN12', 'CN14','AL90', 'BARA', 'BRTM', 'BVHS', 'COVG','GRIS','HAMM',
    #
    # 'GNVL','CRST']
    # single_site_pwv_plot(Micheal)
    # Micheal.hurricane_track_plot()
    # Alberto = Hurricane("Alberto", 2018)
    print('\n-----------------------Done---------------------------')

