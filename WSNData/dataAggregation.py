__author__ = 'fangzhenpeng'

from formatData import formatData

def getC1():
    getEnvironment={
        'humidity':lambda x:x,
        'temperature':lambda x:x,
        'light':lambda x:x,
    }

    fileBase = 'C1-60001-2011-08-'
    dateList = ['03']
    format = (('timeStamp','string'),('type','string'),('sID','int'),('sinkID','int'),
              ('parentID','int'),('humidity','int'),('temperature','int'),('light','int'),('path',(None,'int')))
    environment = ('humidity','temperature','light')
    fd = formatData()
    routerLog = {}
    for date in dateList:
        routerLog[date] = fd.getFormatData(format,fileBase+date+'.txt',' ')

    startTime = '2011:08:03:00:00:00'
    lastTimeStamp = int(fd.getTimeStamp(startTime))
    endTime = lastTimeStamp + 86400
    interval = 600
    routerTable = {}
    for i in range(lastTimeStamp,endTime,interval):
        routerTable[i] = {'router':{}}

    offset = 60
    nextTimeStamp = lastTimeStamp + interval
    nextTimeStampOffset = nextTimeStamp + offset
    for log in routerLog['03']:
        now = fd.getTimeStamp(log['timeStamp'][0:19])
        timeStamp = lastTimeStamp
        if now > nextTimeStampOffset:
            lastTimeStamp = nextTimeStamp
            nextTimeStamp += interval
            nextTimeStampOffset += interval
            timeStamp = lastTimeStamp
        elif now > nextTimeStamp:
            if routerTable[lastTimeStamp].has_key(log['sID']):
                timeStamp = nextTimeStamp
        routerTable[timeStamp][log['sID']] = {}
        for type in environment:
            routerTable[timeStamp][log['sID']][type] = getEnvironment[type](log[type])
        if log['pathSize'] > 0:
            routerTable[timeStamp]['router'][log['sID']] = log['parentID']
            for i in range(len(log['path'])-1):
                routerTable[timeStamp]['router'][log['path'][i]] = log['path'][i+1]
    return  routerTable

if __name__ == "__main__":
    print getC1()[1312301400]
