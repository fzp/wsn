__author__ = 'jin-yc10'

import csv, os

NodeInfo = {}
NodeInfoCsvFile = open(os.path.join(os.path.dirname(__file__), "1000-2000-baidu.txt"),"r")
NodeInfoCsvObj = csv.reader(NodeInfoCsvFile)
for nodeInfo in NodeInfoCsvObj:
    NodeInfo[nodeInfo[0]] = nodeInfo

NodeInfoCsvFile.close()

if __name__ == "__main__":
    print os.path.abspath(os.curdir)
    print NodeInfo