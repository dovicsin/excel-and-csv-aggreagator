import re
import csv
from utils.columnRename import columnRename
from utils.rowCounter import rowCounter
from utils.connectData import connectData

def CSVToData(config, file):
    
    data = []

    if not 'data' in config:
        return []
    
    dataSources = config['data']   

    for dataSource in dataSources:
        headerNames = dataSource['headerNames']
        sourceFile = file

        if ('external' in dataSource and dataSource['external']==True):
            sourceFileRegexp = config['sourceFile'].replace('.', '\.').replace('*', '(.*)?')
            unicFileID = re.findall( f'({sourceFileRegexp})',file)[0][1]
            externalFileName = dataSource['filePrefix'] + unicFileID + dataSource['extension']
            sourceFile = file.rsplit('/', 1)[0] + '/' + externalFileName

        with open(sourceFile, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=config['delimiter'] or ',')
            csvRawData = [row for row in reader]

        csvHeader = csvRawData[0]

        columns = [csvHeader.index(column_name) if column_name in csvHeader else None for column_name in headerNames]
        csvData = []
        for row in csvRawData:
            csvData.append([row[column] for column in columns])
        if 'method' in dataSource:
            method = dataSource['method'];
            if method['type'] == 'count':
                csvData = rowCounter(csvData)
        if 'rename' in dataSource:
            columnRename(dataSource,headerNames, dataSource["rename"] )
        if 'connect' in dataSource:
            data = connectData(data, csvData,  dataSource['connect'], headerNames)
        elif not data: 
            data = csvData;
    return data