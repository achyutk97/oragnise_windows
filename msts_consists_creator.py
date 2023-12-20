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

        dictTrainRake = {}
        for i, j in zip(self.trainNumbers, self.wholeTrainName):
            print(i)
            dictTrainRake[j] = self.searchInWebShareRakePosition(i)

        jsonData = json.dumps(dictTrainRake, indent=4)

        with open("TrainData.json", "w") as fd:
            fd.write(jsonData)

        print(jsonData)

    @staticmethod
    def fixUrl(url):
        temp = url.split("/")
        fixUrl = temp[4][1:]
        temp[4] = fixUrl
        return "/".join(temp)
    

    def findRake(metaData):

        findRake = re.findall(r"Composition: (.*) Rake Sharing", str(metaData))
        if len(findRake) == 0:
            return "NA"
        
        return findRake[0]
    
    def searchInWebShareRakePosition(self, train):

        # data = requests.get("https://www.trainman.in/coach-position/12627", timeout=3)

        # print(data.text)

        page = requests.get(f"https://www.google.dz/search?q= indiarailinfo.com {train}")
        soup = BeautifulSoup(page.content)
        import re
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

            metaData = soup.findAll("meta")[1] 
            

            return MstsConsistGen.findRake(metaData)
        return "Not Found"

obj = MstsConsistGen()
obj.findallTrainInHTML()