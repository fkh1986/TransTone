import math
import pyaudio
import array
import numpy as np
import wave

frequencyR = (697,770, 852, 941)
frequencyC = (1209, 1336, 1477, 1633)

samplingFreq = 44100
sr = 44100
tonePeriod = 4
volume = 0.5


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

def GenSineWave(f,fs,t):
    tp = range(0,int(fs*t))
    sineSig = [np.sin(2*np.pi*f*ts/fs) for ts in tp]
    return sineSig


digitFreqs = list()

for digit in digits:
    digitFreqs.append([frequencyR[digits[digit][0]-1],frequencyC[digits[digit][1]-1]])

print(digitFreqs)
print(digitFreqs[0][0])
print(digitFreqs[0][1])

sin1 = GenSineWave(digitFreqs[0][0],samplingFreq,tonePeriod)
sin2 = GenSineWave(digitFreqs[0][1],samplingFreq,tonePeriod)

test = [a+b for a,b in zip(sin1, sin2)]
atest = np.asarray(test).astype(np.float32)
print(atest)
print(len(atest))

p = pyaudio.PyAudio()
stream = p.open(rate=sr, channels = 1, format= pyaudio.paFloat32, output = True)

stream.write(volume*atest)

stream.close()
p.terminate()


