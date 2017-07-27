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

# Define a tuple for the rows and columns for each DTMF digit from 0-F
# In original DTMF digit E and F do not exist
# The # and * digits where replaced by E and F in order to be able to transmit data in Hexadecimal format

digits = {'0': [frequencyR[3], frequencyC[1]],
          '1': [frequencyR[0], frequencyC[0]],
          '2': [frequencyR[0], frequencyC[1]],
          '3': [frequencyR[0], frequencyC[2]],
          '4': [frequencyR[1], frequencyC[0]],
          '5': [frequencyR[1], frequencyC[1]],
          '6': [frequencyR[1], frequencyC[2]],
          '7': [frequencyR[2], frequencyC[0]],
          '8': [frequencyR[2], frequencyC[1]],
          '9': [frequencyR[2], frequencyC[2]],
          'a': [frequencyR[0], frequencyC[3]],
          'b': [frequencyR[1], frequencyC[3]],
          'c': [frequencyR[2], frequencyC[3]],
          'd': [frequencyR[3], frequencyC[3]],
          'e': [frequencyR[3], frequencyC[0]],
          'f': [frequencyR[3], frequencyC[2]]
          }

# This function is used to generate DTMF from Frequency 1 and Frequency 2, with a certain Sampling Frequency
# for a period of t seconds, and applying volume v scaling, for every ts sample time
# Sinusoidal tone waves are generated with the following formula:
# Sinusoidal DTMF Tone = A * (Sin(2*pi*f1/fs*ts) + Sin(2*pi*f2/fs*ts))

def GenDTMF(f1, f2, fs, t, v):
    sineSig = array.array('f',(v*(math.sin(2*math.pi*ts * (f1 / fs)) + math.sin(2*math.pi*ts * (f2 / fs)))
                               for ts in range(int(fs*t)))).tostring()
    return sineSig

# This function is used to encode a URL into a shortened URL
# TinyURL was used as it requires no tokens or authentications
# Another benefit for shortened URLs is to standardize the URLs prefix "http://tinyurl.com/"
# This way the URL can be shortened even more by removing the prefix

def EncodeTinyLink(url):

    # Used TinyURL to avoid using tokens or authentications
    shortener = pyshort.Shortener('Tinyurl')
    TinyURL = shortener.short(URLText)

    # The consant prefix in the TinyURL is standard and can be removed altogether, and added in the receiving station
    constURL = "http://tinyurl.com/"
    if constURL in TinyURL:
        lenconstURL = len(constURL)
        StripTinyURL = TinyURL[lenconstURL:]
        print(TinyURL)          # for debugging
        print(StripTinyURL)     # for debugging

        # Convert the TinyURL from string into Hexadecimal digits to be sent using DTMF
        URLHex = StripTinyURL.encode().hex()
        print(URLHex)           # for debugging
        return URLHex

# This function plays the Hexadecimal digits representing the stripped URL string using DTMF tones
# It also returns the floating point representation for the actual audio wave
# This wave will be captured by the receiving station, recorded, analyzed and decoded back to a URL

def PlayLinkStream(hexdata):
    p = pyaudio.PyAudio()
    stream = p.open(rate=sr, channels=1, format=pyaudio.paFloat32, output=True)

    # Generate the DTMF sinusoidal tones
    for hexdigit in URLHex:
        waveData = GenDTMF(digits[hexdigit][0], digits[hexdigit][1], samplingFreq, tonePeriod, volume)
        stream.write(waveData)

    stream.close()
    p.terminate()
    return waveData


# User URL input

URLText = input("Please Enter URL: ")

# TinyURL encoding for the User URL
# A valid URL should begin with http:// or https://

#### CONSIDER HANDLING ERRORS FOR INVALID URLS ####
URLHex = EncodeTinyLink(URLText)


# Play tone stream for User URL
waveData = PlayLinkStream(URLHex)
