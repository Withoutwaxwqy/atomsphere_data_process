
# 此函数废弃，功能包含于类 Hurricane里
def pwv_raw_urllist_gen(sitelist, st, et, urllistpath):
    '''
    根据测站和时间生成wget下载pwv原始观测文件所需要的urllist.txt
    下载网站 http://facility.unavco.org/
    url example:
                http:
                1  http://facility.unavco.org/data/gps-gnss/data-access-methods/dai1/get_data.php?pview=original&code=1LSU&start=20181006&end=20181015&display=1
                2  http://facility.unavco.org/data/gps-gnss/data-access-methods/dai1/download/214722/1lsu.zip
                ftp:
                1  ftp://data-out.unavco.org/pub/rinex/obs
                2  http://data-out.unavco.org/pub/rinex/obs/2018/001/1lsu0010.18d.Z
    args:
        :param sitelist:    测站列表
                ! type of sitelist: array(shape=(n,2), dtype='|i4, object')
        :param st:          start time (type : tuple, shape= (1:2), format:(yyyy,ddd) ddd为年积日
        :param et:          end   time 规范同上
        :param urllistpath :urllist.txt文件的路径
    :return: None
    TODO: 本程序只能用于一年内连续数据数据的下载， 跨年的数据下载还需要进一步完善
    '''
    raw_dir_list = "ftp://data-out.unavco.org/pub/rinex/obs/2018"
    days = range(st[1],et[1]+1)
    with open(urllistpath, 'w') as f:
        for eachsite in sitelist:
            for eachday in days:
                outline = "{}/{}/{}{}0.18d.Z\n".format(raw_dir_list, str(eachday).zfill(3), eachsite[1].lower(), str(eachday).zfill(3))
                f.write(outline)
    return 0

