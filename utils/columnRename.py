def columnRename(data, headerList, renameList):
    dataHeader = data[0]
    for rename in renameList:
        if rename["from"] in headerList:
            headerList[headerList.index(rename["from"])] = rename["to"]
        if rename["from"] in dataHeader:
            dataHeader[dataHeader.index(rename["from"])] = rename["to"]
    data[0] = dataHeader