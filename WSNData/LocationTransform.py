__author__ = 'jin-yc10'

# node id, NULL, x, y, useless field, useless field
# 1001,NULL,120.372923333333,31.4834383333333,46.1,NULL,2

# translate from GPS to Baidu-Location

import csv
import json, base64, urllib

NodeInfoCsvFile = open("1000-2000.txt","r")
NodeInfoOutCsvFile = open("1000-2000-baidu.txt", "w")
NodeInfoCsvObj = csv.reader(NodeInfoCsvFile)
NodeInfoWriter = csv.writer(NodeInfoOutCsvFile)
skipFirstRow = True
for nodeInfo in NodeInfoCsvObj:
    if skipFirstRow:
        skipFirstRow = False
        pass
    else:
        x = nodeInfo[2]
        y = nodeInfo[3]
        print nodeInfo[0], '\r',
        if x == '0' or y == '0':
            continue
        response = urllib.urlopen('http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x='+str(x)+'&y='+str(y)).read()
        jsonobj = json.loads(response)
        bx = base64.decodestring(jsonobj['x'])
        by = base64.decodestring(jsonobj['y'])
        NodeInfoWriter.writerow(nodeInfo[0:4] + [bx, by])

NodeInfoCsvFile.close()
NodeInfoOutCsvFile.close()