import pandas as pd
import pdfplumber
from io import StringIO
import numpy as np



class HourlyPrecip:
    def __init__(self,file,FileType,DataSource):
        # pdf/csv/text...
        self.ft = FileType
        # LCD ....
        self.ds = DataSource
        self.file = file
    def ReadPDFHeader(self,text):
        StrText = StringIO(text)
        StaInfo = []
        while True:
            line = StrText.readline()
            ls = line.split()
            if ls[0] == 'Current' and ls[1] == 'Location:':
                elv = float(ls[3]) * 0.3048 # conver ft. to m
                lat = float(ls[6][:-1])
                lon = float(ls[9][:-1])
                StaInfo.append(lat)
                StaInfo.append(lon)
                StaInfo.append(elv)
            elif ls[0] == 'Station:':
                StaID = line.split("(")
                if len(StaID) == 1:
                    line = StrText.readline()
                    StaID = line.split("(")
                StaInfo.append(StaID[1][0:4])
                break
        return StaInfo
    def FilterList(self,line):
        NewLine = []
        for i in range(len(line)):
            if line[i] != None:
                if line[i] == '':
                    precip = 0
                elif line[i] == 'T':
                    precip = 0.001
                elif line[i] == 'M':
                    precip = None
                else:
                    if line[i].find('s') > -1:
                        precip = float(line[i][:-1])
                    elif line[i].find('*') > -1:
                        precip = None
                    else:
                        precip = float(line[i])
                NewLine.append(precip)
        return NewLine

    def ReadPDFTable(self,table):
        record_list = table[0]
        NewList = []
        for line in record_list[2:]:
            if line[0] == 'Maximum Short Duration Precipitation':
                break
            NewLine = self.FilterList(line[0:34])
            NewList.append(NewLine)
        return NewList
    def ReadPDFFile(self):
        path = self.file.split('.')[0]
        # savepdf = np.zeros(2, dtype=[('staInfo',"f4",(1,4)),('data','f4',(30,25))])
        with open(path+'siteInfo.txt', 'w') as f1:
            with open(path+'Date.txt', 'w') as f2:
                with pdfplumber.open(self.file) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        table = page.extract_tables()
                        HeadData = self.ReadPDFHeader(text)
                        TableData = self.ReadPDFTable(table)
                        if TableData == [] or TableData.shape[0] < 30 or TableData.shape[1] < 25:
                            continue
                        else:
                            # 当有数据的时候才进行读数据
                            for item in HeadData:
                                f1.write(str(item)+'\t')
                            f1.write('\n')

                            for i in range(30):
                                for j in range(25):
                                    f2.write(str(TableData[i][j])+'\t')
                                f2.write('\n')

        

        


        
        pass