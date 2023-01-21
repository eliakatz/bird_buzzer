import RPi.GPIO as GPIO
import scipy
import numpy as np
import pandas as pd
import pyaudio
#from gpiozero import Buzzer
from time import sleep
import wave
import alsaaudio
import librosa
import librosa.display
import matplotlib.pyplot as plt
import sklearn as sk
import joblib as jbl
import sys

import warnings
warnings.filterwarnings('ignore')

#constants
TEMP_FILE = 'temp.wav'
SR = 44100
MOD_PATH = '/home/eliana/proj-birds/scarecrow/'
GPIO_TRUE=17
GPIO_FALSE=18
GPIO_SWITCH=12


runcode=True
while runcode==True:
    try:       
        # execute the buzzer (or light)
        def buzz(io):
            #Select GPIO mode
            GPIO.setmode(GPIO.BCM)
            #Set buzzer - pin 17 as output
            buzzer=io
            GPIO.setup(buzzer,GPIO.OUT)

            #Run forever loop
            #while True:
            for i in range(3):
                GPIO.output(buzzer,GPIO.HIGH)
            #    print ("Beep")
                sleep(0.5) # Delay in seconds
                GPIO.output(buzzer,GPIO.LOW)
            #    print ("No Beep")
                sleep(0.5)
                i+=1


        # capture the sound from the microphone
        def capture_sound():
            duration = 3 # sample duration in seconds
            sample_rate = 44100
            total_size = sample_rate * duration
            # inp: input data
            inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
            inp.setchannels(1)
            inp.setrate(sample_rate)
            inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            inp.setperiodsize(total_size)
         
            # save the data to temporary file
            w = wave.open(TEMP_FILE, 'w')
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)

            l, data = inp.read()

            data = np.fromstring(data, dtype='float32')
            w.writeframes(data)

            w.close()
            print('Finished')

        capture_sound()

        class Bird:
        #    def __init__(self, file_index, name):
            def __init__(self):
        #        self.name = name
        #        self.file_index = file_index
                self.signal = [] # the audio file raw data
                self.sr = 0 # sample_rate
                self.sc = [] # spectral centroid
                self.stft = [] # short time fourier transform
                self.Y = [] # spectrogram
                self.loud_freqs = [] # the frequencies of the higher eights part of the db.
                self.loudest_freq = 0


        b=Bird()
        b.signal, b.sr = librosa.load(TEMP_FILE, sr=SR, mono=True, duration=3)

        # Extracting Short-Time Fourier Transform
        FRAME_SIZE = 2048
        HOP_SIZE = 512

        # Visualizing the spectrogram (based on Valerio Veraldo's example)
        # plot a spectrogram 
         
        def plot_spectrogram(Y, sr, hop_length, y_axis="linear", title='', counter=0):
            plt.figure(figsize=(25, 10))
            librosa.display.specshow(Y, 
                                    sr=sr, 
                                    hop_length=hop_length, 
                                    x_axis="time", 
                                    y_axis=y_axis,
                                    cmap='coolwarm')
            
            plt.title(title)
            plt.colorbar(format="%+2.f")
        #    plt.savefig("images/spec"+title+str(counter)+".png") # used to save the images


        frames = range(len(b.signal))
        t = librosa.frames_to_time(frames, hop_length=HOP_SIZE)

        plot=False # calculate only
        #plot=True # calculate and plot the spectrograms
        counter=0 # used for saving the plots with unique name

        # extract Short-Time Fourier Transform
        S_b = librosa.stft(b.signal, n_fft=FRAME_SIZE, hop_length=HOP_SIZE)

        # calculate the spectrogram
        Y_b = librosa.power_to_db(np.abs(S_b) ** 2)  #Y(m,k) = |S(m,k)|^2

        if plot:
            # plot the spectrogram
            plot_spectrogram(Y_b, SR, HOP_SIZE, y_axis="log", counter=counter)
            counter+=1
        
        # save to bird object
        b.stft = S_b
        b.Y = Y_b

        # minimize the intensity up to freq=256. These frequencies are due to background noise, especially 
        # the 48 Hz segments that is captured as the loudest frequency, and has nothing to do with the birds.
        # It's just the AC frequency (the closest product of 16 to 50 Hz (the AC frequency))
        y_new= np.copy(b.Y)
        y_new[:16] = b.Y.min()
        y_new

        # find the loudest freq and the loudest range (the loudest eighth part)
        hi=y_new.max()-((y_new.max()-y_new.min())/8)
        b.loud_freqs= (np.unique(np.where(y_new > hi)[0])+1) * 16
        b.loudest_freq = (np.where(y_new == y_new.max())[0]+1) * 16

        # create a dataframe of the frequencies
        df = pd.DataFrame({'hi_lim': b.loud_freqs.max(),
                        'lo_lim': np.maximum(b.loud_freqs.min(), 192),
                        'loudest_freq': b.loudest_freq})
        df

        # numeric columns
        numeric = ['hi_lim', 'lo_lim', 'loudest_freq']

        # run the best model:
    
        # decision tree classifier (although the best is dtc with downsample, I prefer using the model without downsample
        # as there are few samples already, and the result is 'too good to be true')
        dtc = jbl.load(MOD_PATH + 'bird-dtc.joblib')
        pred_dtc = dtc.predict(df)
     

        # activate the buzzer
        if pred_dtc:
            buzz(GPIO_TRUE)
        else:
            buzz(GPIO_FALSE)
        
        GPIO.cleanup() # Clean up

    except KeyboardInterrupt:   #ctrl+c to interrupt
        print('Stopped')
        runcode=False
        GPIO.cleanup() # Clean up



