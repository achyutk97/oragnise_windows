import config as cg
import random
import re
import os
import sys

D = 1
E = 1
def find_file(file_name_regex):
  """Recursively searches for a file in a directory and all its subdirectories that matches the given regular expression.

  Args:
    file_name_regex: A regular expression to match the file name.
    directory: The directory to start searching from.

  Returns:
    A list of all the full paths to the files that match the regular expression.
  """
  directory = cg.MSTS_DIR
  file_paths = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      if re.match(file_name_regex, file):
        file_paths.append(os.path.join(root, file))

  return file_paths

# Example usage:
def findCombination(regexFile):
    file_paths = find_file(regexFile)
    train_data = []
    if file_paths:
        for file_path in file_paths:
            # print(f"Found file at: {file_path}")
            file = file_path.split("\\")
            train_data.append((file[-1].split(".")[0], file[-2]))
    else:
        print("No files found.")
    return random.choice(train_data)

def getDieselLoco():
    engType = r"(.*)(wdg|WDG)(.*).eng$"
    data = findCombination(engType)
    return data

def getElectricLoco():
    engType = r"(.*)(wag|WAG)(.*).eng$"
    data = findCombination(engType)
    return data

def getEngineData(choice):
    no_of_engines = random.randint(1, 3)
    engineData = []
    counter = 0
    
    for i in range(no_of_engines):
        if choice:
            engFile, dirName = getDieselLoco()
        else:
            engFile, dirName = getElectricLoco()
        template = f"""Engine (
			UiD ( {counter} )
			EngineData ( "{engFile}" "{dirName}" )
		)"""
        counter += 1
        engineData.append(template)
    return engineData
        
        
def getCaboose(counter):
    Caboose = f"""\n		Wagon (
			WagonData ( "IR_Caboose_new" "ASM - IR Freight" )
			UiD ( {counter+1} )
		)"""
    return Caboose

def getGoodsRake(n):
    list_Of_Freight = ["BCNA", "BOXN", "BRN", "BTP", "CON", "HOPPER", "BTFLN"]
    
    freightTye = random.choice(list_Of_Freight)
    wagType = fr"(.*)({freightTye})(.*).wag$"
    
    fileName, Dir = findCombination(wagType)
    rakeData = []
    counter = 2
    for i in range(n):
        template = f"""\n		Wagon (
			WagonData ( "{fileName}" "{Dir}" )
			UiD ( {counter} )
		)"""
        counter += 1
        rakeData.append(template)
    
    rakeData.append(getCaboose(counter))
    
    return rakeData

def GoodsConsistsGen(goodsName, noOfRakes, eng):
    engData = getEngineData(eng)
    temp = getGoodsRake(noOfRakes)
    
    
    template = f'''SIMISA@@@@@@@@@@JINX0D0t______

Train (
	TrainCfg ( "{goodsName}"
		Name ( "{goodsName}" )
		Serial ( 1 )
		MaxVelocity ( 38.88889 0.24002 )
		NextWagonUID ( 24 )
		Durability ( 1.00000 )
		{"".join(engData)}{"".join(temp)}
	)
)
'''
    dirName = os.getcwd() + "/consists/"

    if not (os.path.exists(dirName)):
        os.mkdir(dirName)
            
    with open(f"{dirName}{goodsName}.con", "wb") as fd:
        fd.write(template.encode("utf-16"))

def createGoodsConsists(noOfRakes, index):
    global E, D
    try:
        choice = random.choice([0, 1]) # 0 Diesel 1 Electric
        if choice:
            fileName = f"Goods_D_{D}"
            D += 1
        else:
            Eng = getElectricLoco()
            fileName = f"Goods_E_{E}"
            E += 1
        print(f"Generating {fileName}....")
        GoodsConsistsGen(fileName, noOfRakes, choice)
        return 0
    except Exception as e:
        print(e)
        return -1

def main(consistCont):
    rakeCount = random.randint(40, 50)
    for i in range(consistCont):
        createGoodsConsists(rakeCount, i)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Provied Consist count and rakeCount")
        exit(1)
    main(int(sys.argv[1]))

