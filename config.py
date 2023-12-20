import os

CWD = os.getcwd() + "\\"
InputFile = CWD + "input.log"
LHB = r"C:\Users\achyu\OneDrive\Documents\My Games\Train Simulator\TRAINS\TRAINSET\VG_LHB_COACHES_SLEEPER"
ICF = r"C:\Users\achyu\OneDrive\Documents\My Games\Train Simulator\TRAINS\TRAINSET\BGPro_ICF"
CHAIRCAR = r"C:\Users\achyu\OneDrive\Documents\My Games\Train Simulator\TRAINS\TRAINSET\VG_LHB_COACHES"

LHB_PARENT = os.path.split(LHB)[-1]
ICF_PARENT = os.path.split(ICF)[-1]