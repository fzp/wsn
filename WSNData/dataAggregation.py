__author__ = 'fangzhenpeng'

import pickle
from formatData import formatData
def addLink(router,son,father):
    if router.has_key(son) and router[son][0] == father:
        router[son][1]+=1
    else:
        router[son] = [father,1]

def getC1():
    fileBase = 'C1-60001-2011-08-'
    dateList = ['03']
    format = (('timeStamp','string'),('type','string'),('sID','int'),('sinkID','int'),
              ('parentID','int'),('humidity','int'),('temperature','int'),('light','int'),('path',(None,'int')))
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
        routerTable[timeStamp][log['sID']]['temperature'] = round(log['temperature']*0.01 - 40,2)
        routerTable[timeStamp][log['sID']]['humidity'] = round((routerTable[timeStamp][log['sID']]['temperature']-25)
                                                               *(0.01+0.00008*log['humidity'])- 4 + 0.0405*log['humidity'] \
                                                               - 0.0000028*log['humidity']*log['humidity'],2)
        if log['pathSize'] > 0:
            addLink(routerTable[timeStamp]['router'],log['sID'],log['parentID'])
            for i in range(len(log['path'])-1):
                addLink(routerTable[timeStamp]['router'],log['path'][i],log['path'][i+1])
    return  routerTable

def getC1FromFile():
    file = open('./WSNData/03')
    c1 = file.read()
    c1 = pickle.loads(c1)
    file.close()
    return c1

routerTable = getC1FromFile()

if __name__ == "__main__":
    #file = open('03','w')
    #file.write(pickle.dumps(getC1()))
    #file.close()

    #print getC1()[1312301400]
    print getC1FromFile()[1312301400]