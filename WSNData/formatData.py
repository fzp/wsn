__author__ = 'fangzhenpeng'

import csv
import os
import types
import time

class formatData:
    changeType = {
        'int':lambda x:int(x),
        'float':lambda x:float(x),
        'string':lambda x:x,
    }

    #date format
    def getDate(self,dateStr):
        date = dateStr.split(':')
        return (int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),int(date[5]),int(date[6]))

    #get timeStamp
    def getTimeStamp(self,dateStr):
        return time.mktime(time.strptime(dateStr[0:19],'%Y:%m:%d:%H:%M:%S'))

    #get date row by row,save in list
    def getRawData(self,fileName,deli = ","):
        file = open(os.path.join(os.path.dirname(__file__), fileName),"r")
        cr = csv.reader(file, delimiter = deli)
        rawDate = []
        for entry in cr:
            rawDate.append(filter(None,entry))
        file.close()
        return rawDate

    #get format data
    def getFormatData(self,format,fileName,deli = ","):
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
                    if entry[keySize] > 10:
                        jRange = 10
                    else:
                        jRange = entry[keySize]
                    for j in range(jRange):
                        if value[0] == None:
                            subEntry = self.changeType[value[1]](rawEntry[index])
                            index+=1
                        else:
                            subEntry = {}
                            if type(value[0]) != types.TupleType:
                                subEntry[value[0]]=self.changeType[value[1]](rawEntry[index])
                                index+=1
                            else:
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
    print fd.getTimeStamp(date[0]['timeStamp'])
