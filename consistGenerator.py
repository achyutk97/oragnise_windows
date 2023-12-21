import os
import config
import json
import re

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
    template = f"""\n		Wagon (
			WagonData ( {fileName} )
			UiD ( {counter} )
		)"""
    return template


def generateConsistFileUsingTemplate(trainName, rakeData):

    # template = f"""SIMISA@@@@@@@@@@JINX0D0t______

    # Train (
    #     TrainCfg ( {trainName}
    #         Name ( {trainName} )
    #         Serial ( 1 )
    #         MaxVelocity ( 38.88889 0.24002 )
    #         NextWagonUID ( 24 )
    #         Durability ( 1.00000 )
    #         Engine (
    #             UiD ( 0 )
    #             EngineData ( BRW_BSL_22974_WAP4 BRW_BSL_22974_WAP4 )
    #         )
    # """
    temp = []
    for i in rakeData:
        temp.append(i)

    # template += "))"

    template = f'''SIMISA@@@@@@@@@@JINX0D0t______

Train (
	TrainCfg ( "{trainName}"
		Name ( "{trainName}" )
		Serial ( 1 )
		MaxVelocity ( 38.88889 0.24002 )
		NextWagonUID ( 24 )
		Durability ( 1.00000 )
		Engine (
			UiD ( 0 )
			EngineData ( BRW_BSL_22974_WAP4 BRW_BSL_22974_WAP4 )
		){"".join(temp)}
	)
)
'''
    dirName = os.getcwd() + "/consists/"

    if not (os.path.exists(dirName)):
        os.mkdir(dirName)
            
    with open(f"{dirName}{trainName}.con", "wb") as fd:
        fd.write(template.encode("utf-16le"))


def readJsonAndCreateTemplate():
    with open("TrainData.json", "r") as fd:
        data = fd.read()

    # convert json to dict
    TrainDataDict = json.loads(data)

    for i in TrainDataDict.keys():
        findAllRakes = re.findall(r"[A-Za-z0-9]+", TrainDataDict[i])
        counter = 1
        listHolder = []
        for j in findAllRakes:
            if "NA" in j:
                print(i)
                continue
            if ("loco" in j.lower()) or ("eng" in j.lower()):
                continue
            fileName = findCoachesName(j.upper())
            listHolder.append(TemplateUpdater(fileName, counter))
            counter+=1;
        if len(findAllRakes[1:]) ==  listHolder:
            raise Exception("Issue")
        generateConsistFileUsingTemplate(i, listHolder)



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
        elif value.startswith("B") or value.startswith("AC3") or value.startswith("A3") or value.startswith("A4"):
            return valueFinder("AC_3")
        elif value.startswith("AC2") or value.startswith("A2"):
            return valueFinder("AC_2")
        elif value.startswith("HA") or value.startswith("H1") or value.startswith("A1") or value.startswith("AC1"):
            return valueFinder("VG_LHB_AC_FIRST")
        elif value.startswith("UR") or value.startswith("G"):
            return valueFinder("VG_LHB_SECONDCLASS")
        elif value.startswith("EOG"):
            return valueFinder("VG_LHB_EOG")
        elif value.startswith("HCP"):
            return valueFinder("VG_LHB_HPCV")
        elif value.startswith("PC"):
            return valueFinder("VG_LHB_PANTRY_CAR")
        elif value.startswith("S") or value.startswith("D1"):
            return valueFinder("VG_LHB_SLEEPER")
        elif value.startswith("M"):
            return valueFinder("VG_LHB_AC_3_TIER_ECONOMY")
        else:
            print(value)
            return "NA Na"

openReadICFAndLHBFilesNames()

readJsonAndCreateTemplate()

# openTempFile()