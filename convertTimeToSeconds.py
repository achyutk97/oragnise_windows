import re


TIME_FINDER = r"\d{2}:\d{2}\n-\n\d{2}:\d{2}"
def get_sec(time_str):
    """Get seconds from time."""
    h, m= time_str.split(':')
    return int(h) * 3600 + int(m) * 60



def readTime():
    data = ""
    with open("time_Holder.log", "r") as fd:
        data = fd.read()
    
    if data == "":
        exit(1)
    
    time = re.findall(TIME_FINDER, data)

    if len(time) == 0:
        exit(1)
    
    arrList = []
    derptList = []
    for i in time:
        startTime = i.splitlines()[0]
        endTime = i.splitlines()[-1]

        startTime = get_sec(startTime)
        endTime = get_sec(endTime)

        arrList.append(startTime)
        derptList.append(endTime)

    return arrList, derptList


def readActFileToUpdateTime():
    data = ""

    arrList, derptList = readTime()

    with open("actFileData.log", "r") as fd:
        data = fd.readlines()

    arrCoun = 0
    dept = 0
    for idx, i in enumerate(data):
        if "ArrivalTime" in i:
            temp = f"ArrivalTime ( {arrList[arrCoun]} )"
            number = re.findall(r"ArrivalTime \( (\d*) \)", i)
            print(temp)
            print(number)
            data[idx] = i.replace(f"ArrivalTime ( {number[0]} )", temp)
            arrCoun+=1
        elif "DepartTime" in i:
            temp = f"DepartTime ( {derptList[dept]} )"
            number = re.findall(r"DepartTime \( (\d*) \)", i)
            data[idx] = i.replace(f"DepartTime ( {number[0]} )", temp)
            dept+=1
        else:
            continue

    data = "".join(data)

    with open("MyFile.log", "w") as fd:
        fd.write(data)



readActFileToUpdateTime()
readTime()


