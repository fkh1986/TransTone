import math
import pyaudio
import array
import numpy as np
import wave

frequencyR = (697, 770, 852, 941)
frequencyC = (1209, 1336, 1477, 1633)

samplingFreq = 44100
sr = 44100
tonePeriod = 0.05
volume = 0.5


digits = {'0': [4, 2],
          '1': [1, 1],
          '2': [1, 2],
          '3': [1, 3],
          '4': [2, 1],
          '5': [2, 2],
          '6': [2, 3],
          '7': [3, 1],
          '8': [3, 2],
          '9': [3, 3],
          'A': [1, 4],
          'B': [2, 4],
          'C': [3, 4],
          'D': [4, 4],
          'E': [4, 1],
          'F': [4, 3]}


def GenDTMF(f1, f2, fs, t, volume):
#    tp = range(0, int(fs*t))
#    sineSig = [np.sin(2*np.pi*f1*ts/fs) + np.sin(2*np.pi*f2*ts/fs) for ts in tp]
    sineSig = array.array('f',((volume * math.sin(i / (f1 / 100.)) + volume * math.sin(i / (f2 / 100.)))
                               for i in range(int(fs*t)))).tostring()

    return sineSig


digitFreqs = list()

for digit in digits:
    digitFreqs.append([frequencyR[digits[digit][0]-1], frequencyC[digits[digit][1]-1]])

print(digitFreqs)
print(digitFreqs[0][0])
print(digitFreqs[0][1])


p = pyaudio.PyAudio()
stream = p.open(rate=sr, channels=1, format=pyaudio.paFloat32, output=True)

for i in range(15):
#    sin1 = GenSineWave(digitFreqs[i][0], samplingFreq, tonePeriod)
#    sin2 = GenSineWave(digitFreqs[i][1], samplingFreq, tonePeriod)
    test = GenDTMF(digitFreqs[i][0], digitFreqs[i][1], samplingFreq, tonePeriod, volume)
#   test = [a+b for a, b in zip(sin1, sin2)]
#    atest = np.asarray(test).astype(np.float32)
    #print(atest)
    #print(len(atest))
    atest = test

    stream.write(atest)

stream.close()
p.terminate()
