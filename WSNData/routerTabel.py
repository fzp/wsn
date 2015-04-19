__author__ = 'fangzhenpeng'

from formatData import formatData

nodes = {}
fd = formatData()
nodeList = fd.getRawData("1000-2000-baidu.txt")
for entry in nodeList:
    nodes[entry[0]] = entry

fileBase = 'C2-60001-2011-08-'
dateList = ['03']
format = (('timeStamp','string'),('type','string'),('sID','int'),('sinkID','int'),
          ('parentID','int'),('neighbor',(('ID','int'),('RSSI','int'),('ETX','float'))))

routerLog = {}
for date in dateList:
    routerLog[date] = fd.getFormatData(format,fileBase+date+'.txt',' ')

lastTime = '2011:08:03:00:00:'
routerTable = {lastTime:{}}
for log in routerLog['03']:
    sec = log['timeStamp'][0:17]
    if sec not in routerTable:
        routerTable[sec] = routerTable[lastTime]
    for i in range(log['neighborSize']-1):
        routerTable[sec][log['neighbor'][i]['ID']] = log['neighbor'][i+1]['ID']

if __name__ == "__main__":
    #print nodes
    print routerLog['03'][0]
    print routerTable['2011:08:03:06:14:']
    print len(routerTable['2011:08:03:06:14:'])