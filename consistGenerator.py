import os
import config
import json

lhb = [i for i in os.listdir(config.LHB) if i.endswith(".wag")]
icf = [i for i in os.listdir(config.ICF) if i.endswith(".wag")]
chairCar = [i for i in os.listdir(config.CHAIRCAR) if i.endswith(".wag")]

def openTempFile():

    with open("temp.con", "r") as fd:
        data = fd.read()
    
    print(data)

def openReadICFAndLHBFilesNames():
    pass


def TemplateUpdater(fileName, counter):
    template = f"""
            Wagon (
                WagonData ( {fileName} )
                UiD ( {counter} )
            )
            """
    return template


def generateConsistFileUsingTemplate(trainName, rakeData):

    template = f"""SIMISA@@@@@@@@@@JINX0D0t______

    Train (
        TrainCfg ( {trainName}
            Name ( {trainName} )
            Serial ( 1 )
            MaxVelocity ( 38.88889 0.24002 )
            NextWagonUID ( 24 )
            Durability ( 1.00000 )
            Engine (
                UiD ( 0 )
                EngineData ( BRW_BSL_22974_WAP4 BRW_BSL_22974_WAP4 )
            )
    """
    for i in rakeData:
        template += i

    template += "))"

    with open(f"{trainName}.con", "w") as fd:
        fd.write(template)

def readJsonAndCreateTemplate():
    with open("TrainData.json", "r") as fd:
        data = fd.read()

    # convert json to dict
    TrainDataDict = json.loads(data)
    
    listHolder = []
    counter = 0
    for i in TrainDataDict.keys():
        print(TrainDataDict[i].split("-"))
        if "-" in TrainDataDict[i]:
            for j in TrainDataDict[i].split("-"):
                print(j)
                # return FileName and File location
                fileName = findCoachesName(j)
                listHolder.append(TemplateUpdater(fileName, counter))
                counter+=1;
            generateConsistFileUsingTemplate(i, listHolder)
        break

    print(listHolder)



def valueFinder(value):
    for i in lhb:
        if value.lower() in i.lower():
            j = i.split(".wag")
            return f"{j[0]} {config.LHB_PARENT}"

def findCoachesName(value: str):
        if value.startswith("L"):
            return ("NA, NA")
        elif value.startswith("SLR"):
            return valueFinder("SLR")
        elif value.startswith("B") or value.startswith("AC3"):
            return valueFinder("AC_3")
        elif value.startswith("A1") or value.startswith("AC1"):
            return valueFinder("AC_2")
        elif value.startswith("HA"):
            return valueFinder("VG_LHB_AC_FIRST")
        elif value.startswith("UR") or value.startswith("G"):
            return valueFinder("VG_LHB_SECONDCLASS")
        elif value.startswith("EOG"):
            return valueFinder("VG_LHB_EOG")
        elif value.startswith("HCP"):
            return valueFinder("VG_LHB_HPCV")
        elif value.startswith("PC"):
            return valueFinder("VG_LHB_PANTRY_CAR")
        else:
            return valueFinder("VG_LHB_SLEEPER")

openReadICFAndLHBFilesNames()

readJsonAndCreateTemplate()

# openTempFile()