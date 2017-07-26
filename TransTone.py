import math
import pyaudio
import array
import pyshorteners as pyshort
import numpy as np
import wave

frequencyR = (697, 770, 852, 941)
frequencyC = (1209, 1336, 1477, 1633)

samplingFreq = 44100
sr = 44100
tonePeriod = 0.1
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
    sineSig = array.array('f',((volume * math.sin(i / (f1 / 100.)) + volume * math.sin(i / (f2 / 100.)))
                               for i in range(int(fs*t)))).tostring()
    return sineSig

def EncodeTinyLink(url):
    shortener = pyshort.Shortener('Tinyurl')
    TinyURL = shortener.short(URLText)
    constURL = "http://tinyurl.com/"
    if constURL in TinyURL:
        lenconstURL = len(constURL)
        StripTinyURL = TinyURL[lenconstURL:]
        print(TinyURL)
        print(StripTinyURL)
        URLHex = StripTinyURL.encode().hex()
        print(URLHex)
        return URLHex


digitFreqs = list()

for digit in digits:
    digitFreqs.append([frequencyR[digits[digit][0]-1], frequencyC[digits[digit][1]-1]])


URLText = input("Please Enter URL: ")
URLHex = EncodeTinyLink(URLText)

p = pyaudio.PyAudio()
stream = p.open(rate=sr, channels=1, format=pyaudio.paFloat32, output=True)


for hexdigit in URLHex:
    test = GenDTMF(digitFreqs[int(hexdigit, 16)][0], digitFreqs[int(hexdigit, 16)][1], samplingFreq, tonePeriod, volume)
    stream.write(test)

stream.close()
p.terminate()
