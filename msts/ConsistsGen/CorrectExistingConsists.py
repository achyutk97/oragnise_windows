import re
import os
import sys
import config
import msts_consists_creator as mcc

def listFiles(inputPath):
    listOfFiles = os.listdir(inputPath)
    return listOfFiles


def findWagonsAndEngineCount(data:str):
    wagonCount = 0
    engineCount = 0
    
    for i in data.splitlines():
        if "Wagon (" in i:
            wagonCount += 1
        elif "Engine (" in i:
            engineCount += 1
        else:
            continue
        
    return (wagonCount, engineCount)

def findTrainType():
    pass

def findRakeType():
    pass

def findTheFileExistsOrNot():
    pass

def readFiles(files: list):
    obj = mcc.MstsConsistGen()
    for i in files:
        if not i.endswith(".con"):
            print("\n", i, "error\n")
            continue
        correctPath = fr"{config.INPUT_CONSISTS_CORRECTOR_FILE}/{i}"
        data = ""
        # print(i)
        try:
            with open(correctPath, "r", encoding="utf-16") as fd:
                data = fd.read()
            print(data)
        except Exception as e:
            with open(correctPath, "r", encoding="utf-16-le") as fd:
                data = fd.read()    
        
        if data == "":
            # print(i, "Failed")
            continue
        # print(findWagonsAndEngineCount(data))
        
        trainNumber = re.findall(config.RegexForTrainNumber, i)
        
        if trainNumber != []:
            # print(trainNumber)
            trainNumber = trainNumber[0][1:]
            obj.trainNumbers.append(trainNumber)
            obj.wholeTrainName.append(i)
            
    obj.findTrains()
    
files = listFiles(config.INPUT_CONSISTS_CORRECTOR_FILE)

readFiles(files)