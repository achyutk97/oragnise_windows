
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

temp = r"C:\Users\achyu\OneDrive\Documents\My Games\Train Simulator\TRAINS\TRAINSET\BGPro_ICF"

import os
import magic

blob = open('01437 Solapur - Tirupati Special Fare Special.con', 'rb').read()
m = magic.Magic(mime_encoding=True)
encoding = m.from_buffer(blob)
print(encoding)

print(os.path.split(temp))


