# -*- encoding: utf-8 -*-
'''
@File    :   test.py.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author    @Version    @Desciption
------------       -------     --------    -----------
2022/1/7 10:56   WangQiuyi      1.0         None
'''
import pandas as pd
import numpy as np
def statics_gird(f):
    p = pd.read_csv(f)
    lon = np.arange(0, 260, 5)
    lat = np.arange(0, 60, 5)
    plon = p['CPT_lon'] + 180
    plat = p['CPT_lat'] + 30
    norm1lon =

    s = 1

def main():
    f = r'D:\RISHANA_2007_1qcCTP.csv'
    statics_gird(f)
if __name__ == '__main__':
    main()
