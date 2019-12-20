import speech_recognition as sr
import time
import win32com.client
from chatterbot import ChatBot 

chatbot = ChatBot('Achala')

speaker = win32com.client.Dispatch("SAPI.SpVoice")

r = sr.Recognizer()
while True:
    with sr.Microphone() as source:    
        print("Say something!")
        st = time.time()
        audio = r.listen(source, phrase_time_limit=4)
        et = time.time()
        print('time taken to read file: ',(et-st),'s')
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            st = time.time()
            text=str(r.recognize_google(audio))
            et = time.time()
            print('time taken to recognize: ', (et-st),'s')
            print("You said: " + text)
            
            st = time.time()
            rep = chatbot.get_response(text)
            _ = speaker.Speak(rep)
            et = time.time()
            print("Bot said: "+ str(rep))
            
            print('time taken to speak: ',et-st)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
