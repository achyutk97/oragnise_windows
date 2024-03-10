import os
import shutil
import re

ACT_SERVICES_FOLDER = r"E:\DCIM\Train Simulator\ROUTES\TSDRV4\SERVICES"
CONSISTS_DIR = r"E:\DCIM\Train Simulator\TRAINS\CONSISTS"

# Train_Config ( "07663 vijayapura - raichur passenger special" )

def findFiles():
    listServicesFiles = os.listdir(ACT_SERVICES_FOLDER)
    
    for i in listServicesFiles:
        fileLoc = fr"{ACT_SERVICES_FOLDER}\{i}"
        data = []
        with open(fileLoc, "r", encoding="utf-16") as fd:
            data = fd.readlines()
        
        for j in data:
            if "Train_Config" in j:
                value = re.findall(r'Train_Config \( (.*) \)', j)
                fileName = ""
                
                for i in value[0]:
                    if i != '"':
                        fileName += i
                
                copyConsistsFileName = fr"{CONSISTS_DIR}\{fileName}.con"
                if not os.path.exists(os.getcwd()+"\con"):
                    os.mkdir("con/")
                shutil.copy(copyConsistsFileName, "./con/")

if __name__ == "__main__":
    findFiles()