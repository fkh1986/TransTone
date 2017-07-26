import math
frequencyR = [697,770, 852, 941]
frequencyC = [1209, 1336, 1477, 1633]

samplingFreq = 44000
tonePeriod = 0.25


digits = {'0' : [4,2],
          '1' : [1,1],
          '2' : [1,2],
          '3' : [1,3],
          '4' : [2,1],
          '5' : [2,2],
          '6' : [2,3],
          '7' : [3,1],
          '8' : [3,2],
          '9' : [3,3],
          'A' : [1,4],
          'B' : [2,4],
          'C' : [3,4],
          'D' : [4,4],
          'E' : [4,1],
          'F' : [4,3]}

digitFreqs = list()

for digit in digits:
    digitFreqs.append([frequencyR[digits[digit][0]-1],frequencyC[digits[digit][1]-1]])


def GenSineWave(f,fs,t):
    for i in range(
