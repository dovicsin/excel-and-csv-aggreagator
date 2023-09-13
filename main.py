import os
import csv
import yaml
import glob
from excelToData import excelToData
from CSVToData import CSVToData
from utils.dataAggregator import dataAggregator
from utils.addPlusInfo import addPlusInfo
from utils.deleteFilesInDirectory import deleteFilesInDirectory


def createDirectory(directoryPath):
    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)

configFile = 'config/index.yaml'

defaultSourceDirectory = 'source/'
defaultTargetDirectory = 'dist/'
deleteFilesInDirectory(defaultTargetDirectory)
createDirectory(defaultTargetDirectory)

with open(configFile, 'r') as yaml_file:
    cofigParameters = yaml.safe_load(yaml_file)[0]

allConfig = [];
for configParamter in cofigParameters["configList"]:
    with open(configParamter['config'], 'r') as configFile:
        try: 
            config = yaml.safe_load(configFile)
            for element in config:
                element['tool'] = configParamter['name']
                allConfig.append(element)

        except FileNotFoundError:
            print(f"A(z) {configFile} nevű YAML állomány nem található.")
        except Exception as e:
            print(f"Hiba történt a YAML állomány olvasása során: {str(e)}")

for config in allConfig:
    sourceDirectory = os.path.join(defaultSourceDirectory,config['sourceDirectory'])
    sourceFile = config['sourceFile']
    mergedTargetFileName = config['outputName'] if 'outputName' in config else sourceFile.split('.')[0].replace('*', 'all')
    mergedTargetFile = os.path.join(defaultTargetDirectory,mergedTargetFileName+ '.csv')
    mergedFile = open(mergedTargetFile, 'a')

    fileList = glob.glob(os.path.join(sourceDirectory,sourceFile))
    firstWrited = False
    for file in fileList:
        fileExtension = os.path.splitext(file)[1]
        csv_file_name = os.path.basename(file).split('.')[0] + '.csv'

        data = []
        if fileExtension.startswith('.xls'):
            data = excelToData(config, file)
        elif fileExtension.startswith('.csv'):
            data = CSVToData(config, file)
        else:
            print(f"A(z) {file} fájl nem támogatott formátumú.")
            continue

        if 'agregate' in config:
            for agregate in config['agregate']:
                data = dataAggregator(data, aggregate_keys=agregate['columns'], aggregation_name=agregate['name'], operation=agregate['operation'])

        if 'info' in config:
            addPlusInfo(data, config['info'])
        
        writer = csv.writer(mergedFile, delimiter=';')    
        for row in data if not firstWrited else data[1:]:
            writer.writerow(row)

        firstWrited = True
    
    print(f'A(z) {mergedTargetFile} mentve.')
    mergedFile.close()

    
    
