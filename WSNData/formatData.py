__author__ = 'fangzhenpeng'

import csv
import os
import types

class formatData:
    changeType = {
        'int':lambda x:int(x),
        'float':lambda x:float(x),
        'string':lambda x:x,
    }

    #日期格式化
    def getDate(self,dateStr):
        date = dateStr.split(':')
        return (int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),int(date[5]),int(date[6]))

    #按行获取数组，每行用列表方式组织数据
    def getRawData(self,fileName,deli):
        file = open(os.path.join(os.path.dirname(__file__), fileName),"r")
        cr = csv.reader(file, delimiter = deli)
        rawDate = []
        for entry in cr:
            rawDate.append(filter(None,entry))
        file.close()
        return rawDate

    #用于获取格式化数据
    #此方法可以递归实现，适用范围更广
    def getFormatData(self,format,fileName,deli):
        rawData = self.getRawData(fileName,deli)
        structuredDate = []
        for rawEntry in rawData:
            index = 0
            entry = {}
            for key,value in format:
                dataType = type(value)
                if(dataType == types.StringType):
                    entry[key] = self.changeType[value](rawEntry[index])
                    index+=1
                elif(dataType == types.TupleType):
                    keySize = key+'Size'
                    entry[keySize] = int(rawEntry[index])
                    index+=1
                    entry[key] = []
                    for j in range(entry[keySize]):
                        subEntry = {}
                        for subKey,subType in value:
                            subEntry[subKey]=self.changeType[subType](rawEntry[index])
                            index+=1
                        entry[key].append(subEntry)
            structuredDate.append(entry)
        return structuredDate

if __name__ == '__main__':
    fd = formatData()
    format = (('timeStamp','string'),('type','string'),('sID','int'),('sinkID','int'),('parentID','int'),('neighbor',(('ID','int'),('RSSI','int'),('ETX','float'))))
    date = fd.getFormatData(format,'C2-60001-2011-08-03.txt', ' ')
    print date[0]
