__author__ = 'jin-yc10'

from WSNData.receptionRatio import receptionDict, receptionMeta
from dateutil import rrule
from datetime import datetime, timedelta

s = "2011-08-03 00-00-00"
e = "2011-08-05 23-59-59"
st = datetime.strptime(s, '%Y-%m-%d %H-%M-%S')
et = datetime.strptime(e, '%Y-%m-%d %H-%M-%S')

changeSet = {}

def insert(dict, src, dst, raw):
    if not src in dict:
        dict[src] = {}
    if not dst in dict[src]:
        dict[src][dst] = 1
        if len(dict[src].keys()) > 1:
            # print src, dict[src]
            if not changeSet.has_key(src):
                changeSet[src] = []
            # print raw
            changeSet[src].append(raw)
            return 1
        else:
            return 0
    else:
        dict[src][dst] += 1
        return 0

def onlyInsert(dict, src, dst):
    if not src in dict:
        dict[src] = {}
    if not dst in dict[src]:
        dict[src][dst] = 1
    else:
        dict[src][dst] += 1

def routeAggregate(routes):
    result = {}
    for troute in routes:
        cnt = len(troute)
        for rr in range(0, cnt-1):
            onlyInsert(result, int(troute[rr]), int(troute[rr+1]))
        else:
            continue
    return result


def getTopoIterator():
    for dt in rrule.rrule(rrule.MINUTELY, dtstart=st, until=et):
        try:
            tempArray = receptionDict[dt.day][dt.hour][dt.minute]
            for troute in tempArray:
                cnt = int(troute[8])
                if(cnt < 11 and cnt > 0):
                    routes = [troute[2]] + troute[9:9+cnt]
                    yield (routes, troute)
                else:
                    continue
        except KeyError:
            # print "no data at", dt.day, dt.hour, dt.minute
            pass

def getRelatedTopo(nodeId):
    relatedTopos = []
    for (topo, raw) in getTopoIterator():
        # print topo, raw
        for id in topo:
            if int(id) == int(nodeId):
                # print id, nodeId, raw
                relatedTopos.append(topo)
    return routeAggregate(relatedTopos)

r = {}
changeMeta = {}
for dt in rrule.rrule(rrule.MINUTELY, dtstart=st, until=et):
    try:
        tempArray = receptionDict[dt.day][dt.hour][dt.minute]
        for troute in tempArray:
            cnt = int(troute[8])
            if(cnt < 11 and cnt > 0):
                routes = troute[9:9+cnt]
                # print routes
                receptionMeta[dt.day][dt.hour][dt.minute]['c'] += insert(r, int(troute[2]), int(routes[0]), troute)
                # print int(troute[2]), int(routes[0])
                for rr in range(0, cnt-1):
                    insert(r, int(routes[rr]), int(routes[rr+1]), troute)
                    # print int(routes[rr]), int(routes[rr+1])
            else:
                continue
    except KeyError:
        # print "no data at", dt.day, dt.hour, dt.minute
        pass