__author__ = 'jin-yc10'

from formatData import formatData

dateList = ['03', '04', '05']
fileBase = 'C1-60001-2011-08-'
receptionDict = {} # reception[date][hour][minute] = [data]
receptionMeta = {}
print 'Loading C1 data...'
fd = formatData()
for date in dateList:
    receptionDict[int(date)] = {}
    receptionMeta[int(date)] = {}
    # 2011:08:03:00:00:05:687: C1  1273 60001  1277  2947  6625     3     6  1277  1269  1272  1348  1375  1182     0     0     0     0
    c1 = fd.getRawData(fileBase+date+'.txt', deli=" ")
    for d in c1:
        (y,m,da,h,mi,sec,us) = fd.getDate(d[0])
        # print y, m, da, h, mi, sec, us
        if(not receptionDict[da].has_key(h)):
            receptionDict[da][h] = {}
            receptionMeta[da][h] = {}
        if(not receptionDict[da][h].has_key(mi)):
            receptionDict[da][h][mi] = []
        receptionDict[da][h][mi].append(d) # fastest
print 'Loading C1 data done'
# print receptionDict
for d in receptionDict:
    hs = receptionDict[d].keys()
    for h in sorted(hs):
        ms = receptionDict[d][h].keys()
        for m in sorted(ms):
            receptionMeta[d][h][m] = len(receptionDict[d][h][m])

if __name__ == '__main__':
    for d in receptionDict:
        for h in receptionDict[d]:
            print d, h
            ms = receptionDict[d][h].keys()
            for m in sorted(ms):
                print d, h, m, len(receptionDict[d][h][m])