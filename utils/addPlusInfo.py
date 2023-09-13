def addPlusInfo(data, infoList):
    keys = data[0]
    aggregated_values = data[1:]

    for info in infoList:
        keyIndex = "insertIndex" in info and info["insertIndex"] or len(keys)-1
        keys.insert(keyIndex, info['name'])

        for row in aggregated_values:
            row.insert(keyIndex, info['value'])
    return [keys] + aggregated_values