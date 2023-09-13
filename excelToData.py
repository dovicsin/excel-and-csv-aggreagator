import xlrd
import re
from utils.columnRename import columnRename
from utils.rowCounter import rowCounter
from utils.connectData import connectData

def excelToData(config, file):
    workbook = xlrd.open_workbook(file)
    data = []

    if not 'sheets' in config:
        return []
    
    sheets = config['sheets']   

    for sheet in sheets:
        sheetName = sheet['sheetName']
        headerNames = sheet['headerNames']
        headerRow = sheet['headerRow']

        if ('external' in sheet and sheet['external']==True):
            sourceFileRegexp = config['sourceFile'].replace('.', '\.').replace('*', '(.*)?')
            unicFileID = re.findall( f'({sourceFileRegexp})',file)[0][1]
            externalFileName = sheet['filePrefix'] + unicFileID + sheet['extension']
            externalFilePath = file.rsplit('/', 1)[0] + '/' + externalFileName
            externalWorkBook = xlrd.open_workbook(externalFilePath)
            worksheet = externalWorkBook.sheet_by_name(sheetName)
        else:
            worksheet = workbook.sheet_by_name(sheetName)
        columns = [worksheet.row_values(headerRow).index(column_name) if column_name in worksheet.row_values(headerRow) else None for column_name in headerNames]
        sheetData = []
        for row in range(headerRow, worksheet.nrows):
            sheetData.append([worksheet.cell_value(row, column) for column in columns])

        if 'method' in sheet:
            method = sheet['method'];
            if method['type'] == 'count':
                sheetData = rowCounter(sheetData)
        if 'rename' in sheet:
            columnRename(sheetData,headerNames, sheet["rename"] )
        if 'connect' in sheet:
            data = connectData(data, sheetData,  sheet['connect'], headerNames)
        elif not data: 
            data = sheetData;
    return data