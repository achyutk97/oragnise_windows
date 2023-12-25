
    # LHB_EOG = []
    # LHB_SLR = []
    # LHB_AC3 = []
    # LHB_AC2 = []
    # for i in lhb:
    #     if "eog" in i.lower():
    #         LHB_EOG.append(i)
    #     elif "slr" in i.lower():
    #         print(i.lower())
    #         LHB_SLR.append(i)
    #     elif "AC_3" in i.lower():
    #         LHB_AC3.append(i)
    #     elif "AC_2" in i.lower():
    #         LHB_AC2.append(i)
    #     elif "AC_FIRST" in i.lower():
            
    
    # print(LHB_SLR)

# temp = r"C:\Users\achyu\OneDrive\Documents\My Games\Train Simulator\TRAINS\TRAINSET\BGPro_ICF"

# import os
# import magic

# blob = open('01437 Solapur - Tirupati Special Fare Special.con', 'rb').read()
# m = magic.Magic(mime_encoding=True)
# encoding = m.from_buffer(blob)
# print(encoding)

# print(os.path.split(temp))

from bs4 import BeautifulSoup

# import re
# with open("22639.html", "rb") as fd:
#     data = fd.read()

# soup = BeautifulSoup(data)
# loco = soup.find("span", {"class": "loco"})

# loco = BeautifulSoup(str(loco))



# rakeType = soup.find("div", class_=re.compile("rakeType", re.I))
# if rakeType is None:
#     rakeType = ">LHB Rake<"
# findCorrectRake = re.search(r">(.*)<", str(rakeType))
# print(findCorrectRake.group(1))

import os
import re

WAP4 = r"C:\Users\achyu\OneDrive\Documents\My Games\Train Simulator\TRAINS\TRAINSET"
ALCO = r"C:\Users\achyu\OneDrive\Documents\My Games\Train Simulator\TRAINS\TRAINSET"
WDM3D = r"C:\Users\achyu\OneDrive\Documents\My Games\Train Simulator\TRAINS\TRAINSET\BGPro - WDM-3A Rebuilts"

# regex = re.compile('(BRW_(.*)_WAP4.*eng$)')
# regex = re.compile('(BRW(.*)_WDG*.*eng$)')
