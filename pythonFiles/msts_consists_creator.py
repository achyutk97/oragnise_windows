import config
import re
import warnings
from bs4 import GuessedAtParserWarning
import requests
from bs4 import BeautifulSoup
warnings.filterwarnings('ignore', category=GuessedAtParserWarning)

import json

FIND_ALL_TRAIN = r"(\d.*)/(.*)\b "
FIND_HTTP_LINK = r"href=\"/url\?q=((.*)\d)&"

class MstsConsistGen:
    def __init__(self):
        self.trainNumbers = []
        self.wholeTrainName = []
        self.data = ""

    def findallTrainInHTML(self):
        with open(config.InputFile, "r") as fd:
            self.data = fd.read()

        if len(self.data) == 0:
            raise Exception("Please provide proper input file.")
        
        findAllTrain = re.findall(FIND_ALL_TRAIN, self.data)

        for train in findAllTrain:
            self.trainNumbers.append(train[0])
            self.wholeTrainName.append(" ".join(train))
        
        numberOfTrainPresent = len(self.trainNumbers)

        dictTrainRake = {}
        for i, j in zip(self.trainNumbers, self.wholeTrainName):
            dictTrainRake[j] = {}
            loco, rakeType, rakePosition = self.searchInWebShareRakePosition(i)
            dictTrainRake[j]["loco"] = loco
            dictTrainRake[j]["rakeType"] = rakeType
            dictTrainRake[j]["rakePosition"] = rakePosition

        jsonData = json.dumps(dictTrainRake, indent=4)

        if len(dictTrainRake.keys()) == numberOfTrainPresent:
            raise Exception(f"Some Train missing {numberOfTrainPresent}, {len(dictTrainRake.keys())}")
        
        with open("TrainData.json", "w") as fd:
            fd.write(jsonData)

    @staticmethod
    def fixUrl(url):
        temp = url.split("/")
        fixUrl = temp[4][1:]
        temp[4] = fixUrl
        return "/".join(temp)
    

    def findRake(soup):
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
    
    def findRakeType(self, soup):
        rakeType = soup.find("div", class_=re.compile("rakeType", re.I))

        if rakeType is None:
            rakeType = ">LHB Rake<"
        findCorrectRake = re.search(r">(.*)<", str(rakeType))

        return findCorrectRake.group(1)

    def searchInWebShareRakePosition(self, train):
        page = requests.get(f"https://www.google.dz/search?q= indiarailinfo.com {train}")
        soup = BeautifulSoup(page.content)
        links = soup.findAll("a")

        trainFound = ""
        for i in links:
            # import pdb;pdb.set_trace()
            if "https://indiarailinfo.com/train/" in str(i):
                trainFound = str(i)
                break
        
        if trainFound:
            findTrain = re.findall(FIND_HTTP_LINK, trainFound)[0][0]
            if len(findTrain) <= 0:
                exit(0)
            

            fix_url = MstsConsistGen.fixUrl(findTrain)
            data  = requests.get(fix_url)
            soup = BeautifulSoup(data.content)

            
            loco = self.findCorrectLoco(soup)
            rake = self.findRakeType(soup)
            rakePosition = MstsConsistGen.findRake(soup)
            return loco, rake, rakePosition
        return "Not Found", "NA", "NA"

obj = MstsConsistGen()
obj.findallTrainInHTML()