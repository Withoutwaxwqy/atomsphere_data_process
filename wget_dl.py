import os
# 此函数废弃，功能包含于类 Hurricane里
#调用wget.exe,利用urllist.exe进行下载(不使用)

def pwv_url_gen(url_dir, urllistpath, DOY_s:int, DOY_e:int, interval = 'hourly'):
    '''
    生成urllist.txt来提供给wget
    :param url_dir:
    :param urllistpath:
    :param DOY_s:
    :param DOY_e:
    :param interval:
    :return:NotImplemented
    '''
    with open(urllistpath) as f:
        for i in range(DOY_s,DOY_e):
            for j in range(24):
                pass #TODO
    return 0

def wget_run(urltxtpath, wgetpath):

    return 0