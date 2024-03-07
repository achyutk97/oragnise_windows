import config
import re
import warnings
from bs4 import GuessedAtParserWarning
import requests
from bs4 import BeautifulSoup
import wget
import os
import consistGenerator as cg
import time
import sys
warnings.filterwarnings('ignore', category=GuessedAtParserWarning)

import json

FIND_ALL_TRAIN = r"(\d.*)/(.*)\b "
FIND_HTTP_LINK = r"href=\"/url\?q=((.*)\d)&"
FIND_HTTP_EDGE = r"href=\"(.*)\"><div class=\"tpic\">"

class MstsConsistGen:
    def __init__(self):
        self.trainNumbers = []
        self.wholeTrainName = []
        self.data = ""

    
    def findTrains(self):
        numberOfTrainPresent = len(self.trainNumbers)
            
        dictTrainRake = {}
        c = 0
        for i, j in zip(self.trainNumbers, self.wholeTrainName):
            c+=1
            dictTrainRake[j] = {}
            loco, rakeType, rakePosition = self.searchInWebShareRakePosition(i)
            dictTrainRake[j]["loco"] = loco
            dictTrainRake[j]["rakeType"] = rakeType
            dictTrainRake[j]["rakePosition"] = rakePosition
            dictTrainRake[j]["trainType"] = self.findTrainType(j)

        jsonData = json.dumps(dictTrainRake, indent=4)

        with open("TrainData.json", "w") as fd:
            fd.write(jsonData)
            
        if len(dictTrainRake.keys()) != numberOfTrainPresent:
            raise Exception(f"Some Train missing {numberOfTrainPresent}, {len(dictTrainRake.keys())}")
            
            
                
    def findallTrainInHTML(self):
        if len(sys.argv) < 2:
            with open(config.InputFile, "r") as fd:
                self.data = fd.read()

            if len(self.data) == 0:
                raise Exception("Please provide proper input file.")
            
            findAllTrain = re.findall(FIND_ALL_TRAIN, self.data)

            for train in findAllTrain:
                self.trainNumbers.append(train[0])
                self.wholeTrainName.append(" ".join(train))
            
            
            # numberOfTrainPresent = len(self.trainNumbers)

            # dictTrainRake = {}
            # for i, j in zip(self.trainNumbers, self.wholeTrainName):
            #     dictTrainRake[j] = {}
            #     loco, rakeType, rakePosition = self.searchInWebShareRakePosition(i)
            #     dictTrainRake[j]["loco"] = loco
            #     dictTrainRake[j]["rakeType"] = rakeType
            #     dictTrainRake[j]["rakePosition"] = rakePosition
            #     dictTrainRake[j]["trainType"] = self.findTrainType(j)

            # jsonData = json.dumps(dictTrainRake, indent=4)

            # if len(dictTrainRake.keys()) != numberOfTrainPresent:
            #     raise Exception(f"Some Train missing {numberOfTrainPresent}, {len(dictTrainRake.keys())}")
            
            # with open("TrainData.json", "w") as fd:
            #     fd.write(jsonData)
        else:
            with open(config.IndividualTrainPath, "r") as fd:
                self.data = fd.read()
                
            if len(self.data) == 0:
                raise Exception("Please provide proper input file.")
            
            for i in self.data.split("\n"):
                self.trainNumbers.append(i.split()[0])
                self.wholeTrainName.append(i)
          
        self.findTrains()


    @staticmethod
    def fixUrl(url):
        temp = url.split("/")
        fixUrl = temp[4][1:]
        temp[4] = fixUrl
        return "/".join(temp)
    
    def findRake(self, soup):
        metaData = soup.findAll("meta")[1]

        findRake = re.findall(r"Composition: (.*) Rake Sharing", str(metaData))
        if len(findRake) == 0:
            return "NA"
        
        return findRake[0]
    
    def findCorrectLoco(self, soup):
        loco = soup.find("a", href=re.compile("/loco/", re.I))

        if loco is None:
            loco = ">NA<"
        findCorrectLoco = re.search(r">(.*)<", str(loco))

        return findCorrectLoco.group(1)
    
    def findTrainType(self, train:str):
        if train.endswith("Vande Bharat Express"):
            return "Vande Bharat"
        elif train.endswith("InterCity SF Express"):
            return "Intercity"
        elif train.endswith("Duronto Express"):
            return "Duronto Express"
        elif train.endswith("Shatabdi Express"):
            return "Shatabdi Express"
        elif train.endswith("Jan Shatabdi Express"):
            return "Jan Shatabdi Express"
        elif train.endswith("Garib Rath Express"):
            return "Garib Rath Express"
        elif train.endswith("MMTS"):
            return "MMTS"
        elif "DEMU" in train:
            return "DEMU"
        elif "MEMU" in train:
            return "MEMU"
        else:
            return "Express"
    
    def findRakeType(self, soup):
        rakeType = soup.find("div", class_=re.compile("rakeType", re.I))

        if rakeType is None:
            rakeType = ">LHB Rake<"
        findCorrectRake = re.search(r">(.*)<", str(rakeType))

        return findCorrectRake.group(1)

    def SearchThroughGoogle(self, train: str):
        page = requests.get(f"https://www.google.dz/search?q= indiarailinfo.com {train}")
        soup = BeautifulSoup(page.content)
        links = soup.findAll("a")

        trainFound = ""
        for i in links:
            if "https://indiarailinfo.com/train/" in str(i):
                trainFound = str(i)
                break
        
        findTrain = ""
        if trainFound:
            findTrain = re.findall(FIND_HTTP_LINK, trainFound)[0][0]
            if len(findTrain) <= 0:
                exit(0)

        return findTrain
    # <span style="font-weight:bold;">Vande Bharat</span>
    # <span style="font-weight:bold;color:inherit;">SuperFast</span>
    
    def SearchThroughEdge(self, train: str):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        # try:
        driver = webdriver.Chrome(options=chrome_options)
        # if os.path.exists("./search"):
        #     os.remove("./search")
        url = f"https://www.google.com/search?q={train}%2F+site%3Aindiarailinfo.com"
        print(url)
        driver.get(url)
        # /html/body/div[6]/div/div[5]/div[9]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/span/a/h3
        # /html/body/div[6]/div/div[5]/div[9]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/span/a/h3
        # /html/body/div[4]/main/ol/li[1]/div[1]/a/div[2]/div[2]/div/cite
                                                # //*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/span/a/div/div/span
        website = driver.find_element(By.CLASS_NAME, 'LC20lb')
        # //*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/span/a/div/div/div/cite
        # website = driver.find_element("xpath", '//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/span/a/h3')
                                                # //*[@id="rso"]/div[1]/div/div/div[1]/div/div/span/a/h3
                                            # '/html/body/div[4]/main/ol/li[1]/h2/a'
        website.click()
        
        railinfo = driver.current_url
        # with open("search", "rb") as fd:
        #     data = fd.read()
        print(railinfo)
        
        driver.quit()
        # except Exception as e:
        #     print(str(e), train)
        #     # driver.get(url)
        #     return ""
        return railinfo

    def searchInWebShareRakePosition(self, train):
        
        findTrain = ""
        try:
            findTrain = self.SearchThroughEdge(train)
            
        except Exception as e:
            print(train, str(e))
            try:
                findTrain = self.SearchThroughGoogle(train)
            except Exception as e:
                print(f"{train} failed")
               
        if len(findTrain) != 0:
            fix_url = MstsConsistGen.fixUrl(findTrain)
            data  = requests.get(fix_url)
            soup = BeautifulSoup(data.content)

            
            loco = self.findCorrectLoco(soup)
            rake = self.findRakeType(soup)
            rakePosition = self.findRake(soup)
            return loco, rake, rakePosition
        return "Not Found", "NA", "NA"


if __name__ == "__main__":
    obj = MstsConsistGen()
    obj.findallTrainInHTML()
    cg.readJsonAndCreateTemplate()