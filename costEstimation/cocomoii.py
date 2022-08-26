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

    return 0.91 + 0.01 * sum
