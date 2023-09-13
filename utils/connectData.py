def connectData(data, connected, connectKeys, headerNames):
    mainKeys = data[0]
    connectedKeys = connected[0]

    if not connectKeys["from"] in connectedKeys or not connectKeys["to"] in mainKeys:
        return data
    
    mainData = data[1:]
    connectedData = connected[1:]

    conectedColumnKey = mainKeys.index(connectKeys["to"])

    updated_data = []

    for row in mainData:
        connectedValue = row[conectedColumnKey]
        found = False

        for new_item in connectedData:

            if connectedValue == new_item[0]:
                updated_data.append(row + [new_item[1]])
                found = True
                break

        if not found:
            updated_data.append(row + [0])


    if connectKeys['from'] == connectKeys['to']:
        headerNames.remove(connectKeys['from'])
    mainKeys.extend(headerNames)

    updated_data.insert(0, mainKeys);
    return updated_data
    
