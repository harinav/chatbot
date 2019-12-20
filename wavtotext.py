import speech_recognition as sr 
AUDIO_FILE = ("D3.wav")
# use the audio file as the audio source 
r = sr.Recognizer() 
#data=[]
with sr.AudioFile(AUDIO_FILE) as source: 
    #reads the audio file. Here we use record instead of 
    #listen 
 #   print(source)
    audio = r.record(source)
    print("You said: " + r.recognize_google(audio))

# In[18]:
