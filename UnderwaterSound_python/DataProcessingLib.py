import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sp
import wave
#import os

def spectrogram(data, fs, nfft=1024, op=90, title='', freqMin=0, freqMax=0):
    plt.figure()
    os = round(nfft * op / 100)
    plt.specgram(data, Fs=fs, NFFT=nfft, cmap='rainbow', noverlap=os)
    plt.title(title)
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")
    if freqMax == 0:
        freqMax = fs/2
    plt.ylim(freqMin, freqMax)
    plt.colorbar(label = 'Intensity [dB]')
    plt.show()

def waveform(data, fs, tMax=0, tMin=0, title=''):
    plt.figure()
   # data = data - (sum(data)/len(data))
    t = np.linspace(0, 1/fs*len(data), len(data))
    if tMax == 0:
        tMax = t[-1]
    plt.plot(t, data)
    plt.xlim(tMin, tMax)
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Signal Amplitude')
    plt.show()

    ######################################################
def fft(data, fs, freqMin = 0, freqMax = 0, title = ''):
    if freqMax == 0:
        freqMax = fs/2
    plt.figure()
    y = np.fft.fft(data)
    t = np.linspace(0, 1 / fs * len(data), len(data))
    df = 1/t[-1]
    f = np.linspace(0, len(t)*df, len(t))
    plt.plot(f, y)
    plt.xlim(freqMin, freqMax)
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.show()
    return y

def lowpass(data, cutoff, fs, order=10):
    cutoff /= (fs/2)
    b, a = sp.butter(order, cutoff, btype='lowpass')
    filtered = sp.filtfilt(b, a, data)
    return filtered

def highpass(data, cutoff, fs, order=10):
    cutoff /= (fs/2)
    b, a = sp.butter(order, cutoff, btype='highpass')
    filtered = sp.filtfilt(b, a, data)
    return filtered

def bandpass(data, cutoffLow, cutoffHigh, fs, order=6):
    cutoffLow /= (fs/2)
    cutoffHigh /= (fs/2)
    b, a = sp.butter(order, [cutoffLow, cutoffHigh], btype='bandpass')
    filtered = sp.lfilter(b, a, data)
    return filtered

def convertAll(directory, fs):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        raw2wav(f, fs)
    print('Done converting')

def raw2wav(filename, fs):
    with open(filename, "rb") as file:
        data = file.read()
        name = filename[:-4] + '.wav'
        with wave.open(name, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)  # number of bytes
            wav.setframerate(fs)
            wav.writeframesraw(data)
            wav.close()
    return name

