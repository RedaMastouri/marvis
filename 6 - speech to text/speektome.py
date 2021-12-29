import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Speak up dude! ')
    audio =  r.listen(source)

try:
    text = r.recognize_google(audio)
    print('You just said that: {}'.format(text))
except:
    print('Sorry I don\'t know what you just said! daaamn')
    