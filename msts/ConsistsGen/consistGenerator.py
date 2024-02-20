import os
import config as config
import json
import re
import random

lhb = [i for i in os.listdir(config.LHB) if i.endswith(".wag")]
icf = [i for i in os.listdir(config.ICF) if i.endswith(".wag")]
chairCar = [i for i in os.listdir(config.CHAIRCAR) if i.endswith(".wag")]



DEFAULT_RAKE = "LOCO SLR GS Se1 S1 S2 S3 S4 S5 S6 S7 S8 S9 S10 S11 S12 S13  B1 B2 B3  B4 A1 GS SLR"


def TemplateUpdater(fileName, counter):
    template = f"""\n		Wagon (
			WagonData ( {fileName} )
			UiD ( {counter} )
		)"""
    return template

def searchLoco(rootdir):
    regex = re.compile('(.*eng$)')

    listENG = []
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if regex.match(file):
                listENG.append((file.split(".")[0], root.split("\\")[-1]))
    return listENG

def findLocoPath(loco):
    if "wap-4" in loco.lower():
        return random.choice(wap4List)
    elif "wap-7" in loco.lower():
        return random.choice(wap7List)
    elif "wap-9" in loco.lower():
        return random.choice(wap9List)
    elif "wdm3d" in loco.lower():
        return random.choice(wdm3dList)
    elif "wdp4d" in loco.lower():
        return random.choice(wdm3dList)
    else:
        return random.choice(wap7List)



wap4List = searchLoco(config.WAP4)
wap7List = searchLoco(config.WAP7)
wadg4List = searchLoco(config.WDG_4)
wadg4dList = searchLoco(config.WDG_4D)
wap5List = searchLoco(config.WAP5)
wap9List = searchLoco(config.WAG9)
wdm3dList = searchLoco(config.WDM3D)
wdp4bList = searchLoco(config.WDP_4B)
wdp4dList = searchLoco(config.WDP_4D)

def generateConsistFileUsingTemplate(TrainDataDict, trainName, rakeData):
    temp = []
    tempLoco = []

    for i in rakeData:
        temp.append(i)

    alco = TrainDataDict[trainName]['loco']

    tempEng = findLocoPath(alco)

    while True:
        if tempEng in tempLoco:
            tempEng = findLocoPath(alco)
            continue
        tempLoco.append(tempEng)
        break
    print(tempEng)
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
			EngineData ( "{tempEng[0]}" "{tempEng[1]}" )
		){"".join(temp)}
	)
)
'''
    dirName = os.getcwd() + "/consists/"

    if not (os.path.exists(dirName)):
        os.mkdir(dirName)
            
    with open(f"{dirName}{trainName}.con", "wb") as fd:
        fd.write(template.encode("utf-16"))


def readJsonAndCreateTemplate():
    with open("TrainData.json", "r") as fd:
        data = fd.read()

    # convert json to dict
    TrainDataDict = json.loads(data)

    for i in TrainDataDict.keys():
        rakePos = TrainDataDict[i]["rakePosition"]
        if "NA" in rakePos:
            print(i)
            rakePos = DEFAULT_RAKE
        findAllRakes = re.findall(r"[A-Za-z0-9]+", rakePos)
        counter = 1
        listHolder = []

        for j in findAllRakes:
            if ("loco" in j.lower()) or ("eng" in j.lower()):
                continue
            if "icf" in TrainDataDict[i]["rakeType"].lower():
                fileName = findCoachesNameForICF(j.upper())
                listHolder.append(TemplateUpdater(fileName, counter))
            elif "lhb" in TrainDataDict[i]["rakeType"].lower():
                fileName = findCoachesNameForLHB(j.upper())
                listHolder.append(TemplateUpdater(fileName, counter))
            else:
                print(i)
                fileName = findCoachesNameForLHB(j.upper())
                listHolder.append(TemplateUpdater(fileName, counter))
            counter+=1;

        if len(findAllRakes[1:]) ==  listHolder:
            raise Exception("Issue")
        generateConsistFileUsingTemplate(TrainDataDict, i, listHolder)

def valueFinder(value):
    for i in lhb:
        if value.lower() in i.lower():
            j = i.split(".wag")
            return f"{j[0]} {config.LHB_PARENT}"
        
def valueFinderForICF(value):
        return f"{value} {config.ICF_PARENT}"



def findCoachesNameForICF(value: str):
    if value.startswith("L"):
        return ("NA, NA")
    elif value.startswith("SLR"):
        return valueFinderForICF("ICF_SLR_Utk")
    elif value.startswith("B") or value.startswith("AC3") or value.startswith("A3") or value.startswith("A4"):
        return valueFinderForICF("ICF_AC3_Utk")
    elif value.startswith("AC2") or value.startswith("A2"):
        return valueFinderForICF("ICF_AC2_Utk")
    elif value.startswith("HA") or value.startswith("H1") or value.startswith("A1") or value.startswith("AC1"):
        return valueFinderForICF("ICF_AC1_Utk")
    elif value.startswith("UR") or value.startswith("G"):
        return valueFinderForICF("ICF_GS_Utk")
    elif value.startswith("EOG"):
        return valueFinderForICF("ICF_SLR_Utk")
    elif value.startswith("HCP"):
        return valueFinderForICF("VG_LHB_HPCV")
    elif value.startswith("PC"):
        return valueFinderForICF("ICF_PC_Utk")
    elif value.startswith("S") or value.startswith("D1") or value.startswith("Se"):
        return valueFinderForICF("ICF_SL_Utk")
    else:
        print(value)
        return "NA Na"
    
def findCoachesNameForLHB(value: str):
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

if __name__ == "__main__":
    readJsonAndCreateTemplate()
