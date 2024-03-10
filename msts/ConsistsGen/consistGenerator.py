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

def searchLoco(rootdir, loco:str=""):
    if loco == "":
        regex = re.compile('(.*eng$)')
    else:
        regex = re.compile(fr"(.*)({loco.upper()}|{loco.lower()})(.*).eng$", )

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



wap4List = searchLoco(config.WAP4, "wap4")
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
            if "DEMU".lower() in TrainDataDict[i]["trainType"].lower():
                rakePos = "DNG D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D12 DNG"
            elif "MEMU".lower() in TrainDataDict[i]["trainType"].lower():
                rakePos = "EG D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D12 EG"
        findAllRakes = re.findall(r"[A-Za-z0-9]+", rakePos)
        counter = 1
        listHolder = []

        LHB_TYPE = ["BGPRO", "VG"]
        LHB_Choice = random.choice(LHB_TYPE)
        
        for j in findAllRakes:
            if ("loco" in j.lower()) or ("eng" in j.lower()):
                continue
            if TrainDataDict[i]["trainType"].lower() == "Express".lower():
                
                if "icf" in TrainDataDict[i]["rakeType"].lower():
                    fileName = findCoachesNameForICF(j.upper())
                    listHolder.append(TemplateUpdater(fileName, counter))
                elif "lhb" in TrainDataDict[i]["rakeType"].lower():
                    if LHB_Choice == "BGPRO":
                        fileName = findBgProLHB(j.upper())
                        listHolder.append(TemplateUpdater(fileName, counter))
                    else:
                        fileName = findCoachesNameForLHB(j.upper())
                        listHolder.append(TemplateUpdater(fileName, counter))
                else:
                    print(i)
                    fileName = findCoachesNameForLHB(j.upper())
                    listHolder.append(TemplateUpdater(fileName, counter))
            elif TrainDataDict[i]["trainType"].lower() == "Shatabdi Express".lower():
                fileName = genShatabdiExp(j.upper())
                listHolder.append(TemplateUpdater(fileName, counter))
            elif TrainDataDict[i]["trainType"].lower() == "Garib Rath Express".lower():
                fileName = genGaribRathExp(j.upper())
                listHolder.append(TemplateUpdater(fileName, counter))
            elif "DEMU".lower() in TrainDataDict[i]["trainType"].lower():
                fileName = getDEMURake(j.upper())
                listHolder.append(TemplateUpdater(fileName, counter))
            elif "MEMU".lower() in TrainDataDict[i]["trainType"].lower():
                fileName = genMEMURake(j.upper())
                listHolder.append(TemplateUpdater(fileName, counter))
            elif "Vande Bharat".lower() in TrainDataDict[i]["trainType"].lower():
                fileName = genVBRakes(j.upper())
                listHolder.append(TemplateUpdater(fileName, counter))
            else:
                print(i)
                fileName = findCoachesNameForLHB(j.upper())
                listHolder.append(TemplateUpdater(fileName, counter))
                
            counter+=1

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


def findBgProLHB(value:str):
    if value.startswith("L"):
        return ("NA, NA")
    elif value.startswith("SLR"):
        return valueFinder("SLR")
    elif value.startswith("B") or value.startswith("AC3") or value.startswith("A3") or value.startswith("A4"):
        return 'Mumbai_Raj_LHB_3A "BGPro - LHB AC Rajdhani Coaches"'
    elif value.startswith("AC2") or value.startswith("A2"):
        return 'Mumbai_Raj_LHB_2A "BGPro - LHB AC Rajdhani Coaches"'
    elif value.startswith("HA") or value.startswith("H1") or value.startswith("A1") or value.startswith("AC1"):
        return 'Mumbai_Raj_LHB_1A "BGPro - LHB AC Rajdhani Coaches"'
    elif value.startswith("UR") or value.startswith("G"):
        return 'LHB_NonAC_GS_WideWIn "BGPro - LHB Non AC Coaches"'
    elif value.startswith("EOG"):
        return 'Mumbai_Raj_LHB_EOG "BGPro - LHB AC Rajdhani Coaches"' 
    elif value.startswith("HCP"):
        return valueFinder("VG_LHB_HPCV")
    elif value.startswith("PC"):
        return 'Mumbai_Raj_LHB_PANTRY "BGPro - LHB AC Rajdhani Coaches"'
    elif value.startswith("S") or value.startswith("D1"):
        return random.choice([('LHB_NonAC_SLP_WideWIn "BGPro - LHB Non AC Coaches"'), ('LHB_NonAC_SLP "BGPro - LHB Non AC Coaches"')])
    elif value.startswith("M"):
        return valueFinder("VG_LHB_AC_3_TIER_ECONOMY")
    else:
        print(value)
        return "NA Na"
    
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

# E:\DCIM\Train Simulator\TRAINS\TRAINSET\VG_LHB_COACHES

def genShatabdiExp(value):
    if value.startswith("EOG"):
        return valueFinder("VG_LHB_EOG")
    elif value.startswith("C"):
        return "VG_LHB_CHAIRCAR_AC_2 VG_LHB_COACHES"
    elif value.startswith("EV"):
        return "VG_LHB_VISTADOME VG_LHB_COACHES"
    elif value.startswith("E"):
        return "VG_LHB_CHAIRCAR_AC_GREY_FIRST VG_LHB_COACHES"
    else:
        print(value)
        return "NA Na"
    
def genGaribRathExp(value):
    if value.startswith("EOG"):
        return "BRW_GARIBRATH_EOG BRW_ICF_GARIBRATH"
    elif value.startswith("GD"):
        return "BRW_GARIBRATH_EOG BRW_ICF_GARIBRATH"
    elif value.startswith("G"):
        return "BRW_GARIBRATH_3AC BRW_ICF_GARIBRATH"
    else:
        print(value)
        return "BRW_GARIBRATH_3AC BRW_ICF_GARIBRATH"

def getDEMURake(value):
    if value.startswith("DNG"):
        return "ICFDEMU_NEW AERO_DMU"
    else:
        return "AERO_DMU_COACH AERO_DMU"
    
def genMEMURake(value):
    if value.startswith("EG"):
        return "MEMUDCYFG RAJ_MEMU2"
    else:
        return "MEMUY AERO_DMU"

def genVBRakes(value):
    if value.startswith("C"):
        return "vbcc VandeBharat"
    else:
        return "vbexcc VandeBharat"


if __name__ == "__main__":
    readJsonAndCreateTemplate()
