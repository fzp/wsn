__author__ = 'fangzhenpeng'

import csv
import os

class formatData:
    def getDate(self,dateStr):
        date = dateStr.split(':')
        return (int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),int(date[5]),int(date[6]))

    def getRawDate(self,fileName,deli):
        file = open(os.path.join(os.path.dirname(__file__), fileName),"r")
        cr = csv.reader(file, delimiter = deli)
        rawDate = []
        for entry in cr:
            rawDate.append(filter(None,entry))
        file.close()
        return rawDate

if __name__ == '__main__':
    fd = formatData()
    date = fd.getRawDate('C1-60001-2011-08-03.txt', ' ')
    print date
