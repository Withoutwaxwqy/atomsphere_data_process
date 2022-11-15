# -*- encoding: utf-8 -*-
'''
@File    :   transform_littleR.py.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author    @Version    @Desciption
------------       -------     --------    -----------
2021/11/19 22:30   WangQiuyi      1.0         None
'''
import fortranformat as ff

def format_gtrop(**kwargs):

    kwargs.setdefault('kx',1)
    kwargs.setdefault('id',' ')
    kwargs.setdefault('platform', 'FM-114 GPSZTD')
    kwargs.setdefault('source', 'GREAT')
    kwargs.setdefault('is_sound', 'F')
    kwargs.setdefault('is_bogus', 'F')
    kwargs.setdefault('is_discard', 'F')
    kwargs.setdefault('valid_field', 6)
    kx = kwargs.get('kx')
    lat = kwargs.get('lat')
    lon = kwargs.get('lon')
    site_name = kwargs.get('site_name').ljust(40)
    id = kwargs.get('id').ljust(40)
    platform = kwargs.get('platform').ljust(40)
    source = kwargs.get('source').ljust(40)
    elv = kwargs.get('elv')
    valid_field = kwargs.get('valid_field')
    is_sound = kwargs.get('is_sound')
    is_bogus = kwargs.get('is_bogus')
    is_discard = kwargs.get('is_disgard')
    date = kwargs.get('date')
    trop = kwargs.get('trop')
    trop_qc = kwargs.get('trop_qc')

    gtrop = {'header':'', 'end':'','tail':''}
    gtrop['header'] = [lat, lon, id, site_name, platform, source, elv, 1, 0,0,0,0, is_sound, is_bogus, is_discard,
                      -888888, -888888, date, -888888.,0,-888888.,0, -888888.,0, -888888.,0, -888888.,
                      0,-888888.,0, -888888.,0, -888888.,0, -888888.,0, -888888.,0,-888888.,0, -888888.,0,
                      -888888.,0, trop, trop_qc]
    gtrop['end'] = [-777777.,0, -777777.,0, -888888.,0, -888888.,0, -888888.,0, -888888.,0,
                     -888888.,0, -888888.,0, -888888.,0, -888888.,0]
    gtrop['tail'] = [kx, 0, 0]

    return gtrop

def write_gtrop_littler(gtrop_formatter):
    header_fortmat = '( 2f20.5 , 2a40 , 2a40 , 1f20.5 , 5i10 , 3L10 , 2i10 , a20 ,  14( f13.5 , i7 ) )'
    data_format = '( 10( f13.5 , i7 ) )'
    end_format = '( 3 ( i7 ) )'
    hearder_writer = ff.FortranRecordWriter(header_fortmat)
    data_writer = ff.FortranRecordWriter(data_format)
    end_writer = ff.FortranRecordWriter(end_format)
    header = hearder_writer.write(gtrop_formatter['header'])
    data = data_writer.write(gtrop_formatter['end'])
    end = end_writer.write(gtrop_formatter['tail'])
    return header, data, end

gtrop_formatter = format_gtrop(lat=29.0,lon=112.1,elv=500.,site_name='ABCD',date='20080205114500',trop=210.1,trop_qc=120)

header, end, tail = write_gtrop_littler(gtrop_formatter)
file_handle=open(r'I:\hubei\hubei_new\test',mode='a+')
file_handle.write(header)
file_handle.write('\r\n')
file_handle.write(end)
file_handle.write('\r\n')
file_handle.write(tail)
file_handle.write('\r\n')
file_handle.close()