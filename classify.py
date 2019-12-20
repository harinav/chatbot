"""
Classifier Program.

1. This Program is used to correctly detect the Test Speaker from a set of previously trained speakers.
2. This program runs the forward algorithm to compute log-likelihoods on each model.

3. A GMM-HMM Model has been built for every speaker using the Training Data. 2 sources have been considered:
    a. ELSDSR Dataset
    b. VCTK-Corpus
4. MFCC Vectors are used as features. (13 features per frame)
5. A small Confusion Estimate can be made in case 2 models have a very close probability.

NOTE:

1.The input format has to be changed in case VCTK-Database is used.
uhj2. no_of_speakers needs to be updated if more Training is done.

"""
from scipy.io import wavfile
from python_speech_features import mfcc
import pickle
import numpy as np
import pyaudio
import wave
import numpy as np
from scipy.io import wavfile
from hmmlearn.hmm import GMMHMM
from python_speech_features import mfcc
import pickle
from os import listdir
from Model import GMMModel

speaker_number=0
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK =32
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "cccc.wav"
audio = pyaudio.PyAudio()
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

print ("Recording...")

frames = []

for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
    data = stream.read(CHUNK,exception_on_overflow=False)
    frames.append(data)

print ("Finished recording")

# stop Recording

stream.stop_stream()
stream.close()
audio.terminate()
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()


""" INPUTS """

no_of_speakers =4 # TODO: 

#Enter Number of Speakers in Training Set (Number of gmodel files)
#test_speech1 ="ne


# TODO: Enter Test File Name Here.
test_speech1="new_test4.wav"
# test_speech1 = 'MASM_Sr11.wav'

""" FEATURE EXTRACTION """

test_speech_name = test_speech1[0:4]
rate, speech1 = wavfile.read(test_speech1)
print(rate)


feature_vectors1 = mfcc(speech1, samplerate=rate)

# feature_vectors1 = feature_vectors1[0:len(feature_vectors1)/2]  # TODO: To get partial audio.

""" COMPUTING LOG PROBABILITIES """

probability_vector = np.empty(no_of_speakers)
dictionary = dict()

for i in range(no_of_speakers):
    model_filename = "gmodel"+str(i+1)
    sample = pickle.load(open(model_filename, "rb"))

    # RUN FORWARD ALGORITHM TO RETURN PROBABILITY.
    p1 = sample.model.score(feature_vectors1)

    # PRINTING THE RESULTS AND MAKING A DICTIONARY
    # print("Probability for " + sample.name + " : " + str(p1))
    probability_vector[i] = p1
    dictionary[sample.name] = p1

""" DECIDING THE CLOSEST MATCH """

closest_match = np.argmax(probability_vector)
print(closest_match)
print(probability_vector)
closest_match_value = np.max(probability_vector)
print(closest_match_value)
closest_match_name = (pickle.load(open("gmodel" + str(closest_match + 1), "rb"))).name
print("\n Log Probabilities...\n")
for x in dictionary:
    print (x, ':', dictionary[x])
print("\nClosest Match : " + closest_match_name)

""" CONFUSION ESTIMATE """

print("Confusion(s):")

yes_confusion = 0
for i in range(no_of_speakers):
    if probability_vector[i] > closest_match_value -100:
        if (pickle.load(open("gmodel"+str(i+1), "rb"))).name != closest_match_name:
            print((pickle.load(open("gmodel"+str(i+1),"rb"))).name)
            yes_confusion = 1

if yes_confusion == 0:
	print("--Nil--")

""" FUTURE EXTENSIONS """

# TODO: Confusion Estimate.
# TODO: Create a threshold to identify if the speaker is new.



