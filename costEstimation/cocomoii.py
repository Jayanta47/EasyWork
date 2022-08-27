import numpy as np

# scale factors

PREC = [6.2, 4.96, 3.72, 2.48, 1.24, 0]
FLEX = [5.07, 4.05, 3.04, 2.03, 1.01, 0]
RESL = [7.07, 5.65, 4.24, 2.83, 1.41, 0]
TEAM = [5.48, 4.38, 3.29, 2.19, 1.10, 0]
PMAT = [7.8, 6.24, 4.68, 3.12, 1.56, 0]

####### EFFORT MULTIPLIER #######

# product factors

RELY = [0.82, 0.92, 1, 1.1, 1.26]
DATA = [-1, 0.9, 1, 1.14, 1.28, -1]
CPLX = [0.73, 0.87, 1, 1.17, 1.34, 1.74]
RUSE = [-1, 0.95, 1, 1.07, 1.15, 1.24]
DOCU = [0.851, 0.91, 1, 1.11, 1.23, -1]

# platform factors

TIME = [-1, -1, 1, 1.11, 1.29, 1.63]
STOR = [-1, -1, 1, 1.05, 1.17, 1.46]
PVOL = [-1, .87, 1, 1.15, 1.30, -1]

# personnel factors

ACAP = [1.42, 1.22, 1, 0.85, 0.71, -1]
PCAP = [1.34, 1.16, 1, 0.88, 0.76, -1]
PCON = [1.29, 1.10, 1, 0.9, 0.81, -1]
APEX = [1.22, 1.10, 1, 0.88, 0.81, -1]
PLEX = [1.19, 1.12, 1, 0.91, 0.85, -1]
LTEX = [1.20, 1.14, 1, 0.91, 0.84, -1]

# project factors

TOOL = [1.17, 1.09, 1, 0.9, 0.78, -1]
SITE = [1.22, 1.09, 1, 0.93, 0.86, 0.8]
SCED = [1.43, 1.14, 1, 1, 1, -1]


B = 0.91


def calculateExponent(level_list):
    sum = 0

    sum += PREC[level_list[0]]
    sum += FLEX[level_list[1]]
    sum += RESL[level_list[2]]
    sum += TEAM[level_list[3]]
    sum += PMAT[level_list[4]]

    return 1.01 + 0.01 * sum


def calculateEffortMultipliers(level_dict):
    EM = 1.0

    a = np.array([
        RELY[level_dict["RELY_level"]],
        DATA[level_dict["DATA_level"]],
        CPLX[level_dict["CPLX_level"]],
        RUSE[level_dict["RUSE_level"]],
        DOCU[level_dict["DOCU_level"]],

        TIME[level_dict["TIME_level"]],
        STOR[level_dict["STOR_level"]],
        PVOL[level_dict["PVOL_level"]],

        ACAP[level_dict["ACAP_level"]],
        PCAP[level_dict["PCAP_level"]],
        PCON[level_dict["PCON_level"]],
        APEX[level_dict["APEX_level"]],
        PLEX[level_dict["PLEX_level"]],
        LTEX[level_dict["LTEX_level"]],

        TOOL[level_dict["TOOL_level"]],
        SITE[level_dict["SITE_level"]],
        SCED[level_dict["SCED_level"]],

    ])

    return a.prod()


def calculateEffort(scale_factor_list, effortM_level_dict, SLOC):
    return 2.94 * ((SLOC)**calculateExponent(scale_factor_list)) * calculateEffortMultipliers(effortM_level_dict)

def calculateTime(effort):
    return 2.5 * (effort)**(0.32)

def calculateDevCost(effort, labor_rate):
    return effort * labor_rate

