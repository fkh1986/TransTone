# This program is intended to transmit links via audio waves
# The input for the transmitter station is a valid web link
# This link is converted to a series of audio tones and played via the speaker output to transmit these tones
# The receiving station will pickup these audio tones
# These tones will be decoded back into the original link sent from the transmitting station

import math
import pyaudio
import array
import pyshorteners as pyshort
import numpy as np
import wave

# Define Frequency Rows & Columns to generate standard DTMF tones

frequencyR = (697, 770, 852, 941)
frequencyC = (1209, 1336, 1477, 1633)

# Define couple of constants

# Sampling Frequency to be used to generate the Sine Wave Signals
samplingFreq = 44100

# Sampling Rate used to play the stream of audio tones
sr = 44100

# The time spent sending each tone
tonePeriod = 0.1

# The volume scaling to avoid clipping the audio signal upon addition of sinusoidal waves
volume = 0.5

# Define the rows and columns for each DTMF digit from 0-F
# In original DTMF digit E and F do not exist
# The # and * digits where replaced by E and F in order to be able to transmit data in Hexadecimal format

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

# Generate DTMF from Frequency 1 and Frequency 2 for a period of t seconds, and applying volume scaling
def GenDTMF(f1, f2, fs, t, volume):
    sineSig = array.array('f',((volume * math.sin(2*math.pi*i * (f1 / fs)) + volume * math.sin(2*math.pi*i * (f2 / fs)))
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

def PlayLinkStream(hexdata):
    p = pyaudio.PyAudio()
    stream = p.open(rate=sr, channels=1, format=pyaudio.paFloat32, output=True)

    for hexdigit in URLHex:
        waveData = GenDTMF(digitFreqs[int(hexdigit, 16)][0], digitFreqs[int(hexdigit, 16)][1], samplingFreq, tonePeriod, volume)
        stream.write(waveData)

    stream.close()
    p.terminate()
    return waveData


digitFreqs = list()

for digit in digits:
    digitFreqs.append([frequencyR[digits[digit][0]-1], frequencyC[digits[digit][1]-1]])


URLText = input("Please Enter URL: ")
URLHex = EncodeTinyLink(URLText)

waveData = PlayLinkStream(URLHex)


